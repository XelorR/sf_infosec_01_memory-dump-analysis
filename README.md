# Memory dump analysis report

As part of SF InfoSec courses homework assessment

## Preparing the environment

00. dump checksum
![](./img/00_dump-checksum.png)

```bash
sha256sum Win7-2515534d.vmem
```
> a3e7409d7aab43921b2e377787e042b52bb241837d5269e7a29ac3f4373a71d8  Win7-2515534d.vmem

01. clonning Volatility3
![](./img/02_clonning-volatility.png)

02. preparing dump isolation
```bash
mkisofs -output-charset utf-8 -o Win7-2515534d.vmem.iso Win7-2515534d.vmem
mkisofs -output-charset utf-8 -o volatility3.iso volatility3
```

03. running VM with mounted ISOs and ports passthrough
```bash
qemu-system-x86_64 -enable-kvm -smp 2 -m 4G -bios /usr/share/edk2/ovmf/OVMF_CODE.fd -drive file=kali-linux-2024.1-live-amd64.iso,format=raw,index=0,media=cdrom -drive file=Win7-2515534d.vmem.iso,format=raw,index=1,media=cdrom -drive file=volatility3.iso,format=raw,index=2,media=cdrom -nic hostfwd=tcp:127.0.0.1:9922-0.0.0.0:22,hostfwd=tcp:127.0.0.1:9980-0.0.0.0:80
```

04. boot Kali in forensic mode
![](./img/04_kali-selecting-forensic-mode.png)

05. dump and volatility mounted in VM read only (copied Volatility to $HOME later)
![](./img/05_dump-and-volatility-mounted.png)

06. installing ssh to control from host and to exchange files
![](./img/06_installing-ssh-in-vm.png)

07. host's file manager and terminal are connected
![](./img/07_file-manager-and-terminal-passthrough.png)

08. comparing checksum with initially checked - **THE SAME!!**
![](./img/08_checksum-again.png)

09. run Volatility
![](./img/09_volatility-running.png)


## Riddles and answers

### Scanning with Volatility V3

At first I was generating outputs of some commonly used commands, like this:

```python
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
```

[outputs](./outputs)

### Final: answering

#### 8.1

![8.1](img/8.1.png)

![8.1 answer](img/8.1_answer.png)

#### 8.2

![8.2](img/8.2.png)

![8.2 answer](img/8.2_answer.png)

#### 8.3

![8.3](img/8.3.png)

As I didn't find PID in Volatility3 dlllist, I just used Volatility2:
```bash
python2.7 ~/volatility/vol.py --profile=Win7SP1x64 -f /media/kali/Win7-2515534d.vmem/Win7-2515534d.vmem dlllist | less
```

And here it is:

![8.3 answer](img/8.3_answer.png)

[Volatility v2 dll list](outputs/05_dlllist_v2.txt)

And, finally, let's check one more time that sha256 sum is still the same:

![](img/11_checksum.png)

- [x] is the same