import os
import subprocess

# Number of Tor instances to create
num_instances = 500

# Base directories for Tor instances
base_dir = os.path.expanduser("~/tor-instances")
os.makedirs(base_dir, exist_ok=True)

# Template for the torrc configuration file
torrc_template = """
SocksPort {socks_port}
ControlPort {control_port}
DataDirectory {data_directory}
"""

# Function to create configuration files and directories
def create_tor_instance(instance_num):
    instance_dir = os.path.join(base_dir, f"tor-instance{instance_num}")
    data_dir = os.path.join(instance_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    socks_port = 9050 + instance_num
    control_port = 10000 + instance_num

    torrc_content = torrc_template.format(
        socks_port=socks_port,
        control_port=control_port,
        data_directory=data_dir
    )

    torrc_path = os.path.join(instance_dir, "torrc")
    with open(torrc_path, "w") as f:
        f.write(torrc_content)
    
    return instance_dir, torrc_path
additional_script_path = os.path.expanduser("~/vocal-proj-termux/main.py")

# Create instances and start them
for i in range(num_instances):
    instance_dir, torrc_path, socks_port, control_port = create_tor_instance(i)
    # Start Tor instance
    subprocess.Popen(["tor", "-f", torrc_path])
    # Run the additional Python script
    subprocess.Popen(["python", additional_script_path, "-socksPort",str(9050+i), "-controlPort",str(10000 + i)])

print(f"{num_instances} Tor instances have been started.")
