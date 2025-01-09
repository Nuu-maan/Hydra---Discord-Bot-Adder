import os
import requests
import time
import json
from colorama import Fore, Style, init
from tls_client import Session
from base64 import b64encode
from json import dumps
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

init(autoreset=True)
os.system('cls')

DATA_FOLDER = 'data'
class Logger:
    @staticmethod
    def timestamp():
        return datetime.now().strftime("%H:%M:%S")
    
    @staticmethod
    def info(message):
        print(f"{Fore.WHITE}[{Logger.timestamp()}] {Fore.BLUE}[INFO] {Style.RESET_ALL}{message}")
    
    @staticmethod
    def success(message):
        print(f"{Fore.WHITE}[{Logger.timestamp()}] {Fore.GREEN}[SUCCESS] {Style.RESET_ALL}{message}")
    
    @staticmethod
    def error(message):
        print(f"{Fore.WHITE}[{Logger.timestamp()}] {Fore.RED}[ERROR] {Style.RESET_ALL}{message}")
    
    @staticmethod
    def warning(message):
        print(f"{Fore.WHITE}[{Logger.timestamp()}] {Fore.YELLOW}[WARNING] {Style.RESET_ALL}{message}")

def solve_hcaptcha(captcha_rqdata=None, captcha_rqtoken=None, razorcap_api_key=None, proxy=None):
    api_url = "https://api.razorcap.xyz/create_task"
    result_url = "https://api.razorcap.xyz/get_result/"
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        'key': razorcap_api_key,
        'type': 'hcaptcha_basic',
        'data': {
            'sitekey': 'a9b5fb07-92ff-493f-86fe-352a2803b3df',
            'siteurl': 'discord.com',
            'proxy': f'http://{proxy}',
            'rqdata': captcha_rqdata if captcha_rqdata else ""
        }
    }

    try:
        Logger.info("Creating captcha task...")
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'error':
            Logger.error(f"Task creation failed: {data.get('message')}")
            return None
            
        task_id = data.get('task_id')
        if not task_id:
            raise ValueError("No task ID received")
            
        Logger.success(f"Task created with ID: {task_id}")

        # Poll for results
        max_attempts = 30
        attempt = 0
        while attempt < max_attempts:
            try:
                result_response = requests.get(f"{result_url}{task_id}")
                result_data = result_response.json()
                status = result_data.get('status')
                
                if status == 'solved':
                    Logger.success("Captcha solved successfully")
                    return result_data.get('response_key')
                elif status == 'error':
                    Logger.error(f"Solving failed: {result_data.get('message')}")
                    return None
                    
                Logger.info("Waiting for solution...")
                attempt += 1
                time.sleep(2)
                
            except Exception as e:
                Logger.error(f"Error checking result: {str(e)}")
                return None
                
        Logger.error("Timed out waiting for solution")
        return None
        
    except Exception as e:
        Logger.error(f"Task creation failed: {str(e)}")
        return None

thread_lock = Lock()

def get_xproperties(buildnum: int):
    properties = {
        "os": "Windows",
        "browser": "Discord Client",
        "release_channel": "discord",
        "client_version": "1.0.59",
        "os_version": "10.0.22621",
        "os_arch": "x64",
        "system_locale": "en-US",
        "client_build_number": buildnum,
        "native_build_number": 31409,
        "client_event_source": None,
        "design_id": 0
    }
    encoded_properties = b64encode(dumps(properties).encode()).decode()
    return encoded_properties

def format_locale(locale):
    locale_lang = locale.split('-')[0]
    formatted = f"{locale},{locale_lang};q=0.7"
    return formatted

properties = get_xproperties(187449)
locale = "pl-PL"

