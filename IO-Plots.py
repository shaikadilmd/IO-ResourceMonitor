# Importing the library Files
import psutil,os,sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Storing ProcessName from command line arguments
processName = sys.argv[1]

# Defining variables to store process id and process name in psutil format
pid = None


# Finding processID and processName from psutil processes
for proc in psutil.process_iter():
    if proc.name() == processName:
        pid = proc.pid
	

if(pid==None):
  print('Not Found: Exiting')
  sys.exit()	

# Creating process variable containing all details using ProcessID
proc = psutil.Process(pid)

#Defining matplot parameters
frame_len = sys.maxint
y_cpu = []
y_mem = []
y_dRead = []
y_dWrite = []
fig,a = plt.subplots(2,2, squeeze=False)
convertMB = 1024*1024

# Function to generate live-plot of resource Allocation
def animate(i):
	io_counters = proc.io_counters() 
	y_cpu.append(round(proc.cpu_percent(interval=1)))
	y_mem.append(round(proc.memory_percent()))
	y_dRead.append(io_counters[2]/convertMB)
	y_dWrite.append(io_counters[3]/convertMB)
	if(len(y_cpu)<=frame_len):
		a[0][0].cla()
		a[0][0].plot(y_cpu,'r',label = 'Real-Time CPU Usage')
		a[0][0].legend(loc = 'upper right',prop={'size': 6})
		a[0][1].cla()
		a[0][1].plot(y_mem,'b',label = 'Real-Time Memory Usage')
		a[0][1].legend(loc = 'upper right',prop={'size': 6})
		a[1][0].cla()
		a[1][0].plot(y_dRead,'g',label = 'Real-Time DiskRead Bytes')
		a[1][0].legend(loc = 'upper right',prop={'size': 6})
		a[1][1].cla()
		a[1][1].plot(y_dWrite,'y',label = 'Real-Time DiskWrite Bytes')
		a[1][1].legend(loc = 'upper right',prop={'size': 6})
	
		
	a[0][0].set_xlabel('Time (s)')
	a[0][0].set_ylabel('CPU (%)')
	a[0][1].set_xlabel('Time (s)')
	a[0][1].set_ylabel('Memory (%)')
	a[1][0].set_xlabel('Time (s)')
	a[1][0].set_ylabel('DiskRead (MB)')
	a[1][1].set_xlabel('Time (s)')
	a[1][1].set_ylabel('DiskWrite (MB)')
	a[0][0].set_title('CPU Usage',color='r')
	a[0][1].set_title('Memory Usage',color='b')
	a[1][0].set_title('DiskRead Usage',color='g')
	a[1][1].set_title('DiskWrite Usage',color='y')
	plt.autoscale(enable=True, axis='y')
	plt.suptitle('Resource Monitor\n\n', fontweight ="bold")
	plt.subplots_adjust(wspace=0.5, hspace=0.5)
	#plt.tight_layout()

	
	
# Calling the function using FuncAnimation function
ani= FuncAnimation(fig,animate,interval = 200)

#Displaying Live-Plot on seperate window
plt.show()


