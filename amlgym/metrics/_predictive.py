r"""
Predictive power metrics assess a domain model ability of predicting actions
applicability and outcomes of executing an action in a state.
The *predicted applicability* evaluates the model ability of predicting whether 
and action is applicable in an environment state.
The *predicted effects* evaluates the model ability of predicting the state reached 
after executing an action in an environment state.
Predictive power metrics are defined with respect to a set of (test) states and a simulator, 
which is required to evaluate if an action is applicable and what is the state reached 
after executing the action in a given (simulated) environment state.
"""
import logging
import warnings
from collections import defaultdict
from contextlib import nullcontext

import unified_planning.model
from alive_progress import alive_bar
from typing import Dict, Sequence
import numpy as np
from unified_planning.shortcuts import SequentialSimulator

from amlgym.modeling.env import Env, StateType, ActionType

# Disable printing of planning engine credits to avoid overloading stdout
unified_planning.shortcuts.get_environment().credits_stream = None


def applicability(simulator: Env | Sequence[Env],
                  simulator_ref: Env | Sequence[Env],
                  test_states: Sequence[StateType] | Sequence[Sequence[StateType]],
                  applicable_actions: Sequence[ActionType] = None,
                  show_progress: bool = True) -> Dict[str, Dict[str, float]]:
    r"""
    Evaluate the predicted applicability metric given the simulator of a domain model :math:`M` and an
    environment simulator :math:`E`. The model :math:`M` and environment simulators share the set :math:`S`
    of states and the set :math:`A` of actions.
    For an action :math:`a\in A`, and state :math:`s\in S`,
    we denote by :math:`app_M(a,S_{test})` and :math:`app(a,S_{test})` the set of states in :math:`S_{test}`
    in which :math:`a` is applicable according to :math:`M` and :math:`E`, respectively.
    We define the predicted applicability metric for every action :math:`a\in A` as:

    * True Positives: :math:`TP_{app}(a)=|app_M(a,S_{test})\cap app(a,S_{test})|`
    * False Positives: :math:`FP_{app}(a)=|app_M(a,S_{test})\setminus app(a,S_{test})|`
    * False Negatives: :math:`FN_{app}(a)=|app(a,S_{test}) \setminus app_M(a,S_{test})|`

    The predicted applicability precision and recall per action are obtained as:

    * Predicted applicability precision of :math:`a`: :math:`P_{app}(a) = \frac{TP_{app}(a)}{TP_{app}(a)+FP_{app}(a)}`
    * Predicted applicability recall of :math:`a`: :math:`R_{app}(a) = \frac{TP_{app}(a)}{TP_{app}(a)+FN_{app}(a)}`

    When :math:`TP_{app}(a) = FP_{app}(a) = 0`, we define :math:`P_{app}(a)=1` and :math:`R_{app}(a)=0`, as the
    domain model :math:`M` never allows :math:`a` to be applied in :math:`S_{test}`.
    Finally, the mean precision and recall of a domain model averages over the actions precision and recall:

    * **Predicted applicability precision** of :math:`M`: :math:`P = \frac{1}{|A|}\sum_{a\in A} P(a)`

    * **Predicted applicability recall** of :math:`M`: :math:`R = \frac{1}{|A|}\sum_{a\in A} R(a)`

    :param simulator: simulator of a domain model :math:`M` to be evaluated.
    :param simulator_env: environment simulator :math:`E` to compare with.
    :param test_states: set :math:`S_{test}` of test states.
    :param applicable_actions: optionally precomputed set of applicable actions for every test state.
    :param show_progress: show a progress bar.

    :return: the predicted applicability precision and recall averaged over all test states and actions.
    """

    if isinstance(simulator, Sequence):
        assert isinstance(simulator_ref, Sequence), ('The applicability evaluation for a sequence of '
                                                     'learned simulators requires a corresponding sequence '
                                                     'of reference simulators: a reference simulator to compare with '
                                                     'for each learned simulator.')
        assert len(simulator_ref) == len(simulator), ("The number of learned and reference simulators "
                                                              "must be equal. Current number of learned simulators "
                                                              f"is {len(simulator)} and reference simulators "
                                                              f"is {len(simulator_ref)}.")
        assert len(simulator_ref) == len(test_states), ("A sequence of states to be evaluated must be provided "
                                                        "for every pair (learned, reference) simulator. "
                                                        f"The current sequence of states has size {len(test_states)}, "
                                                        f"while the number of (learned, reference) simulator "
                                                        f"pairs is {len(simulator_ref)}.")
        simulator_ref_list = simulator_ref
        simulator_learned_list = simulator
        test_states_list = test_states
    else:
        simulator_ref_list = [simulator_ref]
        simulator_learned_list = [simulator]
        test_states_list = [test_states]

    tp = defaultdict(int)
    fp = defaultdict(int)
    fn = defaultdict(int)
    precision = defaultdict(float)
    recall = defaultdict(float)

    bar = alive_bar(len(test_states_list),
                    title=f'Evaluating actions applicability...',
                    length=20) if show_progress else nullcontext()
    with bar as bar:
        for k, (simulator, simulator_ref, states) in enumerate(zip(simulator_learned_list,
                                                                   simulator_ref_list,
                                                                   test_states_list)):
            applicable_in_states = None

            if applicable_actions is not None and k < len(applicable_actions):
                # applicable_actions is a possibly precomputed list of applicable
                # actions for every k-th state in the test set
                applicable_in_states = applicable_actions[k]

            for j, s in enumerate(states):

                s = set(s)  # TODO: use sets in yaml rather than JSON

                # parse the possibly precomputed list of applicable action for the k-th state
                if applicable_in_states is not None:
                    applicable_ref = applicable_in_states[j]
                else:
                    # if no precomputed list of applicable actions is given, compute them
                    applicable_ref = simulator_ref.applicable_actions(s)

                applicable_learned = simulator.applicable_actions(s)

                operators = set(list(applicable_learned.keys()) + list(applicable_ref.keys()))

                for op in operators:
                    tp[op] += len(applicable_ref[op] & applicable_learned[op])
                    fp[op] += len(applicable_learned[op] - applicable_ref[op])
                    fn[op] += len(applicable_ref[op] - applicable_learned[op])

            if show_progress:
                bar()

    operators = set(tp.keys()) | set(fp.keys()) | set(fn.keys())
    for op in operators:

        if (tp[op] + fp[op]) == 0:
            warnings.warn(f"No true and false positives for operator {op}, "
                          f"predicted applicability precision set to 1.", stacklevel=2)
            precision[op] = 1.
        else:
            precision[op] = tp[op] / (tp[op] + fp[op])

        if (tp[op] + fn[op]) == 0:
            warnings.warn(f"No true positives and false negatives for operator {op}, "
                          f"predicted applicability recall set to 1.", stacklevel=2)
            recall[op] = 1.
        else:
            recall[op] = tp[op] / (tp[op] + fn[op])

    return {
        'mean_precision': np.mean(list(precision.values())),
        'mean_recall': np.mean(list(recall.values())),
    }


