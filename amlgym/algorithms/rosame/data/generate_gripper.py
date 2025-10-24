import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
import torch
import torchvision.datasets as datasets
from macq import generate, extract
import argparse
import os

mnist_dataset, target_index = None, None


def init_mnist():
    global mnist_dataset, target_index
    mnist_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=None)
    targets = mnist_dataset.targets
    target_index = {}
    for i in range(10):
        target_index[i] = np.argwhere(targets==i).flatten().tolist()


def state_to_img(state):
    # Turn a macq state to an image
    img = np.empty((grid_shape[0], grid_shape[1], 28, 28))
    
    room_available_loc = [list(range(num_balls)) for _ in range(len(rooms))]
    free_ball_loc = {}
    backgrounds = {(i, j) for i in range(grid_shape[0]) for j in range(grid_shape[1])}
    
    for i in range(len(rooms)):
        if state.fluents[all_fluents[f'(at-robby room {rooms[i]})']]:
            gripper_loc = 2*i
    
    for i in range(1, num_balls+1):
        ball_free = False
        for j in range(len(rooms)):
            if state.fluents[all_fluents[f'(at ball ball{i} room {rooms[j]})']]:
                loc = npr.choice(room_available_loc[j])
                img[2*j+1, loc] = np.asarray(mnist_dataset.__getitem__(npr.choice(target_index[i]))[0])
                free_ball_loc[f'ball{i}'] = (2*j+1, loc)
                room_available_loc[j].remove(loc)
                # Remove the location from background
                backgrounds.remove((2*j+1, loc))
                ball_free = True
                break
        
        if ball_free:
            continue
            
        for g in range(len(grippers)):
            if state.fluents[all_fluents[f'(carry ball ball{i} gripper {grippers[g]})']]:
                img[gripper_loc, g] = 255-np.asarray(mnist_dataset.__getitem__(npr.choice(target_index[i]))[0])
                # Remove the location from background
                backgrounds.remove((gripper_loc, g))
                break
                
    for g in range(len(grippers)):
        if state.fluents[all_fluents[f'(free gripper {grippers[g]})']]:
            img[gripper_loc, g] = 255-np.asarray(mnist_dataset.__getitem__(npr.choice(target_index[0]))[0])
            # Remove the location from background
            backgrounds.remove((gripper_loc, g))
            
    for i, j in backgrounds:
        img[i, j] = np.asarray(mnist_dataset.__getitem__(npr.choice(target_index[0]))[0])
        
    return img, (free_ball_loc, room_available_loc)


def get_next_img(current_img, meta, action):
    next_img = current_img.copy()
    free_ball_loc, room_available_loc = meta
    
    if action.name=='move':
        room_from = rooms.index(action.obj_params[0].name)
        room_to = rooms.index(action.obj_params[1].name)
        temp = next_img[room_from*2, list(range(len(grippers)))]
        next_img[room_from*2, list(range(len(grippers)))] = next_img[room_to*2, list(range(len(grippers)))]
        next_img[room_to*2, list(range(len(grippers)))] = temp
    elif action.name=='pick':
        room = rooms.index(action.obj_params[1].name)
        ball_loc = free_ball_loc[action.obj_params[0].name]
        room_loc = room*2
        gripper_loc = grippers.index(action.obj_params[2].name)
        temp = next_img[room_loc, gripper_loc].copy()
        next_img[room_loc, gripper_loc] = 255-next_img[ball_loc]
        next_img[ball_loc] = 255-temp
        del free_ball_loc[action.obj_params[0].name]
        room_available_loc[room].append(ball_loc[1])
    elif action.name=='drop':
        room = rooms.index(action.obj_params[1].name)
        ball_loc = (room*2+1, npr.choice(room_available_loc[room]))
        room_loc = room*2
        gripper_loc = grippers.index(action.obj_params[2].name)
        temp = next_img[room_loc, gripper_loc].copy()
        next_img[room_loc, gripper_loc] = 255-next_img[ball_loc]
        next_img[ball_loc] = 255-temp
        free_ball_loc[action.obj_params[0].name] = ball_loc
        room_available_loc[room].remove(ball_loc[1])
        
    return next_img, meta


def state_to_label(state):
    label = np.zeros(len(fluents))
    for f in state.fluents:
        label[fluents[f._serialize()]] = state.fluents[f]
    return label


