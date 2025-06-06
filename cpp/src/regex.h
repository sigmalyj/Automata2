#ifndef CPP_REGEX_H
#define CPP_REGEX_H

#include "nfa.h"
#include "parser/regexLexer.h"
#include "parser/regexParser.h"
#include <unordered_set>
#include <vector>
#include <string>
#include <functional>

/**
 * 本文件（包括对应的cpp文件）中已经定义好了一些类和函数，类内也已经定义好了一些成员变量和方法。不建议大家修改这些已经定义好的东西。
 * 但是，为了实现功能，你可以自由地增加新的函数、类等，包括可以在已经定义好的类自由地添加新的成员变量和方法。
 */
/**
 * 保证正则表达式字符串和待操作的文本内容都仅包含ASCII字符，且不包含'\0'。
   * 仅保证pattern不含和换行符'\r' '\n'，但文本串可以含有换行符！
 * 具体要求支持和实现的内容列表，请阅读实验文档的“任务说明”部分。
 * 第二次实验需要实现compile函数（将正则表达式编译为NFA），和match函数（返回串中第一个匹配结果）。
   * 要求支持的特殊字符包括 . \d \w \s \D \W \S
   * 要求支持的flags只有's'一种。
 * 正则表达式中各种字符的具体定义可查看 https://www.runoob.com/regexp/regexp-metachar.html
 */

/**
 * 表示一个正则表达式的类。
 */
class Regex {
public:
    NFA nfa; // 正则表达式所使用的NFA

    /**
     * 解析正则表达式的字符串，生成语法分析树。
     * 你应该在compile函数中调用一次本函数，以得到语法分析树。
     * 通常，你不需要改动此函数，也不需要理解此函数实现每一行的具体含义。
     * 但是，你应当对语法分析树的数据结构(RegexContext)有一定的理解，作业文档中有相关的教程可供参考。
     * @param pattern 要解析的正则表达式的字符串
     * @return RegexContext类的对象的指针。保证不为空指针。
     */
    regexParser::RegexContext *parse(const std::string &pattern);

    /**
     * 编译给定的正则表达式。
     * 具体包括两个过程：解析正则表达式得到语法分析树（这步已经为你写好，即parse方法），
     * 和在语法分析树上进行分析（遍历），构造出NFA（需要你完成的部分）。
     * 在语法分析树上进行分析的方法，可以是直接自行访问该树，也可以是使用antlr的Visitor机制，详见作业文档。
     * 你编译产生的结果，NFA应保存在当前对象的nfa成员变量中，其他内容也建议保存在当前对象下（你可以自由地在本类中声明新的成员）。
     * @param pattern 正则表达式的字符串
     * @param flags 正则表达式的修饰符
     */
    void compile(const std::string &pattern, const std::string &flags = "");

    /**
     * 在给定的输入文本上，进行正则表达式匹配，返回匹配到的第一个结果。
     * 匹配不成功时，返回空vector( return std::vector<std::string>(); ，或使用返回初始化列表的语法 return {}; )；
     * 第二次实验中，匹配成功时，返回仅含一个元素的字符串数组，那个唯一的元素即为匹配结果。例：["abcd"]
     * @param text 输入的文本
     * @return 如上所述
     */
    std::vector<std::string> match(std::string text);

    // 目前仅支持一个默认无参构造函数，且不允许拷贝构造（因为类内有指针）。
    Regex() = default;

    Regex(const Regex &) = delete;

    // 析构函数，和以下那些private变量，是为了管理ANTLR语法分析树所使用的内存的。你不需要阅读和理解它们。
    ~Regex();

private:
    antlr4::ANTLRInputStream *antlrInputStream = nullptr;
    regexLexer *antlrLexer = nullptr;
    antlr4::CommonTokenStream *antlrTokenStream = nullptr;
    regexParser *antlrParser = nullptr;

    /**
     * 辅助函数：递归构造 NFA。
     * @param node 当前语法树节点
     * @param start 当前 NFA 的起始状态
     * @param end 当前 NFA 的接受状态
     */
    void buildNFA(antlr4::tree::ParseTree *node, int start, int end, const std::string &flags);
    char parseSpecialChar(const std::string &sequence);
};

#endif //CPP_REGEX_H