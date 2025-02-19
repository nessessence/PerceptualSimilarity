import argparse
import os
import lpips
import torch
from tqdm import tqdm
if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d0','--dir0', type=str, default='~/DDPM/stylegan2-pytorch/datasets/CelebA-HQ-img/')
    parser.add_argument('-d1','--dir1', type=str, default='data/nessessence/DDPM/projected_output/W/inversed_imgs/')
    parser.add_argument('-o','--out', type=str, default='output/lpips/30k_Celeb_StyleGAN2_W.txt')
    parser.add_argument('-v','--version', type=str, default='0.1')
    parser.add_argument('-size', type=int, default=128)

    parser.add_argument('--use_gpu', action='store_true', help='turn on flag to use GPU')

    opt = parser.parse_args()

    ## Initializing the model
    loss_fn = lpips.LPIPS(net='alex',version=opt.version)
    if(opt.use_gpu):
        loss_fn.cuda()

    # crawl directories
    f = open(opt.out,'w')
    files = os.listdir(opt.dir0)
    
    sum = 0 
    for i,file in tqdm(enumerate(files)):  
        if(os.path.exists(os.path.join(opt.dir1,f"{file.split('.')[0]}.png" ) )):
            # Load images
            img0 = lpips.im2tensor(lpips.load_image(os.path.join(opt.dir0,file),opt.size)) # RGB image from [-1,1]
            img1 = lpips.im2tensor(lpips.load_image(os.path.join(opt.dir1,f"{file.split('.')[0]}.png"),opt.size))

            if(opt.use_gpu):
                img0 = img0.cuda()
                img1 = img1.cuda()

            # Compute distance
            with torch.no_grad():
                dist01 = loss_fn.forward(img0,img1).item()
                sum += dist01
            print(f'avg: {sum/(i+1)}')
            # print('%s: %.3f'%(file,dist01))

            f.writelines('%s: %.6f\n'%(file,dist01))
    print(f'avg: {sum/len(files)}')
    f.writelines(f'sum:{sum}')
    f.writelines(f'avg:{sum/len(files)}')

    f.close()
