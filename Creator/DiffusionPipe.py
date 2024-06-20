from PIL.Image import Image
from diffusers import DiffusionPipeline, StableDiffusionPipeline,StableDiffusion3Pipeline
from torch import float16

from GenPipe import GenPipe


class DiffusionPipe(GenPipe):

    def __init__(self,model_id="runwayml/stable-diffusion-v1-5",weights="artificialguybr/stickers-redmond-1-5-version-stickers-lora-for-sd-1-5",torch_dtype=float16):
        if model_id.endswith(".safetensors"):
            self.pipe=StableDiffusionPipeline.from_single_file(self.cache_dir+"/"+model_id,torch_dtype=torch_dtype)
        else:
            if "-3" in model_id:
                self.pipe=StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3-medium-diffusers", torch_dtype=torch_dtype)
            else:
                self.pipe=DiffusionPipeline.from_pretrained(model_id,cache_dir=self.cache_dir,torch_dtype=torch_dtype)

        #pipe.scheduler = KDPM2AncestralDiscreteScheduler.from_config(pipe.scheduler.config)
        if weights!="": self.pipe.load_lora_weights(weights,cache_dir=self.cache_dir)
        self.pipe.to(self.device)


    def create_image(self,prompt = "mystery",negative_prompt = "",inference=50,scale=256,guidance_scale=4):
        # Define prompts and generate image
        image:Image = self.pipe(
            prompt,
            negative_prompt=negative_prompt,
            width=scale,
            height=scale,
            guidance_scale=guidance_scale,
            num_inference_steps=inference,
            clip_skip=3
        ).images[0]
        return image

