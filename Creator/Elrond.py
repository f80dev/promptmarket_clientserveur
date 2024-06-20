import base64
import datetime
import json
import random
from pathlib import Path
from time import sleep

from multiversx_sdk import QueryRunnerAdapter, SmartContractQueriesController, SmartContractTransactionsFactory, \
    TransactionsFactoryConfig, TransactionsConverter, SmartContractTransactionsOutcomeParser, ApiNetworkProvider
from multiversx_sdk_core import TokenTransfer, Token, Address, Transaction, TransactionComputer
from multiversx_sdk_network_providers import ProxyNetworkProvider
from multiversx_sdk_wallet import UserSigner, UserSecretKey
from multiversx_sdk.abi import Abi

from Network import Network

LIMIT_GAS=500000000

NETWORKS={
    "localnet":{
        "unity":"xEgld",
        "identifier":"TFE-116a67",
        "faucet":"https://devnet-wallet.multiversx.com",
        "proxy":"http://192.168.1.62:7950",
        "explorer":"http://192.168.1.62:7950/transactions",
        "gallery":"https://devnet.xspotlight.com",
        "wallet":"https://devnet-wallet.multiversx.com",
        "nft":"erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u",
        "esdt":"erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u",
        "shard": 1
    },

    "testnet":{
        "unity":"xEgld",
        "faucet":"https://r3d4.fr/elrond/testnet/index.php",
        "proxy":"https://testnet-api.multiversx.com",
        "explorer":"https://testnet-explorer.multiversx.com",
        "wallet":"http://testnet-wallet.multiversx.com",
        "nft":"erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u",
        "esdt":"erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u",
        "shard":0
    },

    #erd1qqqqqqqqqqqqqpgqkwfvpkaf6vnn89508l0gdcx26vpu8eq5d8ssz3lhlf
    "devnet":{
        "unity":"xEgld",
        "identifier":"TFE-116a67",
        "faucet":"https://devnet-wallet.multiversx.com",
        "proxy":"https://devnet-api.multiversx.com",
        "explorer":"https://devnet-explorer.multiversx.com",
        "gallery":"https://devnet.xspotlight.com",
        "wallet":"https://devnet-wallet.multiversx.com",
        "nft":"erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u",
        "esdt":"erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u",
        "shard": 1
    },

    "devnet2":{
        "unity":"xEgld",
        "identifier":"TFE-116a67",
        "faucet":"https://devnet2-wallet.multiversx.com",
        "proxy":"https://devnet2-api.multiversx.com",
        "explorer":"https://devnet2-explorer.multiversx.com",
        "gallery":"https://devnet2.xspotlight.com",
        "wallet":"https://devnet2-wallet.multiversx.com",
        "nft":"erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u",
        "esdt":"erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u",
        "shard": 1
    },

    "mainnet":{
        "unity":"Egld",
        "identifier":"",
        "faucet":"",
        "proxy":"https://api.multiversx.com",
        "explorer":"https://explorer.multiversx.com",
        "wallet":"https://wallet.multiversx.com",
        "gallery":"https://xspotlight.com",
        "nft":"erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u",
        "esdt":"erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u",
        "shard": 1
    }
}

def now(format="dec"):
    rc= datetime.datetime.now(tz=None).timestamp()
    if format=="hex":return hex(int(rc*10000))
    if format=="random" or format=="rand":return hex(int(rc*10000)+random.randint(0,1000000))
    return rc



