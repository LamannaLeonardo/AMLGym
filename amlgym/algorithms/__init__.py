import difflib
import inspect
from pathlib import Path
import pkgutil
import importlib

registry = {}

package_dir = Path(__file__).resolve().parent
for _, module_name, is_pkg in pkgutil.iter_modules([str(package_dir)]):

    if is_pkg:
        continue
    module = importlib.import_module(f"{__name__}.{module_name}")

    # Expose algorithm classes to allow import such as: from amlgym.algorithms import OffLAM
    if 'AlgorithmAdapter' not in module_name:
        class_obj = getattr(module, module_name, None)
        assert class_obj is not None, f"{module_name}.{module_name} class is not defined"

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name.lower() == module_name.lower():
                registry[name.lower()] = obj


def get_algorithm(name, **kwargs):
    """
    Retrieve an algorithm by name from the registry.

    If the name is not found, raises a ValueError with suggestions for close matches.
    """
    try:
        return registry[name.lower()](**kwargs)
    except KeyError:
        # Find close matches to the requested name
        matches = difflib.get_close_matches(name, registry.keys(), n=3, cutoff=0.6)
        suggestions = f" Did you mean: {', '.join(matches)}?" if matches else ""
        available = ", ".join(sorted(registry.keys()))
        raise ValueError(
            f"Unknown algorithm '{name}'. Available algorithms: {available}.{suggestions}"
        ) from None


def print_algorithms() -> None:
    """
    Print available algorithms and their constructor parameters.
    """
    print("================== AMLGym algorithms suite ==================")
    for i, (name, cls) in enumerate(sorted(registry.items())):
        sig = inspect.signature(cls.__init__)
        params = [
            str(p)
            for pname, p in sig.parameters.items()
            if pname != "self"
            and str(p) != "**kwargs"
        ]

        # Print algorithm name
        print(f"\n{i + 1} - {name}({', '.join(params)})")

        # Print reference
        ref = getattr(cls, "_reference", None)

        if isinstance(ref, dict):
            ref_str = "\n".join(f"\x1B[3m\033[1m\t{k}: {v}.\033[0m" for k, v in ref.items())
        else:
            ref_str = "\tNo reference provided"

        print(ref_str)
