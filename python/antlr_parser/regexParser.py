# Generated from regex.g4 by ANTLR 4.12.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,25,100,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,1,0,1,0,1,0,5,0,36,8,0,10,0,12,0,39,9,0,1,1,
        4,1,42,8,1,11,1,12,1,43,1,2,1,2,3,2,48,8,2,1,3,1,3,3,3,52,8,3,1,
        4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,3,5,62,8,5,1,6,1,6,3,6,66,8,6,1,6,
        4,6,69,8,6,11,6,12,6,70,1,6,1,6,1,7,1,7,1,8,1,8,1,8,3,8,80,8,8,1,
        9,1,9,1,9,1,9,1,10,1,10,1,11,1,11,3,11,90,8,11,1,12,1,12,1,13,1,
        13,1,14,1,14,1,15,1,15,1,15,0,0,16,0,2,4,6,8,10,12,14,16,18,20,22,
        24,26,28,30,0,4,1,0,14,19,1,0,20,22,2,0,7,9,23,25,4,0,1,4,6,6,8,
        13,20,25,95,0,32,1,0,0,0,2,41,1,0,0,0,4,45,1,0,0,0,6,51,1,0,0,0,
        8,53,1,0,0,0,10,61,1,0,0,0,12,63,1,0,0,0,14,74,1,0,0,0,16,79,1,0,
        0,0,18,81,1,0,0,0,20,85,1,0,0,0,22,87,1,0,0,0,24,91,1,0,0,0,26,93,
        1,0,0,0,28,95,1,0,0,0,30,97,1,0,0,0,32,37,3,2,1,0,33,34,5,1,0,0,
        34,36,3,2,1,0,35,33,1,0,0,0,36,39,1,0,0,0,37,35,1,0,0,0,37,38,1,
        0,0,0,38,1,1,0,0,0,39,37,1,0,0,0,40,42,3,4,2,0,41,40,1,0,0,0,42,
        43,1,0,0,0,43,41,1,0,0,0,43,44,1,0,0,0,44,3,1,0,0,0,45,47,3,6,3,
        0,46,48,3,22,11,0,47,46,1,0,0,0,47,48,1,0,0,0,48,5,1,0,0,0,49,52,
        3,10,5,0,50,52,3,8,4,0,51,49,1,0,0,0,51,50,1,0,0,0,52,7,1,0,0,0,
        53,54,5,2,0,0,54,55,3,0,0,0,55,56,5,3,0,0,56,9,1,0,0,0,57,62,3,28,
        14,0,58,62,3,20,10,0,59,62,5,13,0,0,60,62,3,12,6,0,61,57,1,0,0,0,
        61,58,1,0,0,0,61,59,1,0,0,0,61,60,1,0,0,0,62,11,1,0,0,0,63,65,5,
        4,0,0,64,66,3,14,7,0,65,64,1,0,0,0,65,66,1,0,0,0,66,68,1,0,0,0,67,
        69,3,16,8,0,68,67,1,0,0,0,69,70,1,0,0,0,70,68,1,0,0,0,70,71,1,0,
        0,0,71,72,1,0,0,0,72,73,5,5,0,0,73,13,1,0,0,0,74,75,5,6,0,0,75,15,
        1,0,0,0,76,80,3,30,15,0,77,80,3,20,10,0,78,80,3,18,9,0,79,76,1,0,
        0,0,79,77,1,0,0,0,79,78,1,0,0,0,80,17,1,0,0,0,81,82,3,30,15,0,82,
        83,5,7,0,0,83,84,3,30,15,0,84,19,1,0,0,0,85,86,7,0,0,0,86,21,1,0,
        0,0,87,89,3,26,13,0,88,90,3,24,12,0,89,88,1,0,0,0,89,90,1,0,0,0,
        90,23,1,0,0,0,91,92,5,22,0,0,92,25,1,0,0,0,93,94,7,1,0,0,94,27,1,
        0,0,0,95,96,7,2,0,0,96,29,1,0,0,0,97,98,7,3,0,0,98,31,1,0,0,0,9,
        37,43,47,51,61,65,70,79,89
    ]

