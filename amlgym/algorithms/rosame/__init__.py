import sys

# TODO: replace this temporary patch with update pypi ROSAME package
# Load the actual SAM package (relative import)
from . import models as _models

sys.modules["models"] = _models
