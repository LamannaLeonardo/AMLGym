r"""
Problem solving metrics assess a domain model ability of solving problems.
The *solving ratio* evaluates the model ability of producing plans that are
applicable in the environment and achieve the given goal.
The *false plans ratio* measures the ratio of produced plans that are either not
applicable in the environment or do not achieve the given goal.
Problem solving metrics are defined with respect to a set of problems and a planner.
"""
import contextlib
import os
import warnings

from alive_progress import alive_bar
from unified_planning.engines import PlanGenerationResultStatus, ValidationResultStatus
from unified_planning.io import PDDLReader, PDDLWriter
from unified_planning.shortcuts import PlanValidator, OneshotPlanner
from typing import Dict, List


def problem_solving(model_learn_path: str,
                    model_ref_path: str,
                    problem_paths: List[str],
                    timeout=60,
                    show_progress: bool = True) -> Dict[str, float]:
    """
    Solve the given problems using the model to be evaluated and return:
     (i) the solving plans ratio in the environment defined by the reference model
     (ii) the false plans ratio in the environment defined by the reference model
     (iii) the ratio of problems deemed unsolvable
     (iv) the ratio of problems where the planning process timed out
     (v) the ratio of problems that raised syntax errors during parsing in unified planning

    :param model_learn_path: learned model path
    :param model_ref_path: reference model path
    :param problem_paths: list of problem paths
    :param timeout: planner timeout

    :return: solving and false plans ratios, deemed unsolvable problems, timed out planning processes
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
    syntax_errors = 0

    # Solve the problem with the learned model
    bar = alive_bar(len(problem_paths),
                    title=f'Evaluating problem solving...',
                    length=20) if show_progress else contextlib.nullcontext()
    with bar as bar:
        for problem_path in problem_paths:

            try:
                problem = reader.parse_problem(model_learn_path, problem_path)
            except SyntaxError as err:
                warnings.warn(
                    f"Failed to parse problem '{problem_path}' with domain "
                    f"{model_learn_path}: {err}",
                    stacklevel=2
                )
                syntax_errors += 1
                continue

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
                    solving += 1
                else:
                    false_plans += 1

                os.remove('tmp')
            else:
                if result.status == PlanGenerationResultStatus.TIMEOUT:
                    timed_out += 1
                elif result.status in [PlanGenerationResultStatus.UNSOLVABLE_PROVEN,
                                       PlanGenerationResultStatus.UNSOLVABLE_INCOMPLETELY]:
                    unsolvable += 1

            if show_progress:
                bar()

    return {
        'solving_ratio': solving / len(problem_paths),
        'false_plans_ratio': false_plans / len(problem_paths),
        'unsolvable_ratio': unsolvable / len(problem_paths),
        'timed_out': timed_out / len(problem_paths),
        'syntax_errors': syntax_errors / len(problem_paths)
    }


def validate_plan(model_path: str,
                  problem_path: str,
                  plan_path: str,) -> float:
    """
    Validate the solution plan to the given problem in the environment defined by the given model.
    The definition of valid plan follows the one provided in "PDDL2. 1: An extension to PDDL for
    expressing temporal planning domains", M. Fox and D. Long, JAIR 2003.

    :param model_path: path to the PDDL model defining the environment.
    :param problem_path: path to the PDDL problem to be solved.
    :param plan_path: path to the solution plan for the PDDL problem.

    :return: true if the plan is valid, otherwise false.
    """
    reader = PDDLReader()
    # Parse problem
    problem = reader.parse_problem(model_path, problem_path)
    # Parse plan
    plan = reader.parse_plan(problem, plan_path)

    with PlanValidator() as validator:
        result = validator.validate(problem, plan)

    return result.status == ValidationResultStatus.VALID
