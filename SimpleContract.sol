// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract SimpleContract{
    string public IPFS_Hash;
    constructor(){
        IPFS_Hash="";
    }
    function setIPFSHash(string memory hash) public{
        IPFS_Hash=hash;
    }

    function getIPFSHash() public view returns(string memory){
        return IPFS_Hash;
    } 

}
