from web3 import Web3
import json

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

print("=" * 60)
print("BLOCKCHAIN CONNECTION TEST")
print("=" * 60)

# Check connection
try:
    is_connected = w3.is_connected()
    print(f"✓ Connected to Ganache: {is_connected}")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    exit(1)

# Get accounts
accounts = w3.eth.accounts
print(f"✓ Available accounts: {len(accounts)}")
if accounts:
    print(f"  - Default account: {accounts[0]}")

# Contract details
contract_address = '0x3B2bD66c48FADbcb0E63137B3958018494B9fB0B'
print(f"\n✓ Testing contract at: {contract_address}")

# Check if contract exists
code = w3.eth.get_code(contract_address)
if code == b'' or code == b'\x00':
    print("✗ ERROR: No contract found at this address!")
    print("\nPossible solutions:")
    print("  1. Redeploy your contract in Remix/Ganache")
    print("  2. Update CONTRACT_ADDRESS in both Python and HTML files")
    print("  3. Make sure Ganache workspace is the same as when you deployed")
    exit(1)
else:
    print(f"✓ Contract code found (length: {len(code)} bytes)")

# Contract ABI (updated with originalMessage field)
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
try:
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    print("✓ Contract instance created")
except Exception as e:
    print(f"✗ Error creating contract instance: {e}")
    exit(1)

# Test getTotalMessages
print("\n" + "=" * 60)
print("TESTING CONTRACT FUNCTIONS")
print("=" * 60)

try:
    total = contract.functions.getTotalMessages().call()
    print(f"✓ getTotalMessages() returned: {total}")
except Exception as e:
    print(f"✗ Error calling getTotalMessages(): {e}")
    print("\nThis means the contract doesn't have this function or isn't deployed correctly.")
    exit(1)

# Test getAllMessages
try:
    messages = contract.functions.getAllMessages().call()
    print(f"✓ getAllMessages() returned: {len(messages)} messages")
    
    if len(messages) > 0:
        print("\nStored messages:")
        for i, msg in enumerate(messages[:5]):  # Show first 5
            print(f"\n  Message {i+1}:")
            print(f"    Hash: {msg[0][:20]}...")
            print(f"    Original Message: {msg[1]}")
            print(f"    Timestamp: {msg[2]}")
            print(f"    Sender: {msg[3]}")
            print(f"    Info: {msg[4]}")
    else:
        print("  (No messages stored yet)")
        
except Exception as e:
    print(f"✗ Error calling getAllMessages(): {e}")
    print("\nThis is the same error you're seeing in the web interface.")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("\nIf you see errors above:")
print("  1. Make sure your Ganache is running")
print("  2. Redeploy the MessageHashStorage contract")
print("  3. Update the contract address in both files if it changed")
