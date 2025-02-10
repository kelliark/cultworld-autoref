import json
import time
import requests
from eth_account import Account
from eth_account.messages import encode_defunct
import secrets
from web3.auto import w3
import random
import sys
from datetime import datetime
from colorama import init, Fore, Style

init()

def print_banner():
    print(f"{Fore.CYAN}  _____        _             __    \n"
          f" / ___/ _____ (_)____   ____/ /____\n"
          f" \\__ \\ / ___// // __ \\ / __  // __ \\ \n"
          f" ___/ // /__ / // / / // /_/ // /_/ /\n"
          f"/____/ \\___//_//_/ /_/ \\__,_/ \\____/\n"
          f"\nScindo | Cult.World Multi Auto Referrals{Style.RESET_ALL}")

def log_message(message, status="info"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_map = {
        "success": Fore.GREEN,
        "error": Fore.RED,
        "warning": Fore.YELLOW,
        "info": Fore.BLUE
    }
    color = status_map.get(status, Fore.BLUE)
    print(f"{color}[{timestamp}] {message}{Style.RESET_ALL}")

def load_list(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def save_wallet(ref_code, private_key, address):
    filename = f"{ref_code}.txt"
    with open(filename, 'a') as f:
        f.write(f"{private_key}:{address}\n")

def get_unused_proxy(proxies, used_proxies):
    available = list(set(proxies) - set(used_proxies))
    if not available:
        used_proxies.clear()
        available = proxies.copy()
    proxy = random.choice(available)
    used_proxies.add(proxy)
    return proxy

def create_wallet():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    return private_key, acct.address

def get_headers():
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://cult.world',
        'referer': 'https://cult.world/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    }

def get_challenge(address, proxy):
    url = "https://cults-apis-1181.ippcoin.com/auth/challenge"
    data = {"wallet_address": address}
    try:
        response = requests.post(url, headers=get_headers(), json=data, proxies={'http': proxy, 'https': proxy})
        if response.status_code == 200:
            return response.json().get('data', {}).get('challenge')
    except:
        return None

def sign_message(private_key, challenge):
    message = encode_defunct(text=challenge)
    signed_message = w3.eth.account.sign_message(message, private_key=private_key)
    return signed_message.signature.hex()

def login(address, challenge, signature, proxy, ref_code):
    url = "https://cults-apis-1181.ippcoin.com/auth/login"
    data = {"wallet_address": address, "challenge": challenge, "response": signature, "referral_code": ref_code}
    try:
        response = requests.post(url, headers=get_headers(), json=data, proxies={'http': proxy, 'https': proxy})
        return response.json()
    except:
        return None

def main():
    print_banner()
    proxies = load_list('proxies.txt')
    ref_codes = load_list('refs.txt')
    if not proxies or not ref_codes:
        log_message("Missing proxies or referral codes!", "error")
        return
    
    used_proxies = set()
    wallet_count = 0
    
    try:
        while True:
            wallet_count += 1
            proxy = get_unused_proxy(proxies, used_proxies)
            ref_code = random.choice(ref_codes)
            private_key, address = create_wallet()
            log_message(f"Created Wallet #{wallet_count} - Address: {address} - Using Referral: {ref_code}")
            challenge = get_challenge(address, proxy)
            if not challenge:
                log_message("Failed to get challenge, skipping wallet", "error")
                continue
            signature = sign_message(private_key, challenge)
            login_result = login(address, challenge, signature, proxy, ref_code)
            if login_result and login_result.get('status') == 200:
                save_wallet(ref_code, private_key, address)
                log_message(f"Wallet {wallet_count} registered successfully under referral {ref_code}!", "success")
    except KeyboardInterrupt:
        log_message(f"\nStopping... Total wallets: {wallet_count}", "warning")
        sys.exit(0)

if __name__ == "__main__":
    main()
