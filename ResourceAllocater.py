import psutil,sys
import ast,csv
import time
from datetime import datetime
from threading import Thread
import threading,schedule

# Storing the command line arguments
Process = sys.argv[1]
Period = int(sys.argv[2])
PollingFrequency = int(sys.argv[3])
Switch = float(sys.argv[4])
newCPUAffinity = sys.argv[5]
maxMemoryLock = int(sys.argv[6])
maxFileSize = int(sys.argv[7])

newCPUAffinity = ast.literal_eval(newCPUAffinity)

pid=None

# Getting specific process details from list of processes 
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


proc.cpu_affinity(newCPUAffinity)
cpuAff_new = proc.cpu_affinity()
proc.rlimit(psutil.RLIMIT_MEMLOCK, (maxMemoryLock,maxMemoryLock))
proc.rlimit(psutil.RLIMIT_FSIZE, (maxFileSize,maxFileSize))
print('renewed')
newSoftMem, newHardMem = proc.rlimit(psutil.RLIMIT_MEMLOCK)
newSoftFsize, newHardFsize = proc.rlimit(psutil.RLIMIT_FSIZE)



    
def job(proc,newCPUAffinity,maxMemoryLock,maxFileSize):
	proc.cpu_affinity(newCPUAffinity)
        cpuAff_new = proc.cpu_affinity()
        proc.rlimit(psutil.RLIMIT_MEMLOCK, (maxMemoryLock,maxMemoryLock))
        proc.rlimit(psutil.RLIMIT_FSIZE, (maxFileSize,maxFileSize))
	print('renewed')
        newSoftMem, newHardMem = proc.rlimit(psutil.RLIMIT_MEMLOCK)
        newSoftFsize, newHardFsize = proc.rlimit(psutil.RLIMIT_FSIZE)

        #print('PID:',pid,'CPU Affinity:',cpuAff_new,'newMaxRAM:',newHardMem,'newMaxFileSize:',newHardFsize)
    
    
	
		
schedule.every(int(Switch*Period)).seconds.do(job,proc,newCPUAffinity,maxMemoryLock,maxFileSize)
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
        print('hey') 	 
    	now = datetime.now()		
        current_time = now.strftime("%H:%M:%S")
        io_counters = proc.io_counters() 
        writer.writerow([current_time,round(proc.cpu_percent(interval=1)),round(proc.memory_percent()),io_counters[2]/convertMB,io_counters[3]/convertMB])        
        time.sleep(PollingFrequency)
        schedule.run_pending()    
     

     	
		
     













