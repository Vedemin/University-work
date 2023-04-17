from typing import Union
from local_search.algorithms.hill_climbing.hill_climbing import HillClimbing
from local_search.problems.base.state import State
from local_search.problems.base.problem import Problem


class WorstChoiceHillClimbing(HillClimbing):
    """
    Implementation of hill climbing local search.

    Pretty exotic version of hill climbing. Algorithm works, by checking all the available moves
    and selecting the worst one that improves the current state.
    """

    def _climb_the_hill(self, model: Problem, state: State) -> Union[State, None]:
        # TODO:
        # - go trough all the neighbors (_get_neighbours is your friend)
        # - find the worst improving state (with minimal model.improvement(....) > 0)
        # return it (or the current state if there is no improving state)!
        returnState = state
        neighbours = []

        for neighbour in self._get_neighbours(model, state):
            neighbours.append(neighbour)

        def sortFunc(ns: State):
            return model.improvement(ns, state)

        neighbours.sort(key=sortFunc)
        for neighbour in neighbours:
            if model.improvement(neighbour, state) > 0:
                return neighbour

        return state

