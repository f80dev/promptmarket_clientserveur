import io

import pytest as pytest
from PIL import Image

from Artist import Artist, MODELS
from DiffusionPipe import DiffusionPipe
from Elrond import Elrond
from PromptMarket import PromptMarket
from nftstorage import NFTStorage

NETWORK_TO_USE="devnet"
CONTRACT_ADDR="erd1qqqqqqqqqqqqqpgqlxchpm3mvkugq5vf9yht54stcsyk99t7835s09ktfy"
ARTIST="erd1sv7dlrry2l4ptkhvk64hxs3qmg7pgphlvszcxkuuj92jutulkr2qs4qe8q"     #user4

@pytest.fixture()
def promptmarket():
    return PromptMarket(Elrond(NETWORK_TO_USE,"./promptmarket.abi.json"),CONTRACT_ADDR)

@pytest.fixture()
def artist():
    return Artist(ARTIST,1)


@pytest.fixture()
def pipe():
    return DiffusionPipe(MODELS["StableDiffusion3"],"")

def test_list_prompt(promptmarket:PromptMarket):
    rc=promptmarket.prompt_list()
    assert len(rc)>0

def test_add_prompt(promptmarket:PromptMarket):
    user="./wallet/user1.pem"
    rc=promptmarket.add_prompt(user,"a blue rabbit on a beach",1,30,256,"AIRDROP-bc8a67",10)
    rc=promptmarket.add_prompt(user,"a green fish in a forest",1,30,256,"AIRDROP-bc8a67",10)
    assert len(rc)>0

def test_add_render(promptmarket:PromptMarket):
    creator="./wallet/user1.pem"
    rc=promptmarket.add_render(creator,1,"http://nfluent.io",2)
    assert len(rc)>0


def test_storage():
    image=Image.open("./static/image.webp")
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr,format="WEBP")
    result=NFTStorage().add(img_byte_arr.getvalue(),"image/webp")
    assert "cid" in result

def test_create_image(pipe):
    img=pipe.create_image("a rabbit on the beach","",60,256)
    img.save("image.webp",format="webp")


def test_artist_render(artist,promptmarket):
    artist.render(promptmarket,1)


