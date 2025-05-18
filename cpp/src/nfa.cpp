#include "nfa.h"
#include <sstream>
#include <stack>
#include <tuple>
#include <utility>
#include <vector>
#include <set>
#include "utils.h"
using namespace std;

/**
 * 在自动机上执行指定的输入字符串。
 * @param text 输入字符串
 * @return 若拒绝，请 return Path::reject(); 。若接受，请手工构造一个Path的实例并返回。
 */

bool MatchRule(const Rule &rule, char c)
{
    if (rule.type == NORMAL)
    {
        return rule.by[0] == c;
    }
    else if (rule.type == RANGE)
    {
        return rule.by[0] <= c && c <= rule.to[0];
    }
    else if (rule.type == SPECIAL)
    {
        if (rule.by == ".")
            return !(c == '\r' || c == '\n');
        else if (rule.by == "d")
            return isdigit(c);
        else if (rule.by == "w")
            return isalnum(c) || c == '_';
        else if (rule.by == "D")
            return !isdigit(c);
        else if (rule.by == "W")
            return !isalnum(c) && c != '_';
        else if (rule.by == "s")
            return isspace(c);
        else if (rule.by == "W")
            return !isalnum(c) && c != '_';
        else if (rule.by == "S")
            return !isspace(c);
        else if (rule.by == "D")
            return !isdigit(c);
    }
    return false;
}

Path NFA::exec(std::string text) {
    // 遍历输入字符串的每个位置，尝试从该位置开始匹配
    for (size_t start_pos = 0; start_pos <= text.length(); ++start_pos) {
        // 获取从当前位置开始的子字符串
        std::string substring = text.substr(start_pos);
        
        // 初始化一个栈，栈中存放当前状态、剩余字符串和路径
        std::stack<std::tuple<int, std::string, Path>> s;
        s.push({0, substring, Path()}); // 初态，子字符串，初始路径
        std::set<std::pair<int, std::string>> visited; // 使用一个集合记录访问过的状态和输入位置组合

        while (!s.empty()) {
            // 获取当前状态、剩余字符串和路径
            auto [state, str, path] = s.top();
            s.pop();

            // 如果当前状态和剩余字符串的组合已经访问过，跳过
            if (visited.count({state, str}) > 0) {
                continue;
            }
            visited.insert({state, str}); // 标记当前状态和剩余字符串的组合为已访问

            // 将当前状态加入路径
            path.states.push_back(state);

            // 如果当前状态是终态，返回路径
            if (is_final[state]) {
                // 计算已匹配的文本长度
                size_t matched_length = substring.length() - str.length();
                // 提取匹配的文本
                path.matched_text = substring.substr(0, matched_length);
                return path;
            }

            // 遍历当前状态的所有转移规则
            for (const auto &rule : rules[state]) {
                if (rule.type == EPSILON) { // epsilon-转移
                    Path new_path = path;
                    new_path.consumes.push_back(""); // 记录空字符消耗
                    s.push({rule.dst, str, new_path});
                } else if (!str.empty() && MatchRule(rule, str[0])) { // 一般转移
                    Path new_path = path;
                    new_path.consumes.push_back(str.substr(0, 1)); // 记录消耗的字符
                    s.push({rule.dst, str.substr(1), new_path});
                }
            }
        }
    }

    // 如果没有找到路径，返回拒绝
    return Path::reject();
}
/**
 * 将Path转为（序列化为）文本的表达格式（以便于通过stdout输出）
 * 你不需要理解此函数的含义、阅读此函数的实现和调用此函数。
 */
std::ostream &operator<<(std::ostream &os, Path &path)
{
    if (!path.states.empty())
    {
        if (path.consumes.size() != path.states.size() - 1)
        {
            os << "Path对象无效：consumes.size()不等于states.size()-1！";
            return os;
        }
        for (int i = 0; i < path.consumes.size(); ++i)
        {
            os << path.states[i] << " " << path.consumes[i] << " ";
        }
        os << path.states[path.states.size() - 1];
    }
    else
        os << std::string("Reject");
    return os;
}

/**
 * 从自动机的文本表示构造自动机
 * 你不需要理解此函数的含义、阅读此函数的实现和调用此函数。
 */
NFA NFA::from_text(const std::string &text)
{
    NFA nfa = NFA();
    bool reading_rules = false;
    std::istringstream ss(text);
    std::string line, type;
    while (std::getline(ss, line))
    {
        if (line.empty())
            continue;
        if (line.find("type:") == 0)
        {
            type = strip(line.substr(5));
            continue;
        }
        if (type != "nfa")
            throw std::runtime_error("输入文件的类型不是nfa！");
        if (line.find("states:") == 0)
        {
            nfa.num_states = std::stoi(line.substr(7));
            for (int i = 0; i < nfa.num_states; ++i)
            {
                nfa.rules.emplace_back();
                nfa.is_final.push_back(false);
            }
            continue;
        }
        else if (line.find("final:") == 0)
        {
            if (nfa.num_states == 0)
                throw std::runtime_error("states必须出现在final和rules之前!");
            std::istringstream ss2(line.substr(6));
            int t;
            while (true)
            {
                ss2 >> t;
                if (!ss2.fail())
                    nfa.is_final[t] = true;
                else
                    break;
            }
            reading_rules = false;
            if (ss2.eof())
                continue;
        }
        else if (line.find("rules:") == 0)
        {
            if (nfa.num_states == 0)
                throw std::runtime_error("states必须出现在final和rules之前!");
            reading_rules = true;
            continue;
        }
        else if (line.find("input:") == 0)
        {
            reading_rules = false;
            continue;
        }
        else if (reading_rules)
        {
            auto arrow_pos = line.find("->"), space_pos = line.find(' ');
            if (arrow_pos != std::string::npos && space_pos != std::string::npos && arrow_pos < space_pos)
            {
                int src = std::stoi(line.substr(0, arrow_pos));
                int dst = std::stoi(line.substr(arrow_pos + 2, space_pos - (arrow_pos + 2)));
                auto content = line.substr(space_pos + 1);
                bool success = true;
                while (success && !content.empty())
                {
                    auto p = content.find(' ');
                    if (p == std::string::npos)
                        p = content.size();
                    else if (p == 0)
                        p = 1; // 当第一个字母是空格时，说明转移的字符就是空格。于是假定第二个字母也是空格（如果不是，会在后面直接报错）
                    Rule rule{dst};
                    if (p == 3 && content[1] == '-')
                    {
                        rule.type = RANGE;
                        rule.by = content[0];
                        rule.to = content[2];
                    }
                    else if (p == 2 && content[0] == '\\')
                    {
                        if (content[1] == 'e')
                            rule.type = EPSILON;
                        else
                        {
                            rule.type = SPECIAL;
                            rule.by = content[1];
                        }
                    }
                    else if (p == 1 && (p >= content.length() || content[p] == ' '))
                    {
                        rule.type = NORMAL;
                        rule.by = content[0];
                    }
                    else
                        success = false;
                    nfa.rules[src].push_back(rule);
                    content = content.substr(std::min(p + 1, content.size()));
                }
                if (success)
                    continue;
            }
        }
    }
    if (!ss.eof())
        throw std::runtime_error("无法parse输入文件！(stringstream在getline的过程中发生错误)");
    return nfa;
}
