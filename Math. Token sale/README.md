# Token sale

Our aim is to decrease starting balance of contract(*1 ether*).  

There are only one method with transfer function **sell** and there are require statement before:
```solidity
require(balanceOf[msg.sender] >= numTokens);
```

So we should increase our balance. There are **buy** method:
```solidity
 uint256 constant PRICE_PER_TOKEN = 1 ether;
 ...
function buy(uint256 numTokens) public payable {
        require(msg.value == numTokens * PRICE_PER_TOKEN);

        balanceOf[msg.sender] += numTokens;
}
```	

How could we topup balanceOf at more amount than actual value of transaction? Let's try to use integer overflow. There is possible overflow in multiplying operation: ```numTokens * PRICE_PER_TOKEN```.

We need to solve next equation:
```x = (y * 10^18) mod 2^256```

What is a first **y** when ```y * 10^18 > 2^256```? It is 115792089237316195423570985008687907853269984665640564039458.  
Now lets calculate x value for such y. It will be equal to 415992086870360064 wei. 

After calling  **buy** with **numTokens** equal to 115792089237316195423570985008687907853269984665640564039458 and **value** equal to 415992086870360064, we should get 115792089237316195423570985008687907853269984665640564039458 on our balance. After it we could withdraw *1 ether* with **sell** function.