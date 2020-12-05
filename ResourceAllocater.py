# Importing the Library files
import psutil,sys
import ast,csv
import time
from datetime import datetime
from threading import Thread
import threading,schedule

# Storing the command line arguments
Process = sys.argv[1]     #Name of process
Period = int(sys.argv[2]) # A length of time (seconds) in which to monitor the processes
PollingFrequency = int(sys.argv[3]) # Monitor resource every interval of PollingFrequency
Switch = float(sys.argv[4]) 
newCPUAffinity = sys.argv[5]  # New CPUAffinity to be assigned at Switch*Period interval
maxMemoryLock = int(sys.argv[6]) # New maximum memory to be assigned at Switch*Period interval
maxFileSize = int(sys.argv[7])  # New max filesize to be assigned at Switch*Period interval

newCPUAffinity = ast.literal_eval(newCPUAffinity)

pid=None

# Getting process details(processID) from list of processes 
for procNameId in psutil.process_iter():
    if procNameId.name() == Process:
        pid = procNameId.pid
       
        

if(pid==None):
  print("Not Found: Exiting")
  sys.exit()


proc = psutil.Process(pid)
convertMB = 1024*1024

# Getting CPUAffinity, Memory and FileSize limits of the process
cpuAff_curr = proc.cpu_affinity()
softMem, hardMem = proc.rlimit(psutil.RLIMIT_MEMLOCK)
softFsize, HardFsize = proc.rlimit(psutil.RLIMIT_FSIZE)

print(int(Period*Switch))
print('PID:',pid,'CPU Affinity:',cpuAff_curr,'MaxRAM:',hardMem,'maxFileSize',HardFsize)

# Initially assigning new CPUAffinity, Memory and FileSize limits
proc.cpu_affinity(newCPUAffinity)
cpuAff_new = proc.cpu_affinity()
proc.rlimit(psutil.RLIMIT_MEMLOCK, (maxMemoryLock,maxMemoryLock))
proc.rlimit(psutil.RLIMIT_FSIZE, (maxFileSize,maxFileSize))

newSoftMem, newHardMem = proc.rlimit(psutil.RLIMIT_MEMLOCK)
newSoftFsize, newHardFsize = proc.rlimit(psutil.RLIMIT_FSIZE)

# Scheduling job to assign new CPUAffinity, Memory and FileSize limits every interval of  Switch*Period seconds
def allotResources(proc,newCPUAffinity,maxMemoryLock,maxFileSize):
        proc.cpu_affinity(newCPUAffinity)
        cpuAff_new = proc.cpu_affinity()
        proc.rlimit(psutil.RLIMIT_MEMLOCK, (maxMemoryLock,maxMemoryLock))
        proc.rlimit(psutil.RLIMIT_FSIZE, (maxFileSize,maxFileSize))
        newSoftMem, newHardMem = proc.rlimit(psutil.RLIMIT_MEMLOCK)
        newSoftFsize, newHardFsize = proc.rlimit(psutil.RLIMIT_FSIZE)

        #print('PID:',pid,'CPU Affinity:',cpuAff_new,'newMaxRAM:',newHardMem,'newMaxFileSize:',newHardFsize)

# Scheduling the job using schedule function    		
schedule.every(int(Switch*Period)).seconds.do(allotResources,proc,newCPUAffinity,maxMemoryLock,maxFileSize)

# Creating and Generating the csv report of Resource utilization by the process
with open('resMonitor.csv', 'w') as file:
     writer = csv.writer(file)
     writer.writerow(["PID", "CPU Affinity", "MaxRAM","maxFileSize"])
     writer.writerow([pid, cpuAff_curr, hardMem, HardFsize])
     writer.writerow([pid, cpuAff_new, newHardMem, newHardFsize])

     writer.writerow([''])
     writer.writerow([''])
     writer.writerow([''])
    
     writer.writerow(["timestamp","CPU utilization(%)","memory utilization(%)","cumulative bytes read(MB)","cumulative bytes written(MB)"])
        
     while(True):	 
    	now = datetime.now()		
        current_time = now.strftime("%H:%M:%S")
        io_counters = proc.io_counters() 
        writer.writerow([current_time,round(proc.cpu_percent(interval=1)),round(proc.memory_percent()),io_counters[2]/convertMB,io_counters[3]/convertMB])        
        time.sleep(PollingFrequency)
        schedule.run_pending()    
     

     	
		
     













