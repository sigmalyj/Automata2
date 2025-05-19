#include "regex.h"

/**
 * 注：如果你愿意，你可以自由的using namespace。
 */

/**
 * 编译给定的正则表达式。
 * 具体包括两个过程：解析正则表达式得到语法分析树（这步已经为你写好，即parse方法），
 * 和在语法分析树上进行分析（遍历），构造出NFA（需要你完成的部分）。
 * 在语法分析树上进行分析的方法，可以是直接自行访问该树，也可以是使用antlr的Visitor机制，详见作业文档。
 * 你编译产生的结果，NFA应保存在当前对象的nfa成员变量中，其他内容也建议保存在当前对象下（你可以自由地在本类中声明新的成员）。
 * @param pattern 正则表达式的字符串
 * @param flags 正则表达式的修饰符
 */
void Regex::compile(const std::string &pattern, const std::string &flags) {
    // 解析正则表达式得到语法分析树
    regexParser::RegexContext *tree = parse(pattern);
    
    // 初始化NFA
    nfa.num_states = 2; // 开始和结束状态
    nfa.rules.resize(nfa.num_states);
    nfa.is_final.resize(nfa.num_states, false);
    nfa.is_final[1] = true; // 设置接受状态
    
    // 构建NFA
    buildNFA(tree, 0, 1, flags);
}

/**
 * 分析出现的特殊转义字符并进行处理。
 * 能处理以下情况：
 * 1. 常见控制字符的转义序列，如 \n (换行符), \t (制表符) 等。
 * 2. 十六进制转义序列，形式为 \xHH，其中 HH 是十六进制数字，用于表示 ASCII 字符。
 *    如果序列不合法或超出 ASCII 范围，将捕获并处理异常，返回空字符。
 * 3. 如果输入的字符串不符合上述任何一种格式，函数默认返回字符串的第二个字符。
 *    这一默认行为假设输入的字符串总是表示一个有效的转义序列。
 * @param sequence: 代表可能包含转义序列的字符串。
 * @return 对应于转义序列的字符，或在处理错误时返回空字符('\0')。
 */
char Regex::parseSpecialChar(const std::string &sequence) {
    // 处理常见控制字符的转义序列
    static const std::unordered_map<std::string, char> escapeMap = {
        {"\\f", '\f'},
        {"\\n", '\n'},
        {"\\r", '\r'},
        {"\\t", '\t'},
        {"\\v", '\v'}
    };

    // 处理固定的转义字符
    auto it = escapeMap.find(sequence);
    if (it != escapeMap.end()) {
        return it->second;
    }

    // 处理十六进制转义序列 \xHH
    if (sequence.size() > 2 && sequence[0] == '\\' && sequence[1] == 'x') {
        try {
            size_t processedChars = 0;
            int asciiValue = std::stoi(sequence.substr(2), &processedChars, 16);
            if (processedChars != sequence.size() - 2) {
                throw std::runtime_error("无效的十六进制序列");
            }
            return static_cast<char>(asciiValue);
        } catch (const std::exception&) {
            return '\0'; // 返回空字符代表错误
        }
    }

    // 处理预定义字符类
    if (sequence == "\\w") return 'w';
    if (sequence == "\\W") return 'W';
    if (sequence == "\\d") return 'd';
    if (sequence == "\\D") return 'D';
    if (sequence == "\\s") return 's';
    if (sequence == "\\S") return 'S';

    // 默认返回第二个字符，假设输入总是有效的
    return sequence.size() > 1 ? sequence[1] : '\0';
}


/**
 * 递归构造 NFA 的辅助函数。
 * @param node 当前语法树节点
 * @param start 当前 NFA 的起始状态
 * @param end 当前 NFA 的接受状态
 * @param flags 正则表达式的修饰符
 */
