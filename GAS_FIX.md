# 🔧 Gas Limit Fix

## Problem Fixed
**Error**: "VM Exception while processing transaction: out of gas"

## Solution
Updated `index.html` to include a gas limit of 500,000 for storing messages.

## What Changed
```javascript
// Before (caused error):
.send({ from: accounts[0] })

// After (fixed):
.send({ 
    from: accounts[0],
    gas: 500000  // Sufficient gas for transaction
})
```

## How to Use Now

1. **Refresh your browser** (Ctrl + F5 or Cmd + Shift + R)
2. **Enter a message** in the input box
3. **Click "Store on Blockchain"**
4. ✅ **Success!** Message will be stored without gas errors

## Why This Happened
- Ganache has a default gas limit
- Complex transactions (storing strings) need more gas
- We now explicitly set 500,000 gas, which is plenty for storing messages

## Test It Now
Open `index.html` in your browser and try storing a message!
