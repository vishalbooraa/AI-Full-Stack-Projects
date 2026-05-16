import argparse
import torch
from pathlib import Path
from utils.utils import *
from torch.utils.data import DataLoader
from utils.models import VGGEncoder,Decoder
import torch.optim as optim
import torch.nn as nn
from tqdm import tqdm
from torchvision.utils import save_image

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
        default=256,
        help="Final size of the output images"
    )

    parser.add_argument(
        "--content_size",
        type=int,
        default=128,
        help="Size of the content images"
    )

    parser.add_argument(
        "--style_size",
        type=int,
        default=128,
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

    parser.add_argument(
        "--lr",
        type=float,
        default=1e-4,
        help="Learning rate for training"
    )

    parser.add_argument(
        "--lr_decay",
        type=float,
        default=5e-5,
        help="Learning rate decay for training"
    )

    parser.add_argument(
        "--num_epochs",
        type=int,
        default=2,
        help="Number of epochs for training"
    )

    parser.add_argument(
        "--content_weight",
        type=float,
        default=1.0,
        help="Weight for content loss"
    )

    parser.add_argument(
        "--style_weight",
        type=float,
        default=10.0,
        help="Weight for style loss"
    )   

    parser.add_argument(
        "--save_interval",
        type=int,
        default=1,
        help="Interval for saving the model"
    )

    parser.add_argument(
        "--resume",
        action="store_true",
        help="Whether to resume training from a checkpoint or not",
        default=False
    )
    parser.add_argument(
        "--decoder_path",
        type=str,
        default="",
        help="Path to decoder checkpoint for resuming training"
    )
    parser.add_argument(
        "--optimizer_path",
        type=str,
        default="",
        help="Path to optimizer checkpoint for resuming training"
    )

    parser.add_argument(
        "--log_interval",
        type=int,
        default=1,
        help="Interval for logging training progress"
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

    print(f"Number of content images: {len(content_dataset)}")
    print(f"Number of style images: {len(style_dataset)}")

    content_dataloader = DataLoader(content_dataset, batch_size=args.batch_size, shuffle=True,pin_memory=True,drop_last=True)
    style_dataloader = DataLoader(style_dataset, batch_size=args.batch_size, shuffle=True,pin_memory=True,drop_last=True)


    encoder=VGGEncoder(args.vgg).to(device)
    decoder=Decoder().to(device)

    optimizer=optim.Adam(decoder.parameters(),lr=args.lr)

    scheduler=optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lambda epoch: 1/(1+args.lr_decay*epoch))

    if args.resume:
        decoder.load_state_dict(torch.load(args.decoder_path))
        optimizer.load_state_dict(torch.load(args.optimizer_path))
    print("Starting training...")

    mse_loss=nn.MSELoss()

    encoder.eval()
    
    running_loss=None
    runn_closs=None
    runn_sloss=None

    for epoch in range(args.num_epochs):
        progress_bar=tqdm(zip(content_dataloader,style_dataloader),total=min(len(content_dataloader),len(style_dataloader)))
        for content_batch, style_batch in progress_bar:
            content_batch=content_batch.to(device)
            style_batch=style_batch.to(device)
            c_features=encoder(content_batch)
            s_features=encoder(style_batch)
            
            # print("c_features : ",len(c_features))
            # print("s_features : ",len(s_features))
            # print("c_feature shape : ",c_features[0].shape)
            # print("s_feature shape : ",s_features[0].shape)

            t= adaIN(c_features[-1],s_features[-1])

            g=decoder(t)

            g_features=encoder(g)

            loss_c = mse_loss(g_features[-1], t) * args.content_weight
            loss_s=0
            for gf, sf in zip(g_features, s_features):
                g_mean, g_std= calc_mean_std(gf)
                s_mean, s_std= calc_mean_std(sf)
                loss_s+= mse_loss(g_mean, s_mean) + mse_loss(g_std, s_std)
            loss_s*= args.style_weight

            loss=loss_c+loss_s

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            running_loss=loss.item()
            runn_closs=loss_c.item()
            runn_sloss=loss_s.item()
        
        scheduler.step()

        progress_bar.set_description(f"Epoch [{epoch+1}/{args.num_epochs}], Loss: {running_loss:.4f}, Content Loss: {runn_closs:.4f}, Style Loss: {runn_sloss:.4f}")

        running_loss/= len(content_dataloader)
        runn_closs/= len(content_dataloader)
        runn_sloss/= len(content_dataloader)

        if (epoch+1)%args.log_interval==0:
            tqdm.write(f"Epoch [{epoch+1}/{args.num_epochs}], Loss: {running_loss:.4f}, Content Loss: {runn_closs:.4f}, Style Loss: {runn_sloss:.4f}")


        if (epoch+1)%args.save_interval==0:
            torch.save(decoder.state_dict(), save_dir/f"decoder_epoch_{epoch+1}.pth")
            torch.save(optimizer.state_dict(), save_dir/f"optimizer_epoch_{epoch+1}.pth")

            with torch.no_grad():
                test_output=torch.cat([content_batch,style_batch,g],dim=0)
                save_image(test_output,save_dir/f"test_output_epoch_{epoch+1}.png",nrow=args.batch_size)




if __name__ == "__main__":
    main()


