
import itertools
import math
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from pddl_plus_parser.lisp_parsers import ProblemParser, TrajectoryParser
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from experiment_runner.rosame_runner import Rosame_Runner
import sys
from pathlib import Path
from pddl_plus_parser.models import Domain, Observation, State, ActionCall, PDDLFunction, Predicate, GroundedPredicate, create_type_hierarchy_graph

from pddl_plus_parser.lisp_parsers import ProblemParser, TrajectoryParser, DomainParser

sys.path.append("/Users/omarwattad/Documents/Action-Model-Research/sam_learning")
from sam_learning.learners.multi_agent_sam import MultiAgentSAM

def prepare_rosame_data(model, observation):
    """
    Prepares structured data from traces to be used within the ROSAME framework, which the data should be encoded to True/False (0  and 1)
    using the triples that are created using macq every fluent is true takes 1 else 0
    returns:
    - encoded pre_state
    - encoded next_state
    - encoded action
    """
    steps_action = []
    steps_state1, steps_state2 = [], []
    for component in observation.components:
        exec_action = []
        for action in component.grounded_joint_action.actions:
            action_lst = action.__str__()[1:-1].split()

            if len(action_lst) != len(set(action_lst)):
                continue
            if action.__str__()[1:-1] == 'nop ':
                exec_action.append(-1)
            else:
                exec_action.append(model.rosame.actions[action.__str__()[1:-1]])
        steps_action.append(exec_action)
        # if not steps_action: continue
        next_state, pre_state = [], []
        for _, val in component.next_state.state_predicates.items():
            for pred in val:
                next_state.append(pred.untyped_representation[1:-1])
        for _, val in component.previous_state.state_predicates.items():
            for pred in val:
                pre_state.append(pred.untyped_representation[1:-1])
        state1 = [1 if p in pre_state else 0 for p in model.rosame.propositions]
        state2 = [1 if p in next_state else 0 for p in model.rosame.propositions]
        steps_state1.append(state1)
        steps_state2.append(state2)
    return steps_state1,steps_action, steps_state2

def learn_rosame(model, observation):
    """Learns an action model using ROSAME learning with multi-agent joint actions (no 'nop')."""

    # Each step has: state1, joint_action (list of ints), state2
    steps_state1, steps_joint_action, steps_state2 = prepare_rosame_data(model,observation)

    steps_state1_tensor = torch.tensor(np.array(steps_state1)).float()           # [N, num_props]
    steps_joint_action_tensor = torch.tensor(np.array(steps_joint_action))       # [N, num_agents]
    steps_state2_tensor = torch.tensor(np.array(steps_state2)).float()           # [N, num_props]

    batch_sz = 1000
    dataset = TensorDataset(steps_state1_tensor, steps_joint_action_tensor, steps_state2_tensor)
    dataloader = DataLoader(dataset, batch_size=batch_sz, shuffle=False)

    # Collect learnable parameters from all schemas
    parameters = [{'params': schema.parameters(), 'lr': 1e-3} for schema in model.rosame.action_schemas]
    optimizer = optim.Adam(parameters)

    for epoch in range(100):
        epoch_loss = 0.0

        for i, (state_1, joint_actions, state_2) in enumerate(dataloader):
            optimizer.zero_grad()
            total_loss = 0.0

            for agent_idx in range(joint_actions.shape[1]):
                # Get actions for this agent in the batch
                actions = joint_actions[:, agent_idx]
                # actions = actions[actions != -1]
                # print(actions)# [batch_size]
                # Build precondition/add/delete matrices for those actions
                precon, addeff, deleff = model.rosame.build(actions)

                # Predict next state based on effects applied to current state
                predicted_state2 = state_1 * (1 - deleff) + (1 - state_1) * addeff

                # Loss between predicted and actual next state
                effect_loss = F.mse_loss(predicted_state2, state_2, reduction='sum')

                # Precondition validity loss (should not violate preconditions)
                validity_constraint = (1 - state_1) * precon
                precon_loss = F.mse_loss(validity_constraint,
                                         torch.zeros_like(validity_constraint),
                                         reduction='sum')

                # Encourage model to learn 1s in preconditions
                reg_loss = 0.2 * F.mse_loss(precon, torch.ones_like(precon), reduction='sum')

                total_loss += effect_loss + precon_loss + reg_loss

            total_loss.backward()
            optimizer.step()

            epoch_loss += total_loss.item() / batch_sz

        if epoch % 10 == 0:
            print(f"[Epoch {epoch}] Avg Loss: {epoch_loss:.6f}")

dataset_path = Path("/Users/omarwattad/Downloads/ma-sam-main/experiments_dataset")
algo = Rosame_Runner(dataset_path / "satellite/satellite_combined_domain.pddl")
partial_domain = DomainParser(dataset_path / "satellite/satellite_combined_domain.pddl",partial_parsing=True).parse_domain()
print(partial_domain.to_pddl())
observations = []
counter = 0
for traj in [5,6,7,8,9,10,11,12,13,14,15,16,18,19,20]:
    if traj > 9:
        problem = ProblemParser(dataset_path / f"satellite/p{traj}-pfile{traj}.pddl", partial_domain).parse_problem()
    else:
        problem = ProblemParser(dataset_path / f"satellite/p0{traj}-pfile{traj}.pddl", partial_domain).parse_problem()

    if traj > 9:
        observation = TrajectoryParser(partial_domain, problem).parse_trajectory(
            trajectory_file_path=dataset_path / f"satellite/p{traj}-pfile{traj}.trajectory",
            executing_agents=["satellite0", "satellite1", "satellite2", "satellite3", "satellite4", "satellite5",
                              "satellite6", "satellite7", "satellite8", "satellite9"])
    else:
        observation = TrajectoryParser(partial_domain,problem).parse_trajectory(trajectory_file_path=dataset_path / f"satellite/p0{traj}-pfile{traj}.trajectory",executing_agents=["satellite0","satellite1","satellite2","satellite3","satellite4","satellite5","satellite6","satellite7","satellite8","satellite9"])

    observations.append(observation)
    algo.add_problem(problem)
    algo.ground_new_trajectory()
    learn_rosame(algo, observation)
    counter += 1
    sam = MultiAgentSAM(partial_domain)
    learned, _ = sam.learn_combined_action_model(observations)
    with open(f"/Users/omarwattad/Documents/Action-Model-Research/rosame/MA_domains/satellite/MA-SAM_{counter}", "w") as f:
        f.write(learned.to_pddl())
    algo.export_rosame_domain(f"/Users/omarwattad/Documents/Action-Model-Research/rosame/MA_domains/satellite/MA-ROSAME_{counter}.pddl")