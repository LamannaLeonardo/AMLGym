from models.rosame import *
from models.cv_gridworld import *
from data.dataset import *

import torch
import torch.optim as optim

from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms
import torchvision

import random
import argparse
import os


def get_domain_model(domain, device):
    domain_model = load_model(
        os.path.join(
            os.path.dirname(__file__), "models/domains", domain, "domain_model.json"
        ),
        device,
    )
    domain_model.ground_from_json(
        os.path.join(
            os.path.dirname(__file__), "models/domains", domain, "objects.json"
        )
    )
    return domain_model


@torch.no_grad()
def compute_correctness(pred_flat, target_flat):
    """
    Expect input in the shape of (batch_size, trace_len, prop_num)
    """
    trace_len = pred_flat.shape[1]
    prop_num = pred_flat.shape[2]

    pred = pred_flat.reshape(-1, prop_num)
    target = target_flat.reshape(-1, prop_num)
    pred = (pred > 0.5).float()

    correct = torch.sum(torch.isclose(pred, target))

    return float(correct) / prop_num / trace_len


def run(
    epoch,
    cv_model,
    domain_model,
    optimizer,
    data_loader,
    gamma,
    lambda_,
    device,
    to_train=False,
):
    loss_final, acc_running, data_num = 0, 0, 0

    if to_train:
        cv_model.train()  # Set model to training mode
    else:
        cv_model.eval()  # Set model to evaluate mode

    for i, (data, label, action) in enumerate(data_loader):
        data = data.to(device)
        label = label.to(device)
        action = action.to(device)
        trace_len = action.shape[1]
        flattened_data = data.flatten(start_dim=0, end_dim=1)

        with torch.set_grad_enabled(to_train):
            preds = cv_model(flattened_data)
            loss = 0
            # Domain model inference loss
            precon, addeff, deleff = domain_model.build(action.flatten())
            domain_preds = preds * (1 - deleff) + (1 - preds) * addeff
            # domain_preds = 1 - (1-preds*(1-deleff)) * (1-(1-preds)*addeff)
            validity_constraint = (1 - preds) * (precon)
            preds = preds.unflatten(0, (-1, trace_len))
            domain_preds = domain_preds.unflatten(0, (-1, trace_len))
            loss += F.mse_loss(domain_preds[:, :-1], preds[:, 1:], reduction="sum")
            loss += gamma * F.mse_loss(
                domain_preds[:, -1], label[:, -1], reduction="sum"
            )
            loss += F.mse_loss(
                validity_constraint,
                torch.zeros(
                    validity_constraint.shape,
                    dtype=validity_constraint.dtype,
                    device=device,
                ),
                reduction="sum",
            )
            # Add a prior
            loss += lambda_ * F.mse_loss(
                precon,
                torch.ones(precon.shape, dtype=precon.dtype, device=device),
                reduction="sum",
            )
            if to_train:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        loss_final += loss.item()
        acc_running += compute_correctness(preds.data, label[:, :-1])
        data_num += preds.data.shape[0]

    if to_train:
        print(
            "Epoch {} TRAINING SET RESULTS: Average loss: {:.4f} Acc: {:.4f}".format(
                epoch, loss_final, acc_running / data_num
            )
        )
    else:
        print(
            "Epoch {} TESTING SET RESULTS: Average loss: {:.4f} Acc: {:.4f}".format(
                epoch, loss_final, acc_running / data_num
            )
        )

    torch.cuda.empty_cache()


