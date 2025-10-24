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

    # Expose algorithm classes to allow import such as: from aml_evaluation.algorithms import OffLAM
    if module_name != 'AlgorithmAdapter':
        class_obj = getattr(module, module_name, None)
        assert class_obj is not None, f"{module_name}.{module_name} class is not defined"

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name.lower() == module_name.lower():
                registry[name] = obj


def get_algorithm(name, **kwargs):
    try:
        return registry[name](**kwargs)
    except KeyError:
        raise ValueError(f"Algorithm '{name}' not found. Available: {list(registry)}")


def print_algorithms() -> None:
    """
    Print available algorithms and their constructor parameters.
    """
    print("Available algorithms:")
    for name, cls in registry.items():
        sig = inspect.signature(cls.__init__)
        params = [
            str(p)
            for pname, p in sig.parameters.items()
            if pname != "self"
            and str(p) != "**kwargs"
        ]
        print(f"  - {name}({', '.join(params)})")
