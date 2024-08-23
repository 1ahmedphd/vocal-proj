for e in range(500):
    with open(f"./insts/torrc_{e}", "w+") as fp:
        fp.write(f"""Bridge obfs4 146.70.143.174:59254 6C3B46CAAF0185C65BCC09B610F218BE8E560B84 cert=B/Nz4IniTpHTkeOyX6Go0mo0ECDAWkjO3bLgR7xx9SGkVb6MHG+NLu5n+LZQSXSjdtdFIA iat-mode=0
Bridge obfs4 45.142.181.131:42069 6EBCF6B02DA2B982F4080A7119D737366AFB74FA cert=9HyWH/BCwWzNirZdTQtluCgJk+gFhpOqydIuyQ1iDvpnqsAynKF+zcPE/INZFefm86UlBg iat-mode=0
UseBridges 1
SOCKSPort {9050 + e}
ControlPort {1000 + e}""")
