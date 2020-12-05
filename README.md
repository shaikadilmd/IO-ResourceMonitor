# IO-ResourceMonitor
Monitoring resource utilization and assigning resource allocations to processes is critical in MicroProcessors and MicroServices. So, In this project we have developed script for monitoring any specific process in Linux systems for following resources - 

* CPU Utilization
* Memory Utilization
* Disk Read bytes
* Disk Write bytes

The script can also be used to input a period of time over which to monitor these processes and resources consumed by them and set new CPUAffinity,Memory and FileSize for any specific process. 

## Input Parameters 
1. **Process**: The process which will be monitored.
2. **Period**: A length of time (seconds) in which to monitor the processes.
3. **PollingFrequency**: The length of time (seconds) between monitoring utilization of each resource (e.g. monitor each resource every 5s).
4. **Switch**: A floating point value from 0 to 1 which specifies the fraction of the period in which to set new resource allocations (i.e. at time Switch∗Period, the processor affinity of Process will be set to ”New CPU Affinity”).
5. **NewCPUAffinity**: A list of CPU cores to remap the process onto at time Period ∗ Switch.
6. **MaxMemoryLock**: a new maximum memory that the process can lock starting at time
Period ∗ Switch.
7. **Maxfilesize**: a new maximum file size that the process can write starting at time Period ∗ Switch.



# Requirements
---
The Python scripts in this project can be implemented only on Linux Systems
* Linux Environment ( can also be Virtual Machine )
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

### Generate Monitoring Report and IO-plots


Open your Linux Terminal and run these commands.

#### Command to generate Monitoring report in csv format:
```sh
$ python ResourceAllocater.py processName Period PollingFrequency Switch newCPUAffinity newMemoryLock newFileSizeLock  
```

#### Example Command : 
```sh
$ python ResourceAllocater.py firefox 60 3 0.5 [0] 2048 3000000
```

In the command above, the process is allocated with new resources for every 60 * 05 = 30 seconds (Switch*Period) and resources are monitored every 3 seconds (PollingFrequency).
The new RAM assigned is 2048 and maxFileSize is 3000000.

#### Command to generate IO-Plots in PNG Format:
```sh
$ python IO-Plots.py processName
```

#### Example Command : 
```sh
$ python IO-Plots.py firefox 
```


#### IO-Plots Snapshot 
 
![](https://github.com/shaikadilmd/IO-ResourceMonitor/blob/main/MonitorPlots.png)


The plots summarize the CPU Usage(%), Memory Usage(%), DISK I/O Usage in MB.

Interesting Observations from IO-Plots-
1. After the CPU cores have been changed from [0,1] to [0], there was more CPU Usage as the system is now running only on 1 cpu core.
2. To check the increase in Disk I/O, Open Youtube and play any videos in FireFox.
3. After RAM memory was decreased, some of the tabs became slow and the browser was not responding properly.


#### Monitoring Report

You can cross-check the plots from the monitoring report. The Monitoring report contains the details as follows -  

- In the first line of the csv file report- the PID of the process, the CPU affinity of the process, the maximum number of bytes of memory that may be locked into RAM for the process, and the maximum file size that may be written for the process. 
- The second line of the trace file - the PID of the process, the new CPU affinity of the process, the new maximum number of bytes of memory that may be locked into RAM for the process, and the new maximum file size of the process
- Next, the file contains the details of the process in form of - timestamp, CPU utilization(%), memory utilization(%), cumulative bytes read(MB), cumulative bytes written (MB)


|    PID        | CPU Affinity  | MaxRAM  | maxFileSize
| ------------- |:-------------:| -------:|-----------:|
|    14394      |   [0,1]       | 67108864|     -1     |
|    14394      |    [0]        |   2048  |   3000000  |

The above table represents the first two lines in the report after running above example command for firefox process. The first line represents the current resource values and the second line represents the alloted resources from the script.
So, the ProcessID OF firefox in the system was 14394. It had initially two cpu cores 0,1. We updated the cpu cores to only 1 cpu core[0] for testing. Similarly RAM memory and Max FileSize can also be updated and performances of the processes can be compared



### Reporting any Issues/ Clarifications
For any queries/clarifications- Please feel free to contact me on my email below.
* Email - kshaik@uncc.edu


