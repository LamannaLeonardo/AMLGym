
from experiment_runner.trace_generator import TraceGenerator
import sys

from experiment_runner.rosame_runner import Rosame_Runner
from rosame_n_sam import OnlyNumericSam
from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser, TrajectoryParser
from pddl_plus_parser.models import Operator
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader, random_split
import numpy as np
sys.path.append("/Users/omarwattad/Documents/Action-Model-Research/sam_learning")
from sam_learning.learners.numeric_sam import NumericSAMLearner

class NumericRosame:
    def __init__(self,domain_file, problem_file,traces=None):
        self.domain_file = domain_file
        self.problem_file = problem_file
        self.trace_generator = TraceGenerator(domain_file,problem_file)
        self.algorithm = Rosame_Runner(self.trace_generator, traces)
        self.nsam = None

    def prepare_rosame_data(self, trajectory_path):
        """
        implementation:
        input: should be numeric trajectory
        output: discrete predicates that are the indexes of the predicate from rosame propositions list
        parse domain -> problem  -> trajectory ---> typed predicates/actions
        1. takes the trajectories (file of type *.trajectory)
        2. drops every predicate that is not in the propositions list
        3. for predicate in the s (or s')
            3.1 if the name and all the parameters are matched in one of the propositions of rosame
                3.1.1 put 1 in the index of this predicate
                3.1.2 else 0
        4. do the same for the actions
        5. we have now a triplets of state action state that rosame can learn from
        """
        domain = DomainParser(self.domain_file).parse_domain()
        problem = ProblemParser(self.problem_file, domain).parse_problem()
        observation = TrajectoryParser(domain, problem).parse_trajectory(trajectory_path)
        pre = []
        next = []
        actions = []
        for index, action_triplet in enumerate(observation.components):
            action = action_triplet.grounded_action_call
            prev_state = action_triplet.previous_state.state_predicates
            next_state = action_triplet.next_state.state_predicates
            op = Operator(action=domain.actions[action.name], domain=domain, grounded_action_call=action.parameters)
            actions.append(self.get_action_number(op))
            state = self.get_predicates(prev_state)
            pre.append(state)
            state = self.get_predicates(next_state)
            next.append(state)
        return pre, actions, next


    def get_predicate_index(self,pred): #TODO CHANGE!
        for predicate, index in self.algorithm.rosame.propositions.items():
            predicate_parts = predicate.split()
            predicate_name = predicate_parts[0]
            predicate_params = predicate_parts[2::2]
            if predicate_name == pred.name:
                match = True
                for obj in predicate_params:
                    if obj not in pred.grounded_objects:
                        match = False
                        break
                if match:
                    return index
        return None

    def get_predicates(self,predicates):
        state = [0] * len(self.algorithm.rosame.propositions)
        for _, predicate in predicates.items():
            true_index = [self.get_predicate_index(p) for p in predicate]
            for ind in true_index:
                state[ind] = 1
        return state

    def get_action_number(self,op):
        for action, action_number in self.algorithm.rosame.actions.items():
            action_parts = action.split()
            action_name = action_parts[0]
            action_params = action_parts[2::2]
            if action_name == op.name:
                match = True
                for obj in op.grounded_call_objects:
                    if obj not in action_params:
                        match = False
                        break
                if match:
                    return action_number
        return None

    def learn_rosame(self,trajectory_path):
        """Learns an action model using ROSAME learning."""

        steps_state1, steps_action, steps_state2 = self.prepare_rosame_data(trajectory_path)

        steps_state1_tensor = torch.tensor(np.array(steps_state1)).float()
        steps_action_tensor = torch.tensor(np.array(steps_action))
        steps_state2_tensor = torch.tensor(np.array(steps_state2)).float()

        batch_sz = 1000
        dataset = TensorDataset(steps_state1_tensor, steps_action_tensor, steps_state2_tensor)
        dataloader = DataLoader(dataset, batch_size=batch_sz, shuffle=False)

        parameters = []
        for schema in self.algorithm.rosame.action_schemas:
            parameters.append({'params': schema.parameters(), 'lr': 1e-3})
        optimizer = optim.Adam(parameters)

        for epoch in range(100):
            loss_final = 0.0
            for i, (state_1, executed_actions, state_2) in enumerate(dataloader):
                optimizer.zero_grad()
                precon, addeff, deleff = self.algorithm.rosame.build(executed_actions)
                preds = state_1 * (1 - deleff) + (1 - state_1) * addeff
                loss = F.mse_loss(preds, state_2, reduction='sum')
                validity_constraint = (1 - state_1) * (precon)
                loss += F.mse_loss(validity_constraint,
                                   torch.zeros(validity_constraint.shape, dtype=validity_constraint.dtype),
                                   reduction='sum')
                #     loss += model.constraint_loss()
                loss += 0.2 * F.mse_loss(precon, torch.ones(precon.shape, dtype=precon.dtype), reduction='sum')
                loss.backward()
                optimizer.step()
                loss_final += loss.item() / batch_sz
            if epoch % 10 == 0:
                print('Epoch {} RESULTS: Average loss: {:.10f}'.format(epoch, loss_final))

    def learn_numeric_rosame(self,dir_path):
        """
        After learning rosame get the learned domain and put it as an input for r-n-rosame algorithm along-side the observations!
        Implementation:
        1. get rosame data done!
        2. let rosame learn descrete predicates from this data
        3. take the learned rosame model and send it to R-N-SAM
        4. N-SAM learns the numeric fluents and add them to the same domain of learned rosame
        """
        trace_generator = TraceGenerator(dir_path + "/sailing_domain.pddl", dir_path + "/pfile0.pddl",dir_path)
        partial_domain = DomainParser(dir_path + "/sailing_domain.pddl",partial_parsing=False).parse_domain()
        for num_traj in [1,2,3,4,5,6,7,8,9,10,15]:
            for fold in range(5):
                algorithm = Rosame_Runner(trace_generator, None)
                observations = []
                for num_prob in range(fold * num_traj, (fold + 1) * num_traj):
                    print(num_traj, fold, num_prob)
                    trace_generator = TraceGenerator(dir_path + "/sailing_domain.pddl", dir_path + f"/pfile{num_prob}.pddl",dir_path)
                    algorithm.trace_generator = trace_generator
                    problem = ProblemParser(dir_path + f"/pfile{num_prob}.pddl",domain=partial_domain).parse_problem()
                    observation = TrajectoryParser(partial_domain,problem).parse_trajectory(dir_path + f"/pfile{num_prob}.trajectory")
                    observations.append(observation)
                    algorithm.ground_new_trajectory()
                    algorithm.learn_rosame(observation)
                algorithm.export_rosame_domain(f"/Users/omarwattad/Documents/Action-Model-Research/rosame/numeric_rosame/experiments/sailing/rosame_{num_traj}_{fold}.pddl")
                discrete_domain = DomainParser(f"/Users/omarwattad/Documents/Action-Model-Research/rosame/numeric_rosame/experiments/sailing/rosame_{num_traj}_{fold}.pddl",partial_parsing=False).parse_domain()
                nrosame = OnlyNumericSam(partial_domain=discrete_domain, clean_data=False)
                learned_model , _ = nrosame.learn_action_model(observations)
                with open(f"/Users/omarwattad/Documents/Action-Model-Research/rosame/numeric_rosame/experiments/sailing/nRosame_{num_traj}_{fold}.pddl","w") as f:
                    f.write(learned_model.to_pddl())

                nsam = NumericSAMLearner(partial_domain=partial_domain)
                learned_model , _ = nsam.learn_action_model(observations)
                with open(f"/Users/omarwattad/Documents/Action-Model-Research/rosame/numeric_rosame/experiments/sailing/nsam_{num_traj}_{fold}.pddl","w") as f:
                    f.write(learned_model.to_pddl())

dir_path = "/Users/omarwattad/Documents/Action-Model-Research/numeric_datasets/sailing"
model = NumericRosame(dir_path+"/sailing_domain.pddl",dir_path+"/pfile0.pddl")
model.learn_numeric_rosame(dir_path)
