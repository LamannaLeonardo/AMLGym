import numpy as np
import numpy.random as npr
import random
import torch
import torchvision
import matplotlib.pyplot as plt
from macq import generate, extract
import argparse
import os


eminst_dataset, target_index = None, None
palette = {
    'black': np.array([[[0]],[[0]],[[0]]]),
    'red': np.array([[[255]],[[0]],[[0]]])/255,
    'lime': np.array([[[0]],[[255]],[[0]]])/255,
    'blue': np.array([[[0]],[[0]],[[255]]])/255,
    'yellow': np.array([[[255]],[[255]],[[0]]])/255,
    'cyan': np.array([[[0]],[[255]],[[255]]])/255,
    'magenta': np.array([[[255]],[[0]],[[255]]])/255,
}


def init_mnist():
    global eminst_dataset, target_index
    eminst_dataset = torchvision.datasets.EMNIST(root='./data',
                                                 split='balanced',
                                                 train=True,
                                                 download=True,
                                                 transform=torchvision.transforms.Compose([
                                                     lambda img: torchvision.transforms.functional.rotate(img, -90),
                                                     lambda img: torchvision.transforms.functional.hflip(img),
                                                 ]))
    targets = eminst_dataset.targets
    target_index = {}
    # 10 is 'A' for airplane and 29 is 'T' for truck
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 29]:
      target_index[i] = np.argwhere(targets==i).flatten().tolist()


def get_class_img(cls, color):
    return np.asarray(eminst_dataset.__getitem__(npr.choice(target_index[cls]))[0])*(1-palette[color])


def state_to_img(state):
    # Turn a macq state to an image
    img = np.empty((grid_shape[0], grid_shape[1], 3, 28, 28))
    
    backgrounds = {(i, j) for i in range(grid_shape[0]) for j in range(grid_shape[1])}
    
    package_images = {}
    # vehicle_locations map each truck/airplane to a location (e.g. city1-2)
    vehicle_locations = {}
    # item_loc map each package/truck/airplane to an (i, j)
    item_loc ={}
    free_loc = {loc:[(r, c) for r in range(i*3, i*3+3) for c in range(3)]
                for i, loc in enumerate(locations)}
    free_loc.update({a:[(r, c) for r in range(i*3, i*3+3) for c in range(3, 6)]
                     for i, a in enumerate(airports)})
    # Record which packages each truck/plane carries
    vehicle_packages = {v:[] for v in trucks+planes}
    
    for truck in trucks:
        # Find truck's location and assign
        for loc in city_locations[truck_city[truck]]:
            if loc in airports:
                fluent_string = f'(at truck {truck} airport {loc})'
            else:
                fluent_string = f'(at truck {truck} location {loc})'
            if state.fluents[all_fluents[fluent_string]]:
                vehicle_locations[truck] = loc
                assigned_pos = random.choice(free_loc[loc])
                item_loc[truck] = assigned_pos
                free_loc[loc].remove(assigned_pos)
                img[assigned_pos] = get_class_img(29, vehicle_color[truck])
                backgrounds.remove(assigned_pos)
                break
                
    for plane in planes:
        # Find plane's location and assign
        # Plane can only be at airports
        for airport in airports:
            if state.fluents[all_fluents[f'(at airplane {plane} airport {airport})']]:
                vehicle_locations[plane] = airport
                assigned_pos = random.choice(free_loc[airport])
                item_loc[plane] = assigned_pos
                free_loc[airport].remove(assigned_pos)
                img[assigned_pos] = get_class_img(10, vehicle_color[plane])
                backgrounds.remove(assigned_pos)
                break
                
    for i, package in enumerate(packages, 1):
        # Give package an image
        # We remember this image as the original black image for package
        # As it is hard to recover black image from the color image
        package_images[package] = get_class_img(i, 'black')
        # If package is free
        for loc in locations+airports:
            if loc in airports:
                fluent_string = f'(at obj {package} airport {loc})'
            else:
                fluent_string = f'(at obj {package} location {loc})'
            if state.fluents[all_fluents[fluent_string]]:
                assigned_pos = random.choice(free_loc[loc])
                item_loc[package] = assigned_pos
                free_loc[loc].remove(assigned_pos)
                img[assigned_pos] = package_images[package]
                backgrounds.remove(assigned_pos)
                break
        # If package is in a truck or plane
        for vehicle in trucks+planes:
            if vehicle in trucks:
                fluent_string = f'(in obj {package} truck {vehicle})'
            else:
                fluent_string = f'(in obj {package} airplane {vehicle})'
            if state.fluents[all_fluents[fluent_string]]:
                vehicle_packages[vehicle].append(package)
                assigned_pos = random.choice(free_loc[vehicle_locations[vehicle]])
                item_loc[package] = assigned_pos
                free_loc[vehicle_locations[vehicle]].remove(assigned_pos)
                packge_img_wrt_vehicle = package_images[package] * (1-palette[vehicle_color[vehicle]])
                img[assigned_pos] = packge_img_wrt_vehicle
                backgrounds.remove(assigned_pos)
                break
                
    for background in backgrounds:
        img[background] = get_class_img(0, 'black')
                
    return img, (package_images, item_loc, free_loc, vehicle_packages)


