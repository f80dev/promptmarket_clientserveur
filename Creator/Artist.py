import io

from DiffusionPipe import DiffusionPipe
from PromptMarket import PromptMarket
from nftstorage import NFTStorage

MODELS={
    "Pokemon":"justinpinkney/pokemon-stable-diffusion",
    "StableDiffusion3":"stabilityai/stable-diffusion-3-medium",
    "StableDiffusion1.5":"runwayml/stable-diffusion-v1-5"
}

class Artist:
    def __init__(self,address="",model=1):
        self.model=model
        self.address=address
        if model==1:
            self.pipeline=DiffusionPipe(list(MODELS.values())[model],"")

    def render(self,market:PromptMarket,price=1) -> list:
        storage=NFTStorage()
        renders=list()
        for prompt in market.prompt_list(model=self.model):
            img=self.pipeline.create_image(str(prompt["text"],"utf8"),negative_prompt="",inference=prompt["inference"],scale=prompt["scale"])

            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr,format="WEBP")

            _rep=storage.add(img_byte_arr.getvalue(),"image/webp")
            renders.append(market.add_render(self.address,prompt["id"],_rep["url"],price=price))
        return renders



