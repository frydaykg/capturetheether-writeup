import time

from web3 import Web3, HTTPProvider
import urllib3
from solc import compile_source

urllib3.disable_warnings()
web3 = Web3(HTTPProvider('https://ropsten.infura.io/xxxxxxxxxx', {'verify': False}))

private_key = '0x0000000000000000000000000000000000000'
account = web3.eth.account.privateKeyToAccount(private_key)
web3.eth.defaultAccount = account.address

challenge_contract_address = '0x000000000000000000000000000000000'
with open('challenge.sol', 'r') as f:
    contract_source_code = f.read()

compiled_sol = compile_source(contract_source_code, allow_paths='.')['<stdin>:PredictTheBlockHashChallenge']

def send_transaction_sync(tx, args={}):
    args['nonce'] = web3.eth.getTransactionCount(account.address)
    signed_txn = account.signTransaction(tx.buildTransaction(args))
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.eth.waitForTransactionReceipt(tx_hash)

contract = web3.eth.contract(abi=compiled_sol['abi'], address=challenge_contract_address)


print('Locking...')
tx = contract.functions.lockInGuess('0x0000000000000000000000000000000000000000000000000000000000000000')
lock_receipt = send_transaction_sync(tx, {'value': web3.toWei('1', 'ether'), 'gas': 3000000})
lock_block = int(lock_receipt['blockNumber'])
print('Locked')

#Average block mined in 12 seconds so 260 * 12 will be our waiting time
print('Wait', 260*12, 'seconds...')
time.sleep(260*12)


while True:
    current_blockNumber = int(web3.eth.getBlock('latest')['number'])
    if current_blockNumber - lock_block > 260:
        tx = contract.functions.settle()
        receipt = send_transaction_sync(tx,  {'gas': 3000000})
        break
    print('Wait a little bit more...')
    time.sleep(10) # Lets check it every 10 seconds

print('Solved')
