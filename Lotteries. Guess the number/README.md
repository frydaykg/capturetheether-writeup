# Guess the number

Our aim is to make **isComplete** method return true. This will be true if balance of challenge contract will equal to zero.

Balance of contract after creation is equal to *1 ether*. For each guess we should pay *1 ether*, if we will be lucky we will get *2 ether*.
1 + 1 = 2, should be enough to complete this challenge.

Method **guess** check that argument of function is equal to variable in storage that is equal to 42.
```solidity
uint8 answer = 42;

...

if (n == answer) {
	msg.sender.transfer(2 ether);
}
```
So, to complete the challenge we could call **guess** method with argument 42 and value(*1 ether*).

For practice, I solved it with additional solver contract, but it posiible to solve with direct call of challenge contract.

To solve call **solve** method of GuessTheNumberChallengeSolver contract and pass to it challenge contract address and *1 ether*.