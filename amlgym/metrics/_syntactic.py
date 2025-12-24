r"""
Syntactic similarity metrics compare the intersection or difference of the atoms
in the action preconditions and effects between an evaluated domain model :math:`M`
and reference model :math:`M^{*}`.
Let :math:`pre_M(a)` be the set of preconditions of an action :math:`a` according to :math:`M`.

* True Positives: :math:`TP_{pre}(a)=|(pre_M(a)\cap pre_M^{*}(a)|`
* False Positives: :math:`FP_{pre}(a)=|(pre_M(a)\setminus pre_M^{*}(a)|`
* False Negatives: :math:`FN_{pre}(a)=|(pre_M^{*}(a)\setminus pre_M(a))|`

The preconditions precision :math:`P_{pre}` and recall :math:`R_{pre}` are defined as:

* Syntactic precision of :math:`pre_a` : :math:`P_{pre}(a) = \frac{TP_{pre}(a)}{TP_{pre}(a)+FP_{pre}(a)}`
* Syntactic recall of :math:`pre_a`: :math:`R_{pre}(a) = \frac{TP_{pre}(a)}{TP_{pre}(a)+FN_{pre}(a)}`

The precision of an action :math:`a` is defined by summing up :math:`TP(a)` over
the preconditions :math:`pre`, positive effects :math:`eff^+` and negative effects :math:`eff^-`:

* Syntactic precision of :math:`a` : :math:`P(a) = \frac{TP(a)}{TP(a)+FP(a)}`
* Syntactic recall of :math:`a` : :math:`R(a) = \frac{TP(a)}{TP(a)+FN(a)}`

Finally, the overall precision and recall of a domain model averages over the actions precision and recall:

* **Syntactic precision** of :math:`M`: :math:`P = \frac{1}{|A|}\sum_{a\in A} P(a)`
* **Syntactic recall** of :math:`M`: :math:`R = \frac{1}{|A|}\sum_{a\in A} R(a)`


"""

from amlgym.util.SimpleDomainReader import SimpleDomainReader, Operator

from typing import Dict
import numpy as np
import warnings
import copy
from sklearn.metrics import precision_score, recall_score


def syntactic_precision(evaluated_path: str,
                        reference_path: str) -> Dict[str, float]:
    """
    Evaluate the syntactic precision metric of a domain model :math:`M` with
    respect to a reference model :math:`M^{*}`.

    :param evaluated_path: path of the PDDL model to evaluate.
    :param reference_path: path of the PDDL reference model.

    :return: the syntactic precision grouped by preconditions and effects
    """

    eval_model = SimpleDomainReader(input_file=evaluated_path)
    ref_model = SimpleDomainReader(input_file=reference_path)

    # Normalize operator names
    for op_gt, op_eval in zip(ref_model.operators, eval_model.operators):
        op_gt.operator_name = op_gt.operator_name.replace('_', '-')
        op_eval.operator_name = op_eval.operator_name.replace('_', '-')

    # Sort reference model operators
    ref_model.operators.sort(key=lambda op: op.operator_name, reverse=True)
    eval_operator_map = {op.operator_name: op for op in eval_model.operators}

    # Align evaluated operators to the reference order
    eval_model.operators = [
        eval_operator_map.get(op.operator_name, _empty_operator_like(op))
        for op in ref_model.operators
    ]

    # Verify correct operator alignment
    assert all(
        gt_op.operator_name == eval_op.operator_name
        for gt_op, eval_op in zip(ref_model.operators, eval_model.operators)
    )

    # Measure the preconditions/effects precision for every operator
    results = {k: [] for k in ["precs_pos", "precs_neg", "eff_pos", "eff_neg", "overall"]}

    for gt_op, eval_op in zip(ref_model.operators, eval_model.operators):
        metrics = _compute_operator_precision(gt_op, eval_op)
        for key, val in metrics.items():
            results[key].append(val)

    # Aggregate results
    return {
        'precs_pos': np.round(np.mean(results["precs_pos"]), 2),
        'precs_neg': np.round(np.mean(results["precs_neg"]), 2),
        'eff_pos': np.round(np.mean(results["eff_pos"]), 2),
        'eff_neg': np.round(np.mean(results["eff_neg"]), 2),
        'mean': np.round(np.mean(results["overall"]), 2)
    }


