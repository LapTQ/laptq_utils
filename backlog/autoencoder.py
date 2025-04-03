from diffusers import AutoencoderKL
from PIL import Image
import torch
from torchvision import transforms



vae = AutoencoderKL.from_pretrained("CompVis/stable-diffusion-v1-4", subfolder="vae", device_map='auto')


image = Image.open(
    # "/home/lap_awlv/fed-object-detection/data/people_detection/test/images/8JWLHYHHBIFX_jpg.rf.5b5fff2e203a8dac1ab6370734d5ad28.jpg"
    "/home/lap_awlv/fed-object-detection/data/147_rice_2021_11_09_8AM_20_58_edit_63.jpg"
).convert('RGB').resize((512, 512))
image = transforms.ToTensor()(image).unsqueeze(0)
print(image.shape)
out = vae.encode(image*2-1).latent_dist.sample()
print(out.shape)
out = vae.decode(out).sample
print(out[0].shape)
out = (out / 2 + 0.5).clamp(0, 1)
out = out[0].permute(1, 2, 0).detach().cpu().numpy()
out = (out * 255).astype("uint8")
out = Image.fromarray(out)
# out.show()
out.save("/home/lap_awlv/fed-object-detection/outputs/autoencoder/vae_out.png")


# pip install --upgrade diffusers transformers accelerate scipy ftfy safetensors