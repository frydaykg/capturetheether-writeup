pragma solidity ^0.4.21;

import "./challenge.sol";

contract GuessTheNumberChallengeSolver {

    function solve(address contractToSolve) public payable {
        GuessTheNumberChallenge c = GuessTheNumberChallenge(contractToSolve);
        c.guess.value(1 ether)(42);
        msg.sender.transfer(address(this).balance);
    }

     function() payable public {
    }
}