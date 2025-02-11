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
    print(rf"""
{Fore.CYAN}  _____        _             __    
 / ___/ _____ (_)____   ____/ /____
 \__ \ / ___// // __ \ / __  // __ \ 
 ___/ // /__ / // / / // /_/ // /_/ /
/____/ \___//_//_/ /_/ \__,_/ \____/

KELLIARK | Cult.World Multi Auto Referrals{Style.RESET_ALL}
""")

def log_message(wallet_count, address, ip, ref_code, status="info", message=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color_map = {
        "success": Fore.GREEN + Style.BRIGHT,
        "error": Fore.RED + Style.BRIGHT,
        "warning": Fore.YELLOW + Style.BRIGHT,
        "info": Fore.CYAN + Style.BRIGHT,
        "process": Fore.MAGENTA + Style.BRIGHT,
        "address": Fore.WHITE + Style.BRIGHT,
        "ip": Fore.BLUE + Style.BRIGHT,
        "referral": Fore.YELLOW + Style.NORMAL
    }
    
    if status == "process":
        print(f"\n{color_map['process']}━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"Generating Wallet #{wallet_count}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
    else:
        print(f"{color_map[status]}━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        if status == "success":
            print(f"Wallet #{wallet_count} Successfully Generated!")
        elif status == "error":
            print(f"Wallet #{wallet_count} Failed!")
        print(f"{color_map['address']}Address: {address}")
        print(f"{color_map['ip']}IP: {ip}")
        print(f"{color_map['referral']}Referred By: {ref_code}")
        if message:
            print(f"{color_map[status]}{message}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")

def get_ip_info(proxy):
    try:
        response = requests.get('http://ip-api.com/json', proxies={'http': proxy, 'https': proxy}, timeout=5)
        if response.status_code == 200:
            return response.json().get('query', 'Unknown')
    except:
        return "IP lookup failed"

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
        'accept-language': 'en-US,en;q=0.9',
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

def calculate_max_accounts(proxy_count, ref_count):
    # Distribute proxies evenly among referral codes
    # Each proxy can be used twice
    max_per_ref = (proxy_count * 2) // ref_count
    return max_per_ref

def get_user_input(proxy_count, ref_count):
    while True:
        try:
            max_possible = (proxy_count * 2) // ref_count
            
            print(f"\n{Fore.CYAN + Style.BRIGHT}Available Proxies: {proxy_count:,}")
            print(f"Maximum accounts per referral: {max_possible:,}")
            print(f"Total accounts possible: {max_possible * ref_count:,}{Style.RESET_ALL}")
            
            accounts = input(f"\n{Fore.WHITE + Style.BRIGHT}Enter number of accounts per referral (max {max_possible:,}): {Style.RESET_ALL}")
            accounts = int(accounts)
            
            if accounts <= 0:
                print(f"{Fore.RED + Style.BRIGHT}Please enter a number greater than 0{Style.RESET_ALL}")
                continue
                
            if accounts > max_possible:
                print(f"{Fore.YELLOW + Style.BRIGHT}Warning: Requested {accounts:,} accounts but maximum possible is {max_possible:,}")
                print(f"Adjusting to maximum possible: {max_possible:,}{Style.RESET_ALL}")
                accounts = max_possible
            
            return accounts
            
        except ValueError:
            print(f"{Fore.RED + Style.BRIGHT}Please enter a valid number{Style.RESET_ALL}")

def main():
    print_banner()
    proxies = load_list('proxies.txt')
    ref_codes = load_list('refs.txt')
    
    if not proxies or not ref_codes:
        log_message(0, "N/A", "N/A", "N/A", "error", "Missing proxies or referral codes!")
        return
    
    accounts_per_ref = get_user_input(len(proxies), len(ref_codes))
    
    print(f"\n{Fore.CYAN + Style.BRIGHT}Starting generation:")
    print(f"• {accounts_per_ref:,} accounts per referral")
    print(f"• {len(ref_codes)} referral codes")
    print(f"• Total accounts to generate: {accounts_per_ref * len(ref_codes):,}{Style.RESET_ALL}\n")
    
    used_proxies = set()
    wallet_count = 0
    ref_count = {ref: 0 for ref in ref_codes}  # Track accounts per referral
    
    try:
        while True:
            # Check if we've reached the target for all referrals
            if all(count >= accounts_per_ref for count in ref_count.values()):
                print(f"\n{Fore.GREEN + Style.BRIGHT}All referral targets completed!{Style.RESET_ALL}")
                break
                
            wallet_count += 1
            # Get referral code that hasn't reached max accounts
            available_refs = [ref for ref, count in ref_count.items() if count < accounts_per_ref]
            if not available_refs:
                break
            
            ref_code = random.choice(available_refs)
            proxy = get_unused_proxy(proxies, used_proxies)
            
            # Show generating process
            log_message(wallet_count, "", "", "", "process")
            
            private_key, address = create_wallet()
            ip_info = get_ip_info(proxy)
            
            challenge = get_challenge(address, proxy)
            if not challenge:
                log_message(wallet_count, address, ip_info, ref_code, "error", "Challenge request failed!")
                continue
                
            signature = sign_message(private_key, challenge)
            login_result = login(address, challenge, signature, proxy, ref_code)
            
            if login_result and login_result.get('status') == 200:
                save_wallet(ref_code, private_key, address)
                log_message(wallet_count, address, ip_info, ref_code, "success")
                ref_count[ref_code] += 1  # Increment successful registration count
            else:
                log_message(wallet_count, address, ip_info, ref_code, "error", "Registration failed!")
                
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW + Style.BRIGHT}Process stopped.")
        print(f"Progress per referral:")
        for ref, count in ref_count.items():
            print(f"Referral {ref}: {count}/{accounts_per_ref} accounts")
        print(f"Total wallets generated: {wallet_count}{Style.RESET_ALL}")
        sys.exit(0)
        
    # Show final statistics
    print(f"\n{Fore.GREEN + Style.BRIGHT}Generation Complete!")
    print(f"Progress per referral:")
    for ref, count in ref_count.items():
        print(f"Referral {ref}: {count}/{accounts_per_ref} accounts")
    print(f"Total wallets generated: {wallet_count}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
