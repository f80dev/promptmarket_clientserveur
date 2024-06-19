
class Network():
    network=""
    network_name=""
    network_type=""
    keys=[]

    def __init__(self,network:str):
        self.network=network
        if not "-" in network:network="elrond-"+network
        self.network_name=network.split("-")[0]
        self.network_type=network.split("-")[1]

    def create_transaction(self,miner_addr:str,data:str or list,value:float=0.0,receiver=None,contract=None,function="",token="egld"):
        pass

    def query(self,contract:str,method:str,params:[any]=[],caller:str=None):
        pass

    def send_transaction(self,transaction,sign: str=None,password="",timeout=120,simulation=False,delay_between_check=3.0) -> dict:
        pass

    def address_from(self,key:str,password="",format="hex") -> str:
        pass

    def signer_from(self, key:str) -> any:
        pass
