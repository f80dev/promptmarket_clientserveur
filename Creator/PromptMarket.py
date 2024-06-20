from multiversx_sdk.abi import StringValue, U8Value, U32Value, U64Value

from Network import Network





class PromptMarket:

    network:Network
    def __init__(self,network:Network,contract_addr=""):
        self.network=network
        self.contract_addr=contract_addr


    def prompt_list(self,model=-1) -> list:
        rc=list()
        results=self.network.query(self.contract_addr,"prompts")
        for r in results[0]:
            if model==-1 or r.model==model:
                rc.append(r.__dict__)

        return rc


    def add_render(self, creator:str,prompt_id:int, url:str, price:float):
        #voir https://docs.multiversx.com/sdk-and-tools/sdk-py/sdk-py-cookbook#perform-a-contract-deployment pour le typage des arguments
        data=[
            self.network.address_from(creator,format="address"),
            prompt_id,
            url,
            int(price*1e18)
        ]
        _t=self.network.create_transaction(self.network.address_from(creator,format="erd"),data,contract=self.contract_addr,function="add_render")
        rc=self.network.send_transaction(_t,self.network.signer_from(creator))
        return rc

    def add_prompt(self, user, text:str,model:int=1, inference:int=50, scale:int=512,token="",amount:float=0):
        data=[text,model,inference,scale]
        _t=self.network.create_transaction(self.network.address_from(user,format="erd"),data,contract=self.contract_addr,function="add_prompt",value=amount,token=token)
        rc=self.network.send_transaction(_t,self.network.signer_from(user))
        return rc




