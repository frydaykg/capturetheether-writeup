# Predict the future

In this challenge we have 2 main methods: **lockInGuess** and **settle**. In first we are set our guess and in second we calculate hash of current block metadata and compare modulo of it with our guess.  
The problem is that we couldn't mine it in one block, because of this condition:
```solidity
require(block.number > settlementBlockNumber);
```

But we could try as much as we want, and call challenge settle method only when our guess is equal to current hash.
Relay contract is a key! But here are we should try several times(about 10).

It's hard to authorize each transaction in Metamask. That's why I did full automation. Web3.py is good enough tool for such things.  

To solve set your Infura token, private key and chanllenge contract address.
