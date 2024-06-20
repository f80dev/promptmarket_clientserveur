import {Component} from '@angular/core';
import { ExtensionProvider } from "@multiversx/sdk-extension-provider";

import {
  Address, BigUIntValue,
  SmartContractTransactionsFactory, SmartContractTransactionsOutcomeParser, StringValue, Token,
  TokenTransfer, Transaction, TransactionComputer, TransactionsConverter,
  TransactionsFactoryConfig, TransactionWatcher, U16Value, U8Value
} from "@multiversx/sdk-core/out";
import { ApiNetworkProvider } from "@multiversx/sdk-network-providers";
import {ProxyNetworkProvider} from "@multiversx/sdk-network-providers/out";
import {WalletProvider} from "@multiversx/sdk-web-wallet-provider/out";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent extends ApiNetworkProvider {
  title = 'FrontEnd';
  text="un lapin sur une plage"
  inference=30
  scale=256
  //api=inject(NetworkService);

  constructor() {
    super("https://devnet-api.multiversx.com");
  }

  async send_prompt() {
    //voir https://docs.multiversx.com/sdk-and-tools/sdk-js/sdk-js-cookbook-v13#formatting-and-parsing-amounts

    const factoryConfig = new TransactionsFactoryConfig({ chainID: "D" });
    let factory = new SmartContractTransactionsFactory({config: factoryConfig});
    //voir https://github.com/multiversx/mx-sdk-js-web-wallet-provider/blob/main/src/walletProvider.ts
    //let provider:WalletProvider=new WalletProvider("https://devnet-wallet.multiversx.com/")
    //voir https://docs.multiversx.com/sdk-and-tools/sdk-js/sdk-js-cookbook-v13#signing-objects
    const provider = ExtensionProvider.getInstance();
    await provider.init()
    await provider.login()

    let sender=Address.fromBech32(await provider.getAddress());
    let _sender=await this.getAccount(sender)

    // const pemText = await promises.readFile("../wallet/user1.pem", { encoding: "utf8" });
    // let signer = UserSigner.fromPem(pemText);

    // voir l'exemple https://docs.multiversx.com/sdk-and-tools/sdk-js/sdk-js-cookbook-v13#perform-a-contract-deployment
    let args = [new StringValue(this.text),new U8Value(1),new U16Value(this.inference), new U16Value(this.scale)];

    //voir https://multiversx.github.io/mx-sdk-js-core/v13/classes/TokenTransfer.html

    let token_transfer=new TokenTransfer(
      {
        token: new Token({identifier: "AIRDROP-bc8a67"}),
        amount: 4000000000000000000n
      }
    )

    //voir https://docs.multiversx.com/sdk-and-tools/sdk-js/sdk-js-cookbook-v13#transfer--execute
    const transaction = factory.createTransactionForExecute({
      sender: sender,
      contract: Address.fromBech32("erd1qqqqqqqqqqqqqpgq92twlq9u6ke8zd50jlq5gjrrv7q00nrl835sxrz8p4"),
      function: "add_prompt",
      gasLimit: 500000000n,
      nativeTransferAmount:0n,
      arguments: args,
      tokenTransfers:[token_transfer]
    });

    //voir https://docs.multiversx.com/sdk-and-tools/sdk-js/sdk-js-signing-providers/#signing-transactions-1
    //voir exemple https://github.com/multiversx/mx-sdk-js-examples/blob/0d35714c9172ea5a31a7563a155a942b9249782e/signing-providers/src/extension.js#L52
    transaction.nonce=BigInt(_sender.nonce)
    let sign_transaction=await provider.signTransaction(transaction)

    //voir https://docs.multiversx.com/sdk-and-tools/sdk-js/sdk-js-cookbook-v13#creating-network-providers
    //const proxyNetworkProvider = new ProxyNetworkProvider("https://devnet-gateway.multiversx.com");



    //Voir https://docs.multiversx.com/sdk-and-tools/sdk-js/sdk-js-cookbook-v13#broadcast-using-a-network-provider
    //const txHash = await proxyNetworkProvider.sendTransaction(transaction);
    try{
      let rc=await this.sendTransaction(sign_transaction)
    }catch (e) {
      console.log(e)
      debugger
    }


    //Attente du résultat
    //const watcherUsingApi = new TransactionWatcher(apiNetworkProvider);
    // const transactionOnNetworkUsingProxy  = await watcherUsingApi.awaitCompleted(txHash);
    //
    // const converter = new TransactionsConverter();
    // const parser = new SmartContractTransactionsOutcomeParser();
    //
    // const transactionOutcome = converter.transactionOnNetworkToOutcome(transactionOnNetworkUsingProxy);
    // const parsedOutcome = parser.parseDeploy({ transactionOutcome });
  }
}
