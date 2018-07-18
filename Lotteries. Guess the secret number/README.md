# Guess the secret number

As in previous challenge, our aim is to make balance of challenge contract will equal to zero.

Method **guess** check that **keccak256** hash of function argument is equal to variable **answerHash** in storage.
```solidity
bytes32 answerHash = 0xdb81b4d58595fbbbb592d3661a34cdca14d7ab379441400cbfa1b78bc447c365;

...

function guess(uint8 n) public payable {
	require(msg.value == 1 ether);

	if (keccak256(n) == answerHash) {
		msg.sender.transfer(2 ether);
	}
}
```

Function argument has type uint8, it's mean that there are only 256 possible values. We could bruteforce it offline or calculate right value in solver contract.

I chose second option. In **solve** method I iterate through all uint8 range and compare hash of current value with challenge hash.
```solidity
for(uint8 i=0; i < 256; i++) {
	if (keccak256(i) == 0xdb81b4d58595fbbbb592d3661a34cdca14d7ab379441400cbfa1b78bc447c365) {
		c.guess.value(1 ether)(i);
		msg.sender.transfer(address(this).balance);
		return;
    }
}
```

To solve call **solve** method of GuessTheSecretNumberChallengeSolver contract and pass to it challenge contract address and *1 ether*.