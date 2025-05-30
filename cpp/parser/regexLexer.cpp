
// Generated from regex.g4 by ANTLR 4.12.0


#include "regexLexer.h"


using namespace antlr4;



using namespace antlr4;

namespace {

struct RegexLexerStaticData final {
  RegexLexerStaticData(std::vector<std::string> ruleNames,
                          std::vector<std::string> channelNames,
                          std::vector<std::string> modeNames,
                          std::vector<std::string> literalNames,
                          std::vector<std::string> symbolicNames)
      : ruleNames(std::move(ruleNames)), channelNames(std::move(channelNames)),
        modeNames(std::move(modeNames)), literalNames(std::move(literalNames)),
        symbolicNames(std::move(symbolicNames)),
        vocabulary(this->literalNames, this->symbolicNames) {}

  RegexLexerStaticData(const RegexLexerStaticData&) = delete;
  RegexLexerStaticData(RegexLexerStaticData&&) = delete;
  RegexLexerStaticData& operator=(const RegexLexerStaticData&) = delete;
  RegexLexerStaticData& operator=(RegexLexerStaticData&&) = delete;

  std::vector<antlr4::dfa::DFA> decisionToDFA;
  antlr4::atn::PredictionContextCache sharedContextCache;
  const std::vector<std::string> ruleNames;
  const std::vector<std::string> channelNames;
  const std::vector<std::string> modeNames;
  const std::vector<std::string> literalNames;
  const std::vector<std::string> symbolicNames;
  const antlr4::dfa::Vocabulary vocabulary;
  antlr4::atn::SerializedATNView serializedATN;
  std::unique_ptr<antlr4::atn::ATN> atn;
};

::antlr4::internal::OnceFlag regexlexerLexerOnceFlag;
RegexLexerStaticData *regexlexerLexerStaticData = nullptr;

void regexlexerLexerInitialize() {
  assert(regexlexerLexerStaticData == nullptr);
  auto staticData = std::make_unique<RegexLexerStaticData>(
    std::vector<std::string>{
      "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "T__7", "T__8", 
      "T__9", "T__10", "T__11", "AnyCharacter", "CharacterClassAnyWord", 
      "CharacterClassAnyWordInverted", "CharacterClassAnyDecimalDigit", 
      "CharacterClassAnyDecimalDigitInverted", "CharacterClassAnyBlank", 
      "CharacterClassAnyBlankInverted", "ZeroOrMoreQuantifier", "OneOrMoreQuantifier", 
      "ZeroOrOneQuantifier", "EscapedChar", "Digit", "Char"
    },
    std::vector<std::string>{
      "DEFAULT_TOKEN_CHANNEL", "HIDDEN"
    },
    std::vector<std::string>{
      "DEFAULT_MODE"
    },
    std::vector<std::string>{
      "", "'|'", "'('", "')'", "'['", "']'", "'^'", "'-'", "':'", "','", 
      "'{'", "'}'", "'$'", "'.'", "'\\w'", "'\\W'", "'\\d'", "'\\D'", "'\\s'", 
      "'\\S'", "'*'", "'+'", "'\\u003F'"
    },
    std::vector<std::string>{
      "", "", "", "", "", "", "", "", "", "", "", "", "", "AnyCharacter", 
      "CharacterClassAnyWord", "CharacterClassAnyWordInverted", "CharacterClassAnyDecimalDigit", 
      "CharacterClassAnyDecimalDigitInverted", "CharacterClassAnyBlank", 
      "CharacterClassAnyBlankInverted", "ZeroOrMoreQuantifier", "OneOrMoreQuantifier", 
      "ZeroOrOneQuantifier", "EscapedChar", "Digit", "Char"
    }
  );
  static const int32_t serializedATNSegment[] = {
  	4,0,25,114,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
  	6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,2,14,
  	7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,7,20,2,21,
  	7,21,2,22,7,22,2,23,7,23,2,24,7,24,1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,
  	4,1,4,1,5,1,5,1,6,1,6,1,7,1,7,1,8,1,8,1,9,1,9,1,10,1,10,1,11,1,11,1,12,
  	1,12,1,13,1,13,1,13,1,14,1,14,1,14,1,15,1,15,1,15,1,16,1,16,1,16,1,17,
  	1,17,1,17,1,18,1,18,1,18,1,19,1,19,1,20,1,20,1,21,1,21,1,22,1,22,1,22,
  	1,22,1,22,1,22,1,22,3,22,109,8,22,1,23,1,23,1,24,1,24,0,0,25,1,1,3,2,
  	5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,23,12,25,13,27,14,29,15,31,
  	16,33,17,35,18,37,19,39,20,41,21,43,22,45,23,47,24,49,25,1,0,2,1,0,48,
  	57,3,0,48,57,65,70,97,102,114,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,
  	1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,0,0,
  	0,0,19,1,0,0,0,0,21,1,0,0,0,0,23,1,0,0,0,0,25,1,0,0,0,0,27,1,0,0,0,0,
  	29,1,0,0,0,0,31,1,0,0,0,0,33,1,0,0,0,0,35,1,0,0,0,0,37,1,0,0,0,0,39,1,
  	0,0,0,0,41,1,0,0,0,0,43,1,0,0,0,0,45,1,0,0,0,0,47,1,0,0,0,0,49,1,0,0,
  	0,1,51,1,0,0,0,3,53,1,0,0,0,5,55,1,0,0,0,7,57,1,0,0,0,9,59,1,0,0,0,11,
  	61,1,0,0,0,13,63,1,0,0,0,15,65,1,0,0,0,17,67,1,0,0,0,19,69,1,0,0,0,21,
  	71,1,0,0,0,23,73,1,0,0,0,25,75,1,0,0,0,27,77,1,0,0,0,29,80,1,0,0,0,31,
  	83,1,0,0,0,33,86,1,0,0,0,35,89,1,0,0,0,37,92,1,0,0,0,39,95,1,0,0,0,41,
  	97,1,0,0,0,43,99,1,0,0,0,45,108,1,0,0,0,47,110,1,0,0,0,49,112,1,0,0,0,
  	51,52,5,124,0,0,52,2,1,0,0,0,53,54,5,40,0,0,54,4,1,0,0,0,55,56,5,41,0,
  	0,56,6,1,0,0,0,57,58,5,91,0,0,58,8,1,0,0,0,59,60,5,93,0,0,60,10,1,0,0,
  	0,61,62,5,94,0,0,62,12,1,0,0,0,63,64,5,45,0,0,64,14,1,0,0,0,65,66,5,58,
  	0,0,66,16,1,0,0,0,67,68,5,44,0,0,68,18,1,0,0,0,69,70,5,123,0,0,70,20,
  	1,0,0,0,71,72,5,125,0,0,72,22,1,0,0,0,73,74,5,36,0,0,74,24,1,0,0,0,75,
  	76,5,46,0,0,76,26,1,0,0,0,77,78,5,92,0,0,78,79,5,119,0,0,79,28,1,0,0,
  	0,80,81,5,92,0,0,81,82,5,87,0,0,82,30,1,0,0,0,83,84,5,92,0,0,84,85,5,
  	100,0,0,85,32,1,0,0,0,86,87,5,92,0,0,87,88,5,68,0,0,88,34,1,0,0,0,89,
  	90,5,92,0,0,90,91,5,115,0,0,91,36,1,0,0,0,92,93,5,92,0,0,93,94,5,83,0,
  	0,94,38,1,0,0,0,95,96,5,42,0,0,96,40,1,0,0,0,97,98,5,43,0,0,98,42,1,0,
  	0,0,99,100,5,63,0,0,100,44,1,0,0,0,101,102,5,92,0,0,102,109,8,0,0,0,103,
  	104,5,92,0,0,104,105,5,120,0,0,105,106,1,0,0,0,106,107,7,1,0,0,107,109,
  	7,1,0,0,108,101,1,0,0,0,108,103,1,0,0,0,109,46,1,0,0,0,110,111,7,0,0,
  	0,111,48,1,0,0,0,112,113,9,0,0,0,113,50,1,0,0,0,2,0,108,0
  };
  staticData->serializedATN = antlr4::atn::SerializedATNView(serializedATNSegment, sizeof(serializedATNSegment) / sizeof(serializedATNSegment[0]));

  antlr4::atn::ATNDeserializer deserializer;
  staticData->atn = deserializer.deserialize(staticData->serializedATN);

  const size_t count = staticData->atn->getNumberOfDecisions();
  staticData->decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    staticData->decisionToDFA.emplace_back(staticData->atn->getDecisionState(i), i);
  }
  regexlexerLexerStaticData = staticData.release();
}

}

