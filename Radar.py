import math
import numpy as np
from scipy import ndimage, misc
import matplotlib.pyplot as plt

#Reading File
import soundfile as sf
data, samplerate = sf.read('Campus_Experiment.wav')  

#RADAR PARAMETERS
c=3e8               #Speed of light 
Tp=0.014            #Pulse time (Period)
N=Tp*samplerate     #Sampled pulse time
fstart=2364e6       #Start freq.
fstop=2620e6        #Stop freq.
Bw=fstop-fstart     #Bandwitdh

#Range Resolution
range_res=(c)/(2*Bw)
range_max=(range_res*N)/2

#Be sign is (-), inverted plus sign
trig=-1*data[:,1]
s=(-1*data[:,0])

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
zpad=int(4*N)
v=dbc_2(np.fft.fft(sif,zpad)) #fft and decibel convertion with respect to 4*N.
ss_1=int(np.size(v,1)/2)
ss=v[:,0:ss_1]
m=np.amax(v)
range_label=np.linspace(0,range_max,zpad)   
#range_label=range_label1[(int(np.size(range_label1)/range_max)):np.size(range_label1)]       
#plt.imshow(ss-m,extent=(range_label[0],range_label[np.size(range_label)-1],time[0],time[np.size(time)-1]))
#plt.show()
#---------------------------------------------------------------

#2 pulse cancelor RTI plot (RTI with 2-pulse canceller clutter rejection)

sif2=sif[1:np.size(sif,0),:]-sif[0:np.size(sif,0)-1,:] # 2-pulse canceller ((n+1) - n [ROW])

sif3=sif2[:,1:np.size(sif2,1)]-sif2[:,0:np.size(sif2,1)-1] # ((n+1) - n [COLUMN]) (For Noise Rejection)

grad=ndimage.uniform_filter(sif3, size=3, mode='constant') #Moving Average Filter 2-D


v_2=np.fft.fft(grad,zpad)                       
ss_2=dbc_2(abs(v_2[:,0:int(np.size(v_2,1)/2)]))
m_2=np.amax(ss_2)

plt.imshow(ss_2-m_2,cmap='jet',extent=(range_label[0],range_label[np.size(range_label)-1],time[np.size(time)-1],time[0]),aspect='auto')
plt.xlim(0,100)
plt.xlabel('Range (m)')
plt.ylabel('Time (s)')
plt.title('RTI with 2-pulse cancelor clutter rejection')
plt.colorbar()
#plt.clim(-30,30) #The scala without substruction m_2(max) from s_2
plt.clim(-80,0)
plt.show()
#print(range_label[np.size(range_label)/range_max])

#----------------------------------------------
#aa=ss_2-m_2
#aa2 = aa.astype(int)
#np.savetxt("deneme80.txt", np.array(aa2), fmt="%s")

#np.savetxt("foo.csv", np.array(aa2), delimiter=",")

#mydata = np.array(np.array(aa2), dtype=[('foo', 'i'), ('bar', 'f')])
