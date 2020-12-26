import math
import statistics
import numpy as np
import matplotlib.pyplot as plt

#Reading File
import soundfile as sf
data, Fs = sf.read('Off of Newton Exit 17.wav')

c=3e8
Tp=0.250 #pulse time
N=Tp*Fs  #samples per pulse 
fc=2590e6 #center freq.
#print(int(N))

def dbc(ar):
    return 20*math.log10(abs(ar))

dbc_2=np.vectorize(dbc)

s=-1*data[:,1]
s_size=np.size(s)
s_round=round(s_size/N)
#print(s_round)

#Creating doppler vs. time plot data set here
for i in range(1,s_round):
       sif=np.empty((i,int(N)))

for i in range(1,s_round):
       sif[i-1,:]=s[(i-1)*int(N):i*int(N)]

#Subtraction the average DC term 
ave=s.mean()
sif=sif-ave
#print(sif)
#print(ave)

#Doppler vs. time plot:
zpad=int(8*N/2)
v=dbc_2(np.fft.ifft(sif,zpad))
ss_1=int(np.size(v,1)/2)
ss=v[:,0:ss_1]
m=np.amax(ss)
#print(m)
#print(ss)

#Calculating velocity
delta_f=np.linspace(0,Fs/2,np.size(ss,1))
#print(delta_f)
lamda=c/fc
velocity=delta_f*lamda/2

#Time
time=np.linspace(1,Tp*np.size(ss,0),np.size(ss,0))

plt.imshow(ss-m,cmap='jet',extent=(velocity[0],velocity[np.size(velocity)-1],time[0],time[np.size(time)-1]),aspect='auto')
plt.xlim(0,30)
#plt.xticks(np.arange(min(x), max(x)+1, 1.0))
plt.xlabel('Velocity (m/sec)')
plt.ylabel('Time (s)')
plt.title('Doppler vs. Time Intensity (DTI) plot')
plt.colorbar()
plt.clim(-35,0)
plt.show()
