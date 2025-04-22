# Generated from regex.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .regexParser import regexParser
else:
    from regexParser import regexParser

# This class defines a complete listener for a parse tree produced by regexParser.
class regexListener(ParseTreeListener):

    # Enter a parse tree produced by regexParser#regex.
    def enterRegex(self, ctx:regexParser.RegexContext):
        pass

    # Exit a parse tree produced by regexParser#regex.
    def exitRegex(self, ctx:regexParser.RegexContext):
        pass


    # Enter a parse tree produced by regexParser#expression.
    def enterExpression(self, ctx:regexParser.ExpressionContext):
        pass

    # Exit a parse tree produced by regexParser#expression.
    def exitExpression(self, ctx:regexParser.ExpressionContext):
        pass


    # Enter a parse tree produced by regexParser#expressionItem.
    def enterExpressionItem(self, ctx:regexParser.ExpressionItemContext):
        pass

    # Exit a parse tree produced by regexParser#expressionItem.
    def exitExpressionItem(self, ctx:regexParser.ExpressionItemContext):
        pass


    # Enter a parse tree produced by regexParser#normalItem.
    def enterNormalItem(self, ctx:regexParser.NormalItemContext):
        pass

    # Exit a parse tree produced by regexParser#normalItem.
    def exitNormalItem(self, ctx:regexParser.NormalItemContext):
        pass


    # Enter a parse tree produced by regexParser#group.
    def enterGroup(self, ctx:regexParser.GroupContext):
        pass

    # Exit a parse tree produced by regexParser#group.
    def exitGroup(self, ctx:regexParser.GroupContext):
        pass


    # Enter a parse tree produced by regexParser#single.
    def enterSingle(self, ctx:regexParser.SingleContext):
        pass

    # Exit a parse tree produced by regexParser#single.
    def exitSingle(self, ctx:regexParser.SingleContext):
        pass


    # Enter a parse tree produced by regexParser#characterGroup.
    def enterCharacterGroup(self, ctx:regexParser.CharacterGroupContext):
        pass

    # Exit a parse tree produced by regexParser#characterGroup.
    def exitCharacterGroup(self, ctx:regexParser.CharacterGroupContext):
        pass


    # Enter a parse tree produced by regexParser#characterGroupNegativeModifier.
    def enterCharacterGroupNegativeModifier(self, ctx:regexParser.CharacterGroupNegativeModifierContext):
        pass

    # Exit a parse tree produced by regexParser#characterGroupNegativeModifier.
    def exitCharacterGroupNegativeModifier(self, ctx:regexParser.CharacterGroupNegativeModifierContext):
        pass


    # Enter a parse tree produced by regexParser#characterGroupItem.
    def enterCharacterGroupItem(self, ctx:regexParser.CharacterGroupItemContext):
        pass

    # Exit a parse tree produced by regexParser#characterGroupItem.
    def exitCharacterGroupItem(self, ctx:regexParser.CharacterGroupItemContext):
        pass


    # Enter a parse tree produced by regexParser#characterRange.
    def enterCharacterRange(self, ctx:regexParser.CharacterRangeContext):
        pass

    # Exit a parse tree produced by regexParser#characterRange.
    def exitCharacterRange(self, ctx:regexParser.CharacterRangeContext):
        pass


    # Enter a parse tree produced by regexParser#characterClass.
    def enterCharacterClass(self, ctx:regexParser.CharacterClassContext):
        pass

    # Exit a parse tree produced by regexParser#characterClass.
    def exitCharacterClass(self, ctx:regexParser.CharacterClassContext):
        pass


    # Enter a parse tree produced by regexParser#quantifier.
    def enterQuantifier(self, ctx:regexParser.QuantifierContext):
        pass

    # Exit a parse tree produced by regexParser#quantifier.
    def exitQuantifier(self, ctx:regexParser.QuantifierContext):
        pass


    # Enter a parse tree produced by regexParser#lazyModifier.
    def enterLazyModifier(self, ctx:regexParser.LazyModifierContext):
        pass

    # Exit a parse tree produced by regexParser#lazyModifier.
    def exitLazyModifier(self, ctx:regexParser.LazyModifierContext):
        pass


    # Enter a parse tree produced by regexParser#quantifierType.
    def enterQuantifierType(self, ctx:regexParser.QuantifierTypeContext):
        pass

    # Exit a parse tree produced by regexParser#quantifierType.
    def exitQuantifierType(self, ctx:regexParser.QuantifierTypeContext):
        pass


    # Enter a parse tree produced by regexParser#char.
    def enterChar(self, ctx:regexParser.CharContext):
        pass

    # Exit a parse tree produced by regexParser#char.
    def exitChar(self, ctx:regexParser.CharContext):
        pass


    # Enter a parse tree produced by regexParser#charInGroup.
    def enterCharInGroup(self, ctx:regexParser.CharInGroupContext):
        pass

    # Exit a parse tree produced by regexParser#charInGroup.
    def exitCharInGroup(self, ctx:regexParser.CharInGroupContext):
        pass



del regexParser