# Add current project to sys path
import contextlib
import json
import logging
import os
import sys

import pandas as pd
from unified_planning.engines import ValidationResultStatus, PlanGenerationResultStatus

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

import copy
import warnings

from alive_progress import alive_bar

from amlgym.util.SimpleDomainReader import SimpleDomainReader
import numpy as np
import os
import re
import shutil
from typing import List, Dict, Set

import unified_planning.model
from tarski.grounding import LPGroundingStrategy
from unified_planning.io import PDDLReader, PDDLWriter
from tarski.io import PDDLReader as tarskiPDDLReader
from unified_planning.plans import ActionInstance
from unified_planning.shortcuts import SequentialSimulator, PlanValidator, OneshotPlanner

# Disable printing of planning engine credits to avoid overloading stdout
unified_planning.shortcuts.get_environment().credits_stream = None


def syntactic_eval(model_learned, model_reference):

    eval_model = SimpleDomainReader(input_file=model_learned)
    model_reference = SimpleDomainReader(input_file=model_reference)

    for op_gt, op_eval in zip(model_reference.operators, eval_model.operators):
        op_gt.operator_name = op_gt.operator_name.replace('_', '-')
        op_eval.operator_name = op_eval.operator_name.replace('_', '-')

    # Sort operators list
    model_reference.operators = sorted(model_reference.operators, key=lambda x: x.operator_name, reverse=True)
    eval_operatos_name = [op.operator_name for op in eval_model.operators]
    sorted_eval_operators = []
    for op in model_reference.operators:
        if op.operator_name in eval_operatos_name:
            operator = next((o for o in eval_model.operators if o.operator_name == op.operator_name), None)
            sorted_eval_operators.append(operator)
        else:
            new_operator = copy.deepcopy(op)
            new_operator.precs_pos = []
            new_operator.precs_neg = []
            new_operator.eff_pos = []
            new_operator.eff_neg = []
            sorted_eval_operators.append(new_operator)
    eval_model.operators = sorted_eval_operators

    assert bool(np.all([gt_op.operator_name == learned_op.operator_name for gt_op, learned_op in
                        zip(model_reference.operators, eval_model.operators)]))

    all_pre_pos_precision = []
    all_pre_neg_precision = []
    all_eff_pos_precision = []
    all_eff_neg_precision = []
    all_pre_pos_recall = []
    all_pre_neg_recall = []
    all_eff_pos_recall = []
    all_eff_neg_recall = []
    overall_recall = []
    overall_precision = []

    for gt_op, learned_op in zip(model_reference.operators, eval_model.operators):
        fn_pre_pos = len(set([p for p in gt_op.precs_pos if p not in learned_op.precs_pos]))
        fp_pre_pos = len(set([p for p in learned_op.precs_pos if p not in gt_op.precs_pos]))
        tp_pre_pos = len(set([p for p in learned_op.precs_pos if p in gt_op.precs_pos]))

        fn_pre_neg = len(set([p for p in gt_op.precs_neg if p not in learned_op.precs_neg]))
        fp_pre_neg = len(set([p for p in learned_op.precs_neg if p not in gt_op.precs_neg]))
        tp_pre_neg = len(set([p for p in learned_op.precs_neg if p in gt_op.precs_neg]))

        fn_eff_pos = len(set([p for p in gt_op.eff_pos if p not in learned_op.eff_pos]))
        fp_eff_pos = len(set([p for p in learned_op.eff_pos if p not in gt_op.eff_pos]))
        tp_eff_pos = len(set([p for p in learned_op.eff_pos if p in gt_op.eff_pos]))

        fn_eff_neg = len(set([p for p in gt_op.eff_neg if p not in learned_op.eff_neg]))
        fp_eff_neg = len(set([p for p in learned_op.eff_neg if p not in gt_op.eff_neg]))
        tp_eff_neg = len(set([p for p in learned_op.eff_neg if p in gt_op.eff_neg]))

        all_tp = tp_pre_pos + tp_eff_pos + tp_eff_neg + tp_pre_neg
        all_fp = fp_pre_pos + fp_pre_neg + fp_eff_pos + fp_eff_neg
        all_fn = fn_pre_pos + fn_pre_neg + fn_eff_pos + fn_eff_neg

        pre_pos_recall = pre_pos_precision = None
        pre_neg_recall = pre_neg_precision = None
        eff_pos_recall = eff_pos_precision = None
        eff_neg_recall = eff_neg_precision = None

        if tp_pre_pos + fp_pre_pos > 0:
            pre_pos_precision = tp_pre_pos / (tp_pre_pos + fp_pre_pos)
        else:
            warnings.warn('No positive precondition has been learned '
                          f'for operator {gt_op.operator_name} of domain'
                          f' {model_reference.input_file}. '
                          f'Precision of positive preconditions for '
                          f'{gt_op.operator_name} evaluated as 1.')
            pre_pos_precision = 1.

        if tp_pre_neg + fp_pre_neg > 0:
            pre_neg_precision = tp_pre_neg / (tp_pre_neg + fp_pre_neg)
        else:
            warnings.warn('No negative precondition has been learned '
                          f'for operator {gt_op.operator_name} of domain'
                          f' {model_reference.input_file}.'
                          f' Precision of negative preconditions for '
                          f'{gt_op.operator_name} evaluated as 1.')
            pre_neg_precision = 1.

        if tp_eff_pos + fp_eff_pos > 0:
            eff_pos_precision = tp_eff_pos / (tp_eff_pos + fp_eff_pos)
        else:
            warnings.warn('No positive effect has been learned '
                          f'for operator {gt_op.operator_name} of domain'
                          f' {model_reference.input_file}. '
                          f'Precision of positive effects for '
                          f'{gt_op.operator_name} evaluated as 1.')
            eff_pos_precision = 1.

        if tp_eff_neg + fp_eff_neg > 0:
            eff_neg_precision = tp_eff_neg / (tp_eff_neg + fp_eff_neg)
        else:
            warnings.warn('No negative effect has been learned '
                          f'for operator {gt_op.operator_name} of domain'
                          f' {model_reference.input_file}. '
                          f'Precision of negative effects for '
                          f'{gt_op.operator_name} evaluated as 1.')
            eff_neg_precision = 1.

        if tp_pre_pos + fn_pre_pos > 0:
            pre_pos_recall = tp_pre_pos / (tp_pre_pos + fn_pre_pos)
        else:
            assert len(gt_op.precs_pos) == 0
            warnings.warn('No positive precondition exists '
                          f'for operator {gt_op.operator_name} of domain'
                          f' {model_reference.input_file}. '
                          f'Recall of positive preconditions for '
                          f'{gt_op.operator_name} evaluated as 1.')
            pre_pos_recall = 1.

        if tp_pre_neg + fn_pre_neg > 0:
            pre_neg_recall = tp_pre_neg / (tp_pre_neg + fn_pre_neg)
        else:
            assert len(gt_op.precs_neg) == 0
            warnings.warn('No negative precondition exists '
                          f'for operator {gt_op.operator_name} of domain'
                          f' {model_reference.input_file}. '
                          f'Recall of negative preconditions for '
                          f'{gt_op.operator_name} evaluated as 1.')
            pre_neg_recall = 1.

        if tp_eff_pos + fn_eff_pos > 0:
            eff_pos_recall = tp_eff_pos / (tp_eff_pos + fn_eff_pos)
        else:
            assert len(gt_op.eff_pos) == 0
            warnings.warn('No positive effect exists '
                          f'for operator {gt_op.operator_name} of domain'
                          f' {model_reference.input_file}. '
                          f'Recall of positive effects for '
                          f'{gt_op.operator_name} evaluated as 1.')
            eff_pos_recall = 1.

        if tp_eff_neg + fn_eff_neg > 0:
            eff_neg_recall = tp_eff_neg / (tp_eff_neg + fn_eff_neg)
        else:
            assert len(gt_op.eff_neg) == 0
            warnings.warn('No negative effect exists '
                          f'for operator {gt_op.operator_name} of domain'
                          f' {model_reference.input_file}. '
                          f'Recall of negative effects for '
                          f'{gt_op.operator_name} evaluated as 1.')
            eff_neg_recall = 1.

        if all_tp + all_fp > 0:
            overall_precision.append(all_tp / (all_tp + all_fp))
        else:
            warnings.warn('No positive predictions in terms of pos/neg precs/effs '
                          f'for operator {gt_op.operator_name} of domain'
                          f' {model_reference.input_file}. '
                          f'Overall precision '
                          f'{gt_op.operator_name} evaluated as 1.')
            overall_precision.append(1.0)

        if all_tp + all_fn > 0:
            overall_recall.append(all_tp / (all_tp + all_fn))
        else:
            warnings.warn('No negative predictions in terms of pos/neg precs/effs '
                          f'for operator {gt_op.operator_name} of domain'
                          f' {model_reference.input_file}. '
                          f'Overall precision '
                          f'{gt_op.operator_name} evaluated as 1.')
            overall_recall.append(1.0)

        all_pre_pos_precision.append(pre_pos_precision)
        all_pre_neg_precision.append(pre_neg_precision)
        all_eff_pos_precision.append(eff_pos_precision)
        all_eff_neg_precision.append(eff_neg_precision)
        all_pre_pos_recall.append(pre_pos_recall)
        all_pre_neg_recall.append(pre_neg_recall)
        all_eff_pos_recall.append(eff_pos_recall)
        all_eff_neg_recall.append(eff_neg_recall)

    return {'syntactic':
                {
                    'precs_pos_recall': "{0:.2f}".format(np.mean(all_pre_pos_recall)),
                    'precs_neg_recall': "{0:.2f}".format(np.mean(all_pre_neg_recall)),
                    'pos_recall': "{0:.2f}".format(np.mean(all_eff_pos_recall)),
                    'neg_recall': "{0:.2f}".format(np.mean(all_eff_neg_recall)),
                    'precs_pos_precision': "{0:.2f}".format(np.mean(all_pre_pos_precision)),
                    'precs_neg_precision': "{0:.2f}".format(np.mean(all_pre_neg_precision)),
                    'pos_precision': "{0:.2f}".format(np.mean(all_eff_pos_precision)),
                    'neg_precision': "{0:.2f}".format(np.mean(all_eff_neg_precision)),
                    'overall_recall': "{0:.2f}".format(np.mean(overall_recall)),
                    'overall_precision': "{0:.2f}".format(np.mean(overall_precision))
                }
    }