if __name__ == "__main__":
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--domain",
        choices=[
            "grid_blocks",
            "grid_gripper",
            "grid_logistics",
            "synth_blocks",
            "synth_hanoi",
            "synth_8-puzzle",
        ],
    )
    parser.add_argument("--gamma", type=float, default=10)
    parser.add_argument("--lambda_", type=float, default=0.2)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--lr_schema", type=float, default=1e-3)
    parser.add_argument("--lr_gridcv_grid", type=float, default=1e-5)
    parser.add_argument("--lr_gridcv_mlp", type=float, default=1e-3)
    parser.add_argument("--lr_synthcv", type=float, default=1e-3)
    parser.add_argument("--batch_size", type=int, default=128)
    parser.add_argument("--dataset_pth")
    parser.add_argument("--trace_num", type=int)
    parser.add_argument("--trace_len", type=int)
    parser.add_argument("--block_num", type=int, default=5)
    parser.add_argument("--ball_num", type=int, default=6)
    parser.add_argument("--seed", type=int, default=8800)
    parser.add_argument("-s", default="model.pth", help="save address")
    args = parser.parse_args()

    random.seed(args.seed)
    torch.manual_seed(args.seed)

    # Set up domain model and cv model.
    # Gather experiment data.
    if args.domain == "grid_blocks":
        block_num = args.block_num
        domain_model = get_domain_model("blocks", device)
        cv_model = CVGrid(
            GridConv(digit_class_num=block_num + 1, input_channel=1),
            block_dim=(block_num + 1, block_num),
            block_size=28,  # MNIST images are 28x28
            hidden_dim=128,
            digit_class_num=block_num + 1,
            prop_dim=len(domain_model.propositions),
        )
        data_transform = RearrangeColumn(block_num)
    elif args.domain == "grid_gripper":
        ball_num = args.ball_num
        domain_model = get_domain_model("gripper", device)
        cv_model = CVGrid(
            GridConv(digit_class_num=(ball_num + 1) * 2, input_channel=1),
            block_dim=(4, ball_num),
            block_size=28,  # MNIST images are 28x28
            hidden_dim=128,
            digit_class_num=(ball_num + 1) * 2,
            prop_dim=len(domain_model.propositions),
        )
        data_transform = RearrangeBalls(ball_num)
    elif args.domain == "grid_logistics":
        domain_model = get_domain_model("logistics", device)
        digit_class_num = 35
        cv_model = CVGrid(
            GridConv(digit_class_num=digit_class_num, input_channel=3),
            block_dim=(6, 6),
            block_size=28,  # MNIST images are 28x28
            hidden_dim=256,
            digit_class_num=digit_class_num,
            prop_dim=len(domain_model.propositions),
        )
        data_transform = RearrangeItems()
    elif args.domain == "synth_blocks":
        domain_model = get_domain_model("blocks", device)
        cv_model = torchvision.models.resnet18()
        cv_model.fc = nn.Sequential(
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, len(domain_model.propositions)),
        )
        data_transform = transforms.Compose(
            [
                transforms.Resize(64),
                transforms.RandomHorizontalFlip(0.5),
            ]
        )
    elif args.domain == "synth_hanoi":
        domain_model = get_domain_model("hanoi", device)
        cv_model = torchvision.models.resnet18()
        cv_model.fc = nn.Sequential(
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, len(domain_model.propositions)),
        )
        data_transform = transforms.Resize(64)
    elif args.domain == "synth_8-puzzle":
        domain_model = get_domain_model("8-puzzle", device)
        cv_model = torchvision.models.resnet18()
        cv_model.fc = nn.Sequential(
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, len(domain_model.propositions)),
        )
        data_transform = transforms.Resize(64)

    domain_model = domain_model.to(device)
    cv_model = cv_model.to(device)

    # Get Dataset
    if args.domain.startswith("grid"):
        dataset = GridDataset(
            args.dataset_pth, args.trace_len, transforms=data_transform
        )
        training_size = int(args.trace_num * 0.9)
        trainset, testset, _ = random_split(
            dataset,
            [
                training_size,
                args.trace_num - training_size,
                len(dataset) - args.trace_num,
            ],
        )
    else:
        skip = "break_symmetry" if args.domain == "synth_blocks" else 1
        dataset = SynthDataset(
            args.dataset_pth, args.trace_len, skip, transforms=data_transform
        )
        trainset, testset, _ = random_split(
            dataset, [args.trace_num, 100, len(dataset) - args.trace_num - 100]
        )
    train_loader = DataLoader(trainset, args.batch_size, shuffle=True)
    test_loader = DataLoader(testset, args.batch_size, shuffle=True)

    # Create optimizer
    parameters = []
    for schema in domain_model.action_schemas:
        parameters.append({"params": schema.parameters(), "lr": args.lr_schema})
    if args.domain.startswith("grid"):
        parameters.extend(
            [
                {"params": cv_model.mlp.parameters(), "lr": args.lr_gridcv_mlp},
                {
                    "params": cv_model.grid_convnet.parameters(),
                    "lr": args.lr_gridcv_grid,
                },
            ]
        )
    else:
        parameters.extend([{"params": cv_model.parameters(), "lr": args.lr_synthcv}])
    optimizer = optim.Adam(parameters)

    print("---------------------------------")
    print("Domain:", args.domain)
    print("Gamma:", args.gamma)
    print("Lambda:", args.lambda_)
    print("Trace Num:", args.trace_num)
    print("Trace Len:", args.trace_len)
    for epoch in range(args.epochs):
        run(
            epoch,
            cv_model,
            domain_model,
            optimizer,
            train_loader,
            args.gamma,
            args.lambda_,
            device,
            True,
        )
        run(
            epoch,
            cv_model,
            domain_model,
            optimizer,
            test_loader,
            args.gamma,
            args.lambda_,
            device,
            False,
        )
    for schema in domain_model.action_schemas:
        schema.pretty_print()
        print()

    torch.save(
        {"domain_model": domain_model.state_dict(), "cv_model": cv_model.state_dict()},
        args.s,
    )
