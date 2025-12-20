from ._syntactic import syntactic_precision, syntactic_recall
from ._solving import problem_solving
<<<<<<< HEAD
from ._predictive import predictive_power, predicted_effects, applicability
=======
>>>>>>> origin/main

__all__ = [
    "print_metrics",
    "syntactic_precision",
    "syntactic_recall",
    "problem_solving",
<<<<<<< HEAD
    "predictive_power",
    "predicted_effects",
    "applicability",
=======
>>>>>>> origin/main
]


def print_metrics() -> None:
    """
    Display the available metrics.

    :return:
    """
<<<<<<< HEAD
    metrics = [name for name in __all__
               if name not in ["print_metrics", "predictive_power"]]
=======
    metrics = [name for name in __all__ if name != "print_metrics"]
>>>>>>> origin/main
    print("Available metrics:")
    for m in metrics:
        print(f" - {m}")

