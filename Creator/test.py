
import pytest as pytest
from Elrond import Elrond
from PromptMarket import PromptMarket


NETWORK_TO_USE="devnet"
CONTRACT_ADDR="erd1qqqqqqqqqqqqqpgqalkhdmrxpsfxgrp9udmw0l2qn9s5642j835sj336vf"

@pytest.fixture()
def promptmarket():
    return PromptMarket(Elrond(NETWORK_TO_USE),CONTRACT_ADDR)


def test_list_prompt(promptmarket:PromptMarket):
    rc=promptmarket.prompt_list()
    assert len(rc)>0

def test_add_prompt(promptmarket:PromptMarket):
    user="./wallet/user2.pem"
    rc=promptmarket.add_prompt(user,"un lapin vert plage",1,30,128,"AIRDROP-bc8a67",10)
    assert len(rc)>0

def test_add_render(promptmarket:PromptMarket):
    creator="./wallet/user1.pem"
    rc=promptmarket.add_render(creator,1,"http://nfluent.io",2)
    assert len(rc)>0

