.. AMLGym: benchmarking action model learning. documentation master file, created by
   sphinx-quickstart on Fri Oct 24 14:18:00 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


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