# TODO: currently keep it as it is for efficiency
def predictive_eval(model_learned_path: str,
                    model_ref_path: str,
                    traj_problem_paths: Dict[str, str]) -> Dict[str, Dict[str, float] | float]:
    """
    Compute the action applicability (precision and recall) of a learned model w.r.t. a
     reference model by considering all states in the input trajectories

    :param model_learned_path: file path to learned pddl model
    :param model_ref_path: file path to reference pddl model
    :param traj_problem_paths: a dictionary where each key is a path to a pddl trajectory
        and the value a path to the associated pddl problem. This is required as input since
        the trajectory does not explicitly report the set of problem objects, which is
        required to evaluate action applicability by simulating actions.

    :return: action applicability precision and recall grouped by operator
    """

    # Inner helper function for computing all applicable actions in a state
    def get_applicable_actions(simulator: SequentialSimulator,
                               state: unified_planning.model.State,
                               problem,
                               # for efficiency pass the ground actions
                               ground_actions: Dict[str, any]) -> Dict[str, Set[str]]:
        applicable_actions = {op_name:
                                  {objs for objs in all_objs
                                   if simulator._is_applicable(state,
                                                               problem.action(op_name),
                                                               [problem.object(o.lower()) for o in objs])}
                              for op_name, all_objs in ground_actions.items()
                              }
        return applicable_actions

    # Get the reference domain operators
    reader = PDDLReader()
    upl_domain = PDDLReader().parse_problem(model_ref_path)
    operators = {
        a.name: {
            'applicability': {
                'tp': 0,  # true positives
                'fp': 0,  # false positives
                'fn': 0,  # false negatives
                'precision': 0.,
                'recall': 0.,
            },
            'consequentiality': {
                'tp': 0,  # true positives
                'fp': 0,  # false positives
                'fn': 0,  # false negatives
                'precision': 0.,
                'recall': 0.,
            }
        }
        for a in upl_domain.actions}

    # Iterate over each trajectory
    with alive_bar(len(traj_problem_paths),
                   title=f'Evaluating applicability for domain {model_learned_path}',
                   length=20,
                   bar='smooth') as bar:

        for i, t in enumerate(sorted(traj_problem_paths.keys(),
                                     key=lambda x: int(x.split('/')[-1].split('_')[0]))):

            # Read trajectory data
            with open(t, 'r') as f:
                traj_data = f.readlines()
                states = [s for s in traj_data if s.startswith("(:state ")]
                actions = [s for s in traj_data if s.startswith("(:action ")]
                plan_str = '\n'.join([a.replace('(:action ', '').strip()[:-1] for a in actions])

            # Update problem initial state with the initial state of the trajectory. Notice they may be different
            # when the trajectory is obtained by sampling a subtrajectory from the originally generated one.
            problem_file = traj_problem_paths[t]
            shutil.copy(problem_file, 'tmp.pddl')
            with open('tmp.pddl', 'r') as f:
                problem_str = f.read()
            new_atoms = re.findall(r"\([^()]*\)", states[0])
            # Create the new init block
            new_init = "(:init\n" + "\n".join(new_atoms) + "\n)"
            # Replace the init block
            updated_problem = re.sub(r"\(:init[\s\S]*?\)(?=\s*\(:goal)", new_init, problem_str, flags=re.MULTILINE)
            with open('tmp.pddl', 'w') as f:
                # TODO: open issue in unified-planning
                updated_problem = updated_problem.replace('(at_ ', '(at ')
                f.write(updated_problem)

            # Parse unified-planning problem
            problem = PDDLReader().parse_problem(model_ref_path, 'tmp.pddl')
            os.remove('tmp.pddl')

            # Parse unified-planning plan
            plan = reader.parse_plan_string(problem, plan_str)

            # Ground actions with tarski since unified-planning (1.2.0) grounder is inefficient
            tarski_reader = tarskiPDDLReader(raise_on_error=True)
            tarski_reader.parse_domain(model_ref_path)
            tarski_reader.parse_instance(problem_file)
            grounder = LPGroundingStrategy(tarski_reader.problem)
            ground_actions = grounder.ground_actions()

            # Instantiate the simulator
            with SequentialSimulator(problem=problem) as simulator_ref:

                # Get initial state
                current_state = simulator_ref.get_initial_state()
                lpos = re.findall(r'(\w+(?:\([^\)]*\))?)\s*:\s*true', str(current_state))
                lneg = re.findall(r'(\w+(?:\([^\)]*\))?)\s*:\s*false', str(current_state))
                lprev = set(lpos).union(set([f'not_{l}' for l in lneg]))

                # Get applicable actions in the initial state according to the reference model
                app_actions_ref = get_applicable_actions(simulator_ref, current_state, problem, ground_actions)

                # Parse the simulator state into a pddl problem file for checking action applicability
                # in the learned domain, which requires instantiating a `learned simulator`
                new_problem = problem.clone()
                for fluent in problem.initial_values:
                    value = current_state.get_value(fluent)
                    new_problem.set_initial_value(fluent, value)
                PDDLWriter(new_problem).write_problem("tmp.pddl")

                # TODO: open issue in unified-planning
                with open("tmp.pddl", 'r') as f:
                    data = f.read()
                with open("tmp.pddl", 'w') as f:
                    f.write(data.replace("(at_ ", "(at "))

                domain_learned = PDDLReader().parse_problem(model_learned_path, "tmp.pddl")
                simulator_learned = SequentialSimulator(problem=domain_learned)
                os.remove('tmp.pddl')
                app_actions_learned = get_applicable_actions(simulator_learned,
                                                             # current_state,
                                                             simulator_learned.get_initial_state(),
                                                             domain_learned,
                                                             ground_actions)

                for op in operators:
                    operators[op]['applicability']['tp'] += len(app_actions_learned[op].intersection(app_actions_ref[op]))
                    operators[op]['applicability']['fp'] += len(app_actions_learned[op] - (app_actions_ref[op]))
                    operators[op]['applicability']['fn'] += len(app_actions_ref[op] - (app_actions_learned[op]))

                # Simulate the plan
                # TODO: refactor this if there are no efficiency issues
                for a in plan.actions:

                    prev_problem = problem.clone()
                    for fluent in problem.initial_values:
                        value = current_state.get_value(fluent)
                        prev_problem.set_initial_value(fluent, value)
                    PDDLWriter(prev_problem).write_problem("tmp.pddl")
                    # TODO: open issue in unified-planning
                    with open("tmp.pddl", 'r') as f:
                        data = f.read()
                    with open("tmp.pddl", 'w') as f:
                        f.write(data.replace("(at_ ", "(at "))

                    domain_learned = PDDLReader().parse_problem(model_learned_path, "tmp.pddl")

                    # Must reinstantiate with `new_problem` because of unified-planning object references...
                    simulator_learned = SequentialSimulator(problem=domain_learned)
                    os.remove('tmp.pddl')
                    a_learn = ActionInstance(domain_learned.action(a.action.name),
                                             [domain_learned.object(str(o)) for o in a.actual_parameters])

                    applicable_learn = simulator_learned._is_applicable(simulator_learned.get_initial_state(),
                                                            domain_learned.action(a.action.name),
                                                            [domain_learned.object(str(o)) for o in a.actual_parameters])
                    if applicable_learn:
                        next_state_learned = simulator_learned.apply(simulator_learned.get_initial_state(), a_learn)  # init state equals the ref one
                        assert next_state_learned is not None

                        lpos = re.findall(r'(\w+(?:\([^\)]*\))?)\s*:\s*true', str(next_state_learned))
                        lneg = re.findall(r'(\w+(?:\([^\)]*\))?)\s*:\s*false', str(next_state_learned))
                        lnext_learned = set(lpos).union(set([f'not_{l}' for l in lneg]))

                    # Check action is applicable in the environment model
                    applicable_ref = simulator_ref._is_applicable(current_state,
                                                            problem.action(a.action.name),
                                                            [problem.object(str(o)) for o in a.actual_parameters])
                    assert applicable_ref, ('the action of a plan produced by the environment model '
                                            'must be applicable according to the environment model.')
                    if applicable_ref:
                        current_state = simulator_ref.apply(current_state, a)
                        lpos = re.findall(r'(\w+(?:\([^\)]*\))?)\s*:\s*true', str(current_state))
                        lneg = re.findall(r'(\w+(?:\([^\)]*\))?)\s*:\s*false', str(current_state))
                        lnext_ref = set(lpos).union(set([f'not_{l}' for l in lneg]))

                        if current_state is None:
                            raise Exception(f"Error in applying: {a}")

                    # Get applicable actions in the initial state according to the reference model
                    app_actions_ref = get_applicable_actions(simulator_ref,
                                                             current_state,
                                                             problem,
                                                             ground_actions)

                    # Parse the simulator state into a pddl problem file for checking action applicability
                    # in the learned domain, which requires instantiating a `learned simulator`
                    new_problem = problem.clone()
                    for fluent in problem.initial_values:
                        value = current_state.get_value(fluent)
                        new_problem.set_initial_value(fluent, value)
                    PDDLWriter(new_problem).write_problem("tmp.pddl")
                    # TODO: open issue in unified-planning
                    with open("tmp.pddl", 'r') as f:
                        data = f.read()
                    with open("tmp.pddl", 'w') as f:
                        f.write(data.replace("(at_ ", "(at "))

                    domain_learned = PDDLReader().parse_problem(model_learned_path, "tmp.pddl")
                    simulator_learned = SequentialSimulator(problem=domain_learned)
                    os.remove('tmp.pddl')
                    app_actions_learned = get_applicable_actions(simulator_learned,
                                                                 simulator_learned.get_initial_state(),
                                                                 domain_learned,
                                                                 ground_actions)

                    # Update applicability statistics
                    for op in operators:
                        operators[op]['applicability']['tp'] += len(app_actions_learned[op].intersection(app_actions_ref[op]))
                        operators[op]['applicability']['fp'] += len(app_actions_learned[op] - (app_actions_ref[op]))
                        operators[op]['applicability']['fn'] += len(app_actions_ref[op] - (app_actions_learned[op]))

                    # Update consequentiality statistics
                    if applicable_learn and applicable_ref:  # if the action is applicable in both the learned and reference models
                        operators[a.action.name]['consequentiality']['tp'] += len((lnext_learned - lprev)
                                                                    .intersection((lnext_ref - lprev)))
                        operators[a.action.name]['consequentiality']['fp'] += len((lnext_learned - lprev) - lnext_ref)
                        operators[a.action.name]['consequentiality']['fn'] += len((lnext_learned.intersection(lprev)) - lnext_ref)

                    lprev = lnext_ref

            bar()  # update progress bar

    # Compute operator applicability precision and recall
    all_tp_app = 0
    all_fp_app = 0
    all_fn_app = 0
    all_precision_app = []
    all_recall_app = []
    for op in operators:
        if (operators[op]['applicability']['tp'] + operators[op]['applicability']['fp']) == 0:
            if operators[op]['applicability']['fn'] == 0:
                warnings.warn(f"Operator {op} has never been observed, setting predicted "
                              f"applicability precision to None.")
                operators[op]['applicability']['precision'] = None
            else:
                warnings.warn(f"Operator {op} has been observed but never predicted positive, "
                              f"setting predicted applicability precision to 1.")
                operators[op]['applicability']['precision'] = 1.
        else:
            operators[op]['applicability']['precision'] = ((operators[op]['applicability']['tp'])
                                                           / (operators[op]['applicability']['tp']
                                                              + operators[op]['applicability']['fp']))

        if (operators[op]['applicability']['tp'] + operators[op]['applicability']['fn']) == 0:
            if operators[op]['applicability']['fp'] == 0:
                warnings.warn(f"Operator {op} has never been observed, setting predicted "
                              f"applicability recall to None.")
                operators[op]['applicability']['recall'] = None
            else:
                warnings.warn(f"Operator {op} has been observed but never predicted negative, "
                              f"setting predicted applicability recall to 1.")
                operators[op]['applicability']['recall'] = 1.
        else:
            operators[op]['applicability']['recall'] = ((operators[op]['applicability']['tp'])
                                                        / (operators[op]['applicability']['tp']
                                                           + operators[op]['applicability']['fn']))
        all_tp_app += operators[op]['applicability']['tp']
        all_fp_app += operators[op]['applicability']['fp']
        all_fn_app += operators[op]['applicability']['fn']
        all_precision_app.append(operators[op]['applicability']['precision'])
        all_recall_app.append(operators[op]['applicability']['recall'])

    # Compute overall applicability precision and recall
    overall_precision_app = all_tp_app / (all_tp_app + all_fp_app)
    overall_recall_app = all_tp_app / (all_tp_app + all_fn_app)

    # Compute operator consequentiality precision and recall
    all_tp_cons = 0
    all_fp_cons = 0
    all_fn_cons = 0
    all_precision_cons = []
    all_recall_cons = []
    for op in operators:
        if (operators[op]['consequentiality']['tp'] + operators[op]['consequentiality']['fp']) == 0:
            if operators[op]['consequentiality']['fn'] == 0:
                warnings.warn(f"Operator {op} has never been observed, setting predicted "
                              f"effects precision to None.")
                operators[op]['consequentiality']['precision'] = None
            else:
                operators[op]['consequentiality']['precision'] = 1.
        else:
            operators[op]['consequentiality']['precision'] = ((operators[op]['consequentiality']['tp'])
                                                              / (operators[op]['consequentiality']['tp']
                                                                 + operators[op]['consequentiality']['fp']))

        if (operators[op]['consequentiality']['tp'] + operators[op]['consequentiality']['fn']) == 0:
            if operators[op]['consequentiality']['fp'] == 0:
                warnings.warn(f"Operator {op} has never been observed, setting predicted "
                              f"effects recall to None.")
                operators[op]['consequentiality']['recall'] = None
            else:
                operators[op]['consequentiality']['recall'] = 1.
        else:
            operators[op]['consequentiality']['recall'] = ((operators[op]['consequentiality']['tp'])
                                                           / (operators[op]['consequentiality']['tp']
                                                              + operators[op]['consequentiality']['fn']))
        all_tp_cons += operators[op]['consequentiality']['tp']
        all_fp_cons += operators[op]['consequentiality']['fp']
        all_fn_cons += operators[op]['consequentiality']['fn']
        all_precision_cons.append(operators[op]['consequentiality']['precision'])
        all_recall_cons.append(operators[op]['consequentiality']['recall'])

    # Remove undefined metrics (e.g. predicted effects (aka consequentiality) for operators that have
    # never been observed, or were never applicable in the learned model).
    all_precision_cons = [p for p in all_precision_cons if p is not None]
    all_recall_cons = [p for p in all_recall_cons if p is not None]

    # Compute overall consequentiality precision and recall
    overall_precision_cons = all_tp_cons / (all_tp_cons + all_fp_cons)
    overall_recall_cons = all_tp_cons / (all_tp_cons + all_fn_cons)

    return {
        'applicability': {
            'avg_precision': np.mean(all_precision_app),
            'avg_recall': np.mean(all_recall_app),
            'overall_precision': overall_precision_app,
            'overall_recall': overall_recall_app,
        },
        'predicted_effects': {
            'avg_precision': np.mean(all_precision_cons),
            'avg_recall': np.mean(all_recall_cons),
            'overall_precision': overall_precision_cons,
            'overall_recall': overall_recall_cons,
        },
        **operators
    }


