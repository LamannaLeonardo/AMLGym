Algorithms
==========


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

.. toctree::
   :maxdepth: 4
   :titlesonly:

   sam
   offlam
   nolam
   rosame
