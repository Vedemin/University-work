#  Copyright (c) 2021. Created by Mateusz Slazynski for the educational purposes.
#     Feel free to use/modify this code for any greater good.
#     It would be nice however if you mentioned me somewhere.
#     Still, no pressure - have a nice day!

from __future__ import annotations
from src.term import Term, TmAbs, TmVar, TmApp
from src.lambda_program import LambdaProgram
from dataclasses import dataclass
from enum import Enum, auto

class Rule(Enum):
    App1 = 0
    App2 = auto()
    AppAbs = auto()

    def __repr__(self):
        return f"Rule.{self.name}"

@dataclass(frozen=True)
class Transition:
    old_state: LambdaProgram
    new_state: LambdaProgram
    rule: Rule
    witnesses: tuple[Transition] = ()

class NoRuleApplies(Exception):
    pass

class LambdaSemantics:
    '''
        Class representing semantics of the untyped lambda calculus.

        Attributes:
            - free_names: list[str]
                This list stores names of the free variables in order to print them in a pretty way :)
    '''
    def __init__(self, free_names: list[str]):
        self.free_names = free_names

    @staticmethod
    def is_term_val(t: Term) -> bool:
        '''
             This static method checks whether the term is a value.
             Based on the 'isval' function from the TAPL p. 87

             :param t: a Lambda Calculus term
             :return: whether the term is a value
        '''
        # TODO:
        # term is a value only when it is an abstraction (TmAbs)
        match t: # if isn't working here... why?
            case TmAbs(_, _, _):
                return True
            case _:
                return False

    def single_step(self, state_before: Term) -> Transition:
        '''
             This static method checks whether the term is a value.
             Based on the 'eval1' function from the TAPL p. 87

             :param state_before: a Lambda Calculus term
             :return: a transition applied according the Lambda Calculus semantics
        '''

        def transition(new_state: Term, rule: Rule, witnesses: tuple(Transition) = ()) -> Transition:
            ''' Just a helper function to quickly create a transition'''
            return Transition(LambdaProgram(state_before, self.free_names), LambdaProgram(new_state, self.free_names), rule, witnesses)

        # TODO:
        # fill missing cases:
        # - Rule.AppAbs:
        #   * use LambdaSemantics._term_substitute
        # - Rule.App1
        # - Rule.App2

        match state_before:
            # TODO: missing cases...
            case TmApp(_, TmAbs(_, x, t), arg) if LambdaSemantics.is_term_val(arg):
                return transition(LambdaSemantics._term_substitute(arg, t), Rule.AppAbs)
            case TmApp(fi, t1, t2) if LambdaSemantics.is_term_val(t1):
                t2p = self.single_step(t2)
                return transition(TmApp(fi, t1, t2p.new_state), Rule.App1, (t2p,))
            case TmApp(fi, t1, t2):
                t1_ = self.single_step(t1)
                return transition(TmApp(fi, t1_, t2), Rule.App2, (t1_,))
            case _:
                raise NoRuleApplies()

    @staticmethod
    def _term_substitute(s: Term, t: Term) -> Term:
        '''
             This static makes a substitution in t. [0->s]t
             Based on the 'termSubstTop' function from the TAPL p. 87

             :param s: term that should replace the variable
             :param t: term containing variables to be replaced
             :return: new term create according to the substitution rules
        '''
        # TODO:
        # 1) use _term_shift to shift the variables in s by 1
        # 2) use _term_substitute_step to replace all occurences of 0 in t with result of the step 1)
        # 3) use _term_shift to shift the variables in result of the step 2) by -1
        # return result of the step 3)
        s_shft = LambdaSemantics._term_shift(1, s)
        t_sub = LambdaSemantics._term_substitute_step(0, s_shft, t)
        return LambdaSemantics._term_shift(-1, t_sub)

    @staticmethod
    def _term_shift(d: int, term: Term) -> Term:
        '''
             This static method shifts free variable indexes in the term.
             Based on the 'termShift' function from the TAPL p. 86

             :param d: how much the variables should be shifted
             :param term: Lambda Calculus term containing variables to be shifted
             :return: new term with shifted variables
        '''

        # TODO:
        # - define recursive walk function
        #   walk traverses the abstract syntax tree (term) and looks for variables
        #   it has to track the context (how deep we are / how many "abstractions" (TmAbs) is above
        #   a free variable will have index >= the current depth
        #   and such variables need to be shifted by 'd'
        #   tip. all the variables have to be updated when it comes to their context_length (also by 'd')
        # - call 'walk' with initial depth = 0
        def walk(t, depth):
            match t:
                case TmVar(fi, x, cl):
                    if x >= depth:
                        return TmVar(fi, x + d, cl + d)
                    else:
                        return TmVar(fi, x, cl + d)
                case TmAbs(fi, x, t):
                    return TmAbs(fi, x, walk(t, depth + 1))
                case TmApp(fi, t1, t2):
                    return TmApp(fi, walk(t1, depth), walk(t2, depth))

        return walk(term, 0)

    @staticmethod
    def _term_substitute_step(j: int, s: Term, term: TmAbs) -> Term:
        '''
             This static method substitutes variable with given index
             with a given term.
             Based on the 'termSubst' function from the TAPL p. 86

             :param j: index of the variable to be substituted
             :param s: term to be put at the variable place
             :param term: term containing variables to be substituted
             :return: new term with substituted variables
        '''

        # TODO:
        # - define recursive walk function
        #   walk traverses the abstract syntax tree (term) and looks for variables
        #   it has to track the context (how deep we are / how many "abstractions" (TmAbs) is above use
        #   a variable has to be substituted if its index equals sum of depth and j
        #   the new term is the 's' term shifted (_term_shift) by the current depth
        # - call 'walk' with initial depth = 0
        def walk(t, depth):
            match t:
                case TmVar(fi, x, cl):
                    if x == depth + j:
                        return LambdaSemantics._term_shift(depth, s)
                    else:
                        return TmVar(fi, x, cl)
                case TmAbs(fi, x, t1):
                    return TmAbs(fi, x, walk(t1, depth + 1))
                case TmApp(fi, t1, t2):
                    return TmApp(fi, walk(t1, depth), walk(t2, depth))

        return walk(term, 0)
