from web3 import Web3
from solcx import compile_standard, install_solc
import json

print("=" * 60)
print("DEPLOYING MESSAGEHASHSTORAGE CONTRACT")
print("=" * 60)

# Install solidity compiler
print("\n1. Installing Solidity compiler...")
install_solc('0.8.0')

# Read the contract
print("2. Reading contract file...")
with open('contracts/MessageHashStorage.sol', 'r') as file:
    contract_source = file.read()

# Compile the contract
print("3. Compiling contract...")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"MessageHashStorage.sol": {"content": contract_source}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

# Get bytecode and ABI
bytecode = compiled_sol['contracts']['MessageHashStorage.sol']['MessageHashStorage']['evm']['bytecode']['object']
abi = compiled_sol['contracts']['MessageHashStorage.sol']['MessageHashStorage']['abi']

# Connect to Ganache
print("4. Connecting to Ganache...")
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

if not w3.is_connected():
    print("❌ ERROR: Cannot connect to Ganache!")
    print("Make sure Ganache is running on http://127.0.0.1:7545")
    exit(1)

print("✓ Connected to Ganache")

# Get account
accounts = w3.eth.accounts
deployer = accounts[0]
print(f"5. Deploying from account: {deployer}")

# Create contract
MessageHashStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Deploy
print("6. Sending deployment transaction...")
tx_hash = MessageHashStorage.constructor().transact({'from': deployer})

# Wait for transaction receipt
print("7. Waiting for transaction to be mined...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = tx_receipt.contractAddress

print("\n" + "=" * 60)
print("✅ CONTRACT DEPLOYED SUCCESSFULLY!")
print("=" * 60)
print(f"\n📍 Contract Address: {contract_address}")
print(f"📋 Transaction Hash: {tx_hash.hex()}")
print(f"⛽ Gas Used: {tx_receipt.gasUsed}")

# Save ABI to file for reference
with open('MessageHashStorage_ABI.json', 'w') as f:
    json.dump(abi, f, indent=2)
print(f"\n✓ ABI saved to MessageHashStorage_ABI.json")

# Update the address automatically
print(f"\n" + "=" * 60)
print("UPDATING CONTRACT ADDRESS IN FILES")
print("=" * 60)

import re

def update_contract_address(file_path, new_address):
    """Update contract address in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace old address
        old_pattern = r"(contract_address|CONTRACT_ADDRESS)\s*=\s*['\"]0x[a-fA-F0-9]{40}['\"]"
        
        def replacer(match):
            prefix = match.group(1)
            quote = "'" if "'" in match.group(0) else '"'
            return f"{prefix} = {quote}{new_address}{quote}"
        
        updated_content = re.sub(old_pattern, replacer, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✓ Updated {file_path}")
        return True
    except Exception as e:
        print(f"✗ Error updating {file_path}: {e}")
        return False

# Update files
files_to_update = [
    'index.html',
    'test_contract.py'
]

for file in files_to_update:
    update_contract_address(file, contract_address)

print("\n" + "=" * 60)
print("🎉 DEPLOYMENT COMPLETE!")
print("=" * 60)
print("\nNext steps:")
print("1. Open index.html in your browser")
print("2. Try storing a message")
print("3. See it appear on the blockchain!")
print("\n✓ You can also update your Jupyter notebook with this address:")
print(f"   contract_address = '{contract_address}'")
