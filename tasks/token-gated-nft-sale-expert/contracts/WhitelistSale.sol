// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
import "./TieredNFT.sol";

contract WhitelistSale {
    IERC20 public immutable token;
    TieredNFT public immutable nft;
    bytes32 public merkleRoot;

    uint256 public saleStart;
    uint256 public saleEnd;

    // Tier pricing in tokens (with 18 decimals)
    uint256 public constant GOLD_PRICE = 500 * 10**18;
    uint256 public constant SILVER_PRICE = 200 * 10**18;
    uint256 public constant BRONZE_PRICE = 50 * 10**18;

    // Max supply per tier
    uint256 public constant GOLD_MAX = 2;
    uint256 public constant SILVER_MAX = 5;
    uint256 public constant BRONZE_MAX = 10;

    // Current supply per tier
    uint256 public goldMinted;
    uint256 public silverMinted;
    uint256 public bronzeMinted;

    event NFTMinted(address indexed buyer, uint256 tokenId, TieredNFT.Tier tier);
    event RefundIssued(address indexed user, uint256 amount);

    constructor(address _token, address _nft, bytes32 _merkleRoot, uint256 _saleStart, uint256 _saleEnd) {
        token = IERC20(_token);
        nft = TieredNFT(_nft);
        merkleRoot = _merkleRoot;
        saleStart = _saleStart;
        saleEnd = _saleEnd;
    }

    function mintNFT(TieredNFT.Tier tier, bytes32[] calldata merkleProof) external {
        require(block.timestamp >= saleStart && block.timestamp <= saleEnd, "Sale not active");

        // Verify whitelist
        bytes32 leaf = keccak256(abi.encodePacked(msg.sender));
        require(MerkleProof.verify(merkleProof, merkleRoot, leaf), "Not whitelisted");

        // Get price and check supply
        uint256 price;
        if (tier == TieredNFT.Tier.Gold) {
            require(goldMinted < GOLD_MAX, "Gold tier sold out");
            price = GOLD_PRICE;
            goldMinted++;
        } else if (tier == TieredNFT.Tier.Silver) {
            require(silverMinted < SILVER_MAX, "Silver tier sold out");
            price = SILVER_PRICE;
            silverMinted++;
        } else {
            require(bronzeMinted < BRONZE_MAX, "Bronze tier sold out");
            price = BRONZE_PRICE;
            bronzeMinted++;
        }

        // Transfer tokens and mint NFT
        require(token.transferFrom(msg.sender, address(this), price), "Token transfer failed");
        uint256 tokenId = nft.safeMint(msg.sender, tier);
        emit NFTMinted(msg.sender, tokenId, tier);
    }

    function requestRefund(uint256 amount) external {
        require(token.transfer(msg.sender, amount), "Refund failed");
        emit RefundIssued(msg.sender, amount);
    }
}
