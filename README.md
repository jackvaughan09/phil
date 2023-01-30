# phil

## Minimize the time requirement of audit report analysis through consolidation, processing, and indicators

### For Windows Users

1. You'll need to start out by downloading git bash <https://git-scm.com/downloads>

2. Then ensure that you have WSL 2 on your machine.

   1. Check to see if you have it:

  ```powershell
  wsl -l -v

  output:
  NAME        STATE        VERSION
  something   something       2 
  ```

   2. If this is not what you see, then you'll need to either upgrade or install wsl

      - If the wsl command failed, simply run  ```wsl --install```  in administrator powershell and skip the next part
      - If it didn't fail, but you have version 1, you'll need to upgrade.

   3. Upgrading WSL
   4.

### 1. Install Docker

- <https://docs.docker.com/get-docker/>

### 2. Clone phil git repo

- in a Bash terminal, run ```git clone https://www.github.com/hudnash/phil.git```
- if your system doesn't have native bash, get Git Bash, install it
  - <https://git-scm.com/downloads>

### 3. Create a ```data/zip``` folder in your ```phil``` directory

- add some zip folders from the audit website

### 4. run ```sh phil.sh``` in Bash/Git Bash
