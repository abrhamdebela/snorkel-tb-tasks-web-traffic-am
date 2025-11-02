// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./LoyaltyNFT.sol";

contract NFTSale {
    IERC20 public immutable token;
    LoyaltyNFT public immutable nft;
    uint256 public constant PRICE = 100 * 10**18; // 100 tokens

    event NFTMinted(address indexed buyer, uint256 tokenId);

    constructor(address _token, address _nft) {
        token = IERC20(_token);
        nft = LoyaltyNFT(_nft);
    }

    function mintNFT() external {
        require(token.transferFrom(msg.sender, address(this), PRICE), "Token transfer failed");
        nft.safeMint(msg.sender);
        emit NFTMinted(msg.sender, nft.totalSupply() - 1);
    }
}