void Regex::buildNFA(antlr4::tree::ParseTree *node, int start, int end, const std::string &flags) {
    // 如果节点为空，直接返回
    if (!node) return;

    // 使用动态类型转换检查节点类型
    if (auto* regexCtx = dynamic_cast<regexParser::RegexContext*>(node)) {
        // 处理Regex节点
        int initialStart = nfa.num_states++;
        nfa.rules.push_back(std::vector<Rule>());
        
        // 为每个表达式创建子NFA
        auto expressions = regexCtx->expression();
        for (auto exp : expressions) {
            int expStart = nfa.num_states++;
            nfa.rules.push_back(std::vector<Rule>());
            int expEnd = nfa.num_states++;
            nfa.rules.push_back(std::vector<Rule>());

            // 从起始状态到表达式起始状态的ε转移
            Rule startRule;
            startRule.type = EPSILON;
            startRule.dst = expStart;
            nfa.rules[initialStart].push_back(startRule);

            // 递归处理表达式
            buildNFA(exp, expStart, expEnd, flags);

            // 从表达式结束状态到最终状态的ε转移
            Rule endRule;
            endRule.type = EPSILON;
            endRule.dst = end;
            nfa.rules[expEnd].push_back(endRule);
        }

        // 添加从初始创建的开始状态到参数提供的开始状态的ε转移
        Rule initialRule;
        initialRule.type = EPSILON;
        initialRule.dst = initialStart;
        nfa.rules[start].push_back(initialRule);
    }
    else if (auto* exprCtx = dynamic_cast<regexParser::ExpressionContext*>(node)) {
        // 处理Expression节点
        auto items = exprCtx->expressionItem();
        if (items.empty()) {
            // 空表达式，直接连接起始和结束状态
            Rule emptyRule;
            emptyRule.type = EPSILON;
            emptyRule.dst = end;
            nfa.rules[start].push_back(emptyRule);
            return;
        }

        // 为每个表达式项串联构建NFA
        int prevEnd = start;
        for (size_t i = 0; i < items.size(); i++) {
            int itemStart = (i == 0) ? start : nfa.num_states++;
            int itemEnd = (i == items.size() - 1) ? end : nfa.num_states++;
            
            if (i > 0) {
                nfa.rules.push_back(std::vector<Rule>());
                // 从前一个项的结束到当前项的开始添加ε转移
                Rule connectRule;
                connectRule.type = EPSILON;
                connectRule.dst = itemStart;
                nfa.rules[prevEnd].push_back(connectRule);
                
                if (i < items.size() - 1) {
                    nfa.rules.push_back(std::vector<Rule>());
                }
            }
            
            // 处理表达式项
            buildNFA(items[i], itemStart, itemEnd, flags);
            prevEnd = itemEnd;
        }
    }
    else if (auto* itemCtx = dynamic_cast<regexParser::ExpressionItemContext*>(node)) {
        // 处理ExpressionItem节点
        auto normalItem = itemCtx->normalItem();
        auto quantifier = itemCtx->quantifier();

        if (!normalItem) return;

        // 先处理普通项
        if (auto* single = normalItem->single()) {
            // 处理单个字符、字符类或字符组
            buildNFA(single, start, end, flags);
        }
        else if (auto* group = normalItem->group()) {
            // 处理组
            if (group->regex()) {
                buildNFA(group->regex(), start, end, flags);
            }
        }

        // 再处理量词
        if (quantifier) {
            std::string quantText = quantifier->getText();
            bool isLazy = (quantifier->lazyModifier() != nullptr);
            
            // 为量词创建新的开始和结束状态
            int qStart = nfa.num_states++;
            nfa.rules.push_back(std::vector<Rule>());
            int qEnd = nfa.num_states++;
            nfa.rules.push_back(std::vector<Rule>());

            // 根据量词类型添加适当的ε转移
            if (quantText[0] == '?') {
                // 0或1次
                if (isLazy) {
                    // 懒惰匹配：优先跳过
                    Rule skipRule;
                    skipRule.type = EPSILON;
                    skipRule.dst = qEnd;
                    nfa.rules[qStart].push_back(skipRule);
                    
                    Rule matchRule;
                    matchRule.type = EPSILON;
                    matchRule.dst = start;
                    nfa.rules[qStart].push_back(matchRule);
                } else {
                    // 贪婪匹配：优先匹配
                    Rule matchRule;
                    matchRule.type = EPSILON;
                    matchRule.dst = start;
                    nfa.rules[qStart].push_back(matchRule);
                    
                    Rule skipRule;
                    skipRule.type = EPSILON;
                    skipRule.dst = qEnd;
                    nfa.rules[qStart].push_back(skipRule);
                }
                
                // 从原始结束状态到新结束状态的ε转移
                Rule connectRule;
                connectRule.type = EPSILON;
                connectRule.dst = qEnd;
                nfa.rules[end].push_back(connectRule);
            }
            else if (quantText[0] == '*') {
                // 0次或多次
                if (isLazy) {
                    // 懒惰匹配：优先结束
                    Rule skipRule;
                    skipRule.type = EPSILON;
                    skipRule.dst = qEnd;
                    nfa.rules[qStart].push_back(skipRule);
                    
                    Rule loopRule;
                    loopRule.type = EPSILON;
                    loopRule.dst = qEnd;
                    nfa.rules[end].push_back(loopRule);
                    
                    Rule repeatRule;
                    repeatRule.type = EPSILON;
                    repeatRule.dst = start;
                    nfa.rules[end].push_back(repeatRule);
                    
                    Rule startRule;
                    startRule.type = EPSILON;
                    startRule.dst = start;
                    nfa.rules[qStart].push_back(startRule);
                } else {
                    // 贪婪匹配：优先循环
                    Rule startRule;
                    startRule.type = EPSILON;
                    startRule.dst = start;
                    nfa.rules[qStart].push_back(startRule);
                    
                    Rule repeatRule;
                    repeatRule.type = EPSILON;
                    repeatRule.dst = start;
                    nfa.rules[end].push_back(repeatRule);
                    
                    Rule loopRule;
                    loopRule.type = EPSILON;
                    loopRule.dst = qEnd;
                    nfa.rules[end].push_back(loopRule);
                    
                    Rule skipRule;
                    skipRule.type = EPSILON;
                    skipRule.dst = qEnd;
                    nfa.rules[qStart].push_back(skipRule);
                }
            }
            else if (quantText[0] == '+') {
                // 1次或多次
                if (isLazy) {
                    // 懒惰匹配：优先结束
                    Rule loopRule;
                    loopRule.type = EPSILON;
                    loopRule.dst = qEnd;
                    nfa.rules[end].push_back(loopRule);
                    
                    Rule repeatRule;
                    repeatRule.type = EPSILON;
                    repeatRule.dst = start;
                    nfa.rules[end].push_back(repeatRule);
                    
                    Rule startRule;
                    startRule.type = EPSILON;
                    startRule.dst = start;
                    nfa.rules[qStart].push_back(startRule);
                } else {
                    // 贪婪匹配：优先循环
                    Rule repeatRule;
                    repeatRule.type = EPSILON;
                    repeatRule.dst = start;
                    nfa.rules[end].push_back(repeatRule);
                    
                    Rule loopRule;
                    loopRule.type = EPSILON;
                    loopRule.dst = qEnd;
                    nfa.rules[end].push_back(loopRule);
                    
                    Rule startRule;
                    startRule.type = EPSILON;
                    startRule.dst = start;
                    nfa.rules[qStart].push_back(startRule);
                }
            }
        }
    }
    else if (auto* singleCtx = dynamic_cast<regexParser::SingleContext*>(node)) {
        // 处理Single节点
        if (singleCtx->char_()) {
            auto charNode = singleCtx->char_();
            Rule r;
            r.dst = end;
            r.type = NORMAL;
            
            if (charNode->EscapedChar()) {
                r.by = parseSpecialChar(charNode->EscapedChar()->getText());
            } else {
                r.by = charNode->getText()[0];
            }
            
            nfa.rules[start].push_back(r);
        }
        else if (singleCtx->characterClass()) {
            // 处理字符类 \d \w \s 等
            Rule r;
            r.dst = end;
            r.type = SPECIAL;
            
            auto classNode = singleCtx->characterClass();
            if (classNode->CharacterClassAnyWord()) r.by = 'w';
            else if (classNode->CharacterClassAnyWordInverted()) r.by = 'W';
            else if (classNode->CharacterClassAnyDecimalDigit()) r.by = 'd';
            else if (classNode->CharacterClassAnyDecimalDigitInverted()) r.by = 'D';
            else if (classNode->CharacterClassAnyBlank()) r.by = 's';
            else if (classNode->CharacterClassAnyBlankInverted()) r.by = 'S';
            
            nfa.rules[start].push_back(r);
        }
        else if (singleCtx->AnyCharacter()) {
            // 处理点号匹配任意字符
            Rule r;
            r.dst = end;
            r.type = SPECIAL;
            r.by = (flags == "s") ? ',' : '.';
            
            nfa.rules[start].push_back(r);
        }
        else if (singleCtx->characterGroup()) {
            // 处理字符组 [a-z] [^0-9] 等
            auto groupCtx = singleCtx->characterGroup();
            bool isNegative = (groupCtx->characterGroupNegativeModifier() != nullptr);
            auto items = groupCtx->characterGroupItem();
            
            if (isNegative) {
                // 处理否定字符组 [^...]
                Rule negRule;
                negRule.dst = end;
                negRule.type = NEGATIVE;
                
                for (auto item : items) {
                    if (auto charInGroup = item->charInGroup()) {
                        Rule subRule;
                        subRule.type = NORMAL;
                        
                        if (charInGroup->EscapedChar()) {
                            subRule.by = parseSpecialChar(charInGroup->EscapedChar()->getText());
                        } else {
                            subRule.by = charInGroup->getText()[0];
                        }
                        
                        negRule.negativeRules.push_back(subRule);
                    }
                    else if (auto charRange = item->characterRange()) {
                        Rule subRule;
                        subRule.type = RANGE;
                        
                        auto fromChar = charRange->charInGroup()[0];
                        auto toChar = charRange->charInGroup()[1];
                        
                        if (fromChar->EscapedChar()) {
                            subRule.by = parseSpecialChar(fromChar->EscapedChar()->getText());
                        } else {
                            subRule.by = fromChar->getText()[0];
                        }
                        
                        if (toChar->EscapedChar()) {
                            subRule.to = parseSpecialChar(toChar->EscapedChar()->getText());
                        } else {
                            subRule.to = toChar->getText()[0];
                        }
                        
                        negRule.negativeRules.push_back(subRule);
                    }
                    else if (auto charClass = item->characterClass()) {
                        Rule subRule;
                        subRule.type = SPECIAL;
                        
                        if (charClass->CharacterClassAnyWord()) subRule.by = 'w';
                        else if (charClass->CharacterClassAnyWordInverted()) subRule.by = 'W';
                        else if (charClass->CharacterClassAnyDecimalDigit()) subRule.by = 'd';
                        else if (charClass->CharacterClassAnyDecimalDigitInverted()) subRule.by = 'D';
                        else if (charClass->CharacterClassAnyBlank()) subRule.by = 's';
                        else if (charClass->CharacterClassAnyBlankInverted()) subRule.by = 'S';
                        
                        negRule.negativeRules.push_back(subRule);
                    }
                }
                
                nfa.rules[start].push_back(negRule);
            } else {
                // 处理普通字符组 [...]
                int itemStart = start;
                
                // 为每个字符组项创建分支
                for (auto item : items) {
                    Rule r;
                    r.dst = end;
                    
                    if (auto charInGroup = item->charInGroup()) {
                        r.type = NORMAL;
                        
                        if (charInGroup->EscapedChar()) {
                            r.by = parseSpecialChar(charInGroup->EscapedChar()->getText());
                        } else {
                            r.by = charInGroup->getText()[0];
                        }
                    }
                    else if (auto charRange = item->characterRange()) {
                        r.type = RANGE;
                        
                        auto fromChar = charRange->charInGroup()[0];
                        auto toChar = charRange->charInGroup()[1];
                        
                        if (fromChar->EscapedChar()) {
                            r.by = parseSpecialChar(fromChar->EscapedChar()->getText());
                        } else {
                            r.by = fromChar->getText()[0];
                        }
                        
                        if (toChar->EscapedChar()) {
                            r.to = parseSpecialChar(toChar->EscapedChar()->getText());
                        } else {
                            r.to = toChar->getText()[0];
                        }
                    }
                    else if (auto charClass = item->characterClass()) {
                        r.type = SPECIAL;
                        
                        if (charClass->CharacterClassAnyWord()) r.by = 'w';
                        else if (charClass->CharacterClassAnyWordInverted()) r.by = 'W';
                        else if (charClass->CharacterClassAnyDecimalDigit()) r.by = 'd';
                        else if (charClass->CharacterClassAnyDecimalDigitInverted()) r.by = 'D';
                        else if (charClass->CharacterClassAnyBlank()) r.by = 's';
                        else if (charClass->CharacterClassAnyBlankInverted()) r.by = 'S';
                    }
                    
                    nfa.rules[itemStart].push_back(r);
                }
            }
        }
    }
}