def get_next_img(current_img, meta, action):
    next_img = current_img.copy()
    package_images, item_loc, free_loc, vehicle_packages = meta
    
    if action.name=='load-truck' or action.name=='load-airplane':
        # Color the package with truck/airplane color
        package = action.obj_params[0].name
        vehicle = action.obj_params[1].name
        vehicle_packages[vehicle].append(package)
        next_img[item_loc[package]] = package_images[package] * (1-palette[vehicle_color[vehicle]])
    elif action.name=='unload-truck' or action.name=='unload-airplane':
        # Color the package black (replace with the saved original image, easier)
        package = action.obj_params[0].name
        vehicle = action.obj_params[1].name
        vehicle_packages[vehicle].remove(package)
        next_img[item_loc[package]] = package_images[package]
    elif action.name=='drive-truck' or action.name=='fly-airplane':
        # Move the truck/airplane, together with all packages in it
        vehicle = action.obj_params[0].name
        loc_from = action.obj_params[1].name
        loc_to = action.obj_params[2].name
        vehicle_pos_from = item_loc[vehicle]
        vehicle_pos_to = random.choice(free_loc[loc_to])
        free_loc[loc_from].append(vehicle_pos_from)
        free_loc[loc_to].remove(vehicle_pos_to)
        item_loc[vehicle] = vehicle_pos_to
        # Move vehicle
        temp = next_img[vehicle_pos_to].copy()
        next_img[vehicle_pos_to] = next_img[vehicle_pos_from]
        next_img[vehicle_pos_from] = temp
        # Move all the packages the vehicle carries
        for package in vehicle_packages[vehicle]:
            package_pos_from = item_loc[package]
            package_pos_to = random.choice(free_loc[loc_to])
            free_loc[loc_from].append(package_pos_from)
            free_loc[loc_to].remove(package_pos_to)
            item_loc[package] = package_pos_to
            temp = next_img[package_pos_to].copy()
            next_img[package_pos_to] = next_img[package_pos_from]
            next_img[package_pos_from] = temp
            
    return next_img, meta


def show_mnist_image(raw):
    plt.figure()
    img_shown = np.transpose(raw, (0, 1, 3, 4, 2))
    img_shown = np.concatenate(np.concatenate(img_shown,axis=1), axis=1).astype(np.uint8)

    plt.imshow(255-img_shown)


def get_actions_and_props(packages, trucks, planes, locations, airports, cities):
    actions = [f"load-truck location {loc} obj {package} truck {truck}"
    for loc in locations+airports for package in packages for truck in trucks]
    actions.extend([f"load-airplane airplane {plane} airport {airport} obj {package}"
        for plane in planes for airport in airports for package in packages])
    actions.extend([f"unload-truck location {loc} obj {package} truck {truck}"
        for loc in locations+airports for package in packages for truck in trucks])
    actions.extend([f"unload-airplane airplane {plane} airport {airport} obj {package}"
        for plane in planes for airport in airports for package in packages])
    actions.extend([f"drive-truck city {city} location {loc1} location {loc2} truck {truck}"
        for city in cities for loc1 in locations+airports for loc2 in locations+airports if loc1!=loc2 for truck in trucks])
    actions.extend([f"fly-airplane airplane {plane} airport {airport1} airport {airport2}"
        for plane in planes for airport1 in airports for airport2 in airports if airport1!= airport2])
    actions = {k: v for v, k in enumerate(actions)}
    propositions = [f"at location {loc} movable {movable}"
    for loc in locations+airports for movable in packages+trucks+planes]
    propositions.extend([f"in obj {package} transport {transport}"
        for package in packages for transport in trucks+planes])
    propositions.extend([f"in-city city {city} location {loc}"
        for city in cities for loc in locations+airports])
    propositions = {k: v for v, k in enumerate(propositions)}
    return actions, propositions


