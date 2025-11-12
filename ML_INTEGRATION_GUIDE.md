# 🚨 ML Model Integration - Storing Suspicious Messages as Evidence

## ✅ What Changed

The system now stores **original suspicious messages** (not just hashes) on the blockchain as evidence!

### 🔄 Updates Made:

1. **✅ Smart Contract Updated**
   - Added `originalMessage` field to store the actual message text
   - Now stores: Hash + Original Message + Metadata

2. **✅ New Python Script Created**
   - `store_suspicious_messages.py` - Reads from ML model CSV and stores on blockchain
   - Automatically includes Telegram sender ID and timestamp

3. **✅ Dashboard Enhanced**
   - Shows original suspicious message on each card
   - Click card to see full evidence details
   - Displays sender ID from Telegram bot

---

## 🚀 How to Use (Step-by-Step)

### **Step 1: Redeploy the Contract**

Since we updated the contract structure, you need to redeploy it:

```bash
python deploy_contract.py
```

This will:
- Compile the updated contract
- Deploy to Ganache
- Auto-update all files with new address

### **Step 2: Store Suspicious Messages**

After your ML model detects suspicious messages:

```bash
python store_suspicious_messages.py
```

This script will:
- Read `suspicious_messages_with_hash.csv`
- Store each suspicious message on blockchain with:
  - ✅ Original message text ("weed", "or cocaine", etc.)
  - ✅ Message hash (for verification)
  - ✅ Telegram sender ID
  - ✅ Original timestamp from Telegram
  - ✅ Blockchain timestamp

### **Step 3: View on Dashboard**

Open `dashboard.html` to see:
- **Cards showing actual suspicious messages**
- Each card displays the message preview
- Click any card to see FULL EVIDENCE:
  - 📝 Original suspicious message
  - 🔐 Hash for verification
  - 👤 Telegram sender ID
  - 📅 When it was sent
  - ⛓️ Blockchain proof

---

## 📊 What The Dashboard Shows

### **Card View (Grid):**
```
┌────────────────────────┐
│ ID: 3                  │
│ ⚠️ "or cocaine"       │
│ 📅 2025-10-24 07:00:19│
│ 👤 0x34F6a6...        │
│ Click for full details │
└────────────────────────┘
```

### **Detailed View (When Clicked):**
```
╔════════════════════════════════╗
║ MESSAGE DETAILS                ║
╠════════════════════════════════╣
║ ID: #3                         ║
║                                ║
║ ⚠️ SUSPICIOUS MESSAGE:         ║
║   "or cocaine"                 ║
║                                ║
║ Hash: 7bdda8bff4a42183...      ║
║                                ║
║ Detection Time:                ║
║   Local: 10/24/2025 7:00:19 AM║
║                                ║
║ Source: Telegram Bot           ║
║   Sender ID: 8432945463        ║
║   Original Time: 2025-10-24... ║
╚════════════════════════════════╝
```

---

## 🔄 Complete Workflow

### **1. Telegram Bot Collects Messages**
Your bot (in `ml.ipynb`) saves messages to `flagged_messages.csv`

### **2. ML Model Detects Suspicious**
ML model classifies messages:
- `suspicious=1` → Flagged as suspicious
- Saves to `suspicious_messages_with_hash.csv`

### **3. Store on Blockchain**
```bash
python store_suspicious_messages.py
```
Stores suspicious messages with full evidence

### **4. View Evidence**
Open `dashboard.html` → See all suspicious messages → Click for details

---

## 📁 Files Involved

| File | Purpose |
|------|---------|
| `contracts/MessageHashStorage.sol` | Updated smart contract with originalMessage field |
| `store_suspicious_messages.py` | **NEW!** Stores suspicious messages from ML model |
| `dashboard.html` | Updated to display original messages |
| `deploy_contract.py` | Redeploys updated contract |
| `suspicious_messages_with_hash.csv` | Input file (from ML model) |

---

## 🎯 Example: Your Current Data

From your CSV, you have 3 suspicious messages:

1. **"weed"** - From sender 8432945463 at 2025-10-24 06:55:03
2. **"weed"** - From sender 8432945463 at 2025-10-24 07:00:15
3. **"or cocaine"** - From sender 8432945463 at 2025-10-24 07:00:19

After running `store_suspicious_messages.py`, all 3 will be stored on blockchain with full evidence!

---

## ⚖️ Legal Evidence Features

This system creates **tamper-proof evidence** because:

✅ **Original message** is stored (not just hash)
✅ **Sender ID** is preserved from Telegram
✅ **Timestamp** shows when message was sent
✅ **Hash** proves message integrity
✅ **Blockchain** makes it immutable
✅ **Dashboard** provides easy access for review

Perfect for:
- Law enforcement investigations
- Evidence collection
- Audit trails
- Compliance reporting

---

## 🔧 Quick Commands

```bash
# 1. Redeploy contract (REQUIRED - do this first!)
python deploy_contract.py

# 2. Store suspicious messages
python store_suspicious_messages.py

# 3. Test the contract
python test_contract.py

# 4. Run ML model to get suspicious messages
# (Run cells in ml.ipynb)
```

---

## ⚠️ IMPORTANT: Must Redeploy!

Since we changed the contract structure, you MUST:

1. **Run `python deploy_contract.py`** (This redeploys with new structure)
2. **Then run `python store_suspicious_messages.py`** (This stores your ML data)
3. **Open `dashboard.html`** (See the results!)

---

## 🎉 Result

You now have a complete evidence system that:
- ✅ Captures suspicious Telegram messages
- ✅ Stores them immutably on blockchain
- ✅ Displays them with full context
- ✅ Provides audit trail for investigations
- ✅ Shows sender ID and timestamps
- ✅ Verifiable with cryptographic hashes

**Ready to store your suspicious messages? Run the commands above!** 🚀
