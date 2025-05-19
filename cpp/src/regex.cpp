#include "regex.h"
#include <unordered_map>
#include <stdexcept>
#include <vector>
#include <string>

/**
 * 分析出现的特殊转义字符并进行处理。
 * 能处理以下情况：
 * 1. 常见控制字符的转义序列，如 \n (换行符), \t (制表符) 等。
 * 2. 十六进制转义序列，形式为 \xHH，其中 HH 是十六进制数字，用于表示 ASCII 字符。
 *    如果序列不合法或超出 ASCII 范围，将捕获并处理异常，返回空字符。
 * 3. 预定义字符类，如 \w, \W, \d, \D, \s, \S。
 * 4. 如果输入的字符串不符合上述任何一种格式，函数默认返回字符串的第二个字符。
 * @param sequence: 代表可能包含转义序列的字符串。
 * @return 对应于转义序列的字符，或在处理错误时返回空字符('\0')。
 */
char Regex::parseSpecialChar(const std::string &sequence)
{
    // 处理常见控制字符的转义序列
    static const std::unordered_map<std::string, char> escapeMap = {
        {"\\f", '\f'},
        {"\\n", '\n'},
        {"\\r", '\r'},
        {"\\t", '\t'},
        {"\\v", '\v'}};

    // 检查是否为固定的转义字符
    auto it = escapeMap.find(sequence);
    if (it != escapeMap.end())
    {
        return it->second;
    }

    // 检查是否为十六进制转义序列 \xHH
    if (sequence.size() > 2 && sequence[0] == '\\' && sequence[1] == 'x')
    {
        try
        {
            size_t processedChars = 0;
            int asciiValue = std::stoi(sequence.substr(2), &processedChars, 16);
            if (processedChars != sequence.size() - 2)
            {
                throw std::runtime_error("无效的十六进制序列");
            }
            return static_cast<char>(asciiValue);
        }
        catch (const std::exception &)
        {
            return '\0'; // 返回空字符代表错误
        }
    }

    // 检查是否为预定义字符类
    if (sequence == "\\w")
        return 'w';
    if (sequence == "\\W")
        return 'W';
    if (sequence == "\\d")
        return 'd';
    if (sequence == "\\D")
        return 'D';
    if (sequence == "\\s")
        return 's';
    if (sequence == "\\S")
        return 'S';

    // 默认返回第二个字符，假设输入总是有效的
    return sequence.size() > 1 ? sequence[1] : '\0';
}

/**
 * 递归构造 NFA 的辅助函数。
 * 该函数从语法树的不同节点类型中提取信息，并构造对应的 NFA 片段。
 * @param node 当前语法树节点
 * @param start 当前 NFA 的起始状态
 * @param end 当前 NFA 的接受状态
 * @param flags 正则表达式的修饰符
 */
