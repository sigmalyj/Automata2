#!/usr/bin/env python

import json
import sys
import os
from typing import List, Union, Tuple
from datetime import datetime

import antlr4
from antlr4 import CommonTokenStream, InputStream

from antlr_parser.regexLexer import regexLexer
from antlr_parser.regexParser import regexParser
from nfa import NFA, Rule, RuleType, Path

# 创建日志文件
if len(sys.argv) >= 2:
    # 如果有命令行参数，根据输入文件名命名日志
    input_filename = os.path.basename(sys.argv[1])  # 获取文件名部分（如 "01.in"）
    base_filename = os.path.splitext(input_filename)[0]  # 移除扩展名（得到 "01"）
    log_filename = f"log_{base_filename}.txt"
else:
    # 如果没有命令行参数（从标准输入读取），使用时间戳
    now = datetime.now()
    log_filename = f"log_{now.strftime('%m%d_%H%M')}.txt"

log_file = open(log_filename, "w")

def log(message):
    """写入日志文件"""
    log_file.write(f"{message}\n")
    log_file.flush()


class NFAPosition:
    """
    表示NFA的起始和结束状态。
    """
    def __init__(self, left: int, right: int):
        self.left = left
        self.right = right


class Regex:
    """
    表示一个正则表达式的类。
    """
    def __init__(self):
        self.nfa = NFA()  # 正则表达式所使用的NFA
        self.flags = ""  # 正则表达式的修饰符
        # ANTLR解析器相关
        self.antlr_input_stream = None
        self.antlr_lexer = None
        self.antlr_token_stream = None
        self.antlr_parser = None

    def parse(self, pattern: str) -> regexParser.RegexContext:
        """
        解析正则表达式的字符串，生成语法分析树。
        """
        if self.antlr_input_stream:
            raise RuntimeError("此Regex对象已被调用过一次parse函数，不可以再次调用！")
            
        self.antlr_input_stream = InputStream(pattern)
        self.antlr_lexer = regexLexer(self.antlr_input_stream)
        self.antlr_token_stream = CommonTokenStream(self.antlr_lexer)
        self.antlr_parser = regexParser(self.antlr_token_stream)
        tree = self.antlr_parser.regex()
        
        if not tree:
            raise RuntimeError("parser解析失败(函数返回了None)")
            
        err_count = self.antlr_parser.getNumberOfSyntaxErrors()
        if err_count > 0:
            raise ValueError(f"parser解析失败，表达式中有{err_count}个语法错误！")
            
        # 检查是否解析到字符串结尾
        if self.antlr_token_stream.LA(1) != antlr4.Token.EOF:
            processed_text = self.antlr_token_stream.getText(
                self.antlr_token_stream.get(0),
                self.antlr_token_stream.get(self.antlr_token_stream.index() - 1)
            )
            raise RuntimeError(f"parser解析失败，解析过程未能到达字符串结尾，可能是由于表达式中间有无法解析的内容！已解析的部分：{processed_text}")
            
        return tree

    def parseSpecialChar(self, input_obj: Union[str, regexParser.CharacterClassContext, regexParser.CharInGroupContext]) -> str:
        """
        解析特殊字符、字符类和字符组中的字符。
        整合了原来的 _parse_control_or_hex_escape, _parse_predefined_char_class, _parse_char_from_group 函数。
        
        参数:
            input_obj: 可以是字符串(转义序列)、CharacterClassContext(字符类)或CharInGroupContext(字符组中的字符)
            
        返回:
            解析后的字符或字符类标识符
        """
        # 处理转义字符序列
        if isinstance(input_obj, str):
            escape_map = {
                "\\f": "\f",
                "\\n": "\n",
                "\\r": "\r",
                "\\t": "\t",
                "\\v": "\v"
            }
            
            # 检查固定的转义字符
            if input_obj in escape_map:
                return escape_map[input_obj]
            
            # 检查是否为十六进制转义序列
            if input_obj.startswith("\\x") and len(input_obj) > 2:
                try:
                    hex_value = int(input_obj[2:], 16)
                    return chr(hex_value)
                except (ValueError, OverflowError):
                    return '\0'  # 返回空字符代表错误
            
            # 默认返回第二个字符
            return input_obj[1] if len(input_obj) > 1 else '\0'
        
        # 处理字符类
        elif isinstance(input_obj, regexParser.CharacterClassContext):
            if input_obj.CharacterClassAnyWord():
                return "w"
            if input_obj.CharacterClassAnyWordInverted():
                return "W"
            if input_obj.CharacterClassAnyDecimalDigit():
                return "d"
            if input_obj.CharacterClassAnyDecimalDigitInverted():
                return "D"
            if input_obj.CharacterClassAnyBlank():
                return "s"
            if input_obj.CharacterClassAnyBlankInverted():
                return "S"
            return '\0'  # 未找到匹配的字符类
        
        # 处理字符组中的字符
        elif isinstance(input_obj, regexParser.CharInGroupContext):
            if input_obj.EscapedChar():
                return self.parseSpecialChar(input_obj.EscapedChar().getText())
            return input_obj.getText()[0]
        
        # 未知类型
        return '\0'

    def buildNFA(self, node: Union[regexParser.RegexContext, regexParser.ExpressionContext, 
                                   regexParser.ExpressionItemContext, regexParser.SingleContext, 
                                   regexParser.CharacterGroupContext], 
                 node_type: str = "regex") -> NFAPosition:
        """
        构建NFA，整合了原来的多个_nfa_函数。
        
        参数:
            node: ANTLR解析树节点
            node_type: 节点类型，可以是 'regex', 'expression', 'expression_item', 'single', 'character_group'
            
        返回:
            NFA的起始和终止状态位置
        """
        # 处理整个正则表达式
        if node_type == "regex":
            # 创建初态
            start_state = self.nfa.num_states
            self.nfa.num_states += 1
            self.nfa.rules.append([])

            # 遍历所有子表达式
            sub_positions = []
            for expression in node.expression():
                sub_position = self.buildNFA(expression, "expression")
                sub_positions.append(sub_position)

                # 从正则表达式的初态到每个子表达式的初态创建ε转移
                self.nfa.rules[start_state].append(Rule(dst=sub_position.left, type=RuleType.EPSILON))

            # 创建终态
            end_state = self.nfa.num_states
            self.nfa.num_states += 1
            self.nfa.rules.append([])

            # 从每个子表达式的终态到正则表达式的终态创建ε转移
            for sub_position in sub_positions:
                self.nfa.rules[sub_position.right].append(Rule(dst=end_state, type=RuleType.EPSILON))

            return NFAPosition(start_state, end_state)
        
        # 处理表达式
        elif node_type == "expression":
            # 获取表达式中的所有表达式项
            items = node.expressionItem()
            positions = [self.buildNFA(item, "expression_item") for item in items]

            if not positions:
                # 空表达式，创建一个空的NFA
                start = self.nfa.num_states
                self.nfa.num_states += 1
                self.nfa.rules.append([])
                return NFAPosition(start, start)

            # 连接各个NFA片段
            for i in range(len(positions) - 1):
                self.nfa.rules[positions[i].right].append(Rule(dst=positions[i + 1].left, type=RuleType.EPSILON))

            return NFAPosition(positions[0].left, positions[-1].right)
        
        # 处理表达式项
        elif node_type == "expression_item":
            normal_item = node.normalItem()
            quantifier = node.quantifier()

            # 处理普通项
            if normal_item.single():
                position = self.buildNFA(normal_item.single(), "single")
            elif normal_item.group():
                position = self.buildNFA(normal_item.group().regex(), "regex")
            else:
                raise ValueError("不支持的表达式项类型")

            # 处理量词
            if quantifier:
                quantifier_text = quantifier.getText()
                is_lazy = quantifier.lazyModifier() is not None  # True表示是懒惰模式
                
                new_start = self.nfa.num_states
                new_end = self.nfa.num_states + 1
                self.nfa.num_states += 2
                self.nfa.rules.extend([[], []])

                if quantifier_text.startswith("?"):
                    # 0次或1次
                    if is_lazy:
                        # 懒惰匹配：优先跳过
                        self.nfa.rules[new_start].append(Rule(dst=new_end, type=RuleType.EPSILON))
                        self.nfa.rules[new_start].append(Rule(dst=position.left, type=RuleType.EPSILON))
                    else:
                        # 贪婪匹配：优先匹配
                        self.nfa.rules[new_start].append(Rule(dst=position.left, type=RuleType.EPSILON))
                        self.nfa.rules[new_start].append(Rule(dst=new_end, type=RuleType.EPSILON))
                    self.nfa.rules[position.right].append(Rule(dst=new_end, type=RuleType.EPSILON))
                
                elif quantifier_text.startswith("*"):
                    # 0次或多次
                    if is_lazy:
                        # 懒惰匹配：优先结束
                        self.nfa.rules[new_start].append(Rule(dst=new_end, type=RuleType.EPSILON))
                        self.nfa.rules[position.right].append(Rule(dst=new_end, type=RuleType.EPSILON))
                        self.nfa.rules[position.right].append(Rule(dst=position.left, type=RuleType.EPSILON))
                        self.nfa.rules[new_start].append(Rule(dst=position.left, type=RuleType.EPSILON))
                    else:
                        # 贪婪匹配：优先循环
                        self.nfa.rules[new_start].append(Rule(dst=position.left, type=RuleType.EPSILON))
                        self.nfa.rules[position.right].append(Rule(dst=position.left, type=RuleType.EPSILON))
                        self.nfa.rules[position.right].append(Rule(dst=new_end, type=RuleType.EPSILON))
                        self.nfa.rules[new_start].append(Rule(dst=new_end, type=RuleType.EPSILON))
                
                elif quantifier_text.startswith("+"):
                    # 1次或多次
                    if is_lazy:
                        # 懒惰匹配：尽快结束
                        self.nfa.rules[position.right].append(Rule(dst=new_end, type=RuleType.EPSILON))
                        self.nfa.rules[position.right].append(Rule(dst=position.left, type=RuleType.EPSILON))
                        self.nfa.rules[new_start].append(Rule(dst=position.left, type=RuleType.EPSILON))
                    else:
                        # 贪婪匹配：优先循环
                        self.nfa.rules[position.right].append(Rule(dst=position.left, type=RuleType.EPSILON))
                        self.nfa.rules[position.right].append(Rule(dst=new_end, type=RuleType.EPSILON))
                        self.nfa.rules[new_start].append(Rule(dst=position.left, type=RuleType.EPSILON))
                
                position = NFAPosition(new_start, new_end)

            return position
        
        # 处理单个元素
        elif node_type == "single":
            # 创建开始和结束状态
            start = self.nfa.num_states
            self.nfa.num_states += 1
            self.nfa.rules.append([])

            end = self.nfa.num_states
            self.nfa.num_states += 1
            self.nfa.rules.append([])

            # 根据节点类型处理
            if node.char():
                # 处理单个字符
                char_node = node.char()
                char_text = char_node.getText()
                
                if char_node.EscapedChar():
                    char = self.parseSpecialChar(char_text)
                else:
                    char = char_text[0]
                    
                self.nfa.rules[start].append(Rule(dst=end, type=RuleType.NORMAL, by=char))
                
            elif node.characterClass():
                # 处理字符类
                char_class = self.parseSpecialChar(node.characterClass())
                self.nfa.rules[start].append(Rule(dst=end, type=RuleType.SPECIAL, by=char_class))
                
            elif node.AnyCharacter():
                # 处理点号（任意字符）
                # 根据's'标志决定点号的行为
                dot_type = "," if self.flags == "s" else "."
                self.nfa.rules[start].append(Rule(dst=end, type=RuleType.SPECIAL, by=dot_type))
                
            elif node.characterGroup():
                # 处理字符组
                group_position = self.buildNFA(node.characterGroup(), "character_group")
                self.nfa.rules[start].append(Rule(dst=group_position.left, type=RuleType.EPSILON))
                self.nfa.rules[group_position.right].append(Rule(dst=end, type=RuleType.EPSILON))
                
            else:
                raise ValueError("不支持的单个正则表达式元素类型")

            return NFAPosition(start, end)
        
        # 处理字符组
        elif node_type == "character_group":
            # 创建开始和结束状态
            start = self.nfa.num_states
            self.nfa.num_states += 1
            self.nfa.rules.append([])

            end = self.nfa.num_states
            self.nfa.num_states += 1
            self.nfa.rules.append([])

            # 检查是否为否定字符组
            is_negative = node.characterGroupNegativeModifier() is not None
            items = node.characterGroupItem()

            # 根据是否否定分两种情况处理
            if is_negative:
                # 处理否定字符组
                item_start = self.nfa.num_states
                self.nfa.num_states += 1
                self.nfa.rules.append([])
                
                item_end = self.nfa.num_states
                self.nfa.num_states += 1
                self.nfa.rules.append([])

                # 创建否定规则
                negative_rule = Rule(dst=item_end, type=RuleType.NEGATIVE)
                negative_rule.negativeRules = []  # 初始化否定规则列表
                
                # 添加子规则
                for item in items:
                    if item.charInGroup():
                        char = self.parseSpecialChar(item.charInGroup())
                        neg_rule = Rule(dst=0, type=RuleType.NORMAL, by=char)
                        negative_rule.negativeRules.append(neg_rule)
                    elif item.characterClass():
                        char_class = self.parseSpecialChar(item.characterClass())
                        neg_rule = Rule(dst=0, type=RuleType.SPECIAL, by=char_class)
                        negative_rule.negativeRules.append(neg_rule)
                    elif item.characterRange():
                        start_char = self.parseSpecialChar(item.characterRange().charInGroup(0))
                        end_char = self.parseSpecialChar(item.characterRange().charInGroup(1))
                        neg_rule = Rule(dst=0, type=RuleType.RANGE, by=start_char, to=end_char)
                        negative_rule.negativeRules.append(neg_rule)

                self.nfa.rules[item_start].append(negative_rule)
                
                # 连接规则
                self.nfa.rules[start].append(Rule(dst=item_start, type=RuleType.EPSILON))
                self.nfa.rules[item_end].append(Rule(dst=end, type=RuleType.EPSILON))
            else:
                # 处理普通字符组
                for item in items:
                    item_start = self.nfa.num_states
                    self.nfa.num_states += 1
                    self.nfa.rules.append([])
                    
                    item_end = self.nfa.num_states
                    self.nfa.num_states += 1
                    self.nfa.rules.append([])
                    
                    # 创建规则
                    rule = None
                    if item.charInGroup():
                        char = self.parseSpecialChar(item.charInGroup())
                        rule = Rule(dst=item_end, type=RuleType.NORMAL, by=char)
                    elif item.characterClass():
                        char_class = self.parseSpecialChar(item.characterClass())
                        rule = Rule(dst=item_end, type=RuleType.SPECIAL, by=char_class)
                    elif item.characterRange():
                        start_char = self.parseSpecialChar(item.characterRange().charInGroup(0))
                        end_char = self.parseSpecialChar(item.characterRange().charInGroup(1))
                        rule = Rule(dst=item_end, type=RuleType.RANGE, by=start_char, to=end_char)
                    
                    if rule:
                        self.nfa.rules[item_start].append(rule)
                    
                    # 连接规则
                    self.nfa.rules[start].append(Rule(dst=item_start, type=RuleType.EPSILON))
                    self.nfa.rules[item_end].append(Rule(dst=end, type=RuleType.EPSILON))

            return NFAPosition(start, end)
        
        else:
            raise ValueError(f"不支持的节点类型: {node_type}")

    def compile(self, pattern: str, flags: str = "") -> None:
        """
        编译正则表达式，构建NFA
        """
        self.flags = flags
        tree = self.parse(pattern)
        
        # 使用 buildNFA 构建整个NFA
        nfa_position = self.buildNFA(tree, "regex")
        
        # 设置终态
        self.nfa.is_final = [False] * self.nfa.num_states
        self.nfa.is_final[nfa_position.right] = True
        
        # 调试信息写入日志
        log(f"NFA 状态数: {self.nfa.num_states}")
        log(f"NFA 终态: {nfa_position.right}")
        log("NFA 规则:")
        for i, rules in enumerate(self.nfa.rules):
            log(f"  状态 {i}:")
            for rule in rules:
                log(f"    -> 状态 {rule.dst}, 类型: {rule.type}, 字符: '{rule.by}'")

    def match(self, text: str) -> List[str]:
        """
        在文本中匹配正则表达式
        """
        for i in range(len(text)):
            substr = text[i:]
            log(f"尝试从位置 {i} 匹配: '{substr}'")
            # 将 log 函数传递给 nfa.exec
            path = self.nfa.exec(substr, log)
            if path and path.states:
                match_result = "".join(path.consumes)
                log(f"匹配成功: '{match_result}'")
                return [match_result]
            else:
                log("匹配失败")
        return []


