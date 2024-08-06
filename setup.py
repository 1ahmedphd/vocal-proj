import os
import stem.process
from stem.control import Controller
import time

TOR_PATH = '/usr/bin/tor'  # Path to the tor executable
BASE_SOCKS_PORT = 9050  # Starting port for SOCKS
BASE_CONTROL_PORT = 9051  # Starting port for control

def start_tor_instance(socks_port, control_port, data_dir):
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    tor_process = stem.process.launch_tor_with_config(
        config={
            'SocksPort': str(socks_port),
            'ControlPort': str(control_port),
            'DataDirectory': data_dir,
            'Log': 'NOTICE file /dev/null',  # Reduce logging to avoid disk usage
        },
        tor_cmd=TOR_PATH,
        init_msg_handler=lambda line: print(line) if 'Bootstrapped' in line else None,
    )
    
    return tor_process

def connect_to_control_port(control_port):
    controller = Controller.from_port(port=control_port)
    controller.authenticate()
    return controller

def main(num_instances):
    tor_instances = []
    for i in range(num_instances):
        socks_port = BASE_SOCKS_PORT + i
        control_port = BASE_CONTROL_PORT + i
        data_dir = f'tor_data_{i}'
        
        print(f'Starting Tor instance {i+1} on ports {socks_port} (SOCKS) and {control_port} (Control)')
        tor_process = start_tor_instance(socks_port, control_port, data_dir)
        tor_instances.append(tor_process)
        
        # Optional: connect to the control port
        controller = connect_to_control_port(control_port)
        print(f'Connected to Tor instance {i+1} control port')
        
        # You can perform additional actions using the controller here
        controller.close()
    
    try:
        # Keep the script running to keep Tor instances alive
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print('Shutting down Tor instances...')
        for tor_process in tor_instances:
            tor_process.terminate()

if __name__ == "__main__":
    num_instances = 500  # Number of Tor instances to run
    main(num_instances)
