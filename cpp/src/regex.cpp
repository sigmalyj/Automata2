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
    // 解析正则表达式，生成语法分析树
    regexParser::RegexContext *tree = Regex::parse(pattern);

    // 初始化 NFA 的状态
    nfa.num_states = 0; // 状态计数初始化
    nfa.rules.clear();
    nfa.is_final.clear();

    // 创建起始状态和接受状态
    int startState = nfa.num_states++;
    int acceptState = nfa.num_states++;
    nfa.rules.resize(nfa.num_states); // 确保规则列表大小与状态数一致
    nfa.is_final.resize(nfa.num_states, false);
    nfa.is_final[acceptState] = true;

    // 构造 NFA
    buildNFA(tree, startState, acceptState, flags);

    // 设置 NFA 的起始状态和接受状态
    nfa.is_final[acceptState] = true;
}
/**
 * 递归构造 NFA 的辅助函数。
 * @param node 当前语法树节点
 * @param start 当前 NFA 的起始状态
 * @param end 当前 NFA 的接受状态
 * @param flags 正则表达式的修饰符
 */
void Regex::buildNFA(antlr4::tree::ParseTree *node, int start, int end, const std::string &flags) {
    if (nfa.rules.size() <= std::max(start, end)) {
        nfa.rules.resize(std::max(start, end) + 1);
    }

    if (auto regexNode = dynamic_cast<regexParser::RegexContext *>(node)) {
        // regex: expression ('|' expression)* ;
        int previousState = start;
        for (size_t i = 0; i < regexNode->expression().size(); ++i) {
            int nextState = (i == regexNode->expression().size() - 1) ? end : nfa.num_states++;
            if (nfa.rules.size() <= nextState) {
                nfa.rules.resize(nextState + 1);
            }
            buildNFA(regexNode->expression(i), previousState, nextState, flags);
            previousState = nextState;
        }
    } else if (auto expressionNode = dynamic_cast<regexParser::ExpressionContext *>(node)) {
        // expression: expressionItem+ ;
        int currentStart = start;
        for (size_t i = 0; i < expressionNode->expressionItem().size(); ++i) {
            int nextState = (i == expressionNode->expressionItem().size() - 1) ? end : nfa.num_states++;
            if (nfa.rules.size() <= nextState) {
                nfa.rules.resize(nextState + 1);
            }
            buildNFA(expressionNode->expressionItem(i), currentStart, nextState, flags);
            currentStart = nextState;
        }
    } else if (auto itemNode = dynamic_cast<regexParser::ExpressionItemContext *>(node)) {
        // expressionItem: normalItem quantifier? ;
        if (itemNode->quantifier()) {
            int loopStart = nfa.num_states++;
            int loopEnd = nfa.num_states++;
            if (nfa.rules.size() <= loopEnd) {
                nfa.rules.resize(loopEnd + 1);
            }
            buildNFA(itemNode->normalItem(), loopStart, loopEnd, flags);

            // 处理量词
            if (itemNode->quantifier()->quantifierType()->ZeroOrMoreQuantifier()) {
                nfa.rules[start].push_back({loopStart, EPSILON, "", ""});
                nfa.rules[loopEnd].push_back({loopStart, EPSILON, "", ""});
                nfa.rules[loopEnd].push_back({end, EPSILON, "", ""});
                nfa.rules[start].push_back({end, EPSILON, "", ""});
            } else if (itemNode->quantifier()->quantifierType()->OneOrMoreQuantifier()) {
                nfa.rules[loopEnd].push_back({loopStart, EPSILON, "", ""});
                nfa.rules[loopEnd].push_back({end, EPSILON, "", ""});
            } else if (itemNode->quantifier()->quantifierType()->ZeroOrOneQuantifier()) {
                nfa.rules[start].push_back({end, EPSILON, "", ""});
                nfa.rules[start].push_back({loopStart, EPSILON, "", ""});
                nfa.rules[loopEnd].push_back({end, EPSILON, "", ""});
            }
        } else {
            buildNFA(itemNode->normalItem(), start, end, flags);
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

    // 如果匹配成功，返回匹配的路径
    if (!result.states.empty()) {
        std::string matched;
        for (const auto &consume : result.consumes) {
            matched += consume;
        }
        return {matched};
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