if __name__ == '__main__':
    try:
        if len(sys.argv) >= 2:
            with open(sys.argv[1], "r") as f:
                text = f.read()
        else:
            text = sys.stdin.read()

        typ = ""
        pattern = None
        flags = ""
        input_str = None
        replacement = None
        lines = text.splitlines(keepends=True)
        lenBeforeInputLine = 0
        for line in lines:
            if line.startswith("type:"):
                typ = line[5:].strip()
            elif line.startswith("pattern: "):
                pattern = line.splitlines()[0][9:]  # 去掉结尾的换行符
            elif line.startswith("flags:"):
                flags = line[6:].strip()
            elif line.startswith("replacement: "):
                replacement = line.splitlines()[0][13:]  # 去掉结尾的换行符
            elif line.startswith("input: "):
                input_str = text[lenBeforeInputLine + 7:]
            lenBeforeInputLine += len(line)
        if pattern is None or input_str is None:
            raise ValueError("pattern或input未找到！注意pattern: 和input: ，冒号后面必须有空格！")

        log(f"处理输入 - 类型: {typ}, 模式: {pattern}, 标志: {flags}")
        
        regex = Regex()
        regex.compile(pattern, flags)
        if typ == "find" or typ == "match":
            result = regex.match(input_str)
            # 这是唯一需要输出到标准输出的结果
            print(json.dumps(result))
        else:
            raise ValueError("不支持的输入文件类型！")
    except Exception as e:
        log(f"发生异常: {e}")
        raise
    finally:
        log_file.close()