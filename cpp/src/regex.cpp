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
    regexParser::RegexContext *tree = Regex::parse(pattern); // 这是语法分析树
    // TODO 第二次实验中，请你完成这个函数
    //
}

/**
 * 在给定的输入文本上，进行正则表达式匹配，返回匹配到的第一个结果。
 * 匹配不成功时，返回空vector( return std::vector<std::string>(); ，或使用返回初始化列表的语法 return {}; )；
 * 第二次实验中，匹配成功时，返回仅含一个元素的字符串数组，那个唯一的元素即为匹配结果。例：["abcd"]
 * @param text 输入的文本
 * @return 如上所述
 */
std::vector<std::string> Regex::match(std::string text) {
    // TODO 第二次实验中，请你完成这个函数
    //
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
