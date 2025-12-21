# AMLGym: benchmarking action model learning
<!-- Define badges -->
<div style="display: flex; gap: 10px;">
   
  <a href="https://opensource.org/licenses/MIT" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" height="20"/></a>
    
  <a href="https://pypi.python.org/pypi/amlgym" target="_blank">
    <img src="https://badge.fury.io/py/amlgym.svg" height="20"/></a>
    
  <a href="https://amlgym.readthedocs.io/en/latest/" target="_blank">
    <img src="https://readthedocs.org/projects/amlgym/badge/?version=latest" height="20"/></a>

</div>


Framework for experimenting with action model 
learning approaches and evaluating the learned domain models.



### Installation
```
pip install amlgym
```

### Example usage
```
from amlgym.algorithms import get_algorithm
agent = get_algorithm('OffLAM')
model = agent.learn('path/to/domain.pddl', ['path/to/trace0', 'path/to/trace1'])
print(model)
```

### Documentation
Tutorials and API documentation is accessible on [Read the Docs](https://amlgym.readthedocs.io/en/latest/)


## State-of-the-art Algorithms
AMLGym provides seamless integration with state-of-the-art algorithms 
for offline learning classical planning domains from an input set of 
trajectories in the following settings:
1. **full** observability: SAM [1].
2. **partial** observability: OffLAM [2].
3. **full** and **noisy** observability: NOLAM [3], ROSAME [4].

[1] ["Safe Learning of Lifted Action Models", B. Juba and H. S. Le, and R. Stern, 
Proceedings of the 18th International Conference on Principles of Knowledge 
Representation and Reasoning, 2021.](https://proceedings.kr.org/2021/36/)

[2] ["Lifted Action Models Learning from Partial Traces", L. Lamanna, L. Serafini,
A. Saetti, A. Gerevini, and P. Traverso, Artificial Intelligence Journal, 
2025.](https://www.sciencedirect.com/science/article/abs/pii/S0004370224001929)

[3] ["Action Model Learning from Noisy Traces: a Probabilistic Approach", L. Lamanna 
and L. Serafini, Proceedings of the Thirty-Fourth International Conference on 
Automated Planning and Scheduling, 2024.](
https://ojs.aaai.org/index.php/ICAPS/article/view/31493)

[4] ["Neuro-symbolic learning of lifted action models from visual traces", X. Kai, 
S. Gould, and S. Thiébaux, Proceedings of the Thirty-Fourth International Conference on 
Automated Planning and Scheduling, 2024.](https://ojs.aaai.org/index.php/ICAPS/article/download/31528/33688)


### Adding an algorithm
PRs with new or existing state-of-the-art algorithms are welcome:

1. Add the algorithm PyPI package in `requirements.txt`
2. Create a Python class in `algorithms` which inherits from `AlgorithmAdapter.py` and implements the `learn` method


## Evaluation

AMLGym can evaluate a PDDL model by means of several metrics:
1. _Syntactic similarity_ 
2. _Problem solving_
3. _Predicted applicability and predicted effects_

## Benchmarking
See the [benchmark](/amlgym/benchmarks/README.md) package for details.

## License
This project is licensed under the MIT License - see the [LICENSE](/LICENSE.md) file for details.

## Citing
Not yet available
