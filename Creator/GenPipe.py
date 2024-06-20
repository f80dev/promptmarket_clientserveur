from PIL.Image import Image


MODELS={
    "Pokemon":"justinpinkney/pokemon-stable-diffusion",
    "StableDiffusion3":"stabilityai/stable-diffusion-3-medium",
    "StableDiffusion1.5":"runwayml/stable-diffusion-v1-5"
}


class GenPipe:
    cache_dir="./cache"
    device="cuda"
    pipe=None
    def __init__(self,model_id:str,weights:str):
        pass

    def create_image(prompt = "mystery",negative_prompt = "",inference=10,scale=400,guidance_scale=4) -> Image:
        pass