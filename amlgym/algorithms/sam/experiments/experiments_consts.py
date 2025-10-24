from sam_learning.learners import NumericSAMLearner, IncrementalNumericSAMLearner
from sam_learning.learners.baseline_learners.naive_numeric_sam import NaivePolynomialSAMLearning
from utilities import LearningAlgorithmType

DEFAULT_SPLIT = 5

NUMERIC_ALGORITHMS = [
    LearningAlgorithmType.numeric_sam,
    LearningAlgorithmType.plan_miner,
    LearningAlgorithmType.naive_nsam,
    LearningAlgorithmType.naive_polysam,
    LearningAlgorithmType.incremental_nsam,
]

DEFAULT_NUMERIC_TOLERANCE = 0.1

MAX_SIZE_MB = 5


NUMERIC_SAM_ALGORITHM_VERSIONS = {
    LearningAlgorithmType.numeric_sam: NumericSAMLearner,
    LearningAlgorithmType.naive_nsam: NaivePolynomialSAMLearning,
    LearningAlgorithmType.incremental_nsam: IncrementalNumericSAMLearner,
}
