import unittest
import warnings
from collections import defaultdict

from amlgym.metrics import predicted_effects, predictive_power


class ToyEnv:
    """One operator ``a``, applicable in every state, with fixed add and delete effects."""

    def __init__(self, adds, dels):
        self.adds, self.dels = set(adds), set(dels)

    def applicable_actions(self, s):
        return defaultdict(set, {'a': {'(a)'}})

    def apply(self, s, a):
        return (set(s) - self.dels) | self.adds


class TestPredictedEffects(unittest.TestCase):
    # In state {p, q} the reference action deletes p and adds r.
    reference = ToyEnv(adds={'r'}, dels={'p'})
    states = [{'p', 'q'}]
    cases = {  # learned model, expected (precision, recall)
        'exact': (ToyEnv({'r'}, {'p'}), (1., 1.)),
        'missing add': (ToyEnv(set(), {'p'}), (1., .5)),
        'missing delete': (ToyEnv({'r'}, set()), (1., .5)),
        'spurious add': (ToyEnv({'r', 's'}, {'p'}), (2 / 3, 1.)),
        'spurious delete': (ToyEnv({'r'}, {'p', 'q'}), (2 / 3, 1.)),
        'no effects': (ToyEnv(set(), set()), (1., 0.)),
    }

    def check(self, metric):
        for name, (learned, (precision, recall)) in self.cases.items():
            with self.subTest(name), warnings.catch_warnings():
                warnings.simplefilter('ignore')
                result = metric(learned, self.reference, self.states)
                self.assertAlmostEqual(result['mean_precision'], precision)
                self.assertAlmostEqual(result['mean_recall'], recall)

    def test_predicted_effects(self):
        self.check(lambda *args: predicted_effects(*args, show_progress=False))

    def test_predictive_power(self):
        self.check(lambda *args: predictive_power(*args, show_progress=False)['predicted_effects'])


if __name__ == '__main__':
    unittest.main()
