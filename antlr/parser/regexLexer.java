// Generated from regex.g4 by ANTLR 4.12.0
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class regexLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.12.0", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, AnyCharacter=13, CharacterClassAnyWord=14, 
		CharacterClassAnyWordInverted=15, CharacterClassAnyDecimalDigit=16, CharacterClassAnyDecimalDigitInverted=17, 
		CharacterClassAnyBlank=18, CharacterClassAnyBlankInverted=19, ZeroOrMoreQuantifier=20, 
		OneOrMoreQuantifier=21, ZeroOrOneQuantifier=22, EscapedChar=23, Digit=24, 
		Char=25;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "T__7", "T__8", 
			"T__9", "T__10", "T__11", "AnyCharacter", "CharacterClassAnyWord", "CharacterClassAnyWordInverted", 
			"CharacterClassAnyDecimalDigit", "CharacterClassAnyDecimalDigitInverted", 
			"CharacterClassAnyBlank", "CharacterClassAnyBlankInverted", "ZeroOrMoreQuantifier", 
			"OneOrMoreQuantifier", "ZeroOrOneQuantifier", "EscapedChar", "Digit", 
			"Char"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'|'", "'('", "')'", "'['", "']'", "'^'", "'-'", "':'", "','", 
			"'{'", "'}'", "'$'", "'.'", "'\\w'", "'\\W'", "'\\d'", "'\\D'", "'\\s'", 
			"'\\S'", "'*'", "'+'", "'?'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, "AnyCharacter", "CharacterClassAnyWord", "CharacterClassAnyWordInverted", 
			"CharacterClassAnyDecimalDigit", "CharacterClassAnyDecimalDigitInverted", 
			"CharacterClassAnyBlank", "CharacterClassAnyBlankInverted", "ZeroOrMoreQuantifier", 
			"OneOrMoreQuantifier", "ZeroOrOneQuantifier", "EscapedChar", "Digit", 
			"Char"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public regexLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "regex.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\u0004\u0000\u0019r\u0006\uffff\uffff\u0002\u0000\u0007\u0000\u0002\u0001"+
		"\u0007\u0001\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004"+
		"\u0007\u0004\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007"+
		"\u0007\u0007\u0002\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b"+
		"\u0007\u000b\u0002\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002"+
		"\u000f\u0007\u000f\u0002\u0010\u0007\u0010\u0002\u0011\u0007\u0011\u0002"+
		"\u0012\u0007\u0012\u0002\u0013\u0007\u0013\u0002\u0014\u0007\u0014\u0002"+
		"\u0015\u0007\u0015\u0002\u0016\u0007\u0016\u0002\u0017\u0007\u0017\u0002"+
		"\u0018\u0007\u0018\u0001\u0000\u0001\u0000\u0001\u0001\u0001\u0001\u0001"+
		"\u0002\u0001\u0002\u0001\u0003\u0001\u0003\u0001\u0004\u0001\u0004\u0001"+
		"\u0005\u0001\u0005\u0001\u0006\u0001\u0006\u0001\u0007\u0001\u0007\u0001"+
		"\b\u0001\b\u0001\t\u0001\t\u0001\n\u0001\n\u0001\u000b\u0001\u000b\u0001"+
		"\f\u0001\f\u0001\r\u0001\r\u0001\r\u0001\u000e\u0001\u000e\u0001\u000e"+
		"\u0001\u000f\u0001\u000f\u0001\u000f\u0001\u0010\u0001\u0010\u0001\u0010"+
		"\u0001\u0011\u0001\u0011\u0001\u0011\u0001\u0012\u0001\u0012\u0001\u0012"+
		"\u0001\u0013\u0001\u0013\u0001\u0014\u0001\u0014\u0001\u0015\u0001\u0015"+
		"\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016"+
		"\u0001\u0016\u0003\u0016m\b\u0016\u0001\u0017\u0001\u0017\u0001\u0018"+
		"\u0001\u0018\u0000\u0000\u0019\u0001\u0001\u0003\u0002\u0005\u0003\u0007"+
		"\u0004\t\u0005\u000b\u0006\r\u0007\u000f\b\u0011\t\u0013\n\u0015\u000b"+
		"\u0017\f\u0019\r\u001b\u000e\u001d\u000f\u001f\u0010!\u0011#\u0012%\u0013"+
		"\'\u0014)\u0015+\u0016-\u0017/\u00181\u0019\u0001\u0000\u0002\u0001\u0000"+
		"09\u0003\u000009AFafr\u0000\u0001\u0001\u0000\u0000\u0000\u0000\u0003"+
		"\u0001\u0000\u0000\u0000\u0000\u0005\u0001\u0000\u0000\u0000\u0000\u0007"+
		"\u0001\u0000\u0000\u0000\u0000\t\u0001\u0000\u0000\u0000\u0000\u000b\u0001"+
		"\u0000\u0000\u0000\u0000\r\u0001\u0000\u0000\u0000\u0000\u000f\u0001\u0000"+
		"\u0000\u0000\u0000\u0011\u0001\u0000\u0000\u0000\u0000\u0013\u0001\u0000"+
		"\u0000\u0000\u0000\u0015\u0001\u0000\u0000\u0000\u0000\u0017\u0001\u0000"+
		"\u0000\u0000\u0000\u0019\u0001\u0000\u0000\u0000\u0000\u001b\u0001\u0000"+
		"\u0000\u0000\u0000\u001d\u0001\u0000\u0000\u0000\u0000\u001f\u0001\u0000"+
		"\u0000\u0000\u0000!\u0001\u0000\u0000\u0000\u0000#\u0001\u0000\u0000\u0000"+
		"\u0000%\u0001\u0000\u0000\u0000\u0000\'\u0001\u0000\u0000\u0000\u0000"+
		")\u0001\u0000\u0000\u0000\u0000+\u0001\u0000\u0000\u0000\u0000-\u0001"+
		"\u0000\u0000\u0000\u0000/\u0001\u0000\u0000\u0000\u00001\u0001\u0000\u0000"+
		"\u0000\u00013\u0001\u0000\u0000\u0000\u00035\u0001\u0000\u0000\u0000\u0005"+
		"7\u0001\u0000\u0000\u0000\u00079\u0001\u0000\u0000\u0000\t;\u0001\u0000"+
		"\u0000\u0000\u000b=\u0001\u0000\u0000\u0000\r?\u0001\u0000\u0000\u0000"+
		"\u000fA\u0001\u0000\u0000\u0000\u0011C\u0001\u0000\u0000\u0000\u0013E"+
		"\u0001\u0000\u0000\u0000\u0015G\u0001\u0000\u0000\u0000\u0017I\u0001\u0000"+
		"\u0000\u0000\u0019K\u0001\u0000\u0000\u0000\u001bM\u0001\u0000\u0000\u0000"+
		"\u001dP\u0001\u0000\u0000\u0000\u001fS\u0001\u0000\u0000\u0000!V\u0001"+
		"\u0000\u0000\u0000#Y\u0001\u0000\u0000\u0000%\\\u0001\u0000\u0000\u0000"+
		"\'_\u0001\u0000\u0000\u0000)a\u0001\u0000\u0000\u0000+c\u0001\u0000\u0000"+
		"\u0000-l\u0001\u0000\u0000\u0000/n\u0001\u0000\u0000\u00001p\u0001\u0000"+
		"\u0000\u000034\u0005|\u0000\u00004\u0002\u0001\u0000\u0000\u000056\u0005"+
		"(\u0000\u00006\u0004\u0001\u0000\u0000\u000078\u0005)\u0000\u00008\u0006"+
		"\u0001\u0000\u0000\u00009:\u0005[\u0000\u0000:\b\u0001\u0000\u0000\u0000"+
		";<\u0005]\u0000\u0000<\n\u0001\u0000\u0000\u0000=>\u0005^\u0000\u0000"+
		">\f\u0001\u0000\u0000\u0000?@\u0005-\u0000\u0000@\u000e\u0001\u0000\u0000"+
		"\u0000AB\u0005:\u0000\u0000B\u0010\u0001\u0000\u0000\u0000CD\u0005,\u0000"+
		"\u0000D\u0012\u0001\u0000\u0000\u0000EF\u0005{\u0000\u0000F\u0014\u0001"+
		"\u0000\u0000\u0000GH\u0005}\u0000\u0000H\u0016\u0001\u0000\u0000\u0000"+
		"IJ\u0005$\u0000\u0000J\u0018\u0001\u0000\u0000\u0000KL\u0005.\u0000\u0000"+
		"L\u001a\u0001\u0000\u0000\u0000MN\u0005\\\u0000\u0000NO\u0005w\u0000\u0000"+
		"O\u001c\u0001\u0000\u0000\u0000PQ\u0005\\\u0000\u0000QR\u0005W\u0000\u0000"+
		"R\u001e\u0001\u0000\u0000\u0000ST\u0005\\\u0000\u0000TU\u0005d\u0000\u0000"+
		"U \u0001\u0000\u0000\u0000VW\u0005\\\u0000\u0000WX\u0005D\u0000\u0000"+
		"X\"\u0001\u0000\u0000\u0000YZ\u0005\\\u0000\u0000Z[\u0005s\u0000\u0000"+
		"[$\u0001\u0000\u0000\u0000\\]\u0005\\\u0000\u0000]^\u0005S\u0000\u0000"+
		"^&\u0001\u0000\u0000\u0000_`\u0005*\u0000\u0000`(\u0001\u0000\u0000\u0000"+
		"ab\u0005+\u0000\u0000b*\u0001\u0000\u0000\u0000cd\u0005?\u0000\u0000d"+
		",\u0001\u0000\u0000\u0000ef\u0005\\\u0000\u0000fm\b\u0000\u0000\u0000"+
		"gh\u0005\\\u0000\u0000hi\u0005x\u0000\u0000ij\u0001\u0000\u0000\u0000"+
		"jk\u0007\u0001\u0000\u0000km\u0007\u0001\u0000\u0000le\u0001\u0000\u0000"+
		"\u0000lg\u0001\u0000\u0000\u0000m.\u0001\u0000\u0000\u0000no\u0007\u0000"+
		"\u0000\u0000o0\u0001\u0000\u0000\u0000pq\t\u0000\u0000\u0000q2\u0001\u0000"+
		"\u0000\u0000\u0002\u0000l\u0000";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}