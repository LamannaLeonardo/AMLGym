from subprocess import Popen, PIPE
import numpy as np
import numpy.random as npr
import random
import torch
import matplotlib.pyplot as plt
import torchvision.datasets as datasets
import math
import argparse
import os


obj_num = 5
state_num = 800
mnist_dataset, target_index = None, None


def const_init_states(generator_addr):
    init_states = []

    p = Popen(f"{generator_addr} -n {obj_num} -p {state_num}", stdout=PIPE, shell=True)
    line = p.stdout.readline()
    for _ in range(state_num):
        init_states.append(p.stdout.readline().decode("utf-8")[:-1])
        p.stdout.readline()
    return init_states


def init_mnist():
    global mnist_dataset, target_index
    mnist_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=None)
    targets = mnist_dataset.targets
    target_index = {}
    for i in range(10):
        target_index[i] = np.argwhere(targets==i).flatten().tolist()


'''
Maintain 3 things: a PDDL model, an numpy array representing image and the current image
'''


def add_to_arr(block, arr, grounds, remains, state_str):
    below = int(state_str[2*block-1])
    if below==0:
        ground = random.choice(grounds)
        grounds.remove(ground)
        arr[obj_num, ground] = block
    else:
        if below in remains:
            remains.remove(below)
            add_to_arr(below, arr, grounds, remains, state_str)
        pos = np.where(arr==below)
        arr[pos[0]-1, pos[1]] = block


def convert_str_arr(state_str):
    arr = np.zeros((obj_num+1, obj_num))
    grounds = list(range(obj_num))
    remains = list(range(1, obj_num+1))
    while remains:
        block = remains.pop(0)
        add_to_arr(block, arr, grounds, remains, state_str)
    return arr


def convert_str_model(state_str):
    model = {f'clear {i}' for i in range(1, obj_num+1)}
    model.add("arm-empty")
    for block in range(1, obj_num+1):
        below = int(state_str[2*block-1])
        if below == 0:
            model.add(f'on-table {block}')
        else:
            model.add(f'on {block} {below}')
            model.remove(f'clear {below}')
    return model

def get_image_from_array(arr):
    '''
    Randomly generate corresponding image
    arr should be a (obj_num+1, obj_num) numpy array (with top row for arm)
    Return a [obj_num+1, obj_num, 28, 28] shape array
    '''
    result = [[] for i in range(obj_num+1)]
    for i in range(obj_num+1):
        for j in range(obj_num):
            num = arr[i][j]
            result[i].append(np.asarray(mnist_dataset.__getitem__(npr.choice(target_index[num]))[0]))
    return np.array(result)


'''
Random Action, Get Next Model, Array and Image
'''


pickup = {
    "precondition": lambda obj: {f'clear {obj}', f'on-table {obj}', 'arm-empty'},
    "add_eff": lambda obj: {f'holding {obj}'},
    "del_eff": lambda obj: {f'clear {obj}', f'on-table {obj}', 'arm-empty'}
}

putdown = {
    "precondition": lambda obj: {f'holding {obj}'},
    "add_eff": lambda obj: {f'clear {obj}', f'on-table {obj}', 'arm-empty'},
    "del_eff": lambda obj: {f'holding {obj}'}
}

stack = {
    "precondition": lambda obj, underobj: {f'clear {underobj}', f'holding {obj}'},
    "add_eff": lambda obj, underobj: {f'clear {obj}', f'on {obj} {underobj}', 'arm-empty'},
    "del_eff": lambda obj, underobj: {f'clear {underobj}', f'holding {obj}'}
}

unstack = {
    "precondition": lambda obj, underobj: {f'clear {obj}', f'on {obj} {underobj}', 'arm-empty'},
    "add_eff": lambda obj, underobj: {f'clear {underobj}', f'holding {obj}'},
    "del_eff": lambda obj, underobj: {f'clear {obj}', f'on {obj} {underobj}', 'arm-empty'},
}


def random_action(current_model):
    actions = []
    for block in range(1, obj_num+1):
        if pickup["precondition"](block).issubset(current_model):
            actions.append(("pickup", block))
        if putdown["precondition"](block).issubset(current_model):
            actions.append(("putdown", block))
        for below in range(1, obj_num+1):
            if stack["precondition"](block, below).issubset(current_model):
                actions.append(("stack", block, below))
            if unstack["precondition"](block, below).issubset(current_model):
                actions.append(("unstack", block, below))
    return random.choice(actions)


def get_next_model(current_model, action):
    if action[0]=='pickup':
        next_model = (current_model-pickup['del_eff'](action[1])).union(pickup['add_eff'](action[1]))
    elif action[0]=='putdown':
        next_model = (current_model-putdown['del_eff'](action[1])).union(putdown['add_eff'](action[1]))
    elif action[0]=='stack':
        next_model = (current_model-stack['del_eff'](action[1], action[2])).union(stack['add_eff'](action[1], action[2]))
    elif action[0]=='unstack':
        next_model = (current_model - unstack['del_eff'](action[1], action[2])).union(unstack['add_eff'](action[1], action[2]))
    return next_model


