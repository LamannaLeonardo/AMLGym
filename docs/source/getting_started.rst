Getting started
=====================

.. toctree::
   :maxdepth: 1
   :titlesonly:

Install AMLGym:

.. code-block:: console

   pip install amlgym


Example usage for passive learning a domain model:

.. code-block:: python

   from amlgym.algorithms import get_algorithm
   from amlgym.benchmarks import get_domain_path, get_trajectories_path
   from amlgym.util.util import empty_domain

   # Get a learning algorithm
   agent = get_algorithm('offlam')

   # Get an input domain path with no preconditions and effects
   domain_path = get_domain_path('blocksworld')
   domain_empty_path = empty_domain(domain_path)

   # Get an input set of trajectory paths to learn from
   traj_paths = get_trajectories_path('blocksworld')

   # Learn a domain model
   model = agent.learn(domain_empty_path, traj_paths)
   print(model)

Further examples are available in the tutorials section for :ref:`tutorials-learning-label`
and :ref:`tutorials-evaluating-label`.
