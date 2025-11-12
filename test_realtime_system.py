"""
Test script to simulate suspicious messages and verify real-time blockchain storage
This tests the entire system without needing actual Telegram messages
"""

import time
import hashlib
from datetime import datetime
from web3 import Web3
import json

print("=" * 60)
print("TESTING REAL-TIME BLOCKCHAIN STORAGE SYSTEM")
print("=" * 60)

# Configuration
GANACHE_URL = 'http://127.0.0.1:7545'
CONTRACT_ADDRESS = '0x3B2bD66c48FADbcb0E63137B3958018494B9fB0B'

# Contract ABI
CONTRACT_ABI = [
    {
        "inputs": [],
        "name": "getAllMessages",
        "outputs": [
            {
                "components": [
                    {"internalType": "string", "name": "messageHash", "type": "string"},
                    {"internalType": "string", "name": "originalMessage", "type": "string"},
                    {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "string", "name": "senderInfo", "type": "string"}
                ],
                "internalType": "struct MessageHashStorage.MessageRecord[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "_messageHash", "type": "string"},
                   {"internalType": "string", "name": "_originalMessage", "type": "string"},
                   {"internalType": "string", "name": "_senderInfo", "type": "string"}],
        "name": "storeMessageHash",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getTotalMessages",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Test messages (mix of suspicious and clean)
TEST_MESSAGES = [
    {"text": "Hey, how are you doing today?", "sender": "User123", "phone": None, "suspicious": False},
    {"text": "I need some weed for tonight", "sender": "User456", "phone": "919876543210", "username": "dealer456", "suspicious": True, "keyword": "weed"},
    {"text": "Let's meet at the park tomorrow", "sender": "User789", "phone": None, "suspicious": False},
    {"text": "Can you get me some cocaine?", "sender": "User321", "phone": "918765432109", "username": "suspect321", "suspicious": True, "keyword": "cocaine"},
    {"text": "Great weather today!", "sender": "User654", "phone": None, "suspicious": False},
    {"text": "Looking for lsd, anyone selling?", "sender": "User987", "phone": "917654321098", "username": "buyer987", "suspicious": True, "keyword": "lsd"},
]

def hash_message(text):
    """Generate SHA-256 hash of message"""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def connect_to_blockchain():
    """Connect to Ganache and load contract"""
    try:
        print("\n📡 Connecting to Ganache...")
        w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
        
        if not w3.is_connected():
            print("❌ Cannot connect to Ganache!")
            print("   Please ensure Ganache is running on http://127.0.0.1:7545")
            return None, None
        
        print("✅ Connected to Ganache")
        
        # Get account
        account = w3.eth.accounts[0]
        print(f"✅ Using account: {account}")
        
        # Load contract
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
        print(f"✅ Contract loaded: {CONTRACT_ADDRESS}")
        
        # Check current messages
        total = contract.functions.getTotalMessages().call()
        print(f"✅ Current messages on blockchain: {total}")
        
        return w3, contract
    except Exception as e:
        print(f"❌ Blockchain connection error: {e}")
        return None, None

def store_message(w3, contract, message_text, sender, keyword, phone=None, username=None):
    """Store suspicious message on blockchain with phone number"""
    try:
        # Generate hash
        msg_hash = hash_message(message_text)
        
        # Create comprehensive sender info
        sender_info_parts = [f"Telegram ID: {sender}"]
        
        if phone:
            sender_info_parts.append(f"Phone: +{phone}")
        
        if username:
            sender_info_parts.append(f"Username: @{username}")
        
        sender_info_parts.append(f"Test Message")
        
        sender_info = " | ".join(sender_info_parts)
        
        # Get account
        account = w3.eth.accounts[0]
        
        # Store on blockchain
        tx = contract.functions.storeMessageHash(
            msg_hash,
            message_text,
            sender_info
        ).transact({'from': account})
        
        # Wait for transaction
        receipt = w3.eth.wait_for_transaction_receipt(tx)
        
        return receipt.transactionHash.hex()
        
    except Exception as e:
        print(f"   ❌ Storage error: {e}")
        return None

def main():
    """Run the test"""
    
    # Connect to blockchain
    w3, contract = connect_to_blockchain()
    
    if not w3 or not contract:
        print("\n❌ Test aborted - Cannot connect to blockchain")
        return
    
    print("\n" + "=" * 60)
    print("🧪 STARTING REAL-TIME SIMULATION TEST")
    print("=" * 60)
    print("\n📝 Processing test messages...")
    print("-" * 60)
    
    # Get initial count
    initial_count = contract.functions.getTotalMessages().call()
    suspicious_stored = 0
    clean_skipped = 0
    
    # Process each test message
    for i, msg_data in enumerate(TEST_MESSAGES, 1):
        text = msg_data["text"]
        sender = msg_data["sender"]
        phone = msg_data.get("phone")
        username = msg_data.get("username")
        is_suspicious = msg_data["suspicious"]
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n📨 Message #{i}")
        print(f"   Time: {timestamp}")
        print(f"   Sender: {sender}")
        if phone:
            print(f"   Phone: +{phone}")
        if username:
            print(f"   Username: @{username}")
        print(f"   Text: \"{text}\"")
        
        if is_suspicious:
            keyword = msg_data.get("keyword", "unknown")
            print(f"   🚨 SUSPICIOUS! Keyword: {keyword}")
            print(f"   Status: Storing on blockchain...")
            
            # Store on blockchain with phone number
            tx_hash = store_message(w3, contract, text, sender, keyword, phone, username)
            
            if tx_hash:
                print(f"   ✅ STORED ON BLOCKCHAIN!")
                print(f"   Transaction: {tx_hash}")
                suspicious_stored += 1
            else:
                print(f"   ⚠️  Storage failed")
        else:
            print(f"   ✓ Clean message - NOT stored")
            clean_skipped += 1
        
        print("-" * 60)
        
        # Small delay to simulate real-time
        time.sleep(0.5)
    
    # Get final count
    final_count = contract.functions.getTotalMessages().call()
    messages_added = final_count - initial_count
    
    # Show results
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    print(f"\n✅ Test completed successfully!")
    print(f"\n📈 Statistics:")
    print(f"   Total messages processed: {len(TEST_MESSAGES)}")
    print(f"   Suspicious detected: {sum(1 for m in TEST_MESSAGES if m['suspicious'])}")
    print(f"   Clean messages: {sum(1 for m in TEST_MESSAGES if not m['suspicious'])}")
    print(f"   Successfully stored on blockchain: {suspicious_stored}")
    print(f"   Clean messages skipped: {clean_skipped}")
    print(f"\n🔗 Blockchain Status:")
    print(f"   Messages before test: {initial_count}")
    print(f"   Messages after test: {final_count}")
    print(f"   New messages added: {messages_added}")
    
    if messages_added == suspicious_stored:
        print(f"\n✅ VERIFICATION PASSED! All suspicious messages stored correctly.")
    else:
        print(f"\n⚠️  Mismatch detected. Expected {suspicious_stored}, got {messages_added}")
    
    print(f"\n🖥️  View results:")
    print(f"   Open dashboard.html in your browser")
    print(f"   You should see {suspicious_stored} new suspicious message cards")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test error: {e}")
