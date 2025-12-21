from ._syntactic import syntactic_precision, syntactic_recall
from ._solving import problem_solving
from ._predictive import predictive_power, predicted_effects, applicability


__all__ = [
    "print_metrics",
    "syntactic_precision",
    "syntactic_recall",
    "problem_solving",
    "predictive_power",
    "predicted_effects",
    "applicability",
]


def print_metrics() -> None:
    """
    Display the available metrics.

    :return:
    """
    metrics = [name for name in __all__
               if name not in ["print_metrics", "predictive_power"]]
    print("Available metrics:")
    for m in metrics:
        print(f" - {m}")