/**
 * 在给定的输入文本上，进行正则表达式匹配，返回匹配到的第一个结果。
 * 匹配不成功时，返回空vector( return std::vector<std::string>(); ，或使用返回初始化列表的语法 return {}; )；
 * 第二次实验中，匹配成功时，返回仅含一个元素的字符串数组，那个唯一的元素即为匹配结果。例：["abcd"]
 * @param text 输入的文本
 * @return 如上所述
 */
std::vector<std::string> Regex::match(std::string text) {
    // 使用 NFA 的 exec 方法执行匹配
    Path result = nfa.exec(text);

    // 如果匹配成功，返回匹配的文本
    if (!result.states.empty()) {
        return {result.matched_text};
    }

    // 匹配失败，返回空数组
    return {};
}
/**
 * 解析正则表达式的字符串，生成语法分析树。
 * 你应该在compile函数中调用一次本函数，以得到语法分析树。
 * 通常，你不需要改动此函数，也不需要理解此函数实现每一行的具体含义。
 * 但是，你应当对语法分析树的数据结构(RegexContext)有一定的理解，作业文档中有相关的教程可供参考。
 * @param pattern 要解析的正则表达式的字符串
 * @return RegexContext类的对象的指针。保证不为空指针。
 */
regexParser::RegexContext *Regex::parse(const std::string &pattern) {
    if (antlrInputStream) throw std::runtime_error("此Regex对象已被调用过一次parse函数，不可以再次调用！");
    antlrInputStream = new antlr4::ANTLRInputStream(pattern);
    antlrLexer = new regexLexer(antlrInputStream);
    antlrTokenStream = new antlr4::CommonTokenStream(antlrLexer);
    antlrParser = new regexParser(antlrTokenStream);
    regexParser::RegexContext *tree = antlrParser->regex();
    if (!tree) throw std::runtime_error("parser解析失败(函数返回了nullptr)");
    auto errCount = antlrParser->getNumberOfSyntaxErrors();
    if (errCount > 0) throw std::runtime_error("parser解析失败，表达式中有" + std::to_string(errCount) + "个语法错误！");
    if (antlrTokenStream->LA(1) != antlr4::Token::EOF)
        throw std::runtime_error("parser解析失败，解析过程未能到达字符串结尾，可能是由于表达式中间有无法解析的内容！已解析的部分："
                                 + antlrTokenStream->getText(antlrTokenStream->get(0),
                                                             antlrTokenStream->get(antlrTokenStream->index() - 1)));
    return tree;
}

// 此析构函数是为了管理ANTLR语法分析树所使用的内存的。你不需要阅读和理解它。
Regex::~Regex() {
    delete antlrInputStream;
    delete antlrLexer;
    delete antlrTokenStream;
    delete antlrParser;
}