class Adder:
    def __init__(self, client_id):
        self.session = Session(client_identifier="chrome110")
        self.client_id = client_id
        self.connect_headers = {
            "authority": "discord.com",
            "method": "GET",
            "path": f"/api/v9/oauth2/authorize?client_id={client_id}&scope=bot%20applications.commands",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": format_locale(locale),
            "authorization": config['token'],
            "referer": "https://discord.com/channels/@me",
            "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": locale,
            "x-super-properties": properties
        }

    def add(self, server_id):
        url = f'https://discord.com/api/v9/oauth2/authorize?client_id={self.client_id}&scope=bot%20applications.commands&integration_type=0'
        headers = {
            "authority": "discord.com",
            "method": "POST",
            "path": f"/api/v9/oauth2/authorize?client_id={self.client_id}&scope=bot%20applications.commands",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": format_locale(locale),
            "authorization": config['token'],
            "content-type": "application/json",
            "origin": "https://discord.com",
            "referer": "https://discord.com/channels/@me",
            "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": locale,
            "x-super-properties": properties
        }
        payload = {
            'guild_id': server_id,
            'permissions': config['permission'],
            'authorize': True
        }

        max_retries = 10 
        retry_count = 0

        while retry_count < max_retries:
            try:
                Logger.info(f"Adding bot {self.client_id} to server {server_id}...")
                addreq = self.session.post(url=url, headers=headers, json=payload)
                
                if addreq.status_code != 200:
                    if 'captcha' in addreq.text:
                        captcha_rqdata = addreq.json().get('captcha_rqdata')
                        captcha_rqtoken = addreq.json().get('captcha_rqtoken')
                        Logger.warning("Captcha detected")
                        
                        key = solve_hcaptcha(
                            captcha_rqdata=captcha_rqdata,
                            captcha_rqtoken=captcha_rqtoken,
                            razorcap_api_key=config['razorcap_key'],
                            proxy=config['proxy']
                        )
                        
                        if key:
                            headers["X-Captcha-Key"] = key
                            headers["X-Captcha-Rqtoken"] = captcha_rqtoken
                            addreq = self.session.post(url, headers=headers, json=payload)
                            
                            if addreq.status_code == 200 and addreq.json().get('location') == 'https://discord.com/oauth2/authorized':
                                Logger.success(f"Bot added to server {server_id}")
                                break
                            else:
                                Logger.error("Failed to add bot after captcha")
                        else:
                            Logger.error("Captcha solving failed")
                    else:
                        Logger.error(f"Failed to add bot. Response: {addreq.text}")
                else:
                    if addreq.json().get('location') == 'https://discord.com/oauth2/authorized':
                        Logger.success(f"Bot added to server {server_id}")
                        break
                    else:
                        Logger.error(f"Failed to add bot. Response: {addreq.text}")

                break
            except Exception as e:
                retry_count += 1
                Logger.error(f"Failed to add bot (Attempt {retry_count}/{max_retries}): {str(e)}")
                if retry_count >= max_retries:
                    Logger.error(f"Max retries reached. Failed to add bot to server {server_id}")
                else:
                    Logger.warning("Retrying...")
                    time.sleep(2)

def print_banner():
    banner = f"""
    {Fore.CYAN}╔══════════════════════════════════════╗
    ║          Hydra Discord Bot Adder     ║
    ║               v1.0.0                 ║
    ╚══════════════════════════════════════╝
    {Style.RESET_ALL}
    """
    print(banner)

def main(server_id):
    try:
        for client_id in config.get('clientIds', []):
            add = Adder(client_id)
            add.add(server_id=server_id)
    except Exception as e:
        Logger.error(f"Exception in main thread for server {server_id}: {str(e)}")

if __name__ == '__main__':
    print_banner()
    
    try:
        config_path = os.path.join(DATA_FOLDER, 'config.json')
        config = json.load(open(config_path))
    except Exception as e:
        Logger.error(f"Failed to load config from {config_path}: {str(e)}")
        exit(1)
    
    if not all(k in config for k in ['token', 'razorcap_key', 'proxy', 'permission', 'clientIds', 'threads']):
        Logger.error("Missing required configuration fields in config.json")
        exit(1)
    
    try:
        guild_ids_path = os.path.join(DATA_FOLDER, 'guild_ids.txt')
        servers = open(guild_ids_path, 'r').read().splitlines()
        servers = [server for server in servers if len(server) >= 10]
    except Exception as e:
        Logger.error(f"Failed to load guild IDs from {guild_ids_path}: {str(e)}")
        exit(1)
    
    Logger.info(f"Loaded {len(servers)} servers and {len(config.get('clientIds', []))} client IDs")
    
    with ThreadPoolExecutor(max_workers=config['threads']) as executor:
        executor.map(main, servers)