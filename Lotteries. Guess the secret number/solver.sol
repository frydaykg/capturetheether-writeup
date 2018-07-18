pragma solidity ^0.4.24;

import "./challenge.sol";

contract GuessTheSecretNumberChallengeSolver {

    function solve(address contractToSolve) public payable {
        GuessTheSecretNumberChallenge c = GuessTheSecretNumberChallenge(contractToSolve);
        for(uint8 i=0; i < 256; i++) {
            if (keccak256(i) == 0xdb81b4d58595fbbbb592d3661a34cdca14d7ab379441400cbfa1b78bc447c365) {
                c.guess.value(1 ether)(i);
                msg.sender.transfer(address(this).balance);
                return;
            }
        }
        msg.sender.transfer(address(this).balance);
    }

     function() payable public {
    }
}