class Elrond(Network):
    def __init__(self,network="elrond-devnet",abi_path=""):
        super().__init__(network)
        self._proxy=ApiNetworkProvider(NETWORKS[self.network_type]["proxy"])
        self.abi=Abi.load(Path(abi_path))

    def query(self,contract:str,method:str,params:[any]=[],caller:str=None):
        """
        voir    voir https://docs.multiversx.com/sdk-and-tools/sdk-py/sdk-py-cookbook/#contract-deployments-and-interactions
        :param contract:
        :param method:
        :param params:
        :param caller:
        :return:
        """
        #voir https://docs.multiversx.com/sdk-and-tools/sdk-py/sdk-py-cookbook/#contract-queries
        if type(params)!=list:params=[params]
        query_runner = QueryRunnerAdapter(self._proxy)
        query_controller = SmartContractQueriesController(query_runner, self.abi)

        assert contract.startswith("erd")

        query  = query_controller.create_query(
            contract=contract,
            function=method,
            arguments=params,
            caller=Address.from_bech32(caller) if caller else None
        )

        #voir https://docs.multiversx.com/sdk-and-tools/sdk-js/sdk-js-cookbook-v13/#contract-queries
        response=query_controller.run_query(query)
        if response.return_code!="ok":
            return None

        return query_controller.parse_query_response(response)


    def signer_from(self,sign:str,password="") -> UserSigner:
        if "/" in sign:
            if sign.endswith(".json") and len(password)>0:
                _signer=UserSigner.from_wallet(Path(sign),password)
            else:
                _signer=UserSigner.from_pem_file(Path(sign))
        else:
            _signer=UserSigner(UserSecretKey.from_string(sign))

        return _signer


    def address_from(self,key:str,password="",format="hex") -> str or Address:
        _user=self.signer_from(key,password)
        if format=="hex": return _user.get_pubkey().hex()
        if format=="erd": return _user.get_pubkey().to_address("erd").to_bech32()
        return _user.get_pubkey().to_address("erd")


    def getExplorer(self, tx:Address or str="", _type="transactions") -> str:
        if type(tx)==Address:
            _type="address"
            tx=tx.toBech32()
        url = NETWORKS[self.network_type]["explorer"] + "/" + _type + "/"
        if len(tx)>0:url=url+tx
        url=url.replace("api","explorer")
        return url



    def send_transaction(self,transaction:Transaction,_signer:UserSigner =None,password="",
                         timeout=120,simulation=False,delay_between_check=3.0) -> dict:
        """
        Envoi d'une transaction signée
        voir https://docs.multiversx.com/sdk-and-tools/sdk-py/sdk-py-cookbook#egld--esdt-transfers
        voir https://docs.multiversx.com/sdk-and-tools/sdk-js/sdk-js-cookbook-v13/#parsing-transaction-outcome-1
        voir https://docs.multiversx.com/sdk-and-tools/sdk-py/sdk-py-cookbook
        :param _sender:
        :param _receiver:
        :param _sign:
        :param value:
        :param data:
        :return:
        """


        if transaction.signature is None or transaction.signature==bytes(0):
            #voir https://docs.multiversx.com/sdk-and-tools/sdk-py/sdk-py-cookbook#signing-objects
            transaction.nonce=self._proxy.get_account(_signer.get_pubkey().to_address("erd")).nonce
            transaction.signature=_signer.sign(TransactionComputer().compute_bytes_for_signing(transaction))


        try:
            d=None
            if not simulation:

                #voir https://docs.multiversx.com/sdk-and-tools/sdk-py/sdk-py-cookbook#relayed-v2
                # builder = RelayedTransactionV2Builder()
                # builder.set_inner_transaction(transaction)
                # builder.set_relayer_nonce(2627)
                # builder.set_network_config(self._proxy.get_network_config())
                # builder.set_relayer_address(Address.from_bech32("erd1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssycr6th"))
                # builder.build()

                hash = self._proxy.send_transaction(transaction)


                start=now()

                t=None
                while now()-start<timeout:
                    sleep(delay_between_check)

                    t=self._proxy.get_transaction(hash)

                    if t.status.status=="success":break
                    if t.status.status=="invalid" or t.status.status=="fail":
                        break

                d=t.to_dictionary()

            else:
                r = self._proxy.simulate_transaction(transaction)
                hash=r.raw["result"]["hash"]

            #voir https://docs.multiversx.com/sdk-and-tools/sdk-py/sdk-py-cookbook/#parsing-transaction-outcome
            converter = TransactionsConverter()
            parser = SmartContractTransactionsOutcomeParser()
            transaction_outcome = converter.transaction_on_network_to_outcome(t)
            parsed_outcome = parser.parse_deploy(transaction_outcome)

            d["explorer"]=self.getExplorer(hash)
            d["error"]=d["status"] if not d["status"]=="success" else ""
            d["results"]=dict()
            d["results"]=parsed_outcome["contracts"]
            return d

        except Exception as inst:
            mess=str(inst.args).split(":")
            mess=":".join(mess[2:]) if len(mess)>2 else ":".join(mess)
            mess=mess.strip()

            if mess.startswith("{"):
                mess=(mess.split("}")[0]+"}").replace("'","\"").replace("None","\"\"")
                return {"error":json.loads(mess),"status":"error","hash":""}

            return {"error":mess,"status":"error","hash":""}



    def create_transaction(self,miner_addr:str,data:str or list,value:float=0.0,receiver=None,contract=None,function="",token="egld",abi="") -> Transaction:
        """

        :param _miner:
        :param data:
        :return:
        voir https://docs.multiversx.com/sdk-and-tools/sdk-py/sdk-py-cookbook/#contract-deployments-and-interactions
        voir https://docs.multiversx.com/sdk-and-tools/sdk-py/sdk-py-cookbook/#contract-deployments-and-interactions
        """
        config = TransactionsFactoryConfig(chain_id=self._proxy.get_network_config().chain_id)
        sc_factory = SmartContractTransactionsFactory(config,self.abi)

        if type(contract)==str: contract=Address.from_bech32(contract)
        if token!="egld":           #voir https://docs.multiversx.com/sdk-and-tools/sdk-py/sdk-py-cookbook/#contract-deployments-and-interactions=
            t=sc_factory.create_transaction_for_execute(
                sender=Address.from_bech32(miner_addr),
                arguments=data,
                contract=contract,
                function=function,
                gas_limit=LIMIT_GAS,
                token_transfers=[TokenTransfer(Token(token), int(value*1e18))]
            )
        else:
            t=sc_factory.create_transaction_for_execute(
                sender=Address.from_bech32(miner_addr),
                arguments=data,
                native_transfer_amount=int(value*1e18),
                contract=contract,
                function=function,
                gas_limit=LIMIT_GAS
            )

        return t
