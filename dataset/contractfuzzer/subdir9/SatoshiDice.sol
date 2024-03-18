pragma solidity ^0.4.18;

contract SatoshiDice {
    struct Bet {
        address user;
        uint256 block;
        uint256 cap;
        uint256 amount;
    }

    uint256 public constant FEE_NUMERATOR = 1;
    uint256 public constant FEE_DENOMINATOR = 100;
    uint256 public constant MAXIMUM_CAP = 100000;
    uint256 public constant MAXIMUM_BET_SIZE = 1e18;

    address owner;
    uint256 public counter = 0;
    mapping(uint256 => Bet) public bets;

    event BetPlaced(uint256 id, address user, uint256 cap, uint256 amount);
    event Roll(uint256 id, uint256 rolled);

    function SatoshiDice() public {
        owner = msg.sender;
    }

    function wager(uint256 cap) public payable {
        require(cap <= MAXIMUM_CAP);
        require(msg.value <= MAXIMUM_BET_SIZE);

        counter++;
        bets[counter] = Bet(msg.sender, block.number + 3, cap, msg.value);
        BetPlaced(counter, msg.sender, cap, msg.value);
    }

    function roll(uint256 id) public {
        Bet storage bet = bets[id];
        require(msg.sender == bet.user);
        require(block.number >= bet.block);

        bytes32 random = keccak256(block.blockhash(bet.block), id);
        uint256 rolled = uint256(random) % MAXIMUM_CAP;
        if (rolled < bet.cap) {
            uint256 payout = (bet.amount * MAXIMUM_CAP) / bet.cap;
            uint256 fee = (payout * FEE_NUMERATOR) / FEE_DENOMINATOR;
            payout -= fee;
            msg.sender.transfer(payout);
        }

        Roll(id, rolled);
        delete bets[id];
    }

    function fund() public payable {}

    function kill() public {
        require(msg.sender == owner);
        selfdestruct(owner);
    }
}
