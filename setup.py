import subprocess
for e in range(1):
    subprocess.Popen(["python", "main.py", "-controlPort", str(1000 + e), "-socksPort", str(9050 + e), "itter", str(e)])