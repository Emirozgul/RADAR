
import math
import statistics
import numpy as np
import matplotlib.pyplot as plt

#Reading File
import soundfile as sf
data, samplerate = sf.read('running_outside_20ms.wav')  

#RADAR PARAMETERS
c=3e8               #Speed of light 
Tp=0.02             #Pulse time
N=Tp*samplerate     #Sampled pulse time
fstart=2260e6       #Start freq.
fstop=2590e6        #Stop freq.
Bw=fstop-fstart     #Bandwitdh

#Range Resolution
range_res=(c)/(2*Bw)
range_max=(range_res*N)/2

#Be sign is (-), inverted plus sign
trig=-1*data[:,0]
s=-1*data[:,1]

#Decibel funciton
def dbc(ar):
    return 20*math.log10(abs(ar))

dbc_2=np.vectorize(dbc)

#Making (0-1) logic array  
b=0
start_1=trig>b
start=start_1*1

a=np.size(trig,0)
count=0
for i in range(100, a-int(N)+1):
   if start[i]==1 and np.mean(start[i-11:i])==0:
       count=count+1
       sif=np.empty((count,int(N)))
       time=np.empty((count))

count_2=0
for i in range(100, a-int(N)+1):
   if start[i]==1 and np.mean(start[i-11:i])==0:
       count_2=count_2+1
       sif[count_2-1,:]=s[i:i+int(N)]  
       time[count_2-1]=i*1/samplerate

ave=sif.mean(axis=0)
for i in range(np.size(sif,0)+1):
    sif[i-1,:]=sif[i-1,:]-ave

#RTI plot without cancelor
zpad=int(8*N/2)
v=dbc_2(np.fft.ifft(sif,zpad))
ss_1=int(np.size(v,1)/2)
ss=v[:,0:ss_1]
m=np.amax(v)
range_label=np.linspace(0,range_max,zpad)   
       
#plt.imshow(ss-m,extent=(range_label[0],range_label[np.size(range_label)-1],time[0],time[np.size(time)-1]))
#plt.show()
#---------------------------------------------------------------

#2 pulse cancelor RTI plot (RTI with 2-pulse cancelor clutter rejection)
sif2=sif[2:np.size(sif,0),:]-sif[1:np.size(sif,0)-1,:]
v_2=np.fft.ifft(sif2,zpad)                       
ss_2=dbc_2(abs(v_2[:,0:int(np.size(v_2,1)/2)]))
m_2=np.amax(ss_2)

plt.imshow(ss_2-m_2,cmap='jet',extent=(range_label[0],range_label[np.size(range_label)-1],time[0],time[np.size(time)-1]),aspect='auto')
plt.xlabel('Range (m)')
plt.ylabel('Time (s)')
plt.title('RTI with 2-pulse cancelor clutter rejection')
plt.colorbar()
plt.clim(-80,0)
plt.show()