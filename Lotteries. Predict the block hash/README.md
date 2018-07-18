# Predict the block hash

So we are locking guess and block number and after calling **settle**, we are trying to compare our guess and hash of this block.  
There are importnat note, that we couldn't mine two calls in one block:
```solidity
require(block.number > settlementBlockNumber);
```

Looks like good atempt, but on the documentation:
```
block.blockhash(uint blockNumber) returns (bytes32): hash of the given block - only works for 256 most recent, excluding current, block.
```
After 256 block it returns zero-array. What does it mean for us? That after 256 blocks after locking value of ```block.blockhash(settlementBlockNumber)``` will be fixed and will be equal to zero.

As in previous challenge let automate it in web3.py.