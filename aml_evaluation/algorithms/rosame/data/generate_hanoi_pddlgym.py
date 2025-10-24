import pddlgym
import imageio
import matplotlib.pyplot as plt
import numpy as np
import torch
import numpy.random as npr
import random
import argparse


objects = ['d1', 'd2', 'd3', 'd4', 'peg1', 'peg2', 'peg3']
action_order = [f'(move {obj1} {obj2} {obj3})' for obj1 in objects for obj2 in objects for obj3 in objects
                if obj1!=obj2 and obj1!=obj3 and obj2!=obj3]
action_order = {k: v for v, k in enumerate(action_order)}
propositions = [f'(clear {obj})' for obj in objects]
propositions.extend([f'(on {obj1} {obj2})' for obj1 in objects for obj2 in objects if obj1!=obj2])
discs = objects[:4]
propositions.extend([f'(smaller {obj1} {obj2})' for obj1 in discs for obj2 in discs if obj1!=obj2])
propositions = {k: v for v, k in enumerate(propositions)}

def obs_to_label(obs):
    label = np.zeros(len(propositions))
    for literal in obs.literals:
        if literal.pddl_str() not in propositions:
            # This is for handfull
            continue
        label[propositions[literal.pddl_str()]] = 1
    return label

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="-s save_addr")
    parser.add_argument("-s", default="data", help="save address")
    parser.add_argument("--seed", type=int, default=8800)
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    random.seed(args.seed)
    npr.seed(args.seed)

    # Use PDDL Gym
    # https://github.com/tomsilver/pddlgym
    env = pddlgym.make("PDDLEnvHanoi_operator_actions-v0")
    env.fix_problem_index(1)
    obs, info = env.reset()

    labels = []
    actions = []

    # Create a long trace to be cut later
    for i in range(500):#5500
        imageio.imsave(f"{args.s}/{i}.png", env.render())
        plt.close()
        labels.append(obs_to_label(obs))
        action = env.action_space.sample(obs)
        actions.append(action_order[action.pddl_str()])
        obs = env.step(action)[0]

    labels_tensor = torch.tensor(np.array(labels), dtype=torch.float32)
    actions_tensor = torch.tensor(np.array(actions))

    torch.save(labels_tensor, f"{args.s}/labels.pt")
    torch.save(actions_tensor, f"{args.s}/actions.pt")

