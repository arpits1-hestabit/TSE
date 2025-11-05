
# DAY 1 — SYSTEM REVERSE ENGINEERING + NODE & TERMINAL MASTERING

## Learning outcomes
- Master terminal navigation and system inspection
- Deep understanding of PATH, environment variables, Node runtime

---

## Tasks (NO GUI — terminal only)

### 1) Identify & document (paste command + output)
Outputs to each command are pasted below.
- OS version-
    1. Using `cat /etc/os-release`
    - Output:![alt text](<../Attachments/Screenshot from 2025-11-04 11-31-26.png>)
    2. Using `lsb_release –a`
    - Output:
    ![alt text](<../Attachments/Screenshot from 2025-11-04 11-34-53.png>)
    3. Using `hostnamectl`
    - Output : ![alt text](<../Attachments/Screenshot from 2025-11-04 11-37-17.png>)
    
- Current shell
  - Command: `echo $SHELL`
  - Output:![alt text](<../Attachments/Screenshot from 2025-11-04 11-39-23.png>)

- Node binary path
  - Command: `which node`
  - Output:![alt text](<../Attachments/Screenshot from 2025-11-04 11-39-45.png>)
- NPM global installation path
  - Command: `npm root -g` (or `npm prefix -g`)
  - Output:![alt text](<../Attachments/Screenshot from 2025-11-04 11-40-43.png>)
    
- All PATH entries that include "node" or "npm"
  - Command: `echo $PATH | tr ':' '\n' | grep -Ei 'node|npm' || true`
  - Output: ![alt text](<../Attachments/Screenshot from 2025-11-04 12-02-52.png>)

---

### 2) Install & use NVM (Node Version Manager)
- Install NVM:
  - Command:
    ```
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash

    # then restart shell
    ```
- Verify:
  - `nvm --version`
    - Output: ![alt text](../Attachments/image.png)
- Switch versions:
  - Install LTS: `nvm install --lts`
    - Output: ![/Attachments/image1.png](../Attachments/image1.png)
  - Use LTS: `nvm use --lts`
    - Output: ![alt text](<../Attachments/image copy.png>)
  - Install latest: `nvm install node`
    - Output: ![alt text](<../Attachments/image copy 2.png>)
  - Use latest: `nvm use node`
    - Output: ![Attachments/image3.png](../Attachments/image3.png)

---


### 3) introspect.js
Created file `introspect.js` using the `nano` command.
Implementation:
  ![alt text](<../Attachments/Screenshot from 2025-11-04 12-42-32.png>)

File Content:
  ![alt text](../Attachments/Introspect.png)

### 4) STREAM vs BUFFER exercise (performance benchmark)
---

1. Created a large test file (50MB+) using terminal command `dd if=/dev/urandom of=bigfile.txt bs=1M count=100`

    2. Read file using both:
     - fs.readFile (Buffer) -
            ![alt text](<../Attachments/buffer.png>)
     - Stream (fs.createReadStream) - 
            ![alt text](../Attachments/stream.png)

2. Capture execution time + memory usage :-
  -  Execution and Memory time for Buffer.js and Stream.js -
      ![alt text](<../Attachments/image copy 3.png>)

