#!/usr/bin/python3

from subprocess import run, PIPE

commands = [
        "info",
        "pslist",
        "psscan",
        "pstree",
        "handles",
        "dlllist",
        "netstat",
        "netscan",
        "filescan",
        "registry.printkey",
        "hivescan",
        "hivelist",
        "cmdline",
        "malfind",
        ]

for i, command in enumerate(commands):
    print(f"\n\n{i:02} Running {command}")
    result = run([
                  "/home/kali/volatility3/vol.py",
                   "-f", "/media/kali/Win7-2515534d.vmem/Win7-2515534d.vmem",
                   f"windows.{command}",
                  ],
                 stdout=PIPE,
                 text=True,
                 )
    with open(f"/home/kali/Documents/{i:02d}_{command}.txt", "w") as f:
        f.write(result.stdout)
