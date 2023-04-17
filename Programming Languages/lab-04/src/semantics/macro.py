#  Copyright (c) 2021-2021. Created by Mateusz Slazynski for the educational purposes.
#     Feel free to use/modify this code for any greater good.
#     It would be nice however if you mentioned me somewhere.
#     Still, no pressure - have a nice day!
from abc import ABC, abstractmethod
from copy import copy

from src.lambda_program import TypedLambdaProgram
from src.term import Term, TmVar, TmAbs, TmLet, TmApp, TmZero, TmFalse, TmTrue, TmIf, TmIsZero, TmSucc, TmPred, \
    TmLetRec, TmFix, Info, TmUnit, DerivedTerm, UnexpandedTerm


class Macro(ABC):
    '''
    Class representing a basic syntactic macro.

    Methods:
    ========
        expand(term: DerivedTerm) -> Term | None:
            takes a term and expands it, if it possible, returning new term
            if macro is not applicable, this method should return None
    '''
    @abstractmethod
    def expand(self, term: DerivedTerm) -> Term | None:
        pass


class LetRecMacro(Macro):

    def expand(self, term: DerivedTerm) -> Term | None:
        # TODO: this macro should work as the derived form (check the TPL book p. 144)
        #           letrec should be replaced with let + fix
        #       for other terms this method should return None
        match term:
            case TmLetRec(_, x, T1, t1, t2):
                return TmLet(Info.dummy_info(), x, TmFix(Info.dummy_info(), TmAbs(Info.dummy_info(), x, T1, t1)), t2)
            case _:
                return None


class MacroSystem:
    '''
    This class is responsible for expanding derived terms.
    It allows to define macros that transform the program into a more basic form.

    Methods:
    ========
        expand(p: TypedLambdaProgram[UnexpandedTerm]) -> TypedLambdaProgram[Term]:
            translates given program to a form without derived terms
    '''
    def __init__(self, macros: None | list[Macro] = None):
        self.macros : list[Macro] = macros if macros is not None else [LetRecMacro()]

    def _expand_macros(self, term: DerivedTerm) -> Term:
        # TODO: This method should go through all the macros in the self.macros list
        # and try to apply them to the given term.
        # If any macro succeeds it should return the result.
        # Otherwise the original term should be returned unchanged.
        for macro in self.macros:
            if macro.expand(term):
                return macro.expand(term)

        return term

    def _expand_term(self, t: UnexpandedTerm) -> Term:
        # TODO: This method should traverse the given term and try to expand its components.
        # It should match the argument:
        # 1) whether it is an instance of DerivedTerm (isinstance(t, DerivedTerm) is a correct test)
        #    if that's the case, it should try to expand it with _expand_macros
        #    don't forget to call the method recursively on the result
        # 2) in any other case it should just go deeper and call itself recursively
        #    function term_map_vars from term_utils shows how it can be done

        if isinstance(t, DerivedTerm):
            return self._expand_macros(t)
        else:
            return self._expand_term(t)

    def expand(self, p: TypedLambdaProgram[UnexpandedTerm]) -> TypedLambdaProgram[Term]:
        return TypedLambdaProgram(self._expand_term(p.term), p.name_context)
