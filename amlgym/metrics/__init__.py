from ._syntactic import syntactic_precision, syntactic_recall
from ._solving import problem_solving

__all__ = [
    "print_metrics",
    "syntactic_precision",
    "syntactic_recall",
    "problem_solving",
]


def print_metrics() -> None:
    """
    Display the available metrics.

    :return:
    """
    metrics = [name for name in __all__ if name != "print_metrics"]
    print("Available metrics:")
    for m in metrics:
        print(f" - {m}")

