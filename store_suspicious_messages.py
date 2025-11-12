"""
Store Suspicious Messages on Blockchain
This script reads suspicious messages from the ML model CSV and stores them on blockchain
"""

from web3 import Web3
import pandas as pd
import hashlib

print("=" * 60)
print("STORING SUSPICIOUS MESSAGES ON BLOCKCHAIN")
print("=" * 60)

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

if not w3.is_connected():
    print("❌ ERROR: Cannot connect to Ganache!")
    print("Make sure Ganache is running on http://127.0.0.1:7545")
    exit(1)

print("✓ Connected to Ganache")

# Contract address (updated after redeployment)
contract_address = '0x3B2bD66c48FADbcb0E63137B3958018494B9fB0B'

# Updated ABI with originalMessage field
contract_abi = [
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
        "inputs": [],
        "name": "getTotalMessages",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_messageHash", "type": "string"},
            {"internalType": "string", "name": "_originalMessage", "type": "string"},
            {"internalType": "string", "name": "_senderInfo", "type": "string"}
        ],
        "name": "storeMessageHash",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)
accounts = w3.eth.accounts

print(f"✓ Using account: {accounts[0]}")
print(f"✓ Contract address: {contract_address}\n")

# Load suspicious messages
try:
    df = pd.read_csv('suspicious_messages_with_hash.csv')
    print(f"✓ Loaded {len(df)} suspicious messages from CSV\n")
except FileNotFoundError:
    print("❌ ERROR: suspicious_messages_with_hash.csv not found!")
    print("Please run your ML model first to generate suspicious messages.")
    exit(1)

# Store each suspicious message
print("=" * 60)
print("STORING MESSAGES")
print("=" * 60)

stored_count = 0
for index, row in df.iterrows():
    try:
        # Prepare data
        message_hash = row['message_hash']
        original_message = str(row['message'])  # The actual suspicious message
        sender_info = f"Telegram Bot | Sender ID: {row['sender_id']} | Time: {row['timestamp']}"
        
        print(f"\n[{index + 1}/{len(df)}] Storing message...")
        print(f"  Original: {original_message}")
        print(f"  Hash: {message_hash[:20]}...")
        print(f"  Sender: {row['sender_id']}")
        
        # Store on blockchain
        tx_hash = contract.functions.storeMessageHash(
            message_hash,
            original_message,
            sender_info
        ).transact({
            'from': accounts[0],
            'gas': 500000
        })
        
        # Wait for transaction
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt['status'] == 1:
            print(f"  ✅ SUCCESS! Tx: {tx_hash.hex()[:20]}...")
            stored_count += 1
        else:
            print(f"  ❌ FAILED! Transaction reverted")
            
    except Exception as e:
        print(f"  ❌ ERROR: {str(e)}")
        continue

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"✅ Successfully stored: {stored_count}/{len(df)} messages")
print(f"📊 Total messages on blockchain: {contract.functions.getTotalMessages().call()}")
print("\n✅ You can now view these messages on the dashboard!")
print("   Open dashboard.html to see all suspicious messages with evidence")