def show_mnist_image(raw):
    plt.figure()
    digits = np.concatenate(np.concatenate(raw,axis=1), axis=1).astype(np.uint8)

    #img = Image.fromarray(255-board)
    plt.imshow(255-digits, cmap='gray')


def get_actions_and_props(balls, rooms, grippers):
    actions = [f'move room {room_from} room {room_to}'
               for room_from in rooms
               for room_to in rooms
               if room_from!=room_to]
    actions.extend([f'pick ball {ball} gripper {gripper} room {room}'
                    for ball in balls for gripper in grippers for room in rooms])
    actions.extend([f'drop ball {ball} gripper {gripper} room {room}'
                    for ball in balls for gripper in grippers for room in rooms])
    actions = {k: v for v, k in enumerate(actions)}

    fluents = [f'(at-robby room {room})' for room in rooms]
    fluents.extend([f'(at ball {ball} room {room})' for ball in balls for room in rooms])
    fluents.extend([f'(free gripper {gripper})' for gripper in grippers])
    fluents.extend([f'(carry ball {ball} gripper {gripper})' for ball in balls for gripper in grippers])
    fluents = {k: v for v, k in enumerate(fluents)}
    return actions, fluents



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", type=int, default=6, help="ball num")
    parser.add_argument("--rooms", action='store', type=str, nargs='*', default=["rooma", "roomb"])
    parser.add_argument("--grippers", action='store', type=str, nargs='*', default=["left", "right"])
    parser.add_argument("-t", type=int, default=1000, help="trace num")
    parser.add_argument("-l", type=int, default=5, help="trace length")
    parser.add_argument("--skip", type=int, default=1, help="skip between traces")
    parser.add_argument("-s", default="data", help="save address")
    parser.add_argument("--pddl_dom", default="/Users/omarwattad/Documents/Action Model - Research/rosame/data/pddl/gripper/domain2.pddl")
    parser.add_argument("--pddl_prob", default="/Users/omarwattad/Documents/Action Model - Research/rosame/data/pddl/gripper/prob01.pddl")
    parser.add_argument("--seed", type=int, default=8800)
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    npr.seed(args.seed)

    # Grid shape: 2*room_num, ball_num(>=2)
    grid_shape = (2*len(args.rooms), args.b)
    num_balls = args.b
    balls = [f'ball{i}' for i in range(1, num_balls+1)]
    rooms = args.rooms
    grippers = args.grippers
    save_to = args.s
    init_mnist()
    actions, fluents = get_actions_and_props(balls, rooms, grippers)

    trace = generate.pddl.VanillaSampling(dom=args.pddl_dom,
                                          prob=args.pddl_prob,
                                          plan_len = args.t*(args.l+args.skip), num_traces = 1).traces[0]
    all_fluents = {f._serialize():f for f in trace.fluents}
    traces_images = []
    traces_actions = []
    traces_labels = []

    for n in range(args.t):
        trace_images = []
        trace_actions = []
        trace_labels = []
        img, meta = state_to_img(trace.steps[n*(args.l+args.skip)].state)
        for step in range(n*(args.l+args.skip), n*(args.l+args.skip)+args.l):
            trace_images.append(img)
            trace_labels.append(state_to_label(trace.steps[step].state))
            # action parameter order may not be the same as our model
            action = trace.steps[step].action
            action_obj_params = sorted([o for o in action.obj_params], key=lambda o:o.obj_type)
            trace_actions.append(actions[f"{action.name} {' '.join([o.details()for o in action_obj_params])}"])
            img, meta = get_next_img(img, meta, trace.steps[step].action)

            # to debug: if traj. still not valid, implement and run this: val(domain, pre_state, action, next_state) --> true if the transition is valid (precond. satisfied, effects also)

        # Record final state label
        trace_labels.append(state_to_label(trace.steps[n*(args.l+args.skip)+args.l].state))
        
        traces_images.append(trace_images)
        traces_actions.append(trace_actions)
        traces_labels.append(trace_labels)

    traces_images_tensor = torch.tensor(np.array(traces_images))
    traces_actions_tensor = torch.tensor(np.array(traces_actions))
    traces_labels_tensor = torch.tensor(np.array(traces_labels), dtype=torch.float32)

    torch.save(traces_images_tensor, os.path.join(save_to, "features_img.pt"))
    torch.save(traces_actions_tensor, os.path.join(save_to, "actions.pt"))
    torch.save(traces_labels_tensor, os.path.join(save_to, "labels.pt"))