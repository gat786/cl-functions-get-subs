from web3 import Web3
from web3.exceptions import ContractLogicError
from dotenv import load_dotenv
import os

load_dotenv()
web3 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/polygon_mumbai"))

print(web3.is_connected())

functions_owner = "0xEe9Bf52E5Ea228404bB54BCFbbDa8c21131b9039"
my_address = os.getenv("MY_ADDRESS")
print(my_address)

with open("abi.json", "r") as f:
    abi = f.read()
    # print(abi)
    functions_contract = web3.eth.contract(address=functions_owner, abi = abi)
    latest_subscription_id = functions_contract.functions.getCurrentsubscriptionId().call()
    
    print("Latest Subscription ID: ", latest_subscription_id)
    
    for i in range(1,latest_subscription_id):
        try:
            subscription_info = functions_contract.functions.getSubscription(i).call()
            
            if subscription_info[1] == my_address:
                print(f"Our Subscription Found {i}")
                print(subscription_info)
            else:
                print(f"Not our subscription {i}")
                
            # create a folder named subscriptions if it doesn't exist
            if os.path.exists("subscriptions") == False:
                os.mkdir("subscriptions")
            
            with open(f"subscriptions/{i}.txt", "w") as f:
                f.write(str(subscription_info))
        except ContractLogicError as cle:
            print("Contract Logic Error for index ", i)
        
    
