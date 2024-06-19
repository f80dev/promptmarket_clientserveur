from Network import Network


class PromptMarket:

    network:Network
    def __init__(self,network:Network,contract_addr=""):
        self.network=network
        self.contract_addr=contract_addr


    def prompt_list(self):
        result=self.network.query(self.contract_addr,"prompts")
        return result

    def add_render(self, creator:str,prompt_id:int, url:str, price:float):

        data=[
            self.network.address_from(creator,format="address"),
            U32Value(prompt_id),
            url,
            price
        ]
        _t=self.network.create_transaction(self.network.address_from(creator,format="erd"),data,contract=self.contract_addr,function="add_render")
        rc=self.network.send_transaction(_t,self.network.signer_from(creator))
        return rc

    def add_prompt(self, user, text:str,model:int=1, inference:int=50, scale:int=512,token="",amount:float=0):
        data=[text,model,inference,scale]
        _t=self.network.create_transaction(self.network.address_from(user,format="erd"),data,contract=self.contract_addr,function="add_prompt",value=amount,token=token)
        rc=self.network.send_transaction(_t,self.network.signer_from(user))
        return rc