class regexParser ( Parser ):

    grammarFileName = "regex.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'|'", "'('", "')'", "'['", "']'", "'^'", 
                     "'-'", "':'", "','", "'{'", "'}'", "'$'", "'.'", "'\\w'", 
                     "'\\W'", "'\\d'", "'\\D'", "'\\s'", "'\\S'", "'*'", 
                     "'+'", "'?'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "AnyCharacter", "CharacterClassAnyWord", 
                      "CharacterClassAnyWordInverted", "CharacterClassAnyDecimalDigit", 
                      "CharacterClassAnyDecimalDigitInverted", "CharacterClassAnyBlank", 
                      "CharacterClassAnyBlankInverted", "ZeroOrMoreQuantifier", 
                      "OneOrMoreQuantifier", "ZeroOrOneQuantifier", "EscapedChar", 
                      "Digit", "Char" ]

    RULE_regex = 0
    RULE_expression = 1
    RULE_expressionItem = 2
    RULE_normalItem = 3
    RULE_group = 4
    RULE_single = 5
    RULE_characterGroup = 6
    RULE_characterGroupNegativeModifier = 7
    RULE_characterGroupItem = 8
    RULE_characterRange = 9
    RULE_characterClass = 10
    RULE_quantifier = 11
    RULE_lazyModifier = 12
    RULE_quantifierType = 13
    RULE_char = 14
    RULE_charInGroup = 15

    ruleNames =  [ "regex", "expression", "expressionItem", "normalItem", 
                   "group", "single", "characterGroup", "characterGroupNegativeModifier", 
                   "characterGroupItem", "characterRange", "characterClass", 
                   "quantifier", "lazyModifier", "quantifierType", "char", 
                   "charInGroup" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    AnyCharacter=13
    CharacterClassAnyWord=14
    CharacterClassAnyWordInverted=15
    CharacterClassAnyDecimalDigit=16
    CharacterClassAnyDecimalDigitInverted=17
    CharacterClassAnyBlank=18
    CharacterClassAnyBlankInverted=19
    ZeroOrMoreQuantifier=20
    OneOrMoreQuantifier=21
    ZeroOrOneQuantifier=22
    EscapedChar=23
    Digit=24
    Char=25

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.12.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RegexContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(regexParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(regexParser.ExpressionContext,i)


        def getRuleIndex(self):
            return regexParser.RULE_regex

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRegex" ):
                listener.enterRegex(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRegex" ):
                listener.exitRegex(self)




    def regex(self):

        localctx = regexParser.RegexContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_regex)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 32
            self.expression()
            self.state = 37
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 33
                self.match(regexParser.T__0)
                self.state = 34
                self.expression()
                self.state = 39
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expressionItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(regexParser.ExpressionItemContext)
            else:
                return self.getTypedRuleContext(regexParser.ExpressionItemContext,i)


        def getRuleIndex(self):
            return regexParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)




    def expression(self):

        localctx = regexParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_expression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 40
                self.expressionItem()
                self.state = 43 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 59761556) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def normalItem(self):
            return self.getTypedRuleContext(regexParser.NormalItemContext,0)


        def quantifier(self):
            return self.getTypedRuleContext(regexParser.QuantifierContext,0)


        def getRuleIndex(self):
            return regexParser.RULE_expressionItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpressionItem" ):
                listener.enterExpressionItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpressionItem" ):
                listener.exitExpressionItem(self)




    def expressionItem(self):

        localctx = regexParser.ExpressionItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_expressionItem)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            self.normalItem()
            self.state = 47
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 7340032) != 0):
                self.state = 46
                self.quantifier()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NormalItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def single(self):
            return self.getTypedRuleContext(regexParser.SingleContext,0)


        def group(self):
            return self.getTypedRuleContext(regexParser.GroupContext,0)


        def getRuleIndex(self):
            return regexParser.RULE_normalItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNormalItem" ):
                listener.enterNormalItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNormalItem" ):
                listener.exitNormalItem(self)




    def normalItem(self):

        localctx = regexParser.NormalItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_normalItem)
        try:
            self.state = 51
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4, 7, 8, 9, 13, 14, 15, 16, 17, 18, 19, 23, 24, 25]:
                self.enterOuterAlt(localctx, 1)
                self.state = 49
                self.single()
                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 2)
                self.state = 50
                self.group()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GroupContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def regex(self):
            return self.getTypedRuleContext(regexParser.RegexContext,0)


        def getRuleIndex(self):
            return regexParser.RULE_group

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGroup" ):
                listener.enterGroup(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGroup" ):
                listener.exitGroup(self)




    def group(self):

        localctx = regexParser.GroupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_group)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self.match(regexParser.T__1)
            self.state = 54
            self.regex()
            self.state = 55
            self.match(regexParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SingleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def char(self):
            return self.getTypedRuleContext(regexParser.CharContext,0)


        def characterClass(self):
            return self.getTypedRuleContext(regexParser.CharacterClassContext,0)


        def AnyCharacter(self):
            return self.getToken(regexParser.AnyCharacter, 0)

        def characterGroup(self):
            return self.getTypedRuleContext(regexParser.CharacterGroupContext,0)


        def getRuleIndex(self):
            return regexParser.RULE_single

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSingle" ):
                listener.enterSingle(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSingle" ):
                listener.exitSingle(self)




    def single(self):

        localctx = regexParser.SingleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_single)
        try:
            self.state = 61
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [7, 8, 9, 23, 24, 25]:
                self.enterOuterAlt(localctx, 1)
                self.state = 57
                self.char()
                pass
            elif token in [14, 15, 16, 17, 18, 19]:
                self.enterOuterAlt(localctx, 2)
                self.state = 58
                self.characterClass()
                pass
            elif token in [13]:
                self.enterOuterAlt(localctx, 3)
                self.state = 59
                self.match(regexParser.AnyCharacter)
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 60
                self.characterGroup()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharacterGroupContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def characterGroupNegativeModifier(self):
            return self.getTypedRuleContext(regexParser.CharacterGroupNegativeModifierContext,0)


        def characterGroupItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(regexParser.CharacterGroupItemContext)
            else:
                return self.getTypedRuleContext(regexParser.CharacterGroupItemContext,i)


        def getRuleIndex(self):
            return regexParser.RULE_characterGroup

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharacterGroup" ):
                listener.enterCharacterGroup(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharacterGroup" ):
                listener.exitCharacterGroup(self)




    def characterGroup(self):

        localctx = regexParser.CharacterGroupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_characterGroup)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self.match(regexParser.T__3)
            self.state = 65
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.state = 64
                self.characterGroupNegativeModifier()


            self.state = 68 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 67
                self.characterGroupItem()
                self.state = 70 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 67108702) != 0)):
                    break

            self.state = 72
            self.match(regexParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharacterGroupNegativeModifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return regexParser.RULE_characterGroupNegativeModifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharacterGroupNegativeModifier" ):
                listener.enterCharacterGroupNegativeModifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharacterGroupNegativeModifier" ):
                listener.exitCharacterGroupNegativeModifier(self)




    def characterGroupNegativeModifier(self):

        localctx = regexParser.CharacterGroupNegativeModifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_characterGroupNegativeModifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74
            self.match(regexParser.T__5)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharacterGroupItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def charInGroup(self):
            return self.getTypedRuleContext(regexParser.CharInGroupContext,0)


        def characterClass(self):
            return self.getTypedRuleContext(regexParser.CharacterClassContext,0)


        def characterRange(self):
            return self.getTypedRuleContext(regexParser.CharacterRangeContext,0)


        def getRuleIndex(self):
            return regexParser.RULE_characterGroupItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharacterGroupItem" ):
                listener.enterCharacterGroupItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharacterGroupItem" ):
                listener.exitCharacterGroupItem(self)




    def characterGroupItem(self):

        localctx = regexParser.CharacterGroupItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_characterGroupItem)
        try:
            self.state = 79
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 76
                self.charInGroup()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 77
                self.characterClass()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 78
                self.characterRange()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharacterRangeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def charInGroup(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(regexParser.CharInGroupContext)
            else:
                return self.getTypedRuleContext(regexParser.CharInGroupContext,i)


        def getRuleIndex(self):
            return regexParser.RULE_characterRange

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharacterRange" ):
                listener.enterCharacterRange(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharacterRange" ):
                listener.exitCharacterRange(self)




    def characterRange(self):

        localctx = regexParser.CharacterRangeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_characterRange)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            self.charInGroup()
            self.state = 82
            self.match(regexParser.T__6)
            self.state = 83
            self.charInGroup()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharacterClassContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CharacterClassAnyWord(self):
            return self.getToken(regexParser.CharacterClassAnyWord, 0)

        def CharacterClassAnyWordInverted(self):
            return self.getToken(regexParser.CharacterClassAnyWordInverted, 0)

        def CharacterClassAnyDecimalDigit(self):
            return self.getToken(regexParser.CharacterClassAnyDecimalDigit, 0)

        def CharacterClassAnyDecimalDigitInverted(self):
            return self.getToken(regexParser.CharacterClassAnyDecimalDigitInverted, 0)

        def CharacterClassAnyBlank(self):
            return self.getToken(regexParser.CharacterClassAnyBlank, 0)

        def CharacterClassAnyBlankInverted(self):
            return self.getToken(regexParser.CharacterClassAnyBlankInverted, 0)

        def getRuleIndex(self):
            return regexParser.RULE_characterClass

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharacterClass" ):
                listener.enterCharacterClass(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharacterClass" ):
                listener.exitCharacterClass(self)




    def characterClass(self):

        localctx = regexParser.CharacterClassContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_characterClass)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1032192) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QuantifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def quantifierType(self):
            return self.getTypedRuleContext(regexParser.QuantifierTypeContext,0)


        def lazyModifier(self):
            return self.getTypedRuleContext(regexParser.LazyModifierContext,0)


        def getRuleIndex(self):
            return regexParser.RULE_quantifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuantifier" ):
                listener.enterQuantifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuantifier" ):
                listener.exitQuantifier(self)




    def quantifier(self):

        localctx = regexParser.QuantifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_quantifier)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 87
            self.quantifierType()
            self.state = 89
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==22:
                self.state = 88
                self.lazyModifier()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LazyModifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ZeroOrOneQuantifier(self):
            return self.getToken(regexParser.ZeroOrOneQuantifier, 0)

        def getRuleIndex(self):
            return regexParser.RULE_lazyModifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLazyModifier" ):
                listener.enterLazyModifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLazyModifier" ):
                listener.exitLazyModifier(self)




    def lazyModifier(self):

        localctx = regexParser.LazyModifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_lazyModifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            self.match(regexParser.ZeroOrOneQuantifier)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QuantifierTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ZeroOrMoreQuantifier(self):
            return self.getToken(regexParser.ZeroOrMoreQuantifier, 0)

        def OneOrMoreQuantifier(self):
            return self.getToken(regexParser.OneOrMoreQuantifier, 0)

        def ZeroOrOneQuantifier(self):
            return self.getToken(regexParser.ZeroOrOneQuantifier, 0)

        def getRuleIndex(self):
            return regexParser.RULE_quantifierType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuantifierType" ):
                listener.enterQuantifierType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuantifierType" ):
                listener.exitQuantifierType(self)




    def quantifierType(self):

        localctx = regexParser.QuantifierTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_quantifierType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 7340032) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EscapedChar(self):
            return self.getToken(regexParser.EscapedChar, 0)

        def Digit(self):
            return self.getToken(regexParser.Digit, 0)

        def Char(self):
            return self.getToken(regexParser.Char, 0)

        def getRuleIndex(self):
            return regexParser.RULE_char

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterChar" ):
                listener.enterChar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitChar" ):
                listener.exitChar(self)




    def char(self):

        localctx = regexParser.CharContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_char)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 58721152) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharInGroupContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EscapedChar(self):
            return self.getToken(regexParser.EscapedChar, 0)

        def Digit(self):
            return self.getToken(regexParser.Digit, 0)

        def Char(self):
            return self.getToken(regexParser.Char, 0)

        def AnyCharacter(self):
            return self.getToken(regexParser.AnyCharacter, 0)

        def ZeroOrMoreQuantifier(self):
            return self.getToken(regexParser.ZeroOrMoreQuantifier, 0)

        def OneOrMoreQuantifier(self):
            return self.getToken(regexParser.OneOrMoreQuantifier, 0)

        def ZeroOrOneQuantifier(self):
            return self.getToken(regexParser.ZeroOrOneQuantifier, 0)

        def getRuleIndex(self):
            return regexParser.RULE_charInGroup

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharInGroup" ):
                listener.enterCharInGroup(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharInGroup" ):
                listener.exitCharInGroup(self)




    def charInGroup(self):

        localctx = regexParser.CharInGroupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_charInGroup)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 97
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 66076510) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





