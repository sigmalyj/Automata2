grammar regex;

regex : expression ('|' expression)* ;

expression : expressionItem+ ;

expressionItem
    : normalItem quantifier?
    ;

normalItem
    : single // 能匹配一个字符的Item，包括普通的单字符、元字符、字符区间等
	| group // 括号分组
	;

/* Group */
group :
    '('
    regex
    ')'
    ;

/* Single */
single
	: char // 单个字符（普通字符或转义字符）
	| characterClass // \d \w等表示一类字符的元字符
	| AnyCharacter // . 匹配任意字符
	| characterGroup // 中括号字符组，如[012a-z]
	;

AnyCharacter : '.';

/* Character Group & Class */
characterGroup : '[' characterGroupNegativeModifier? characterGroupItem+ ']';

characterGroupNegativeModifier : '^'; // 取反，不匹配后面所列的字符

characterGroupItem
	: charInGroup // 单个字符（普通字符或转义字符），除了-（在group中，-表示字符区间的连字符）
	| characterClass // \d \w等表示一类字符的元字符
	| characterRange // 字符区间，例如a-z
	;

characterRange : charInGroup '-' charInGroup;

characterClass // 以下是本实验要求支持的所有表示一类字符的元字符
	: CharacterClassAnyWord
	| CharacterClassAnyWordInverted
	| CharacterClassAnyDecimalDigit
	| CharacterClassAnyDecimalDigitInverted
	| CharacterClassAnyBlank
	| CharacterClassAnyBlankInverted
	;

CharacterClassAnyWord : '\\w';
CharacterClassAnyWordInverted : '\\W';
CharacterClassAnyDecimalDigit : '\\d';
CharacterClassAnyDecimalDigitInverted : '\\D';
CharacterClassAnyBlank: '\\s';
CharacterClassAnyBlankInverted: '\\S';

/* Quantifiers */
quantifier : quantifierType lazyModifier? ;

lazyModifier: ZeroOrOneQuantifier; // 表示非贪婪匹配的问号

quantifierType
	: ZeroOrMoreQuantifier
	| OneOrMoreQuantifier
	| ZeroOrOneQuantifier
	;

ZeroOrMoreQuantifier : '*';
OneOrMoreQuantifier : '+';
ZeroOrOneQuantifier : '?';

/* 字符列表 */
EscapedChar : '\\' ~[0-9] | '\\x' [0-9a-fA-F][0-9a-fA-F]; // 转义字符的含义详见文档中的说明
Digit : [0-9];
Char: . ;

char // 在普通位置（指不在中括号字符组[]当中）可以出现的一般字符
    : EscapedChar | Digit | Char | ':' | ',' // 在任何位置都一定被解析成一般字符的类型
    | '-' // 当-不在[]中时，就算不转义，也可以作为一般的字符处理。
    ;

charInGroup // 在中括号字符组[]当中可以出现的一般字符
    : EscapedChar | Digit | Char | ':' | ',' // 在任何位置都一定被解析成一般字符的类型
    | '|' | '(' | ')' | '[' | '{' | '}' | '.' | '^' | '$' | '*' | '+' | '?' // 这些字符如果出现在[]中，就算不转义，也可以作为一般的字符处理。
    ;
