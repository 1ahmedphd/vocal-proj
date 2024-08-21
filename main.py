from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from stem import Signal
from stem.control import Controller
import time
from datetime import datetime
import os
import argparse
import subprocess
import signal

start = datetime.now()
parser = argparse.ArgumentParser(description="Process some arguments.")
parser.add_argument('-controlPort', type=int, required=True, help='control port')
parser.add_argument('-socksPort', type=int, required=True, help='socks port')
parser.add_argument('-itter', type=int, required=True, help='itteration')
args = parser.parse_args()
# Set up Tor options for Firefox
tor_proxy = f"127.0.0.1:{args.socksPort}"
firefox_options = Options()
firefox_options.set_preference("network.proxy.type", 1)
firefox_options.set_preference("network.proxy.socks", "127.0.0.1")
firefox_options.set_preference("network.proxy.socks_port", args.socksPort)
firefox_options.set_preference("network.proxy.socks_remote_dns", True)
firefox_options.set_preference("places.history.enabled", False)
firefox_options.set_preference("privacy.clearOnShutdown.offlineApps", True)
firefox_options.set_preference("privacy.clearOnShutdown.passwords", True)
firefox_options.set_preference("privacy.clearOnShutdown.siteSettings", True)
firefox_options.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
firefox_options.set_preference("signon.rememberSignons", False)
firefox_options.set_preference("network.cookie.lifetimePolicy", 2)
firefox_options.set_preference("network.dns.disablePrefetch", True)
firefox_options.set_preference("network.http.sendRefererHeader", 0)
firefox_options.add_argument("--headless")

serv = Service("./geckodriver")

driver = webdriver.Firefox(options=firefox_options, service=serv)

def start_tor(config_file):
    try:
        subprocess.run(["tor", "-f", config_file], check=True)
        print("Tor started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Tor: {e}")

def is_tor_connected():
    try:
        with Controller.from_port(port=args.controlPort) as controller:  # Default control port for Tor Browser is 9151
            controller.authenticate()  # Provide the password here if required
            controller.signal(Signal.NEWNYM)  # Request a new identity
            return True
    except Exception:
        return False

def perform_action():
    try:
        driver.get("http://adfoc.us/8627851")
        print("\033[32m"+"accessed website")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/a/img")))
        print("\033[32m"+"element viewed")
    except Exception as e:
        print("\033[31m"+f"Error performing action: {e}")

def stop_tor():
    try:
        # Find the Tor process ID
        pid = subprocess.check_output(["pgrep", "tor"]).decode().strip()
        
        # Send SIGTERM to the process
        os.kill(int(pid), signal.SIGTERM)
        print("Tor stopped successfully.")
    except subprocess.CalledProcessError:
        print("Tor is not running.")
    except Exception as e:
        print(f"Failed to stop Tor: {e}")

def main():
    start_tor(f"./insts/torrc_{args.itter}")
    while not is_tor_connected():
        print("\033[33m"+"Waiting for Tor to connect...")
        time.sleep(1)  # Check every 1 second
    
    print("\033[32m"+"Tor is connected.")
    perform_action()
    stop_tor()
    end = datetime.now()
    print("\033[32m"+f"Done in {end-start}!")
    # Optionally, terminate the Tor Browser process after performing the action

if __name__ == "__main__":
    main()
