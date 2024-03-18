pragma solidity ^0.4.26;

contract TranferInTwoPart {
    function transfer(address _to) payable {
        uint256 half = msg.value / 2;
        uint256 halfRemain = msg.value - half;

        _to.send(half);
        _to.send(halfRemain);
    }

    // Forward value transfers.
    function() {
        throw;
    }
}
