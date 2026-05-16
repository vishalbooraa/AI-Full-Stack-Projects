from torch.utils.data import Dataset
import os
from PIL import Image
from torchvision import transforms


class ImageFolderDataset(Dataset):
    def __init__(self,root,transform=None):
        super(ImageFolderDataset,self).__init__()
        self.root=root
        self.transform=transform
        self.files=list(os.listdir(root))
        self.files=[p for p in self.files if p.lower().endswith((".jpg",".jpeg",".png"))]

    def __len__(self):
        return len(self.files)
    
    def __getitem__(self,idx):
        img_path=os.path.join(self.root,self.files[idx])
        image=Image.open(img_path).convert("RGB")
        if self.transform:
            image=self.transform(image)
        return image
    

def get_transform(size,crop,final_size):
    transform_list=[]
    if size>0:
        transform_list.append(transforms.Resize(size))
    if crop:
        transform_list.append(transforms.RandomCrop(size))
    else:
        transform_list.append(transforms.Resize(final_size))
    transform_list.append(transforms.ToTensor())
    return transforms.Compose(transform_list)


def adaIN(content_feat, style_feat):
    style_mean, style_std = calc_mean_std(style_feat)
    content_mean, content_std = calc_mean_std(content_feat)

    normalized_feat = (content_feat - content_mean) / content_std

    return normalized_feat * style_std + style_mean

def calc_mean_std(feat, eps=1e-5):
    size=feat.size()
    assert len(size)==4
    batch_size, channels = size[:2]
    feat_mean=feat.view(batch_size, channels, -1).mean(dim=2).view(batch_size, channels, 1, 1)
    feat_std=feat.view(batch_size, channels, -1).std(dim=2).view(batch_size, channels, 1, 1)+eps
    return feat_mean, feat_std
    