def state_to_label(state):
    label = np.zeros(len(propositions))
    for f in state.fluents:
        serialized_list = f._serialize()[1:-1].split(' ')
        if f.name=='at':
            f_string = f'at location {serialized_list[4]} movable {serialized_list[2]}'
        elif f.name=='in':
            f_string = f'in obj {serialized_list[2]} transport {serialized_list[4]}'
        elif f.name=='in-city':
            f_string = f'in-city city {serialized_list[4]} location {serialized_list[2]}'
        label[propositions[f_string]] = state.fluents[f]
    # macq does not recognise static propositions as fluents
    label[propositions["in-city city city1 location city1-1"]] = 1
    label[propositions["in-city city city1 location city1-2"]] = 1
    label[propositions["in-city city city2 location city2-1"]] = 1
    label[propositions["in-city city city2 location city2-2"]] = 1
    return label


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", type=int, default=3000, help="trace num")
    parser.add_argument("-l", type=int, default=10, help="trace length")
    parser.add_argument("--num_packages", type=int, default=6, help="number of packages")
    parser.add_argument("--skip", type=int, default=1, help="skip between traces")
    parser.add_argument("-s", default="data", help="save address")
    parser.add_argument("--pddl_dom", default="data/pddl/logistics/domain.pddl")
    parser.add_argument("--pddl_prob", default="data/pddl/logistics/prob01.pddl")
    parser.add_argument("--seed", type=int, default=8800)
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    random.seed(args.seed)
    npr.seed(args.seed)

    # Hardcode for now
    grid_shape = (6, 6)
    trucks = ['truckred', 'trucklime']
    planes = ['planeblue', 'planeyellow']
    city_locations = {'city1':['city1-1', 'city1-2'],
                      'city2':['city2-1', 'city2-2']}
    truck_city = {'truckred':'city1', 'trucklime':'city2'}
    locations = ['city1-1', 'city2-1']
    airports = ['city1-2', 'city2-2']
    num_packages = args.num_packages
    packages = [f'package{i}' for i in range(1, num_packages+1)]

    vehicle_color = {f'truck{c}':c for c in ['red', 'lime']}
    vehicle_color.update({f'plane{c}':c for c in ['blue', 'yellow']})

    trace = generate.pddl.VanillaSampling(dom=args.pddl_dom,
                                      prob=args.pddl_prob,
                                      plan_len = args.t*(args.l+args.skip), num_traces = 1, max_time=120).traces[0]
    all_fluents = {f._serialize():f for f in trace.fluents}

    init_mnist()
    actions, propositions = get_actions_and_props(packages, trucks, planes, locations, airports, list(city_locations.keys()))

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
            action_obj_params = []
            for o in action.obj_params:
                if 'airplane' not in action.name and o.obj_type=='airport':
                    o.obj_type = 'location'
                action_obj_params.append(o)
            action_obj_params = sorted(action_obj_params, key=lambda o:o.obj_type)
            trace_actions.append(actions[f"{action.name} {' '.join([o.details()for o in action_obj_params])}"])
            img, meta = get_next_img(img, meta, trace.steps[step].action)
        
        # Record final state label
        trace_labels.append(state_to_label(trace.steps[n*(args.l+args.skip)+args.l].state))
        
        traces_images.append(trace_images)
        traces_actions.append(trace_actions)
        traces_labels.append(trace_labels)


    traces_images_tensor = torch.tensor(np.array(traces_images), dtype=torch.float32)
    traces_actions_tensor = torch.tensor(np.array(traces_actions))
    traces_labels_tensor = torch.tensor(np.array(traces_labels), dtype=torch.float32)

    torch.save(traces_images_tensor, os.path.join(args.s, "features_img.pt"))
    torch.save(traces_actions_tensor, os.path.join(args.s, "actions.pt"))
    torch.save(traces_labels_tensor, os.path.join(args.s, "labels.pt"))