def validate_plans(model_path: str,
                   problem_plan_paths: Dict[str, str]) -> float:
    """
    Validate the plans for the given problems according to the given model.
    :param model_path: path to an action model
    :param problem_plan_paths: dictionary where keys are problem paths and values the respective plan paths.
    :return:
    """
    reader = PDDLReader()
    valid_plans = 0
    for problem_path, plan_path in problem_plan_paths.items():
        # Parse problem
        problem = reader.parse_problem(model_path, problem_path)
        # Parse plan
        plan = reader.parse_plan(problem, plan_path)

        with PlanValidator() as validator:
            result = validator.validate(problem, plan)
            if result.status == ValidationResultStatus.VALID:
                valid_plans += 1

    return valid_plans / len(problem_plan_paths)


def validate_plan(model_path: str,
                  problem_path: str,
                  plan_path: str,) -> float:
    reader = PDDLReader()
    # Parse problem
    problem = reader.parse_problem(model_path, problem_path)
    # Parse plan
    plan = reader.parse_plan(problem, plan_path)

    with PlanValidator() as validator:
        result = validator.validate(problem, plan)

    return result.status == ValidationResultStatus.VALID


def problem_solving(model_learn_path: str,
                    model_ref_path: str,
                    problem_paths: List[str],
                    timeout=60) -> Dict[str, Dict[str, float]]:
    """
    Solve the given problems by means of the given model and return the solving and false plan ratio
    according to a reference model.
    :param model_learn_path: learned model path
    :param model_ref_path: reference model path
    :param problem_paths: list of problem paths
    :param timeout: planner timeout
    :return: solving_ratio and false_plans ratio
    """
    reader = PDDLReader()
    DOWNWARD_SEARCH_CFG = 'let(hff,ff(),let(hcea,cea(),lazy_greedy([hff,hcea],preferred=[hff,hcea])))'
    HEUR_PLANNER_CFG = {
        'name': 'fast-downward',
        'params': dict(
            fast_downward_search_config=DOWNWARD_SEARCH_CFG,
            fast_downward_search_time_limit=f"{timeout}s"
        )}

    solving = 0
    false_plans = 0
    unsolvable = 0
    timed_out = 0
    # Solve the problem with the learned model
    for problem_path in problem_paths:

        logging.info(f"Solving problem {problem_path}")

        problem = reader.parse_problem(model_learn_path, problem_path)

        with contextlib.redirect_stdout(open(os.devnull, 'w')):
            with OneshotPlanner(
                    problem_kind=problem.kind,
                    **HEUR_PLANNER_CFG
            ) as planner:
                result = planner.solve(problem, timeout=timeout)
                plan = result.plan

        if plan is not None:  # neither solving_plan nor false_plan
            # Parse problem
            problem_ref = reader.parse_problem(model_ref_path, problem_path)

            PDDLWriter(problem_ref).write_plan(plan, 'tmp')

            if validate_plan(model_ref_path, problem_path, 'tmp'):
                logging.debug(f"Solution plan for problem {problem_path} is valid")
                solving += 1
            else:
                logging.debug(f"Solution plan for problem {problem_path} is not valid")
                false_plans += 1

            os.remove('tmp')
        else:
            if result.status == PlanGenerationResultStatus.TIMEOUT:
                logging.debug(f"No solution plan found for problem {problem_path} within {timeout} seconds")
                timed_out += 1
            elif result.status in [PlanGenerationResultStatus.UNSOLVABLE_PROVEN, PlanGenerationResultStatus.UNSOLVABLE_INCOMPLETELY]:
                logging.debug(f"Problem is not solvable")
                unsolvable += 1

    return {"problem_solving":
        {
            'solving_ratio': solving / len(problem_paths),
            'false_plans_ratio': false_plans / len(problem_paths),
            'unsolvable_ratio': unsolvable / len(problem_paths),
            'timed_out': timed_out / len(problem_paths)
        }
    }


