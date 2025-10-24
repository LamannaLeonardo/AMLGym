import sys

# TODO: replace this temporary patch with update pypi N-SAM package
# Load the actual SAM package (relative import)
from . import utilities as _utilities
from . import sam_learning as _sam_learning

# Inject it into sys.modules under the expected top-level name
sys.modules["utilities"] = _utilities
sys.modules["sam_learning"] = _sam_learning
