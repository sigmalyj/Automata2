#!/usr/bin/env python

import sys
from enum import Enum
from typing import List, Optional

"""
本文件中已经定义好了一些类和函数，类内也已经定义好了一些成员变量和方法。不建议大家修改这些已经定义好的东西。
但是，为了实现功能，你可以自由地增加新的函数、类等，包括可以在已经定义好的类自由地添加新的成员变量和方法。

本文件可以直接作为python的入口点文件。
支持两种运行方式：
1、将输入文件的文件名作为唯一的命令行参数传入。
   例如: python nfa.py ../cases/01.txt
2、若不传入任何参数，则程序将从stdin中读取输入。
"""
"""
在第一次实验中，保证状态转移规则的字母和输入的字符串都仅包含ASCII字符，且不包含'\0'和换行符'\r' '\n'。
第一次实验要求支持的特殊字符有：\d \w \s \D \W \S \. 
前六个的定义同一般正则表达式中的定义，最后一个\.则等同于一般正则表达式中的.，可匹配任何字符。
各个字符的具体定义可查看 https://www.runoob.com/regexp/regexp-metachar.html 
"""


class RuleType(Enum):
    """
    用于表示状态转移的类型的枚举。
    示例用法： if rule.type == RuleType.EPSILON:
    """
    NORMAL = 0  # 一般转移。如 a
    RANGE = 1  # 字符区间转移。如 a-z
    SPECIAL = 2  # 特殊转移。如 \d （注意Rule的by属性里面是没有斜杠的，只有一个字母如d）
    EPSILON = 3  # epsilon-转移。
    NEGATIVE = 4  # 负向转移。表示不匹配的字符。比如 \D 表示不是数字的字符。


class Rule:
    """
    表示一条状态转移规则。
    """
    def __init__(self, dst: int, type: RuleType, by: str = "", to: str = ""):
        self.dst = dst
        self.type = type
        self.by = by
        self.to = to
        self.negativeRules = []  # 负向转移规则列表

class Path:
    """
    表示一条从初态到终态的路径。
    当输入字符串的执行结果是接受时，你需要根据接受的路径，正确构造一个该类的对象并返回。
    """
    states: List[int] = []  # 从初态到终态经历的状态列表。开头必须是0。
    consumes: List[str] = []  # 长度必须为states的长度-1。consumes[i]表示states[i]迁移到states[i+1]时所消耗的字母（若是ε转移，则应设为空串""）

    def __str__(self):
        """
        将Path转为（序列化为）文本的表达格式（以便于通过stdout输出）
        你不需要理解此函数的含义、阅读此函数的实现和调用此函数。
        """
        result = ""
        if len(self.consumes) != len(self.states) - 1: return "Path对象无效：len(consumes)不等于len(states)-1！"
        for i in range(len(self.consumes)):
            result += str(self.states[i]) + " " + self.consumes[i] + " "
        result += str(self.states[-1])
        return result


