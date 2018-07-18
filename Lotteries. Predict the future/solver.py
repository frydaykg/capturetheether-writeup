from web3 import Web3, HTTPProvider
import urllib3
from solc import compile_source

urllib3.disable_warnings()
web3 = Web3(HTTPProvider('https://ropsten.infura.io/xxxxxxxxxxxxxxxxx', {'verify': False}))

private_key = '0x000000000000000000000000000000000'
account = web3.eth.account.privateKeyToAccount(private_key)
web3.eth.defaultAccount = account.address

challenge_contract_address = '0x00000000000000000000000000'
with open('solver.sol', 'r') as f:
    contract_source_code = f.read()

compiled_sol = compile_source(contract_source_code, allow_paths='.')['<stdin>:PredictTheFutureChallengeSolver']

contract = web3.eth.contract(
    abi=compiled_sol['abi'],
    bytecode=compiled_sol['bin'])

def send_transaction_sync(tx, args={}):
    args['nonce'] = web3.eth.getTransactionCount(account.address)
    signed_txn = account.signTransaction(tx.buildTransaction(args))
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.eth.waitForTransactionReceipt(tx_hash)

print('Deploying contract...')
tx = contract.constructor(challenge_contract_address)
tx_contract_receipt = send_transaction_sync(tx)
print('Contract deployed')

c = web3.eth.contract(abi=compiled_sol['abi'], address=tx_contract_receipt.contractAddress)

print('Locking...')
tx = c.functions.lockInGuess()
send_transaction_sync(tx, {'value': web3.toWei('1', 'ether'), 'gas': 3000000})
print('Locked')

count = 0
while not c.functions.isComplete().call():
    print('Try to settle. Count =', count)
    tx = c.functions.settle()
    receipt = send_transaction_sync(tx,  {'gas': 3000000})
    count += 1

print('Solved')