regexLexer::regexLexer(CharStream *input) : Lexer(input) {
  regexLexer::initialize();
  _interpreter = new atn::LexerATNSimulator(this, *regexlexerLexerStaticData->atn, regexlexerLexerStaticData->decisionToDFA, regexlexerLexerStaticData->sharedContextCache);
}

regexLexer::~regexLexer() {
  delete _interpreter;
}

std::string regexLexer::getGrammarFileName() const {
  return "regex.g4";
}

const std::vector<std::string>& regexLexer::getRuleNames() const {
  return regexlexerLexerStaticData->ruleNames;
}

const std::vector<std::string>& regexLexer::getChannelNames() const {
  return regexlexerLexerStaticData->channelNames;
}

const std::vector<std::string>& regexLexer::getModeNames() const {
  return regexlexerLexerStaticData->modeNames;
}

const dfa::Vocabulary& regexLexer::getVocabulary() const {
  return regexlexerLexerStaticData->vocabulary;
}

antlr4::atn::SerializedATNView regexLexer::getSerializedATN() const {
  return regexlexerLexerStaticData->serializedATN;
}

const atn::ATN& regexLexer::getATN() const {
  return *regexlexerLexerStaticData->atn;
}




void regexLexer::initialize() {
  ::antlr4::internal::call_once(regexlexerLexerOnceFlag, regexlexerLexerInitialize);
}
