import argparse
import torch
from pathlib import Path
from utils.utils import *
from torch.utils.data import DataLoader


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--content_dir",
        type=str,
        default="content_data",
        help="Path to content images"
    )

    parser.add_argument(
        "--style_dir",
        type=str,
        default="style_data",
        help="Path to style images"
    )

    parser.add_argument(
        "--vgg",
        type=str,
        default="vgg_normalised.pth",
        help="Path to VGG model"
    )

    parser.add_argument(
        "--experiment_dir",
        type=str,
        default="experiment1",
        help="Experiment name"
    )
    

    parser.add_argument(
        "--final_size",
        type=int,
        default=512,
        help="Final size of the output images"
    )

    parser.add_argument(
        "--content_size",
        type=int,
        default=256,
        help="Size of the content images"
    )

    parser.add_argument(
        "--style_size",
        type=int,
        default=256,
        help="Size of the style images"
    )

    parser.add_argument(
        "--crop",
        action="store_true",
        help="Whether to crop the images to square or not",
        default=True
    )

    parser.add_argument(
        "--batch_size",
        type=int,
        default=4,
        help="Batch size for training"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    device=torch.device("cuda" if torch.cuda.is_available() else "cpu")

    save_dir=Path("experiments")/args.experiment_dir
    save_dir.mkdir(parents=True, exist_ok=True)

    #Save args
    with open(save_dir/"args.txt", "w") as f:
        for arg, value in vars(args).items():
            f.write(f"{arg}: {value}\n")
    
    content_transform = get_transform(args.content_size, args.crop, args.final_size)
    style_transform = get_transform(args.style_size, args.crop, args.final_size)

    content_dataset = ImageFolderDataset(args.content_dir, content_transform)
    style_dataset = ImageFolderDataset(args.style_dir, style_transform)

    content_dataloader = DataLoader(content_dataset, batch_size=args.batch_size, shuffle=True,pin_memory=True,drop_last=True)
    style_dataloader = DataLoader(style_dataset, batch_size=args.batch_size, shuffle=True,pin_memory=True,drop_last=True)

if __name__ == "__main__":
    main()


