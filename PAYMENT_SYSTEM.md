# Phoenix Filter Bot - Payment System Documentation

Complete guide to the USDT payment system and premium benefits.

---

## Table of Contents

1. [Payment System Overview](#payment-system-overview)
2. [User Payment Flow](#user-payment-flow)
3. [Admin Verification Process](#admin-verification-process)
4. [Premium Benefits](#premium-benefits)
5. [Free vs Premium Comparison](#free-vs-premium-comparison)
6. [Configuration](#configuration)
7. [Commands Reference](#commands-reference)

---

## Payment System Overview

The Phoenix Filter Bot uses a **manual verification payment system** where users send USDT directly to your wallet addresses and admins verify the payment.

### Supported Cryptocurrencies

| Network | Coin | Address |
|---------|------|---------|
| **BSC (Binance Smart Chain)** | USDT | `0x58A07f2Ef69a4d7a0C20c0C6B079f059fdE2F669` |
| **Solana** | USDT | `AWDJkMbS4rBCTrzP2AkwfsEBKJobB4rTw2PE2oxb8h1r` |

### Available Plans

| Plan | Duration | Price | Features |
|------|----------|-------|----------|
| **Basic** | 1 Month | $2.99 | Unlimited searches, Priority support |
| **Standard** | 3 Months | $7.99 | All Basic + Ad-free + Custom filters |
| **Premium** | 1 Year | $19.99 | All Standard + Exclusive content + Early access |

---

## User Payment Flow

### Step 1: User Initiates Purchase

User sends `/buy` command to the bot.

```
User: /buy
Bot: Shows 3 plan options (Basic, Standard, Premium)
```

### Step 2: User Selects Plan

User clicks on their preferred plan button.

```
User: Clicks "🥉 Basic ($2.99)"
Bot: Shows payment method options (BSC or Solana)
```

### Step 3: User Selects Payment Method

User chooses between BSC or Solana.

```
User: Clicks "🔗 BSC (USDT)"
Bot: Displays wallet address and payment instructions
```

### Step 4: User Sends Payment

User opens their wallet and sends the exact amount to the provided address.

**Example for BSC:**
- Wallet: MetaMask, Trust Wallet, etc.
- Network: BSC (Binance Smart Chain)
- Token: USDT
- Amount: $2.99 USDT
- Recipient: `0x58A07f2Ef69a4d7a0C20c0C6B079f059fdE2F669`

### Step 5: User Confirms Payment

After sending the transaction, user clicks "✅ I've Sent Payment" button.

```
User: Clicks "✅ I've Sent Payment"
Bot: Stores payment as "awaiting_verification"
Bot: Notifies admin with payment details
```

### Step 6: Admin Verifies Payment

Admin checks the blockchain to verify the payment was received, then approves it.

```
Admin: /approve_payment <payment_id>
Bot: Activates premium for user
Bot: Notifies user of successful activation
```

---

## Admin Verification Process

### Checking Pending Payments

Admins receive automatic notifications when users submit payments. The notification includes:

```
🔔 **New Payment Received**

Payment ID: abc12345
User: @username
User ID: 123456789
Plan: Basic
Amount: $2.99
Duration: 30 days

Please verify the payment on the blockchain and approve using:
/approve_payment abc12345

Or reject with:
/reject_payment abc12345
```

### Verifying on Blockchain

**For BSC Payments:**
1. Go to [BscScan.com](https://bscscan.com)
2. Search for the wallet address: `0x58A07f2Ef69a4d7a0C20c0C6B079f059fdE2F669`
3. Look for incoming USDT transactions matching the amount and user
4. Verify the transaction is confirmed (green checkmark)

**For Solana Payments:**
1. Go to [Solscan.io](https://solscan.io)
2. Search for the wallet address: `AWDJkMbS4rBCTrzP2AkwfsEBKJobB4rTw2PE2oxb8h1r`
3. Look for incoming USDT transactions matching the amount
4. Verify the transaction is confirmed

### Approving Payment

Once verified on the blockchain:

```
/approve_payment <payment_id>
```

**Example:**
```
/approve_payment abc12345
```

**Result:**
- ✅ Premium is activated for the user
- ✅ User receives notification of activation
- ✅ Payment status changes to "approved"
- ✅ Premium duration is added to their account

### Rejecting Payment

If payment cannot be verified:

```
/reject_payment <payment_id>
```

**Example:**
```
/reject_payment abc12345
```

**Result:**
- ❌ Payment is marked as rejected
- ❌ User is notified to contact admin
- ❌ No premium is activated

---

## Premium Benefits

### What Premium Users Get

Premium users enjoy significantly enhanced features and higher limits:

**Search & Discovery:**
- ✅ Unlimited daily searches (vs. 20 for free users)
- ✅ Access to all file types
- ✅ Custom search filters
- ✅ Advanced search options

**Downloads & Storage:**
- ✅ Unlimited daily downloads (vs. 5 for free users)
- ✅ Access to 5GB files (vs. 100MB for free users)
- ✅ 100GB storage space (vs. 500MB for free users)
- ✅ 10 concurrent downloads (vs. 1 for free users)

**Features:**
- ✅ Batch operations (download multiple files at once)
- ✅ Custom filters for organized content
- ✅ Priority support (faster response times)
- ✅ Ad-free experience
- ✅ Early access to new features
- ✅ Exclusive content access

### Checking Premium Status

Users can check their premium status with:

```
/myplan
```

**Output:**
```
✅ **Your Premium Status**

💎 Status: Active
📅 Expires: 2025-11-14
⏰ Days Left: 365
👥 Referrals: 5
```

### Viewing Benefits

Users can see their current benefits and usage:

```
/benefits
```

**Output:**
```
💎 **PREMIUM**

✅ Unlimited daily searches
✅ Unlimited daily downloads
✅ Access to 5GB files
✅ 100GB storage space
✅ 10 concurrent downloads
✅ Batch operations
✅ Custom filters
✅ Priority support
✅ Ad-free experience
✅ Early access to new features

**Today's Usage:**
• Searches: 5/Unlimited
• Downloads: 2/Unlimited

**Remaining Today:**
• Searches: Unlimited
• Downloads: Unlimited
```

---

## Free vs Premium Comparison

| Feature | Free | Premium |
|---------|------|---------|
| **Daily Searches** | 20 | Unlimited |
| **Daily Downloads** | 5 | Unlimited |
| **Max File Size** | 100MB | 5GB |
| **Storage Space** | 500MB | 100GB |
| **Concurrent Downloads** | 1 | 10 |
| **Batch Operations** | ❌ | ✅ |
| **Custom Filters** | ❌ | ✅ |
| **Priority Support** | ❌ | ✅ |
| **Ad-Free** | ❌ | ✅ |
| **Early Access** | ❌ | ✅ |
| **Exclusive Content** | ❌ | ✅ |

---

## Configuration

### Environment Variables

Add these to your deployment platform's environment variables:

```
# Payment Configuration
PAYMENT_ENABLED=True
USDT_BEP20_ADDRESS=0x58A07f2Ef69a4d7a0C20c0C6B079f059fdE2F669
USDT_SOL_ADDRESS=AWDJkMbS4rBCTrzP2AkwfsEBKJobB4rTw2PE2oxb8h1r
PAYMENT_TIMEOUT_MINUTES=30
```

### Customizing Wallet Addresses

To use different wallet addresses, update the environment variables:

```
USDT_BEP20_ADDRESS=your_new_bsc_address
USDT_SOL_ADDRESS=your_new_solana_address
```

### Disabling Payment System

To disable the payment system temporarily:

```
PAYMENT_ENABLED=False
```

---

## Commands Reference

### User Commands

| Command | Description |
|---------|-------------|
| `/buy` | Browse and purchase premium plans |
| `/plan` | View available premium plans |
| `/myplan` | Check current premium status |
| `/benefits` | View your benefits and usage limits |
| `/refer` | Get your referral link and stats |

### Admin Commands

| Command | Description |
|---------|-------------|
| `/approve_payment <id>` | Approve a pending payment |
| `/reject_payment <id>` | Reject a pending payment |
| `/add_premium <user_id> <days>` | Manually add premium (no payment needed) |
| `/remove_premium <user_id>` | Remove premium from user |

---

## Database Schema

### Payments Collection

```javascript
{
  payment_id: "abc12345",           // Unique payment identifier
  user_id: 123456789,               // Telegram user ID
  plan: "basic",                    // Plan type: basic, standard, premium
  price: 2.99,                      // Price in USD
  days: 30,                         // Duration in days
  status: "approved",               // Status: pending, approved, rejected
  created_at: ISODate(...),         // Payment submission time
  verified_at: ISODate(...)         // Verification time (null if rejected)
}
```

### Users Collection (Premium Fields)

```javascript
{
  user_id: 123456789,
  is_premium: true,                 // Premium status
  premium_until: ISODate(...),      // Expiry date/time
  referral_count: 5,                // Number of successful referrals
  // ... other user fields
}
```

### Search Logs Collection

```javascript
{
  user_id: 123456789,
  date: ISODate(...),               // Date (YYYY-MM-DD)
  count: 15                         // Number of searches today
}
```

### Download Logs Collection

```javascript
{
  user_id: 123456789,
  date: ISODate(...),               // Date (YYYY-MM-DD)
  count: 3                          // Number of downloads today
}
```

---

## Troubleshooting

### Payment Not Appearing

**Problem:** User sent payment but it's not showing in notifications

**Solutions:**
1. Check if payment was actually sent on the blockchain
2. Verify the wallet address is correct
3. Check if the transaction is confirmed
4. Ask user to send the transaction hash

### User Not Receiving Premium

**Problem:** Admin approved payment but user doesn't have premium

**Solutions:**
1. Verify payment ID is correct
2. Check if user exists in database
3. Check MongoDB connection
4. Restart the bot

### Wallet Address Issues

**Problem:** Users sending to wrong address

**Solutions:**
1. Double-check wallet addresses in config
2. Make sure addresses are clearly displayed in bot messages
3. Provide QR codes for easy scanning
4. Create a help command with wallet info

---

## Security Best Practices

1. **Verify Payments:** Always verify payments on the blockchain before approving
2. **Keep Addresses Safe:** Don't share private keys
3. **Monitor Wallets:** Regularly check wallet balances
4. **Backup Keys:** Keep secure backups of wallet private keys
5. **Limit Admin Access:** Only trusted users should have admin rights
6. **Log Everything:** All payments are logged for audit purposes

---

## Support

For payment-related issues or questions:

- Contact: **@ph0enix_web**
- Check blockchain explorers (BscScan, Solscan)
- Review payment logs in database
- Check bot logs for errors

---

**Last Updated:** November 14, 2025  
**Payment System Version:** 1.0.0
