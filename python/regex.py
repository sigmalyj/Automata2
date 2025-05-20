#!/usr/bin/env python

import json
import sys
from typing import List

import antlr4.Token
from antlr4 import CommonTokenStream, InputStream

from antlr_parser.regexLexer import regexLexer
from antlr_parser.regexParser import regexParser
from nfa import NFA, Rule, RuleType, Path


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

    @staticmethod
    def parse(pattern: str) -> regexParser.RegexContext:
        """
        解析正则表达式的字符串，生成语法分析树。
        """
        input_stream = InputStream(pattern)
        lexer = regexLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = regexParser(stream)
        tree = parser.regex()
        err_count = parser.getNumberOfSyntaxErrors()
        if err_count > 0:
            raise ValueError(f"parser解析失败，表达式中有{err_count}个语法错误！")
        return tree

    def compile(self, pattern: str, flags: str = "") -> None:
        """
        编译给定的正则表达式，构造NFA。
        """
        self.flags = flags
        tree = self.parse(pattern)
        nfa_position = self._nfa_regex(tree)
        self.nfa.is_final = [False] * self.nfa.num_states
        self.nfa.is_final[nfa_position.right] = True

    def match(self, text: str) -> List[str]:
        """
        在给定的输入文本上，进行正则表达式匹配，返回匹配到的第一个结果。
        """
        for i in range(len(text)):
            path = self.nfa.exec(text[i:])
            if path:
                match_result = "".join(path.consumes)
                return [match_result]
        return []

    def _nfa_regex(self, node: regexParser.RegexContext) -> NFAPosition:
        """
        构造整个正则表达式的NFA。
        """
        start_state = self.nfa.num_states
        self.nfa.num_states += 1
        self.nfa.rules.append([])

        sub_positions = []
        for expression in node.expression():
            sub_position = self._nfa_expression(expression)
            sub_positions.append(sub_position)

            # 从正则表达式的初态到每个子表达式的初态创建ε转移
            self.nfa.rules[start_state].append(Rule(dst=sub_position.left, type=RuleType.EPSILON))

        end_state = self.nfa.num_states
        self.nfa.num_states += 1
        self.nfa.rules.append([])

        # 从每个子表达式的终态到正则表达式的终态创建ε转移
        for sub_position in sub_positions:
            self.nfa.rules[sub_position.right].append(Rule(dst=end_state, type=RuleType.EPSILON))

        return NFAPosition(start_state, end_state)

    def _nfa_expression(self, node: regexParser.ExpressionContext) -> NFAPosition:
        """
        构造表达式的NFA。
        """
        positions = [self._nfa_expression_item(item) for item in node.expressionItem()]

        if not positions:
            return NFAPosition(self.nfa.num_states, self.nfa.num_states)

        for i in range(len(positions) - 1):
            self.nfa.rules[positions[i].right].append(Rule(dst=positions[i + 1].left, type=RuleType.EPSILON))

        return NFAPosition(positions[0].left, positions[-1].right)

    def _nfa_expression_item(self, node: regexParser.ExpressionItemContext) -> NFAPosition:
        """
        构造表达式项的NFA。
        """
        normal_item = node.normalItem()
        quantifier = node.quantifier()

        if normal_item.single():
            position = self._nfa_single(normal_item.single())
        elif normal_item.group():
            position = self._nfa_regex(normal_item.group().regex())
        else:
            raise ValueError("不支持的表达式项类型")

        if quantifier:
            quantifier_text = quantifier.getText()
            new_start = self.nfa.num_states
            new_end = self.nfa.num_states + 1
            self.nfa.num_states += 2
            self.nfa.rules.extend([[], []])

            if quantifier_text == "?":
                self.nfa.rules[new_start].append(Rule(dst=new_end, type=RuleType.EPSILON))
                self.nfa.rules[new_start].append(Rule(dst=position.left, type=RuleType.EPSILON))
                self.nfa.rules[position.right].append(Rule(dst=new_end, type=RuleType.EPSILON))
            elif quantifier_text == "*":
                self.nfa.rules[new_start].append(Rule(dst=new_end, type=RuleType.EPSILON))
                self.nfa.rules[new_start].append(Rule(dst=position.left, type=RuleType.EPSILON))
                self.nfa.rules[position.right].append(Rule(dst=position.left, type=RuleType.EPSILON))
                self.nfa.rules[position.right].append(Rule(dst=new_end, type=RuleType.EPSILON))
            elif quantifier_text == "+":
                self.nfa.rules[new_start].append(Rule(dst=position.left, type=RuleType.EPSILON))
                self.nfa.rules[position.right].append(Rule(dst=position.left, type=RuleType.EPSILON))
                self.nfa.rules[position.right].append(Rule(dst=new_end, type=RuleType.EPSILON))

            position = NFAPosition(new_start, new_end)

        return position

    def _nfa_single(self, node: regexParser.SingleContext) -> NFAPosition:
        """
        构造单个正则表达式元素的NFA。
        """
        start = self.nfa.num_states
        self.nfa.num_states += 1
        self.nfa.rules.append([])

        end = self.nfa.num_states
        self.nfa.num_states += 1
        self.nfa.rules.append([])

        if node.char():
            char_node = node.char()
            if char_node.EscapedChar():
                char = self._parse_control_or_hex_escape(char_node.EscapedChar().getText())
            else:
                char = char_node.getText()
            self.nfa.rules[start].append(Rule(dst=end, type=RuleType.NORMAL, by=char))
        elif node.characterClass():
            char_class = self._parse_predefined_char_class(node.characterClass())
            self.nfa.rules[start].append(Rule(dst=end, type=RuleType.SPECIAL, by=char_class))
        elif node.AnyCharacter():
            self.nfa.rules[start].append(Rule(dst=end, type=RuleType.SPECIAL, by="."))
        elif node.characterGroup():
            group_position = self._nfa_character_group(node.characterGroup())
            self.nfa.rules[start].append(Rule(dst=group_position.left, type=RuleType.EPSILON))
            self.nfa.rules[group_position.right].append(Rule(dst=end, type=RuleType.EPSILON))
        else:
            raise ValueError("不支持的单个正则表达式元素类型")

        return NFAPosition(start, end)

    def _nfa_character_group(self, node: regexParser.CharacterGroupContext) -> NFAPosition:
        """
        构造字符组的NFA。
        """
        start = self.nfa.num_states
        self.nfa.num_states += 1
        self.nfa.rules.append([])

        end = self.nfa.num_states
        self.nfa.num_states += 1
        self.nfa.rules.append([])

        is_negative = node.characterGroupNegativeModifier() is not None
        for item in node.characterGroupItem():
            if item.charInGroup():
                char = self._parse_char_from_group(item.charInGroup())
                self.nfa.rules[start].append(Rule(dst=end, type=RuleType.NORMAL, by=char))
            elif item.characterClass():
                char_class = self._parse_predefined_char_class(item.characterClass())
                self.nfa.rules[start].append(Rule(dst=end, type=RuleType.SPECIAL, by=char_class))
            elif item.characterRange():
                start_char = self._parse_char_from_group(item.characterRange().charInGroup(0))
                end_char = self._parse_char_from_group(item.characterRange().charInGroup(1))
                self.nfa.rules[start].append(Rule(dst=end, type=RuleType.RANGE, by=start_char, to=end_char))
            else:
                raise ValueError("不支持的字符组项类型")

        return NFAPosition(start, end)

    def _parse_control_or_hex_escape(self, sequence: str) -> str:
        """
        解析转义字符。
        """
        escape_map = {
            "\\f": "\f",
            "\\n": "\n",
            "\\r": "\r",
            "\\t": "\t",
            "\\v": "\v"
        }
        if sequence in escape_map:
            return escape_map[sequence]
        if sequence.startswith("\\x"):
            return chr(int(sequence[2:], 16))
        return sequence[1] if len(sequence) > 1 else ""

    def _parse_predefined_char_class(self, node: regexParser.CharacterClassContext) -> str:
        """
        解析预定义字符类。
        """
        if node.CharacterClassAnyWord():
            return "w"
        if node.CharacterClassAnyWordInverted():
            return "W"
        if node.CharacterClassAnyDecimalDigit():
            return "d"
        if node.CharacterClassAnyDecimalDigitInverted():
            return "D"
        if node.CharacterClassAnyBlank():
            return "s"
        if node.CharacterClassAnyBlankInverted():
            return "S"
        return ""

    def _parse_char_from_group(self, node: regexParser.CharInGroupContext) -> str:
        """
        解析字符组中的字符。
        """
        if node.EscapedChar():
            return self._parse_control_or_hex_escape(node.EscapedChar().getText())
        return node.getText()[0]

if __name__ == '__main__':
    """
    程序入口点函数。已经帮你封装好了读取文本输入、调用compile方法和match等方法、输出结果等。
    一般来说，你不需要阅读和改动这里的代码，只需要完成上面Regex类中的标有TODO的函数即可。
    """
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

    regex = Regex()
    regex.compile(pattern, flags)
    if typ == "find" or typ == "match":
        result = regex.match(input_str)
        print(json.dumps(result))
    else:
        raise ValueError("不支持的输入文件类型！")
