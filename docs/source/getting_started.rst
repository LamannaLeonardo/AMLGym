Getting started
=====================

.. toctree::
   :maxdepth: 1
   :titlesonly:

Install AMLGym:

.. code-block:: console

   pip install amlgym


Example usage:

.. code-block:: console

   from amlgym.algorithms import get_algorithm
   agent = get_algorithm('OffLAM')
   model = agent.learn('path/to/domain.pddl', ['path/to/trace0', 'path/to/trace1'])
   print(model)

