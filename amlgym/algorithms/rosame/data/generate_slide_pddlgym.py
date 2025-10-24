import pddlgym
import imageio
import numpy as np
import torch
import numpy.random as npr
import random
import argparse

tiles = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8']
positions = ['x1', 'x2', 'x3', 'y1', 'y2', 'y3']
action_order = [f'(move-up {tile} {pos1} {pos2} {pos3})' for pos1 in positions for pos2 in positions for pos3 in positions for tile in tiles
                if pos1!=pos2 and pos1!=pos3 and pos2!=pos3]
action_order.extend([f'(move-down {tile} {pos1} {pos2} {pos3})' for pos1 in positions for pos2 in positions for pos3 in positions  for tile in tiles
                if pos1!=pos2 and pos1!=pos3 and pos2!=pos3])
action_order.extend([f'(move-left {tile} {pos1} {pos2} {pos3})' for pos1 in positions for pos2 in positions for pos3 in positions for tile in tiles
                if pos1!=pos2 and pos1!=pos3 and pos2!=pos3])
action_order.extend([f'(move-right {tile} {pos1} {pos2} {pos3})' for pos1 in positions for pos2 in positions for pos3 in positions for tile in tiles
                if pos1!=pos2 and pos1!=pos3 and pos2!=pos3])
action_order = {k: v for v, k in enumerate(action_order)}
propositions = [f'(at {tile} {pos1} {pos2})' for pos1 in positions for pos2 in positions if pos1!=pos2 for tile in tiles]
propositions.extend([f'(blank {pos1} {pos2})'  for pos1 in positions for pos2 in positions if pos1!=pos2])
propositions.extend([f'(inc {pos1} {pos2})'  for pos1 in positions for pos2 in positions if pos1!=pos2])
propositions.extend([f'(dec {pos1} {pos2})'  for pos1 in positions for pos2 in positions if pos1!=pos2])
propositions = {k: v for v, k in enumerate(propositions)}
print(propositions)

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
    env = pddlgym.make("PDDLEnvSlidetile-v0", operators_as_actions=True, dynamic_action_space=True)
    obs, info = env.reset()

    labels = []
    actions = []

    for i in range(50): #5500
        img = env.render()
        imageio.imsave(f"{args.s}/{i}.png", img)
        del img
        labels.append(obs_to_label(obs))
        action = env.action_space.sample(obs)
        actions.append(action_order[action.pddl_str()])
        obs = env.step(action)[0]

    labels_tensor = torch.tensor(np.array(labels), dtype=torch.float32)
    actions_tensor = torch.tensor(np.array(actions))

    torch.save(labels_tensor, f"{args.s}/labels.pt")
    torch.save(actions_tensor, f"{args.s}/actions.pt")