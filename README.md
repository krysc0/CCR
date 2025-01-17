# CCR Resources
* [Intro to CCR course on UBLearns](https://ublearns.buffalo.edu/d2l/le/discovery/view/course/209035)

# Prerequisites
* You have to be connected to the UB network to access the CCR. If you're on campus, connecting to Eduroam works. If off campus, connect to the [UB VPN via Cisco Secure Client](https://www.buffalo.edu/ubit/service-guides/connecting/vpn/computer.html).
* The CCR uses LINUX as the operating system. You need to know and use [UNIX commands](https://www.geeksforgeeks.org/linux-commands-cheat-sheet/) in the ssh-agent and in the CCR OnDemand portal. 
* You'll use [Slurm commands](https://hpc.nmsu.edu/discovery/slurm/commands/) to submit job scripts

# Note
* Replace {UBIT} with your own ubit name, {GITHUBusername} with your github username, {CCRusername} with your CCR user name (usually the same as your UBIT)
* In Windows, home ~ refers to the folder `C:\Users\{windows_username}`

# Logging in to the CCR
You have two options for logging in
* SSH agent
* OnDemand portal
  
Both of these options allow you to submit jobs to clusters, manage files etc. Using the OnDemand portal to upload files is easy but can create issues keeping track of old and new versions of files. Once you log in, navigate to the `Files` then `Home Directory` at the top of the page to manage files. You can start an interactive session which gives a graphical user interface to interact with the CCR. For more information, see using the [OnDemand portal](https://docs.ccr.buffalo.edu/en/latest/portals/ood/). 

## Before your first log in using the SSH
Detailed instructions to complete the steps below can be followed from the [CCR](https://docs.ccr.buffalo.edu/en/latest/hpc/login/#connecting-with-ssh) or [Github](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
1. Generate a SSH key pair (public and private)
```bash
ssh-keygen -t ed25519 -C "{UBIT}@buffalo.edu"
```
* You will be prompted to enter file in which to save the key. To use the default location, /c/Users/{windows_username}/.ssh/id_ed25519, press `Enter`.
* You'll be prompted to create a SSH passphrase. Create something memorable. Be careful with spelling. You'll need to use this passphrase each time to get connceted to the CCR.
2. Add the private SSH key to the SSH agent
```bash
eval "$(ssh-agent -s)"
```
3. Add the public SSH key to the CCR Identity Management Portal 
This may take up to 30 minutes to allow you to log in
* Open the public key located at ~/.ssh/id_ed25519.pub and copy the contents from there 
`OR` 
* In the ssh agent use cat to view the contents of the file and copy the contents from there
```bash
cat ~/.ssh/id_ed25519.pub
```
* Login to the [CCR IDM portal](https://idm.ccr.buffalo.edu/auth/login)
* Click on SSH Keys in the left navigation menu
* Click on the "New SSH Key" button, paste the contents of your public key in the text box, and click "Add"

## Logging in regularly
``` bash
ssh {CCRusername}@vortex.ccr.buffalo.edu
```
* The very first time you log in you will be told the authenticity of the host can't be ebstablished and asked if you want to continue connecting. Enter `yes` to continue.
* Each time you want to access this CCR login node you will need to enter the SSH passphrase you created for the key.
# Transferring Files to the CCR
There's lots of ways. Choose whatever works best for you. 
Information can be found [here](https://docs.ccr.buffalo.edu/en/latest/hpc/data-transfer/)
I recommend using Github because it manages file versions and handles data conflicts well.

## Using Github for file management 
### Generate SSH key
``` bash
ssh-keygen -t ed25519 -C "{UBIT}@buffalo.edu"
```
Press enter to save ssh key to default file. Then enter a passphrase (please create a passphrase!)
### Add SSH key to the ssh-agent
``` bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```
Should say identity added and the location
e.g.
Identity added: /user/{UBIT}/.ssh/id_ed25519 ({UBIT}@buffalo.edu)

### Add SSH public-key to your Github
1. Use `cat` to view the contents of the file and copy the contents from there
``` bash
cat ~/.ssh/id_ed25519.pub
```
2. Copy and paste that whole line to [Github](https://github.com/settings/keys) > Settings > SSH and GPG keys

### Test SSH Connection
``` bash
ssh -T git@github.com
```
Ignore the warning. Type `yes`.

### Clone Repository into your folder on CCR
``` bash
git clone --branch {branch} git@github.com:{GITHUBusername}/repositoryname
```

### Maintaining file management
Recommended: make all changes on your local PC only to avoid merge conflicts
``` bash
git pull origin {branch}
```
Other commands such as `git push` and `git stash` will come in handy. You can find useful git commands [here](https://git-scm.com/docs)

# Running code with a slurm script
Prequisite
* You should already be logged in to the CCR 

## Simplest Example using "Hello World"
1. Create a python file to print "Hello World". Vim is just one of the Linux default text editors.
``` bash
vim hello.py
```
2. Press `i` to set mode to insert and write to the file
3. File contents should look something like this
``` python
#!/usr/bin/env python3
print("Hello World")
```
4. Press `esc` to exit insert mode. Type `:wq` to save the file and quit the text editor
5. Back on command line, create slurm script and open it in a text editor. 
``` bash
vim run.sh
```
6. Write to the file to submit a job to a debug node on the CCR.
``` bash
#!/bin/bash
#SBATCH --partition=debug
#SBATCH --qos=debug
python  ./hello.py 
```
7. Back on the command line, submit the job
``` bash
sbatch run.sh
```
8. View the output file
Tip: Pressing `Tab` autocompletes file names within the directory
```bash
cat {slurm-jobid.out}
```

## Simple examle using Gurobi
1. Download the file knapsack.py to your local computer
2. Use `scp` in the SSH agent to copy the file from your computer to the CCR (must be connected to UB network for this to work)
Tip: If your folder name contains whitespaces wrap the folder name in single quotation marks. For example, 'CCR Workshop'/knapsack.py
```bash
scp -v {local-path-to-file} {CCRusername}@vortex.ccr.buffalo.edu.edu:/user/{CCRusername}/{CCR-path-to-file}/.
```
3. Log into the CCR
``` bash
ssh {CCRusername}@vortex.ccr.buffalo.edu
```
4. View the `knapsack.py` file in the text editor to check what modules we need to load
```bash
vim knapsack.py
```
5. Check the module dependecies
``` bash
module spider gurobi
```
4. Create a slurm script to run the gurobi file
```bash
vim test.sh
```
5. Add slurm commands to the slurm script.
``` bash
#!/bin/bash

#SBATCH --cluster=ub-hpc
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute
#SBATCH --mail-user={UBIT}@buffalo.edu
#SBATCH --mail-type=end
#SBATCH --time=00:03:00
#SBATCH --job-name="knapsack"
#SBATCH --output=knapsack.out
#SBATCH --error=knapsack.err
#SBATCH --ntasks=1
#SBATCH --mem=64M
```
6. Add module loads to the slurm script
```bash
module load gcccore/11.2.0
module load gurobi/10.0.1
```
7. Add instructions to run the python file to the slurm script
``` bash
python ./knapsack.py
```
8. Back on command line, run the slurm script
``` bash
sbatch test.sh
```
9. View output of the run
```bash
cat knapsack.out
```
Alternatively, if the run was not succesful error codes would be written to
```bash
cat knapsack.err
```

## Simple example using job array
1. Download the files job.sh and jobarray.py to your local computer
2. Copy the files from your computer to the same directory on the CCR 
3. Log into the CCR
4. Navigate to directory you saved the files in. Make the slurm script executable
```bash
chmod +x job.sh
```
5. Convert script with DOS line breaks to Unix line breaks 
```bash
dos2unix job.sh
```
6. Run job
```bash
sbatch job.sh
```
7. Check progress of the job
``` bash
squeue --user={UBIT}
```
8. Check progress of the job every `x` seconds
``` bash
squeue --user={UBIT} --iterate=x
```
Stop with `CTRL-C`
9. For help with slurm commands
```bash
sbatch --help
```

To be added:
* Why use the CCR
* Creating a python virtual environment to load modules not already on the CCR
* Multithreading vs Multiprocessing in Python