void Regex::buildNFA(antlr4::tree::ParseTree *node, int start, int end, const std::string &flags)
{
    // 如果节点为空，直接返回
    if (!node)
        return;

    // 根据节点类型处理不同的正则表达式元素
    if (auto charNode = dynamic_cast<regexParser::CharContext *>(node))
    {
        // 处理单个字符
        std::string text = charNode->getText();
        char c;
        
        // 检查是否为转义字符
        if (text.size() > 1 && text[0] == '\\') {
            c = parseSpecialChar(text);
        } else {
            c = text[0];
        }
        
        // 添加状态转移规则
        nfa.rules[start].push_back({end, NORMAL, std::string(1, c)});
    }
    else if (auto singleNode = dynamic_cast<regexParser::SingleContext *>(node))
    {
        // 处理单个字符、字符类或任意字符
        if (singleNode->char_())
        {
            std::string text = singleNode->char_()->getText();
            char c;
            
            // 检查是否为转义字符
            if (text.size() > 1 && text[0] == '\\') {
                c = parseSpecialChar(text);
            } else {
                c = text[0];
            }
            
            nfa.rules[start].push_back({end, NORMAL, std::string(1, c)});
        }
        else if (singleNode->characterClass())
        {
            char c = parseSpecialChar(singleNode->characterClass()->getText());
            nfa.rules[start].push_back({end, SPECIAL, std::string(1, c)});
        }
        else if (singleNode->AnyCharacter())
        {
            // 点号匹配任意字符
            nfa.rules[start].push_back({end, SPECIAL, "."});
        }
        else if (singleNode->characterGroup())
        {
            // 处理字符组 [...]
            auto groupCtx = singleNode->characterGroup();
            
            // 检查是否为否定字符组 [^...]
            bool isNegative = (groupCtx->characterGroupNegativeModifier() != nullptr);
            
            if (isNegative) {
                // 处理否定字符组
                nfa.rules[start].push_back({end, NEGATIVE, ""});
                
                // 添加字符组中的所有项
                for (auto item : groupCtx->characterGroupItem()) {
                    if (auto charInGroup = item->charInGroup()) {
                        std::string text = charInGroup->getText();
                        char c = (text.size() > 1 && text[0] == '\\') ? 
                            parseSpecialChar(text) : text[0];
                        
                        Rule negRule;
                        negRule.type = NORMAL;
                        negRule.by = c;
                        nfa.rules[start].back().negativeRules.push_back(negRule);
                    }
                    else if (auto charRange = item->characterRange()) {
                        auto charInGroupList = charRange->charInGroup();
                        std::string startText = charInGroupList[0]->getText();
                        std::string endText = charInGroupList[1]->getText();
                        
                        char startChar = (startText.size() > 1 && startText[0] == '\\') ? 
                            parseSpecialChar(startText) : startText[0];
                        char endChar = (endText.size() > 1 && endText[0] == '\\') ? 
                            parseSpecialChar(endText) : endText[0];
                        
                        Rule negRule;
                        negRule.type = RANGE;
                        negRule.by = startChar;
                        negRule.to = endChar;
                        nfa.rules[start].back().negativeRules.push_back(negRule);
                    }
                }
            } else {
                // 处理普通字符组
                int intermediateStart = nfa.num_states++;
                int intermediateEnd = end;
                nfa.rules.resize(nfa.num_states);
                
                // 从起始状态到中间状态的 epsilon 转移
                nfa.rules[start].push_back({intermediateStart, EPSILON, ""});
                
                // 添加字符组中的所有项
                for (auto item : groupCtx->characterGroupItem()) {
                    if (auto charInGroup = item->charInGroup()) {
                        std::string text = charInGroup->getText();
                        char c = (text.size() > 1 && text[0] == '\\') ? 
                            parseSpecialChar(text) : text[0];
                        
                        nfa.rules[intermediateStart].push_back({intermediateEnd, NORMAL, std::string(1, c)});
                    }
                    else if (auto charRange = item->characterRange()) {
                        auto charInGroupList = charRange->charInGroup();
                        std::string startText = charInGroupList[0]->getText();
                        std::string endText = charInGroupList[1]->getText();
                        
                        char startChar = (startText.size() > 1 && startText[0] == '\\') ? 
                            parseSpecialChar(startText) : startText[0];
                        char endChar = (endText.size() > 1 && endText[0] == '\\') ? 
                            parseSpecialChar(endText) : endText[0];
                        
                        nfa.rules[intermediateStart].push_back({intermediateEnd, RANGE, std::string(1, startChar), std::string(1, endChar)});
                    }
                }
            }
        }
    }
    else if (auto groupNode = dynamic_cast<regexParser::GroupContext *>(node))
    {
        // 处理分组
        int groupStart = nfa.num_states++;
        int groupEnd = nfa.num_states++;
        nfa.rules.resize(nfa.num_states);
        
        // 添加从起始状态到组起始状态的 epsilon 转移
        nfa.rules[start].push_back({groupStart, EPSILON, ""});
        
        // 递归构建组内的 NFA
        buildNFA(groupNode->regex(), groupStart, groupEnd, flags);
        
        // 添加从组结束状态到结束状态的 epsilon 转移
        nfa.rules[groupEnd].push_back({end, EPSILON, ""});
    }
    else if (auto expressionItemNode = dynamic_cast<regexParser::ExpressionItemContext *>(node))
    {
        // 处理表达式项
        auto normalItem = expressionItemNode->normalItem();
        auto quantifier = expressionItemNode->quantifier();
        
        // 首先处理普通项
        if (normalItem) {
            if (normalItem->single()) {
                buildNFA(normalItem->single(), start, end, flags);
            } else if (normalItem->group()) {
                buildNFA(normalItem->group(), start, end, flags);
            }
        }
        
        // 如果有量词，修改状态转移
        if (quantifier) {
            std::string quantifierText = quantifier->getText();
            char quantifierType = quantifierText[0];
            
            switch (quantifierType) {
                case '*': // 0次或多次
                    nfa.rules[start].push_back({end, EPSILON, ""});  // 0次
                    nfa.rules[end].push_back({start, EPSILON, ""});  // 多次
                    break;
                case '+': // 1次或多次
                    nfa.rules[end].push_back({start, EPSILON, ""});  // 多次(至少1次)
                    break;
                case '?': // 0次或1次
                    nfa.rules[start].push_back({end, EPSILON, ""});  // 0次
                    break;
            }
        }
    }
    else if (auto expressionNode = dynamic_cast<regexParser::ExpressionContext *>(node))
    {
        // 处理表达式（连接多个项）
        std::vector<regexParser::ExpressionItemContext*> items = expressionNode->expressionItem();
        
        if (items.empty()) {
            // 空表达式，直接连接起始和结束状态
            nfa.rules[start].push_back({end, EPSILON, ""});
        } else if (items.size() == 1) {
            // 单个表达式项，直接处理
            buildNFA(items[0], start, end, flags);
        } else {
            // 多个表达式项，连接起来
            int currentStart = start;
            
            for (int i = 0; i < items.size() - 1; i++) {
                int intermediateState = nfa.num_states++;
                nfa.rules.resize(nfa.num_states);
                
                buildNFA(items[i], currentStart, intermediateState, flags);
                currentStart = intermediateState;
            }
            
            // 处理最后一个表达式项
            buildNFA(items.back(), currentStart, end, flags);
        }
    }
    else if (auto regexNode = dynamic_cast<regexParser::RegexContext *>(node))
    {
        // 处理选择（|）
        std::vector<regexParser::ExpressionContext*> expressions = regexNode->expression();
        
        if (expressions.empty()) {
            // 空正则表达式，直接连接起始和结束状态
            nfa.rules[start].push_back({end, EPSILON, ""});
        } else if (expressions.size() == 1) {
            // 单个表达式，直接处理
            buildNFA(expressions[0], start, end, flags);
        } else {
            // 多个表达式（选择），创建分支
            for (auto expr : expressions) {
                int branchStart = nfa.num_states++;
                int branchEnd = nfa.num_states++;
                nfa.rules.resize(nfa.num_states);
                
                // 从起始状态到分支起始状态的 epsilon 转移
                nfa.rules[start].push_back({branchStart, EPSILON, ""});
                
                // 处理分支
                buildNFA(expr, branchStart, branchEnd, flags);
                
                // 从分支结束状态到结束状态的 epsilon 转移
                nfa.rules[branchEnd].push_back({end, EPSILON, ""});
            }
        }
    }
}

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
 * 在给定的输入文本上，进行正则表达式匹配，返回匹配到的第一个结果。
 * 匹配不成功时，返回空vector( return std::vector<std::string>(); ，或使用返回初始化列表的语法 return {}; )；
 * 第二次实验中，匹配成功时，返回仅含一个元素的字符串数组，那个唯一的元素即为匹配结果。例：["abcd"]
 * @param text 输入的文本
 * @return 如上所述
 */
std::vector<std::string> Regex::match(std::string text)
{
    // 遍历文本的每个位置，尝试匹配
    for (int i = 0; i < text.size(); i++)
    {
        Path path = nfa.exec(text.substr(i));
        if (!path.states.empty())
        {
            // 构造匹配结果字符串
            std::string matchedStr;
            for (const auto &ch : path.consumes)
            {
                matchedStr += ch;
            }
            return {matchedStr}; // 返回包含匹配结果的数组
        }
    }
    return {}; // 匹配失败返回空数组
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
