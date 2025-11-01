// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract TieredNFT is ERC721, Ownable {
    enum Tier { Gold, Silver, Bronze }

    uint256 private _tokenIdCounter;
    mapping(uint256 => Tier) public tokenTier;

    constructor() ERC721("TieredNFT", "TIER") Ownable(msg.sender) {}

    function safeMint(address to, Tier tier) public onlyOwner returns (uint256) {
        uint256 tokenId = _tokenIdCounter;
        _tokenIdCounter++;
        tokenTier[tokenId] = tier;
        _safeMint(to, tokenId);
        return tokenId;
    }

    function getTier(uint256 tokenId) public view returns (Tier) {
        require(ownerOf(tokenId) != address(0), "Token does not exist");
        return tokenTier[tokenId];
    }
}