class NFA:
    """
    表示一个NFA的类。
    本类定义的自动机，约定状态用编号0~(num_states-1)表示，初态固定为0。
    """
    num_states: int = 0  # 状态个数
    is_final: List[bool] = []  # 用于判断状态是否为终态的数组，长为num_states。is_final[i]为true表示状态i为终态。
    rules: List[List[Rule]] = []  # 表示所有状态转移规则的二维数组，长为num_states。rules[i]表示从状态i出发的所有转移规则。

    def exec(self, text: str, log_func=None) -> Optional[Path]:
        """
        执行NFA匹配，支持懒惰匹配。
        """
        # 使用栈进行深度优先搜索
        stack = [(0, 0, Path())]  # (state, position, path)
        visited = set()           # 使用(state, position)作为访问记录
        
        # 使用传入的日志函数或默认使用print
        log = log_func if log_func else print
        
        log(f"开始匹配文本: '{text}'")
        
        while stack:
            state, pos, path = stack.pop()
            remaining_text = text[pos:] if pos < len(text) else ""
            
            log(f"当前状态: {state}, 位置: {pos}, 剩余文本: '{remaining_text}', 路径: {path.states}")
            
            # 检查是否已访问过该状态位置组合
            state_pos_key = f"{state}_{pos}"
            if state_pos_key in visited:
                continue
            visited.add(state_pos_key)
            
            # 将当前状态添加到路径
            current_path = Path()
            current_path.states = path.states.copy()
            current_path.consumes = path.consumes.copy()
            current_path.states.append(state)
            
            # 检查是否为终态 - 立即返回第一个找到的终态路径
            if self.is_final[state]:
                log(f"发现终态匹配: {state}, 匹配长度: {pos}")
                return current_path
            
            # 存储所有可能的转移，按照懒惰匹配的需要调整顺序
            transitions = []
            
            # 遍历当前状态的所有可能转移
            for rule in self.rules[state]:
                next_state = rule.dst
                consumed = ""
                should_push = False
                new_pos = pos
                
                if rule.type == RuleType.EPSILON:
                    should_push = True
                    log(f"  发现 ε-转移 到状态 {rule.dst}")
                
                elif rule.type == RuleType.NORMAL:
                    if pos < len(text) and text[pos] == rule.by:
                        consumed = text[pos]
                        should_push = True
                        new_pos = pos + 1
                        log(f"  发现普通转移 '{text[pos]}' 到状态 {rule.dst}")
                
                elif rule.type == RuleType.SPECIAL:
                    if pos < len(text) and self.match_rule(rule, text[pos]):
                        consumed = text[pos]
                        should_push = True
                        new_pos = pos + 1
                        log(f"  发现特殊转移 '{text[pos]}' 到状态 {rule.dst}")
                
                elif rule.type == RuleType.RANGE:
                    if pos < len(text) and rule.by <= text[pos] <= rule.to:
                        consumed = text[pos]
                        should_push = True
                        new_pos = pos + 1
                        log(f"  发现范围转移 '{text[pos]}' 到状态 {rule.dst}")
                
                elif rule.type == RuleType.NEGATIVE:
                    if pos < len(text):
                        valid_transition = True
                        for neg_rule in rule.negativeRules:
                            if neg_rule.type == RuleType.NORMAL and text[pos] == neg_rule.by:
                                valid_transition = False
                                break
                            elif neg_rule.type == RuleType.SPECIAL and self.match_rule(neg_rule, text[pos]):
                                valid_transition = False
                                break
                            elif neg_rule.type == RuleType.RANGE and neg_rule.by <= text[pos] <= neg_rule.to:
                                valid_transition = False
                                break
                        
                        if valid_transition:
                            consumed = text[pos]
                            should_push = True
                            new_pos = pos + 1
                            log(f"  发现负向转移 '{text[pos]}' 到状态 {rule.dst}")
                
                # 如果转移有效
                if should_push:
                    new_state_pos_key = f"{next_state}_{new_pos}"
                    if new_state_pos_key not in visited:
                        new_path = Path()
                        new_path.states = current_path.states.copy()
                        new_path.consumes = current_path.consumes.copy()
                        new_path.consumes.append(consumed)
                        
                        # 收集可能的转移
                        transitions.append((next_state, new_pos, new_path))
            
            # 反转转移列表，使得将来先处理可能的懒惰匹配路径（epsilon转移会最先被处理）
            transitions.reverse()
            
            # 将收集到的转移按顺序添加到栈中
            for transition in transitions:
                stack.append(transition)
        
        log("拒绝")
        return None

    def match_rule(self, rule: Rule, c: str) -> bool:
        """
        匹配规则是否适用于给定字符。
        :param rule: 状态转移规则
        :param c: 输入字符
        :return: 是否匹配
        """
        if rule.type == RuleType.NORMAL:
            return rule.by == c
        elif rule.type == RuleType.RANGE:
            return rule.by <= c <= rule.to
        elif rule.type == RuleType.SPECIAL:
            if rule.by == "d":
                return c.isdigit()
            elif rule.by == "w":
                return c.isalnum() or c == "_"
            elif rule.by == "s":
                return c.isspace()
            elif rule.by == "D":
                return not c.isdigit()
            elif rule.by == "W":
                return not (c.isalnum() or c == "_")
            elif rule.by == "S":
                return not c.isspace()
            elif rule.by == ".":
                return c != "\r" and c != "\n"
            elif rule.by == ",":
                return True
        return False

    @staticmethod
    def from_text(text: str) -> "NFA":
        """
        从自动机的文本表示构造自动机
        你不需要理解此函数的含义、阅读此函数的实现和调用此函数。
        """
        nfa = NFA()
        lines = text.splitlines()
        reading_rules = False
        type = ""
        for line in lines:
            if line == "": continue
            if line.startswith("type:"):
                type = line[5:].strip()
                continue
            if type != "nfa": raise ValueError("输入文件的类型不是nfa！")
            if line.startswith("states:"):
                nfa.num_states = int(line[7:])
                nfa.is_final = [False for _ in range(nfa.num_states)]
                nfa.rules = [[] for _ in range(nfa.num_states)]
                continue
            elif line.startswith("final:"):
                if nfa.num_states == 0: raise AssertionError("states必须出现在final和rules之前!")
                content = line[6:].strip()
                for s in content.split(" "):
                    if s == "": continue
                    nfa.is_final[int(s)] = True
                reading_rules = False
                continue
            elif line.startswith("rules:"):
                if nfa.num_states == 0: raise AssertionError("states必须出现在final和rules之前!")
                reading_rules = True
                continue
            elif line.startswith("input:"):
                reading_rules = False
                continue
            elif reading_rules:
                arrow_pos = line.find("->")
                space_pos = line.find(" ")
                if arrow_pos != -1 and space_pos != -1 and arrow_pos < space_pos:
                    src = int(line[0:arrow_pos])
                    dst = int(line[arrow_pos + 2:space_pos])
                    content = line[space_pos + 1:]
                    success = True
                    while success and content != "":
                        p = content.find(" ")
                        if p == -1:
                            p = len(content)
                        elif p == 0:
                            p = 1  # 当第一个字母是空格时，说明转移的字符就是空格。于是假定第二个字母也是空格（如果不是，会在后面直接报错）
                        rule = Rule()
                        rule.dst = dst
                        if p == 3 and content[1] == '-':
                            rule.type = RuleType.RANGE
                            rule.by = content[0]
                            rule.to = content[2]
                        elif p == 2 and content[0] == "\\":
                            if content[1] == "e":
                                rule.type = RuleType.EPSILON
                            else:
                                rule.type = RuleType.SPECIAL
                                rule.by = content[1]
                        elif p == 1 and (p >= len(content) or content[p] == ' '):
                            rule.type = RuleType.NORMAL
                            rule.by = content[0]
                        else:
                            success = False
                        nfa.rules[src].append(rule)
                        content = content[p + 1:]
                    if success:
                        continue
        return nfa


