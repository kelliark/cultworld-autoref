# Cult.World Multi Auto Referrals

## Overview
This project automates wallet creation and referral signups for Cult.World using multiple referral codes and proxy support. Each wallet is registered under a randomly chosen referral code, and successful registrations are logged into separate files based on the referral code used.

## Features
- **Multiple Referral Support**: Uses referral codes from `refs.txt`.
- **Proxy Rotation**: Selects unused proxies from `proxies.txt` to avoid detection.
- **Automatic Wallet Creation**: Generates new Ethereum wallets.
- **Logging & Tracking**:
  - Logs each created wallet along with the referral code used.
  - Saves registered wallets to separate text files named after their referral code.
- **Error Handling**: Skips failed registrations and continues running.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/multi-referral-proxy.git
   cd cultworld-autoref
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Prepare necessary files:
   - **refs.txt**: Add one referral code per line.
   - **proxies.txt**: Add one proxy per line in `http://user:pass@proxy:port` format.

## Usage
Run the script:
```sh
python main.py
```

## File Output
Each successfully registered wallet will be stored in a file named after the referral code used, e.g., `dquov4hraoo6.txt`.

## Dependencies
- `requests`
- `eth-account`
- `colorama`
- `web3`

## Credits and Acknowledgments
Special thanks to:
- [im-hanzou](https://github.com/im-hanzou) - For the inspiration and original concept
