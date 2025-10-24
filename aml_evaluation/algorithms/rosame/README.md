## ROSAME

**ROSAME** (neuRO-Symbolic Action Model lEarner) is a differentiable neuro-symbolic framework for learning lifted action models from visual traces. This repository contains a **modified implementation** of the original ROSAME algorithm introduced in the ICAPS 2024 paper:

📄 **"ROSAME: neuRO-Symbolic Action Model lEarner"**  
by [Kaiyu Xi](https://users.cecs.anu.edu.au/~u7176586/), [Stephen Gould](https://users.cecs.anu.edu.au/~sgould/), and [Sylvie Thiébaux](https://users.cecs.anu.edu.au/~thiebaux/)  
🔗 [**Read the paper**](https://users.cecs.anu.edu.au/~thiebaux/papers/icaps24-rosame.pdf)

## 🔍 Overview
The original ROSAME framework combines:

- Deep learning for visual state prediction from image traces.
- Symbolic reasoning to infer lifted STRIPS-like action models.
- End-to-end differentiability, enabling joint optimization of perception and symbolic model learning.
- This repository builds upon that foundation with several modifications and enhancements:
  - New evaluation metrics for model quality and generalization.
  - Additional experiments on custom datasets and ablation studies.
  -  Numeric Learning Support:
    - Preliminary integration of numeric fluents into the learning process.
    - Enables ROSAME to operate in domains with continuous effects or numeric preconditions.
## 🔧 Key Features

- **Algorithm Adaptation & Extension:**  
  Adapted version of ROSAME with modifications including enhanced state encoding and extended visualization and logging capabilities.

- **Complete Experimental Pipeline:**  
  - **Problem Generator:**  
    Parses PDDL domain and problem files to extract types, predicates, propositions, and an action order dictionary.  
    Two modes are available:
    - Using a custom generator function.
    - Using grounded predicates with `Predicate.ground()` (specific to ROSAME).
  
  - **Trace Generator:**  
    Generates trajectories (state-action traces) from the domain and problem files.
  
  - **Learning Phase:**  
    The ROSAME algorithm processes the generated trajectories:
    - **Trajectory Grounding:** Prepares raw data using `ground_new_trajectory()`.
    - **Model Learning:** Updates the model using `learn_rosame()`, typically over 100–200 epochs.
      
## 🧪 ROSAME Experiment Runner
The ROSAME experimental pipeline is designed to support a full workflow from problem generation to model evaluation. Here’s an overview of its components:

- **Pipeline Overview**
  - **Problem Generator**
    Inputs:
      PDDL domain file (providing types and predicates).
      PDDL problem file (providing current objects).
    Outputs:
      Problem description, propositions, and action order dictionary.

  - **Trace Generator**

    Inputs:
      The parsed domain and problem.
    Outputs:
      Trajectory traces that document state transitions.

- **Algorithm (ROSAME)**  
  The core learning component that builds symbolic action models from trace data.

  **Process:**
  1. Receives the domain definition and corresponding trajectory traces.
  2. Preprocesses and grounds the data using `ground_new_trajectory()`.
  3. Learns the lifted action models by calling `learn_rosame()`, training over a specified number of epochs (e.g., 100 or 200).

  **Iterative Learning:**
  The training procedure runs multiple experiments across:
  - Varying numbers of input trajectories.
  - Multiple cross-validation folds.
  - Different epoch settings for learning robustness and stability.
    
  **Pseudo-code Example:**
    ```python
    experiment = ExperimentRunner(domain_file)

    for num_traj in NUM_OF_TRAJ_LIST:
        for fold in FOLDS:
            for epoch in EPOCHS:
                algorithm = Algorithm(domain_file)

                for num_prob in range(fold * num_traj, (fold + 1) * num_traj):
                    # Parse problem and trajectory
                    problem = ProblemParser(problem_file, domain=domain).parse_problem()
                    trajectory = TrajectoryParser(domain, problem).parse_trajectory(trajectory_file)

                    # Update problem and objects
                    algorithm.add_problem(problem)

                    # Ground and learn
                    algorithm.ground_new_trajectory()
                    algorithm.learn_rosame(trajectory, epoch)
    
            # Save learned model domain.
            algorithm.export_rosame_domain(leaned_model_path)

            # Run statistical experiments on the learned domain.
            experiment.run_single_experiment(learned_model_path,'rosame',num_traj,fold=fold,epoch=epoch)
    
    # Export statistical results
    experiment.export_statistics(path_to_results)



