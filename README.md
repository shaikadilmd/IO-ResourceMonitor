# IO-ResourceMonitor
Monitoring resource utilization and assigning resource allocations to processes is critical in MicroProcessors and MicroServices. So, In this project we have shared script for monitoring any specific process in Linux systems for following resources - 

> CPU Utilization
> Memory Utilization
> Disk Read bytes
> Disk Write bytes

The script can also be used to input a period of time over which to monitor these processes and resources consumed by them and set new CPUAffinity,Memory and FileSize for any specific process. 

Input Parameters - 
> **Process**: The process which will be monitored.
> **Period**: A length of time (seconds) in which to monitor the processes.
> **PollingFrequency**: The length of time (seconds) between monitoring utilization of each resource (e.g. monitor each resource every 5s).
> **Switch**: A floating point value from 0 to 1 which specifies the fraction of the period in which to set new resource allocations (i.e. at time Switch∗Period, the processor affinity of Process will be set to ”New CPU Affinity”).
> **NewCPUAffinity**: A list of CPU cores to remap the process onto at time Period ∗Switch.
> **MaxMemoryLock**: a new maximum memory that the process can lock starting at time
Period ∗ Switch.
> **Maxfilesize**: a new maximum file size that the process can write starting at time Period ∗ Switch.



# Requirements
---
The Python scripts in this project can be implemented only on Linux Systems
* Linux Environment ( can also be Virutal Machine )
* Python 2.7 and higher
* Psutil 1.0 or later
* Matplotlibs


### Installation
Make sure to install basic packages like 

```sh
$ sudo apt-get install -y python-psutil
$ sudo apt-get install python-matplotlib
```

For python3 environments...

```sh
$ sudo apt-get install python3-matplotlib
```

### Generating Monitoring Report and IO-plots


Open your Linux Terminal and run these commands.

Command to generate Monitoring report in csv Format:
```sh
$ python ResourceAllocater.py processName Period PollingFrequency Switch newCPUAffinity newMemoryLock new FileSizeLock  
```

Example Command : 
```sh
$ python resAllocate.py firefox 60 30 0.5 [0] 2048 3000000
```

Command to generate IO-Plots in PNG Format:
```sh
$ python IO-Plots.py processName
```

Example Command : 
```sh
$ python IO-Plots.py firefox 
```


#### IO-Plots Snapshot 

IO-Plots Image - 
![](https://github.com/shaikadilmd/IO-ResourceMonitor/blob/main/MonitorPlots.png)


The plots summarize the CPU Usage(%), Memory Usage(%), DISK I/O Usage in MB.

Interesting Observations -
1. After the CPU cores have been changed from [0,1] to [1], there was more CPU Usage 






