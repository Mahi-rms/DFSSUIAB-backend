from web3 import Web3
from solcx import compile_standard, install_solc, compile_source
import os,json  
from backend import settings
install_solc("0.8.18")

def get_ipfs_hash(tx_hash):
    w3 = Web3(Web3.HTTPProvider(settings.URLConstants.WEB3_PROVIDER))
    if(w3.is_connected()):
        pass

    file_path = "./SimpleContract.sol"
    with open(file_path, 'r') as file:
        file_content = file.read()
    compiled_code = compile_source(file_content, output_values=['abi', 'bin'])
    contract_interface = compiled_code['<stdin>:SimpleContract']
    contract_instance= w3.eth.contract(abi=contract_interface['abi'],bytecode=contract_interface['bin'])
    abi = {"abi":contract_interface['abi']}
    with open("abi.json", "w") as f:
        json.dump(abi['abi'], f)
    
    tx=w3.eth.get_transaction(tx_hash)
    contract = w3.eth.contract(address=tx["to"], abi=abi['abi'])
    func_obj, func_params = contract.decode_function_input(tx["input"])
    return func_params['hash']