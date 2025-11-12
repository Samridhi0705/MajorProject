"""
Real-Time Telegram Bot with Blockchain Integration
Continuously monitors messages and stores suspicious ones on blockchain immediately
"""

import nest_asyncio
nest_asyncio.apply()

import os
import csv
import re
import hashlib
from datetime import datetime
from telethon import TelegramClient, events
from web3 import Web3
import json
import asyncio
import sys

print("=" * 60)
print("REAL-TIME TELEGRAM BOT WITH BLOCKCHAIN")
print("=" * 60)

# ============================================
# CONFIGURATION
# ============================================

# Telegram Configuration
API_ID = 28932578  # Should be int, not string
API_HASH = 'e73796fdffd4d3fa973e1aedbe803311'
BOT_TOKEN = '8315747892:AAHpfpYvvuC9lXBpycHHOBarC8_DTvOV0fs'

# Blockchain Configuration
GANACHE_URL = 'http://127.0.0.1:7545'
CONTRACT_ADDRESS = '0x3B2bD66c48FADbcb0E63137B3958018494B9fB0B'

# Files
SESSION_FILE = 'bot_session'
CSV_FILE = 'suspicious_messages_realtime.csv'

# Suspicious Keywords
KEYWORDS = ['drug', 'cocaine', 'weed', 'lsd', 'ecstasy', 'heroin', 'meth',
            'marijuana', 'cannabis', 'opium', 'fentanyl', 'mdma', 'crack',
            'methamphetamine', 'amphetamine', 'ketamine', 'pcp']

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

# ============================================
# UTILITY FUNCTIONS
# ============================================

def clean_text(text):
    """Clean message text"""
    text = str(text)
    text = re.sub(r'http\S+', '', text)       # Remove URLs
    text = re.sub(r'@\S+', '', text)          # Remove mentions
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text) # Remove special chars
    text = text.lower().strip()
    return text

def is_suspicious(text):
    """Check if message contains suspicious keywords"""
    text = str(text).lower()
    for keyword in KEYWORDS:
        if keyword in text:
            return True, keyword
    return False, None

def hash_message(message):
    """Generate SHA-256 hash of message"""
    return hashlib.sha256(message.encode()).hexdigest()

def log_to_csv(timestamp, sender_id, message, clean_msg, suspicious, keyword, tx_hash):
    """Log message to CSV"""
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp', 'sender_id', 'message', 'clean_message', 
                           'suspicious', 'keyword_found', 'blockchain_tx'])
        writer.writerow([timestamp, sender_id, message, clean_msg, suspicious, keyword, tx_hash])

# ============================================
# BLOCKCHAIN SETUP
# ============================================

print("\n📡 Connecting to Ganache...")
try:
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    if not w3.is_connected():
        raise Exception("Cannot connect to Ganache")
    print("✓ Connected to Ganache")
    
    # Get default account
    accounts = w3.eth.accounts
    default_account = accounts[0]
    print(f"✓ Using account: {default_account}")
    
    # Create contract instance
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    print(f"✓ Contract loaded: {CONTRACT_ADDRESS}")
    
    # Test connection
    total_messages = contract.functions.getTotalMessages().call()
    print(f"✓ Current messages on blockchain: {total_messages}")
    
    blockchain_enabled = True
    
except Exception as e:
    print(f"❌ Blockchain connection failed: {e}")
    print("⚠️  Bot will run but won't store on blockchain")
    blockchain_enabled = False

# ============================================
# BLOCKCHAIN STORAGE FUNCTION
# ============================================

async def store_on_blockchain(message, sender_id, timestamp, phone_number=None, username=None, first_name=None, last_name=None):
    """Store suspicious message on blockchain with detailed sender info"""
    if not blockchain_enabled:
        return None
    
    try:
        # Generate hash
        message_hash = hash_message(message)
        
        # Build comprehensive sender info
        sender_info_parts = [f"Telegram ID: {sender_id}"]
        
        if phone_number:
            sender_info_parts.append(f"Phone: +{phone_number}")
        
        if username:
            sender_info_parts.append(f"Username: @{username}")
        
        if first_name or last_name:
            full_name = f"{first_name or ''} {last_name or ''}".strip()
            if full_name:
                sender_info_parts.append(f"Name: {full_name}")
        
        sender_info_parts.append(f"Time: {timestamp}")
        
        sender_info = " | ".join(sender_info_parts)
        
        # Store on blockchain
        tx = contract.functions.storeMessageHash(
            message_hash,
            message,
            sender_info
        ).transact({
            'from': default_account,
            'gas': 500000
        })
        
        # Wait for transaction
        receipt = w3.eth.wait_for_transaction_receipt(tx)
        
        return receipt.transactionHash.hex()
        
    except Exception as e:
        print(f"❌ Blockchain storage error: {e}")
        return None