def predicted_effects(simulator: Env | Sequence[Env],
                      simulator_env: Env | Sequence[Env],
                      test_states: Sequence[StateType] | Sequence[Sequence[StateType]],
                      applicable_actions: Sequence[ActionType] = None,
                      show_progress: bool = True) -> Dict[str, Dict[str, float]]:
    r"""
    Evaluate the predicted effects metric given the simulator of a domain model :math:`M` and an
    environment simulator :math:`E`. The model :math:`M` and environment simulators share the set :math:`S`
    of states and the set :math:`A` of actions; the evaluation considers actions applicable in a
    state for both :math:`M` and :math:`E`.
    For an action :math:`a\in A`, and state :math:`s\in S`,
    we denote by :math:`a_{M}(s)` and :math:`a(s)` the state resulting from applying :math:`a` in :math:`s`
    according to :math:`M` and :math:`E`, respectively.
    We define the predicted effect metrics for every state :math:`s \in S_{test}`
    and action :math:`a\in A` as:

    * True Positives: :math:`TP_{eff}(s,a)=|(a_M(s)\setminus s)\cap (a(s)\setminus s)|`
    * False Positives: :math:`FP_{eff}(s,a)=|(a_M(s)\setminus s)\setminus a(s)|`
    * False Negatives: :math:`FN_{eff}(s,a)=|(a_M(s)\cap s)\setminus a(s)|`

    The predicted effects mean precision and recall per action are obtained by averaging over all
    states in :math:`S_{test}`, i.e.:

    * True Positives: :math:`TP_{eff}(a)=\sum\limits_{s\in S_{test}}TP_{eff}(s,a)`
    * False Positives: :math:`FP_{eff}(a)=\sum\limits_{s\in S_{test}}TP_{eff}(s,a)`
    * False Negatives: :math:`FN_{eff}(a)=\sum\limits_{s\in S_{test}}FN_{eff}(s,a)`

    * Predicted effects precision of :math:`a` : :math:`P_{eff}(a) = \frac{TP_{eff}(a)}{TP_{eff}(a)+FP_{eff}(a)}`
    * Predicted effects recall of :math:`a` : :math:`R_{eff}(a) = \frac{TP_{eff}(a)}{TP_{eff}(a)+FN_{eff}(a)}`

    When :math:`TP_{eff}(a) = FP_{eff}(a) = 0`, we define :math:`P_{eff}(a)=1` and :math:`R_{eff}(a)=0`.
    Finally, the mean precision and recall of a domain model averages over the actions precision and recall:

    * **Predicted effects precision** of :math:`M`: :math:`P = \frac{1}{|A|}\sum_{a\in A} P(a)`
    * **Predicted effects recall** of :math:`M`: :math:`R = \frac{1}{|A|}\sum_{a\in A} R(a)`

    :param simulator: simulator of a domain model :math:`M` to be evaluated.
    :param simulator_env: environment simulator :math:`E` to compare with.
    :param test_states: set :math:`S_{test}` of test states.
    :param applicable_actions: optionally precomputed set of applicable actions for every test state.
    :param show_progress: show a progress bar.

    :return: the predicted effects mean precision and recall
    """

    if isinstance(simulator, Sequence):
        assert isinstance(simulator_env, Sequence), ('The applicability evaluation for a sequence of '
                                                     'learned simulators requires a corresponding sequence '
                                                     'of reference simulators: a reference simulator to compare with '
                                                     'for each learned simulator.')
        assert len(simulator_env) == len(simulator), ("The number of learned and reference simulators "
                                                              "must be equal. Current number of learned simulators "
                                                              f"is {len(simulator)} and reference simulators "
                                                              f"is {len(simulator_env)}.")
        assert len(simulator_env) == len(test_states), ("A sequence of states to be evaluated must be provided "
                                                        "for every pair (learned, reference) simulator. "
                                                        f"The current sequence of states has size {len(test_states)}, "
                                                        f"while the number of (learned, reference) simulator "
                                                        f"pairs is {len(simulator_env)}.")
        simulator_ref_list = simulator_env
        simulator_learned_list = simulator
        test_states_list = test_states
    else:
        simulator_ref_list = [simulator_env]
        simulator_learned_list = [simulator]
        test_states_list = [test_states]

    tp = defaultdict(int)
    fp = defaultdict(int)
    fn = defaultdict(int)
    precision = defaultdict(float)
    recall = defaultdict(float)

    bar = alive_bar(len(test_states_list),
                    title=f'Evaluating actions applicability...',
                    length=20) if show_progress else nullcontext()
    with bar as bar:
        for k, (simulator, simulator_env, states) in enumerate(zip(simulator_learned_list,
                                                                   simulator_ref_list,
                                                                   test_states_list)):
            applicable_in_states = None

            if applicable_actions is not None and k < len(applicable_actions):
                # applicable_actions is a possibly precomputed list of applicable
                # actions for every k-th state in the test set
                applicable_in_states = applicable_actions[k]

            for j, s in enumerate(states):

                s = set(s)  # TODO: use sets in yaml rather than JSON

                # parse the possibly precomputed list of applicable action for the k-th state
                if applicable_in_states is not None:
                    applicable_ref = applicable_in_states[j]
                else:
                    # if no precomputed list of applicable actions is given, compute them
                    applicable_ref = simulator_env.applicable_actions(s)

                applicable_learned = simulator.applicable_actions(s)

                operators = set(list(applicable_learned.keys()) + list(applicable_ref.keys()))

                # NOTE: consider only actions that are applicable in a given state
                # according to both the evaluated and reference simulators
                for op in operators:
                    for action_label in applicable_ref[op] & applicable_learned[op]:

                        snext_learned = simulator.apply(s, action_label)
                        snext_ref = simulator_env.apply(s, action_label)

                        tp[op] += len((snext_learned - s) .intersection((snext_ref - s)))
                        fp[op] += len((snext_learned - s) - snext_ref)
                        fn[op] += len((snext_learned.intersection(s)) - snext_ref)

            if show_progress:
                bar()

    operators = set(tp.keys()) | set(fp.keys()) | set(fn.keys())
    for op in operators:

        if (tp[op] + fp[op]) == 0:
            warnings.warn(f"No true and false positives for operator {op}, "
                          f"predicted effects precision set to 1.", stacklevel=2)
            precision[op] = 1.
        else:
            precision[op] = tp[op] / (tp[op] + fp[op])


        if (tp[op] + fn[op]) == 0:
            warnings.warn(f"No true positives and false negatives for operator {op}, "
                          f"predicted effects recall set to 1.", stacklevel=2)
            recall[op] = 1.
        else:
            recall[op] = tp[op] / (tp[op] + fn[op])

    return {
        'mean_precision': np.mean(list(precision.values())),
        'mean_recall': np.mean(list(recall.values())),
    }


