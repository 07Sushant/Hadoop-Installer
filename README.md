# Hadoop Installer

This repository provides an automated installation script for setting up Apache Hadoop on Windows systems. The script simplifies the installation process by handling dependencies, configurations, and environment setup.

![Hadoop Installer](https://github.com/07Sushant/Hadoop-Installer/blob/main/img.png)


## Features
- Automates the installation of Hadoop and its dependencies
- Configures environment variables
- Sets up the Hadoop file system
- Verifies the installation with test commands
- Supports single-node cluster setup

## Prerequisites
Ensure you have the following installed before running the script:
- Everything provided in the app

## Installation
### Clone the Repository
```bash
git clone https://github.com/07Sushant/Hadoop-Installer.git
cd hadoop-installer
```

### Run the Installer
Start run.bat:
```bash
run.bat
```

## Usage
After installation, you can start Hadoop services with:
```bash
start-dfs.sh
start-yarn.sh
```
To verify the installation:
```bash
hadoop version
```

## Automated Tasks
The script automates the following steps:
- Installing required packages
- Downloading and extracting Hadoop
- Configuring environment variables and `hadoop-env.sh`
- Setting up SSH access
- Formatting the HDFS Namenode
- Starting Hadoop services

## Verification
After installation, verify Hadoop services by running the following commands:
TO run the below cmd add this belwow PATH in your system
```bash
%HADOOP_HOME%\sbin
```
Now you can run using belwo cmd otherwise next step
```bash
start-dfs.cmd
start-yarn.cmd
```
If above CMD is not working for you try belwo one 

```bash
cd C:\hadoopsetup\hadoop-3.2.4\sbin
.\start-dfs.cmd
.\start-yarn.cmd
```

Then, check running Java processes:
```bash
jps
```
You should see output similar to:
```
NameNode
DataNode
SecondaryNameNode
ResourceManager
NodeManager
```
If all services are running, the installation was successful.

## Troubleshooting
- If you encounter SSH permission issues, ensure that passwordless SSH is set up correctly.
- Verify that Java is installed by running `java -version`.
- Check logs in the `logs/` directory for any errors.

## Contributing
Feel free to fork the repository, make changes, and submit pull requests.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.