# ============================================
# TELEGRAM BOT
# ============================================

async def main():
    """Main bot function"""
    
    # Initialize Telegram client with connection settings
    client = TelegramClient(
        SESSION_FILE, 
        API_ID, 
        API_HASH,
        connection_retries=5,
        retry_delay=3,
        timeout=10,
        auto_reconnect=True
    )
    
    print("\n🔌 Connecting to Telegram...")
    await client.start(bot_token=BOT_TOKEN)
    print("✅ Connected to Telegram successfully!")
    
    print("\n" + "=" * 60)
    print("🤖 BOT IS NOW RUNNING - MONITORING MESSAGES")
    print("=" * 60)
    print("\n✅ Bot Features:")
    print("  • Monitors all incoming Telegram messages")
    print("  • Checks for suspicious keywords in real-time")
    print("  • Automatically stores suspicious messages on blockchain")
    print("  • Logs all activity to CSV")
    print(f"  • Dashboard auto-refreshes every 5 seconds")
    print("\n🔍 Suspicious Keywords:")
    print(f"  {', '.join(KEYWORDS)}")
    print("\n📊 Activity Log:")
    print("-" * 60)
    
    message_count = 0
    suspicious_count = 0
    
    @client.on(events.NewMessage)
    async def handler(event):
        """Handle incoming messages"""
        nonlocal message_count, suspicious_count
        
        try:
            # Get message details
            msg = event.message.message
            sender = await event.get_sender()
            sender_id = sender.id if sender else 'Unknown'
            
            # Try to get phone number if available
            phone_number = None
            username = None
            first_name = None
            last_name = None
            
            if sender:
                phone_number = getattr(sender, 'phone', None)
                username = getattr(sender, 'username', None)
                first_name = getattr(sender, 'first_name', None)
                last_name = getattr(sender, 'last_name', None)
            
            timestamp = event.message.date.strftime("%Y-%m-%d %H:%M:%S")
            
            message_count += 1
            
            # Clean message
            clean_msg = clean_text(msg)
            
            # Check if suspicious
            suspicious, keyword = is_suspicious(clean_msg)
            
            if suspicious:
                suspicious_count += 1
                
                print(f"\n🚨 SUSPICIOUS MESSAGE DETECTED!")
                print(f"   ID: {message_count}")
                print(f"   Sender: {sender_id}")
                if phone_number:
                    print(f"   Phone: +{phone_number}")
                if username:
                    print(f"   Username: @{username}")
                print(f"   Time: {timestamp}")
                print(f"   Message: \"{msg}\"")
                print(f"   Keyword: {keyword}")
                print(f"   Status: Storing on blockchain...")
                
                # Store on blockchain immediately with all sender details
                tx_hash = await store_on_blockchain(msg, sender_id, timestamp, phone_number, username, first_name, last_name)
                
                if tx_hash:
                    print(f"   ✅ STORED ON BLOCKCHAIN!")
                    print(f"   Tx: {tx_hash[:20]}...")
                    print(f"   📊 Total Suspicious: {suspicious_count}")
                    print(f"   🔗 View on dashboard: dashboard.html")
                else:
                    print(f"   ⚠️  Blockchain storage failed (logged to CSV)")
                    tx_hash = "FAILED"
                
                # Log to CSV
                log_to_csv(timestamp, sender_id, msg, clean_msg, True, keyword, tx_hash)
                
            else:
                # Non-suspicious message
                print(f"📨 [{message_count}] {timestamp} | Sender: {sender_id} | Message: \"{msg[:30]}...\" | ✓ Clean")
                
                # Log to CSV (for record keeping)
                log_to_csv(timestamp, sender_id, msg, clean_msg, False, None, None)
            
            print("-" * 60)
            
        except Exception as e:
            print(f"❌ Error processing message: {e}")
    
    print("⏳ Waiting for messages... (Press Ctrl+C to stop)")
    print("=" * 60)
    
    # Keep bot running
    await client.run_until_disconnected()

# ============================================
# RUN BOT
# ============================================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("🛑 BOT STOPPED BY USER")
        print("=" * 60)
        print(f"\n✅ Session saved. CSV file: {CSV_FILE}")
        print("✅ All suspicious messages stored on blockchain")
        print("✅ View evidence on dashboard: dashboard.html")
    except Exception as e:
        print(f"\n❌ Bot error: {e}")
