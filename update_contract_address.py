# Contract Address Update Helper
# Run this after deploying your contract to update all files

# Contract Address Update Helper
# Run this after deploying your contract to update all files

NEW_CONTRACT_ADDRESS = '0xaE036c65C649172b43ef7156b009c6221B596B8b'  # ← The working contract address

import re

def update_contract_address(file_path, new_address):
    """Update contract address in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace old address
        old_pattern = r'0x[a-fA-F0-9]{40}'
        updated_content = re.sub(old_pattern, new_address, content, count=1)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✓ Updated {file_path}")
        return True
    except Exception as e:
        print(f"✗ Error updating {file_path}: {e}")
        return False

if NEW_CONTRACT_ADDRESS == '0xYOUR_NEW_CONTRACT_ADDRESS_HERE':
    print("❌ Please update NEW_CONTRACT_ADDRESS with your deployed contract address!")
    print("\nSteps:")
    print("1. Deploy MessageHashStorage contract in Remix")
    print("2. Copy the deployed contract address")
    print("3. Paste it in line 4 of this file")
    print("4. Run this script again")
else:
    print("=" * 60)
    print("UPDATING CONTRACT ADDRESS")
    print("=" * 60)
    print(f"New address: {NEW_CONTRACT_ADDRESS}\n")
    
    # Update files
    files_to_update = [
        'index.html',
        'test_contract.py'
    ]
    
    for file in files_to_update:
        update_contract_address(file, NEW_CONTRACT_ADDRESS)
    
    print("\n✅ All files updated!")
    print("Now refresh your browser and try again.")