def predictive_power(simulator_learned: Env | Sequence[Env],
                     simulator_ref: Env | Sequence[Env],
                     test_states: Sequence[StateType] | Sequence[Sequence[StateType]],
                     applicable_actions: Sequence[ActionType] = None,
                     show_progress: bool = True) -> Dict[str, Dict[str, Dict[str, float]]]:
    """
    Evaluate both the predicted applicability and predicted effects metrics of a simulated
    domain model :math:`M` with respect to an environment simulator :math:`E` against a test
    set of states :math:`S_{test}`.
    The results can be reproduced by separately executing functions
    :func:`~amlgym.metrics._predictive.predicted_effects` and
    :func:`~amlgym.metrics._predictive.applicability`;
    this function performs a joint and more efficient evaluation of both metrics.

    :param simulator: simulator of a domain model :math:`M` to be evaluated.
    :param simulator_env: environment simulator :math:`E` to compare with.
    :param test_states: set :math:`S_{test}` of test states.
    :param applicable_actions: optionally precomputed set of applicable actions for every test state.
    :param show_progress: show a progress bar.

    :return: the mean precision and recall for both predicted effects and predicted applicability
    """
    
    if isinstance(simulator_learned, Sequence):
        assert isinstance(simulator_ref, Sequence), ('The applicability evaluation for a sequence of '
                                                     'learned simulators requires a corresponding sequence '
                                                     'of reference simulators: a reference simulator to compare with '
                                                     'for each learned simulator.')
        assert len(simulator_ref) == len(simulator_learned), ("The number of learned and reference simulators "
                                                              "must be equal. Current number of learned simulators "
                                                              f"is {len(simulator_learned)} and reference simulators "
                                                              f"is {len(simulator_ref)}.")
        assert len(simulator_ref) == len(test_states), ("A sequence of states to be evaluated must be provided "
                                                        "for every pair (learned, reference) simulator. "
                                                        f"The current sequence of states has size {len(test_states)}, "
                                                        f"while the number of (learned, reference) simulator "
                                                        f"pairs is {len(simulator_ref)}.")
        simulator_ref_list = simulator_ref
        simulator_learned_list = simulator_learned
        test_states_list = test_states
    else:
        simulator_ref_list = [simulator_ref]
        simulator_learned_list = [simulator_learned]
        test_states_list = [test_states]

    predeffs_tp = defaultdict(int)
    predeffs_fp = defaultdict(int)
    predeffs_fn = defaultdict(int)
    predeffs_precision = defaultdict(float)
    predeffs_recall = defaultdict(float)

    app_tp = defaultdict(int)
    app_fp = defaultdict(int)
    app_fn = defaultdict(int)
    app_precision = defaultdict(float)
    app_recall = defaultdict(float)

    bar = alive_bar(len(test_states_list),
                    title=f'Evaluating predictive power...',
                    length=20) if show_progress else nullcontext()
    with bar as bar:
        for k, (simulator_learned, simulator_ref, states) in enumerate(zip(simulator_learned_list,
                                                                           simulator_ref_list,
                                                                           test_states_list)):
            applicable_in_states = None

            if applicable_actions is not None and k < len(applicable_actions):
                # applicable_actions is a possibly precomputed list of applicable
                # actions for every k-th states list in the test set
                applicable_in_states = applicable_actions[k]

            for j, s in enumerate(states):

                s = set(s)  # TODO: use sets in yaml rather than JSON

                # parse the possibly precomputed list of applicable action for the j-th state
                # in the k-th states list
                if applicable_in_states is not None:
                    applicable_ref = applicable_in_states[j]
                else:
                    # if no precomputed list of applicable actions is given, compute them
                    applicable_ref = simulator_ref.applicable_actions(s)

                applicable_learned = simulator_learned.applicable_actions(s)

                operators = set(list(applicable_learned.keys()) + list(applicable_ref.keys()))

                # Evaluate action applicability and predicted effects
                for op in operators:

                    # Predicted effects
                    for action_label in applicable_ref[op] & applicable_learned[op]:

                        snext_learned = simulator_learned.apply(s, action_label)
                        snext_ref = simulator_ref.apply(s, action_label)

                        predeffs_tp[op] += len((snext_learned - s) & (snext_ref - s))
                        predeffs_fp[op] += len((snext_learned - s) - snext_ref)
                        predeffs_fn[op] += len((snext_learned & s) - snext_ref)
                        pass

                    # Action applicability
                    app_tp[op] += len(applicable_ref[op] & applicable_learned[op])
                    app_fp[op] += len(applicable_learned[op] - applicable_ref[op])
                    app_fn[op] += len(applicable_ref[op] - applicable_learned[op])

            if show_progress:
                bar()

    operators = set(predeffs_tp.keys()) | set(predeffs_fp.keys()) | set(predeffs_fn.keys())
    for op in operators:

        if (app_tp[op] + app_fp[op]) == 0:
            warnings.warn(f"No true and false positives for operator {op}, "
                          f"predicted applicability precision set to 1.", stacklevel=2)
            app_precision[op] = 1.
        else:
            app_precision[op] = app_tp[op] / (app_tp[op] + app_fp[op])

        if (app_tp[op] + app_fn[op]) == 0:
            warnings.warn(f"No true positives and false negatives for operator {op}, "
                          f"predicted applicability recall set to 1.", stacklevel=2)
            app_recall[op] = 1.
        else:
            app_recall[op] = app_tp[op] / (app_tp[op] + app_fn[op])

        if (predeffs_tp[op] + predeffs_fp[op]) == 0:
            warnings.warn(f"No true and false positives for operator {op}, "
                          f"predicted effects precision set to 1.", stacklevel=2)
            predeffs_precision[op] = 1.
        else:
            predeffs_precision[op] = predeffs_tp[op] / (predeffs_tp[op] + predeffs_fp[op])


        if (predeffs_tp[op] + predeffs_fn[op]) == 0:
            warnings.warn(f"No true positives and false negatives for operator {op}, "
                          f"predicted effects recall set to 1.", stacklevel=2)
            predeffs_recall[op] = 1.
        else:
            predeffs_recall[op] = predeffs_tp[op] / (predeffs_tp[op] + predeffs_fn[op])

    return {
        'applicability': {
            'mean_precision': np.mean(list(app_precision.values())),
            'mean_recall': np.mean(list(app_recall.values())),
        },
        'predicted_effects': {
            'mean_precision': np.mean(list(predeffs_precision.values())),
            'mean_recall': np.mean(list(predeffs_recall.values())),
        }
    }
