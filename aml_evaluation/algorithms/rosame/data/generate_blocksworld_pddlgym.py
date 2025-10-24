import pddlgym
import imageio
import matplotlib.pyplot as plt
import numpy as np
import torch
import numpy.random as npr
import random
import argparse

blocks = ['a', 'b', 'c', 'd', 'e']
action_order = [f'(pick-up {block})' for block in blocks]
action_order.extend([f'(put-down {block})' for block in blocks])
action_order.extend([f'(stack {block1} {block2})' for block1 in blocks for block2 in blocks if block1!=block2])
action_order.extend([f'(unstack {block1} {block2})' for block1 in blocks for block2 in blocks if block1!=block2])
action_order = {k: v for v, k in enumerate(action_order)}
propositions = ['(handempty)']
propositions.extend([f'(clear {block})' for block in blocks])
propositions.extend([f'(ontable {block})' for block in blocks])
propositions.extend([f'(holding {block})' for block in blocks])
propositions.extend([f'(on {block1} {block2})' for block1 in blocks for block2 in blocks if block1!=block2])
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
    env = pddlgym.make("PDDLEnvBlocks_operator_actions-v0")
    env.fix_problem_index(1)
    obs, info = env.reset()
    labels = []
    actions = []

    # Create a long trace to be cut later
    for i in range(1000): #12000
        # print(obs)
        imageio.imsave(f"{args.s}/{i}.png", env.render())
        plt.close()
        labels.append(obs_to_label(obs))
        action = env.action_space.sample(obs)
        print(action.pddl_str())
        actions.append(action_order[action.pddl_str()])
        obs = env.step(action)[0]


    print(action_order)
    labels_tensor = torch.tensor(np.array(labels), dtype=torch.float32)
    actions_tensor = torch.tensor(np.array(actions))

    torch.save(labels_tensor, f"{args.s}/labels.pt")
    torch.save(actions_tensor, f"{args.s}/actions.pt")