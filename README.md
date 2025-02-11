# Cult.World Multi Auto Referrals

## 🚀 UPGRADED Features
- **Smart Proxy Distribution**: 
  - Automatically calculates maximum accounts based on available proxies
  - Evenly distributes proxies across all referral codes
  - Prevents proxy overuse by limiting 2 accounts per proxy
- **Enhanced Progress Tracking**:
  - Real-time progress monitoring per referral
  - Beautiful colored console output
  - Detailed statistics during and after completion
- **Improved User Interface**:
  - Clear display of available resources
  - Automatic calculation of maximum possible accounts
  - Progress bars and status indicators

## Overview
This project automates wallet creation and referral signups for Cult.World using multiple referral codes and proxy support. Each wallet is registered under a randomly chosen referral code, and successful registrations are logged into separate files based on the referral code used.

## Core Features
- **Multiple Referral Support**: Uses referral codes from `refs.txt`
- **Smart Proxy Rotation**: Selects unused proxies from `proxies.txt` to avoid detection
- **Automatic Wallet Creation**: Generates new Ethereum wallets
- **Advanced Logging & Tracking**:
  - Color-coded status messages
  - Real-time progress updates
  - Separate wallet files per referral code
  - Detailed success/failure reporting
- **Error Handling**: Graceful handling of failures with automatic retry

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/kelliark/cultworld-autoref.git
   cd cultworld-autoref
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Prepare necessary files:
   - **refs.txt**: Add one referral code per line
   - **proxies.txt**: Add one proxy per line in `http://user:pass@proxy:port` format

## Usage
1. Run the script:
   ```sh
   python main.py
   ```
2. The script will:
   - Show available proxies and maximum possible accounts
   - Ask for desired accounts per referral
   - Automatically adjust if number exceeds safe limits
   - Begin wallet generation and registration

## Output Format
### Console Output
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generating Wallet #1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Wallet #1 Successfully Generated!
Address: 0xABC...DEF
IP: 192.168.1.1
Referred By: referral_code
Registration completed successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### File Output
Successfully registered wallets are saved in referral-specific files:
- Format: `referral_code.txt`
- Content: `private_key:wallet_address`

## Dependencies
- `requests`: HTTP requests handling
- `eth-account`: Ethereum wallet operations
- `colorama`: Colored console output
- `web3`: Web3 functionality

## Credits and Acknowledgments
- Original concept by [im-hanzou](https://github.com/im-hanzou)
- Enhanced and upgraded by the community

## Disclaimer
This tool is for educational purposes only. Use at your own risk.
