// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MessageHashStorage {
    
    struct MessageRecord {
        string messageHash;
        string originalMessage;  // Store the actual message for evidence
        uint256 timestamp;
        address sender;
        string senderInfo;
    }
    
    MessageRecord[] public messages;
    mapping(address => uint256[]) public senderMessages;
    
    event MessageStored(
        uint256 indexed messageId,
        string messageHash,
        address indexed sender,
        uint256 timestamp
    );
    
    function storeMessageHash(
        string memory _messageHash,
        string memory _originalMessage,
        string memory _senderInfo
    ) public returns (uint256) {
        uint256 messageId = messages.length;
        
        messages.push(MessageRecord({
            messageHash: _messageHash,
            originalMessage: _originalMessage,
            timestamp: block.timestamp,
            sender: msg.sender,
            senderInfo: _senderInfo
        }));
        
        senderMessages[msg.sender].push(messageId);
        
        emit MessageStored(messageId, _messageHash, msg.sender, block.timestamp);
        
        return messageId;
    }
    
    function getMessage(uint256 _messageId) public view returns (
        string memory messageHash,
        string memory originalMessage,
        uint256 timestamp,
        address sender,
        string memory senderInfo
    ) {
        require(_messageId < messages.length, "Message ID does not exist");
        MessageRecord memory record = messages[_messageId];
        return (record.messageHash, record.originalMessage, record.timestamp, record.sender, record.senderInfo);
    }
    
    function getAllMessages() public view returns (MessageRecord[] memory) {
        return messages;
    }
    
    function getTotalMessages() public view returns (uint256) {
        return messages.length;
    }
    
    function getMessagesBySender(address _sender) public view returns (uint256[] memory) {
        return senderMessages[_sender];
    }
}
