import subprocess
for e in range(1):
    subprocess.Popen(["python3", "main.py", "-sock", str(9050 + e), "-itter", str(e)])