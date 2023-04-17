#  Copyright (c) 2021. Created by Mateusz Slazynski for the educational purposes.
#     Feel free to use/modify this code for any greater good.
#     It would be nice however if you mentioned me somewhere.
#     Still, no pressure - have a nice day!

from src.sprdpl.parse import ParseResult
from src.sprdpl import parse
from src.term import *
from src.type import LambdaType, BaseType, ArrowType


class TypedLambdaParser:

    def __init__(self):
        self.tokens = {
            'COMMENT': (r'#[^\n]*\n', lambda _: None),
            'LAMBDA': r'\\[ \t\n]*',
            'DOT': r'\.[ \t\n]*',
            'ARROW': r'[ \t\n]*->[ \t\n]*',
            'TRUE': r'true',
            'FALSE': r'false',
            'ZERO': r'0',
            'UNIT': r'unit',
            'PRED': r'pred[ \t\n]*',
            'SUCC': r'succ[ \t\n]*',
            'ISZERO': r'iszero[ \t\n]*',
            'IF': r'if[ \t\n]*',
            'THEN': r'[ \t\n]*then[ \t\n]*',
            'ELSE': r'[ \t\n]*else[ \t\n]*',
            'LETREC': r'[ \t\n]*letrec[ \t\n]*',
            'LET': r'[ \t\n]*let[ \t\n]*',
            'IN': r'[ \t\n]*in[ \t\n]*',
            'FIX': r'[ \t\n]*fix[ \t\n]*',
            'EQ': r"[ \t\n]=[ \t\n]*",
            'LPAR': r'\(',
            'SEMICOLON': r"[ \t\n];[ \t\n]*",
            'RPAR': r'\)',
            'COLON': r'[ \t\n]*:[ \t\n]*',
            'SPACE':  r'[ \t\n]+',
            'IDENTIFIER': r'[a-zA-Z][\w]*',
        }

        def reduce_app(p: ParseResult) -> Term:
            if p[1] is None:
                return p[0]
            return TmApp(p[0].info, p[0], p[1][1])

        def reduce_par_app(p: ParseResult) -> Term:
            if p[3] is None:
                return p[1]
            return TmApp(p[1].info, p[1], p[3][1])

        def reduce_abs_app(p: ParseResult) -> Term:
            if p[1] is None:
                return p[0]
            return TmAbs(p[0].info, p[0].arg,  p[1][1], TmApp(p[0].info, p[0].body))

        def reduce_base_type(p: ParseResult) -> LambdaType:
            return BaseType.from_text(p[0])

        def reduce_type(p: ParseResult) -> LambdaType:
            if p[1] is None:
                return p[0]
            return ArrowType(p[0], p[1][1])

        def reduce_par_type(p: ParseResult) -> LambdaType:
            if p[3] is None:
                return p[1]
            return ArrowType(p[1], p[3][1])

        self.grammar = [
            ['term', 'zero', 'unit', 'succ', 'pred', 'iszero', 'fix', 'if', 'true', 'false'],
            ['term', ('variable term_p', reduce_app)],
            ['term', ('abstraction term_p', reduce_abs_app)],
            ['term', ('LPAR term RPAR term_p', reduce_par_app)],
            ['term', ('let term_p', reduce_app)],
            ['term', ('letrec term_p', reduce_app)],
            ['term_p', 'SPACE term'],
            ['term_p', '{}'],
            ['true', ('TRUE', lambda p: TmTrue(Info.from_sprdl_info(p.get_info(0))))],
            ['false', ('FALSE', lambda p: TmFalse(Info.from_sprdl_info(p.get_info(0))))],
            ['if',
             ('IF term THEN term ELSE term', lambda p: TmIf(Info.from_sprdl_info(p.get_info(0)), p[1], p[3], p[5]))],
            ['zero', ('ZERO', lambda p: TmZero(Info.from_sprdl_info(p.get_info(0))))],
            ['unit', ('UNIT', lambda p: TmUnit(Info.from_sprdl_info(p.get_info(0))))],
            ['succ', ('SUCC term', lambda p: TmSucc(Info.from_sprdl_info(p.get_info(0)), p[1]))],
            ['pred', ('PRED term', lambda p: TmPred(Info.from_sprdl_info(p.get_info(0)), p[1]))],
            ['iszero', ('ISZERO term', lambda p: TmIsZero(Info.from_sprdl_info(p.get_info(0)), p[1]))],
            ['variable', ('IDENTIFIER', lambda p: TmNamedVar(Info.from_sprdl_info(p.get_info(0)), p[0]))],
            ['abstraction', ('LAMBDA IDENTIFIER COLON type DOT term', lambda p: TmAbs(Info.from_sprdl_info(p.get_info(0)), p[1], p[3], p[5]))],
            ['let', ('LET IDENTIFIER EQ term IN term', lambda p: TmLet(Info.from_sprdl_info(p.get_info(0)), p[1], p[3], p[5]))],
            ['letrec', ('LETREC IDENTIFIER COLON type EQ term IN term', lambda p: TmLetRec(Info.from_sprdl_info(p.get_info(0)), p[1], p[3], p[5], p[7]))],
            ['fix', ('FIX term', lambda p: TmFix(Info.from_sprdl_info(p.get_info(0)), p[1]))],
            ['type', ('base_type type_p', reduce_type)],
            ['type', ('LPAR type RPAR type_p', reduce_par_type)],
            ['base_type', ('IDENTIFIER', reduce_base_type)],
            ['type_p', 'ARROW type', '{}']
        ]

    def parse(self, input: str) -> NamedTerm:
        lexer = lex.Lexer(self.tokens)
        parser = parse.Parser(self.grammar, 'term')
        tokens = lexer.input(input)
        named_term = parser.parse(tokens)
        return named_term
