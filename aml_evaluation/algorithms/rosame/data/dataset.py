import torch
from torch.utils.data import Dataset
from torchvision import transforms
import torchvision
import random


class RearrangeColumn(object):
    def __init__(self, column_num):
        self.column_num = column_num

    def __call__(self, img):
        idx = torch.randperm(self.column_num)
        return torch.cat((img[:, [0]], img[:, 1:, idx]), 1)


class RearrangeBalls(object):
    def __init__(self, column_num):
        self.column_num = column_num

    def __call__(self, img):
        # img is steps * row * column * 28 * 28
        idx1 = torch.randperm(self.column_num)
        idx2 = torch.randperm(self.column_num)
        return torch.cat(
            (
                img[:, [0]],
                img[:, [1], idx1].unsqueeze(1),
                img[:, [2]],
                img[:, [3], idx2].unsqueeze(1),
            ),
            1,
        )


class RearrangeItems(object):
    def __call__(self, img):
        # img is steps * row * column * 3 * 28 * 28
        indices = [
            [
                [
                    (r, c)
                    for r in range(i * 3, i * 3 + 3)
                    for c in range(j * 3, j * 3 + 3)
                ]
                for j in range(2)
            ]
            for i in range(2)
        ]
        for i in range(2):
            for j in range(2):
                random.shuffle(indices[i][j])
        rows = []
        columns = []
        for r in range(6):
            for c in range(6):
                idx = indices[int(r / 3)][int(c / 3)].pop(0)
                rows.append(idx[0])
                columns.append(idx[1])
        return img[:, rows, columns, :, :, :].unflatten(1, (6, 6))


class GridDataset(Dataset):
    def __init__(self, dataset_path, step_length, transforms=None):
        self.dataset_path = dataset_path
        self.step_length = step_length
        self.transforms = transforms

        with open(f"{dataset_path}/features_img.pt", "rb") as f:
            self.images = torch.load(f)
            if self.images.dim() == 6:
                self.images = self.images.unsqueeze(4).float()
            else:
                self.images = self.images.float()
        with open(f"{dataset_path}/labels.pt", "rb") as f:
            self.labels = torch.load(f)
        with open(f"{dataset_path}/actions.pt", "rb") as f:
            self.actions = torch.load(f)

        self.images = self.images[:, :self.step_length]
        self.labels = self.labels[:, :self.step_length+1]
        self.actions = self.actions[:, :self.step_length]

    def __getitem__(self, index):
        img = self.images[index]
        label = self.labels[index]
        action = self.actions[index]

        if self.transforms is not None:
            img = self.transforms(img)
        return img, label, action

    def __len__(self):
        return len(self.images)


class SynthDataset(Dataset):
    def __init__(self, dataset_path, step_length, skip=1, transforms=None):
        self.dataset_path = dataset_path
        self.step_length = step_length
        self.transforms = transforms

        if skip == "break_symmetry":
            # Break symmetry based on whether the trace length is even or odd
            # Always skip at least one state
            self.skip = 3 - self.step_length % 2
        else:
            self.skip = skip

        with open(f"{dataset_path}/labels.pt", "rb") as f:
            self.labels = torch.load(f)
        with open(f"{dataset_path}/actions.pt", "rb") as f:
            self.actions = torch.load(f)

    def __getname__(self, idx):
        return f"{self.dataset_path}/{idx}.png"

    def __len__(self):
        return int(self.actions.shape[0] / (self.step_length + self.skip))

    def __getitem__(self, idx):
        # For some reason we failed to save the first 10 images
        starting_idx = idx * (self.step_length + self.skip)
        images = [
            torchvision.io.read_image(
                self.__getname__(starting_idx + i),
                mode=torchvision.io.ImageReadMode.RGB,
            )
            for i in range(self.step_length)
        ]
        images = torch.stack(images, dim=0)
        images = images.float()
        labels = self.labels[starting_idx : starting_idx + self.step_length + 1]
        actions = self.actions[starting_idx : starting_idx + self.step_length]

        if self.transforms:
            images = self.transforms(images)

        return images, labels, actions