def solving_eval(model_path: str,
                 problem_plan_paths: Dict[str, str]) -> Dict[str, float]:
    return {'validity': validate_plans(model_path, problem_plan_paths)}


if __name__ == '__main__':

    approaches = ['SAM', 'OffLAM', 'ROSAME', 'NOLAM']

    SYNTACTIC_EVAL = True
    PREDICTIVE_EVAL = True
    SOLVING_EVAL = True
    PROBLEM_SOLVING_DIR = 'problems/solving'

    logging.basicConfig(
        # filename='out.log',
        level=logging.INFO
    )

    metrics_syn = metrics_pred = metrics_solv = dict()

    MAX_TRACES_APPLICABILITY = 100  # lower this for faster debugging
    MAX_PLANNING_SEC = 60  # timeout for problem-solving metrics

    for approach in approaches:
        for run_dir in [d for d in os.listdir(f'../res/{approach}') if '.' not in d]:

            # Read existing metrics (e.g. CPU time)
            with open(f"../res/{approach}/{run_dir}/metrics.json", 'r') as f:
                domain_metrics = json.load(f)

            for model_learned_file in [d for d in os.listdir(f'../res/{approach}/{run_dir}')
                                       if '.pddl' in d]:

                domain = model_learned_file.split('_')[0]

                if domain not in []:
                    model_ref_path = f"../benchmarks/domains/{domain}.pddl"

                    traj_files = sorted(os.listdir(f"../benchmarks/trajectories/applicability/{domain}"),
                                        key=lambda x: int(x.split('/')[-1].split('_')[0]))

                    prob_files = sorted(os.listdir(f"../benchmarks/{PROBLEM_SOLVING_DIR}/{domain}"),
                                        key=lambda x: int(x.split('/')[-1].split('_')[0]))
                    trajs_probs_path = {
                        f"../benchmarks/trajectories/applicability/{domain}/{t}":
                            f"../benchmarks/problems/applicability/{domain}/{t.replace('_traj', '_prob.pddl')}"
                        for k, t in enumerate(traj_files) if k < MAX_TRACES_APPLICABILITY
                    }
                    prob_paths = [f"../benchmarks/{PROBLEM_SOLVING_DIR}/{domain}/{p}" for p in prob_files]

                    model_learned_path = f'../res/{approach}/{run_dir}/{model_learned_file}'

                    if SYNTACTIC_EVAL:
                        metrics_syn = syntactic_eval(model_learned_path, model_ref_path)

                    if PREDICTIVE_EVAL:
                        metrics_pred = predictive_eval(model_learned_path, model_ref_path, trajs_probs_path)

                    if SOLVING_EVAL:
                        metrics_solv = problem_solving(model_learned_path,
                                                       model_ref_path,
                                                       prob_paths,
                                                       timeout=MAX_PLANNING_SEC)

                    domain_metrics[domain] = {
                        **domain_metrics[domain],
                        **metrics_syn,
                        **metrics_pred,
                        **metrics_solv
                    }

            # Extend existing metrics
            with open(f"../res/{approach}/{run_dir}/metrics.json", 'w') as f:
                json.dump(domain_metrics, f, indent=3)

            # Save a reduced set of metrics for later plot
            df_metrics = []
            for d in domain_metrics:
                df_metrics.append({
                    'domain': d,
                    'syn precision': domain_metrics[d]['syntactic']['overall_precision']
                    if 'syntactic' in domain_metrics[d] else None,
                    'syn recall': domain_metrics[d]['syntactic']['overall_recall']
                    if 'syntactic' in domain_metrics[d] else None,
                    'app precision': domain_metrics[d]['applicability']['avg_precision']
                    if 'applicability' in domain_metrics[d] else None,
                    'app recall': domain_metrics[d]['applicability']['avg_recall']
                    if 'applicability' in domain_metrics[d] else None,
                    'predicted_effects precision': domain_metrics[d]['predicted_effects']['avg_precision']
                    if 'predicted_effects' in domain_metrics[d] else None,
                    'predicted_effects recall': domain_metrics[d]['predicted_effects']['avg_recall']
                    if 'predicted_effects' in domain_metrics[d] else None,
                    'solving_ratio': domain_metrics[d]['problem_solving']['solving_ratio']
                    if 'problem_solving' in domain_metrics[d] else None,
                    'false_plans_ratio': domain_metrics[d]['problem_solving']['false_plans_ratio']
                    if 'problem_solving' in domain_metrics[d] else None,
                })
            pd.DataFrame(df_metrics).to_excel(f"../res/{approach}/{run_dir}/metrics.xlsx",
                                              index=False, float_format='%.2f')
