# Guess the random number

Again our aim is to make balance of challenge contract will equal to zero.

Method **guess** checks that argument of function is equal to answer. Answer is calculated in constructor like this:
```solidity
answer = uint8(keccak256(block.blockhash(block.number - 1), now));
```

There are two approaches:

### Get answer value from blockchain

We could read storage of contract and get answer value. Answer stored on 0 offset. Let solve it with Web3.
```javascript
var contractAddress = '0x00000000000000000000000000000000000000000';
var abiOfChallenge = [{"constant" : false, "inputs" : [{"name" : "n", "type" : "uint8"}], "name" : "guess", "outputs" : [], "payable" : true, "stateMutability" : "payable", "type" : "function"}, {"constant" : true, "inputs" : [], "name" : "isComplete", "outputs" : [{"name" : "", "type" : "bool"}], "payable" : false, "stateMutability" : "view", "type" : "function"}, {"inputs" : [], "payable" : true, "stateMutability" : "payable", "type" : "constructor"}];
var contract = web3.eth.contract(abiOfChallenge).at(contractAddress);
web3.eth.getStorageAt(contractAddress, 0, (error, result) => {	
	var answer = web3.toBigNumber(result).toNumber();
	contract.guess.sendTransaction(answer, {from: web3.eth.defaultAccount, value: web3.toWei(1)});
});
```

Success!

### Get block index and time from blockchain

Another option is to get metadata of challenge contract's birth block. It easy to do with https://ropsten.etherscan.io/

E.g. 
Contract address https://ropsten.etherscan.io/address/0x7E0013b0Dad0568d225A84585b3BC53b8386701A =>  
Creator transaction hash https://ropsten.etherscan.io/tx/0xd86e79806fe29c78707cb41a43dff1c7e666b96ce3bc1e1f4a86bee51907b813

Block Height: 3616777  
TimeStamp: Jul-11-2018 04:20:16 PM +UTC => 1531326016 Unix Timestamp

Solver will calculate answer and send it to challenge. But there are one restriction, block.blockhash could return not zero values only for last 256 blocks. So hurry to solve your challenge.