def exportJFLAP(nfa: NFA, filename="./result.jff", distance=80, yLevels=5):
    """
    将NFA导出成JFLAP的格式，以便于可视化。生成的文件可以直接用JFLAP打开。
    这是一个给你的工具函数，你直接使用即可，不需要理解和修改其中的内容。
    注意提交OJ的版本不应调用此函数，否则OJ评测机会产生错误(PE 输出格式错误)。
    @param nfa:
    @param filename: 可选 默认保存在当前目录下的result.jff文件。
    @param distance: 可选 JFLAP图中两个状态的距离
    @param yLevels: 可选 JFLAP图中纵向有多少级。默认为5，如果画出来的东西不便查看建议调小到2~3。
    """
    seqStr = "①②③④⑤⑥⑦⑧⑨"
    with open(filename, "w") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><structure>\n"
                "<type>fa</type>\n<automaton>\n")
        for i in range(nfa.num_states):
            y = abs(((i / 2) % (yLevels * 2 - 2)) - (yLevels - 1)) * distance
            f.write(f'<state id="{i}" name="{i}"><x>{i * distance}</x><y>{y}</y>')
            if i == 0: f.write("<initial/>")
            if nfa.is_final[i]: f.write("<final/>")
            f.write("</state>\n")
            for j, rule in enumerate(nfa.rules[i]):
                f.write(f'<transition><from>{i}</from><to>{rule.dst}</to>')
                if rule.type == RuleType.EPSILON:
                    if len(nfa.rules[i]) == 1:
                        f.write("<read/>")
                    else:
                        f.write(f'<read>λ{seqStr[j]}</read>')
                else:
                    read = rule.by
                    if read == "<": read = "&lt;"  # 转义掉<符号
                    if rule.type == RuleType.SPECIAL:
                        read = "\\" + rule.by
                    elif rule.type == RuleType.RANGE:
                        read = rule.by + "-" + rule.to
                    f.write(f'<read>{read}</read>')
                f.write("</transition>\n")
        f.write("</automaton>\n</structure>\n")
        print(f'JFLAP exported to {filename} !')


if __name__ == '__main__':
    """
    程序入口点函数。已经帮你封装好了读取文本输入、构造自动机并执行字符串、输出结果等。
    一般来说，你不需要阅读和改动这里的代码，只需要完成exec函数即可。
    """
    if len(sys.argv) >= 2:
        with open(sys.argv[1], "r") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    input_str = None
    lines = text.splitlines()
    for line in lines:
        if line.startswith("input: "): input_str = line[7:]
    if input_str is None:
        raise ValueError("未找到输入字符串！注意输入字符串必须以input: 开头，其中冒号后面必须有空格！")

    nfa = NFA.from_text(text)
    result = nfa.exec(input_str)
    if result is None:
        print("Reject", end='')
    else:
        print(str(result), end='')