def get_next_arr_img(current_arr, current_img, action):
    next_arr = current_arr.copy()
    next_img = current_img.copy()

    # Arm position is in the middle of the top row
    arm_pos = (0, math.floor(obj_num/2))
    random_zero = np.asarray(mnist_dataset.__getitem__(npr.choice(target_index[0]))[0])
    block_pos = np.where(current_arr==action[1])

    if action[0]=='pickup' or action[0]=='unstack':
        next_arr[arm_pos[0], arm_pos[1]] = action[1]
        next_arr[block_pos[0], block_pos[1]]=0
        next_img[arm_pos[0], arm_pos[1]] = next_img[block_pos[0], block_pos[1]]
        next_img[block_pos[0], block_pos[1]] = random_zero
    elif action[0]=='stack':
        below_pos = np.where(current_arr==action[2])
        next_arr[below_pos[0]-1, below_pos[1]] = action[1]
        next_arr[arm_pos[0], arm_pos[1]] = 0
        next_img[below_pos[0]-1, below_pos[1]] = next_img[arm_pos[0], arm_pos[1]]
        next_img[arm_pos[0], arm_pos[1]] = random_zero
    elif action[0]=='putdown':
        ground = np.random.choice(np.where(current_arr[-1]==0)[0])
        next_arr[obj_num, ground] = action[1]
        next_arr[arm_pos[0], arm_pos[1]] = 0
        next_img[obj_num, ground] = next_img[arm_pos[0], arm_pos[1]]
        next_img[arm_pos[0], arm_pos[1]] = random_zero

    return next_arr, next_img


def show_mnist_image(raw):
    plt.figure()
    digits = np.concatenate(np.concatenate(raw,axis=1), axis=1).astype(np.uint8)
    plt.imshow(255-digits, cmap='gray')


'''
Create Dataset
'''


def get_actions_and_props():
    actions = [f'pickup {block}' for block in range(1, obj_num+1)]
    actions.extend([f'putdown {block}' for block in range(1, obj_num+1)])
    actions.extend([f'stack {block} {below}' for block in range (1, obj_num+1) for below in range(1, obj_num+1) if block!=below])
    actions.extend([f'unstack {block} {below}' for block in range (1, obj_num+1) for below in range(1, obj_num+1) if block!=below])
    actions = {k: v for v, k in enumerate(actions)}
    propositions = ['arm-empty']
    propositions.extend([f'clear {block}' for block in range(1, obj_num+1)])
    propositions.extend([f'on-table {block}' for block in range(1, obj_num+1)])
    propositions.extend([f'holding {block}' for block in range(1, obj_num+1)])
    propositions.extend([f'on {block1} {block2}' for block1 in range(1, obj_num+1) for block2 in range(1, obj_num+1) if block1!=block2])
    propositions = {k: v for v, k in enumerate(propositions)}
    return actions, propositions


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="-o objectnum, -t trace_num, -l trace_length, -s save_addr")
    parser.add_argument("-o", type=int, default=5, help="object num")
    parser.add_argument("-t", type=int, default=800, help="trace num")
    parser.add_argument("-l", type=int, default=10, help="trace length")
    parser.add_argument("-s", default="data", help="save address")
    parser.add_argument("-g", default="blocks-world-generator-and-planner/bbwstates_src/bbwstates", help="initial state generator")
    parser.add_argument("--seed", type=int, default=8800)
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    random.seed(args.seed)
    npr.seed(args.seed)

    obj_num = args.o
    state_num = args.t
    step_num = args.l
    save_to = args.s
    generator_addr = args.g

    actions, propositions = get_actions_and_props()

    features_img = []
    labels = []
    executed_actions = []

    init_states = const_init_states(generator_addr)
    init_mnist()

    for init_state in init_states:
        print(init_states)
        model = convert_str_model(init_state)
        arr = convert_str_arr(init_state)
        img = get_image_from_array(arr)
        # Randomly break data symmetry
        if random.random()>0.5:
            action = random_action(model)
            model = get_next_model(model, action)
            arr, img = get_next_arr_img(arr, img, action)

        feature = []
        label = []
        executed_action = []
        for i in range(step_num):
            # Record current state img
            feature.append(img)
            # Record current state label
            state_label = np.zeros(len(propositions))
            for p in model:
                state_label[propositions[p]] = 1
            label.append(state_label)
            # Select a random action
            action = random_action(model)
            # Record the action
            executed_action.append(actions[' '.join(map(str, action))])
            # Execute the action
            model = get_next_model(model, action)
            # Get next state
            arr, img = get_next_arr_img(arr, img, action)

        # Record final state label
        state_label = np.zeros(len(propositions))
        for p in model:
            state_label[propositions[p]] = 1
        label.append(state_label)

        features_img.append(feature)
        labels.append(label)
        executed_actions.append(executed_action)

    features_img_tensor = torch.tensor(np.array(features_img))
    labels_tensor = torch.tensor(np.array(labels), dtype=torch.float32)
    actions_tensor = torch.tensor(np.array(executed_actions))

    torch.save(features_img_tensor, os.path.join(save_to, "features_img.pt"))
    torch.save(labels_tensor, os.path.join(save_to, "labels.pt"))
    torch.save(actions_tensor, os.path.join(save_to, "actions.pt"))