def syntactic_recall(evaluated_path: str,
                     reference_path: str) -> Dict[str, float]:
    """
    Evaluate the syntactic recall metric of a domain model :math:`M` with
    respect to a reference model :math:`M^{*}`.

    :param evaluated_path: path of the PDDL model to evaluate.
    :param reference_path: path of the PDDL reference model.

    :return: the syntactic recall grouped by preconditions and effects
    """

    eval_model = SimpleDomainReader(input_file=evaluated_path)
    ref_model = SimpleDomainReader(input_file=reference_path)

    # Normalize operator names
    for op_gt, op_eval in zip(ref_model.operators, eval_model.operators):
        op_gt.operator_name = op_gt.operator_name.replace('_', '-')
        op_eval.operator_name = op_eval.operator_name.replace('_', '-')

    # Sort reference model operators
    ref_model.operators.sort(key=lambda op: op.operator_name, reverse=True)
    eval_operator_map = {op.operator_name: op for op in eval_model.operators}

    # Align evaluated operators to the reference order
    eval_model.operators = [
        eval_operator_map.get(op.operator_name, _empty_operator_like(op))
        for op in ref_model.operators
    ]

    # Verify correct operator alignment
    assert all(
        gt_op.operator_name == eval_op.operator_name
        for gt_op, eval_op in zip(ref_model.operators, eval_model.operators)
    )

    # Measure the preconditions/effects precision for every operator
    results = {k: [] for k in ["precs_pos", "precs_neg", "eff_pos", "eff_neg", "overall"]}

    for gt_op, eval_op in zip(ref_model.operators, eval_model.operators):
        metrics = _compute_operator_recall(gt_op, eval_op)
        for key, val in metrics.items():
            results[key].append(val)

    # Aggregate results
    return {
        'precs_pos': np.round(np.mean(results["precs_pos"]), 2),
        'precs_neg': np.round(np.mean(results["precs_neg"]), 2),
        'eff_pos': np.round(np.mean(results["eff_pos"]), 2),
        'eff_neg': np.round(np.mean(results["eff_neg"]), 2),
        'mean': np.round(np.mean(results["overall"]), 2)
    }


def _empty_operator_like(op: Operator) -> Operator:
    """
    Return a copy of op with all preconditions and effects empty.

    :param op: input operator

    :return: a copy of `op` with no preconditions and no effects
    """
    new_op = copy.deepcopy(op)
    new_op.precs_pos = []
    new_op.precs_neg = []
    new_op.eff_pos = []
    new_op.eff_neg = []
    return new_op


def _compute_operator_precision(reference_op: Operator,
                                evaluated_op: Operator) -> Dict[str, float]:
    """
    Compute syntactic precision of preconditions and effects of a single operator.

    :param reference_op: ground-truth operator
    :param evaluated_op: operator to be evaluated

    :return: operator syntactic precision grouped by preconditions and effects
    """
    categories = {
        "precs_pos": (reference_op.precs_pos, evaluated_op.precs_pos),
        "precs_neg": (reference_op.precs_neg, evaluated_op.precs_neg),
        "eff_pos": (reference_op.eff_pos, evaluated_op.eff_pos),
        "eff_neg": (reference_op.eff_neg, evaluated_op.eff_neg),
    }

    precisions = {}
    all_tp = all_fp = all_fn = 0

    for key, (gt, pred) in categories.items():
        universe = list(set(gt) | set(pred))
        y_true = [1 if p in gt else 0 for p in universe]
        y_pred = [1 if p in pred else 0 for p in universe]

        if not universe:
            # No predicates at all
            warnings.warn(f"No {key} for operator {reference_op.operator_name}, "
                          f"precision set to 1.", stacklevel=2)
            precision = 1.0
        else:
            precision = precision_score(y_true, y_pred, zero_division=1.)

        precisions[key] = precision

        # Compute tp/fp/fn counts for overall precision
        gt_set, pred_set = set(gt), set(pred)
        all_tp += len(gt_set & pred_set)
        all_fp += len(pred_set - gt_set)
        all_fn += len(gt_set - pred_set)

    overall_precision = (
        all_tp / (all_tp + all_fp)
        if (all_tp + all_fp) > 0
        else 1.0
    )

    precisions["overall"] = overall_precision
    return precisions


def _compute_operator_recall(reference_op: Operator,
                             evaluated_op: Operator) -> Dict[str, float]:
    """
    Compute syntactic recall of preconditions and effects of a single operator.

    :param reference_op: ground-truth operator
    :param evaluated_op: operator to be evaluated

    :return: operator syntactic recall grouped by preconditions and effects
    """
    categories = {
        "precs_pos": (reference_op.precs_pos, evaluated_op.precs_pos),
        "precs_neg": (reference_op.precs_neg, evaluated_op.precs_neg),
        "eff_pos": (reference_op.eff_pos, evaluated_op.eff_pos),
        "eff_neg": (reference_op.eff_neg, evaluated_op.eff_neg),
    }

    recalls = {}
    all_tp = all_fp = all_fn = 0

    for key, (gt, pred) in categories.items():
        universe = list(set(gt) | set(pred))
        y_true = [1 if p in gt else 0 for p in universe]
        y_pred = [1 if p in pred else 0 for p in universe]

        if not universe:
            # No predicates at all
            warnings.warn(f"No {key} for operator {reference_op.operator_name}, "
                          f"recall set to 1.", stacklevel=2)
            recall = 1.0
        else:
            recall = recall_score(y_true, y_pred, zero_division=1.)

        recalls[key] = recall

        # Compute tp/fp/fn counts for overall recall
        gt_set, pred_set = set(gt), set(pred)
        all_tp += len(gt_set & pred_set)
        all_fp += len(pred_set - gt_set)
        all_fn += len(gt_set - pred_set)

    overall_recall = (
        all_tp / (all_tp + all_fn)
        if (all_tp + all_fn) > 0
        else 1.0
    )

    recalls["overall"] = overall_recall
    return recalls
