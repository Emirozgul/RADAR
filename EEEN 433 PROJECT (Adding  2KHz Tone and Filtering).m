clear all
close all
clc
pkg load signal

[mysignal fs]=audioread('Original Sound.wav');   

nf=1024*16;
mysignal_fft=fft(mysignal,nf);  %fft of the mysignal
f=(fs/2)*linspace(0,1,nf/2+1);
figure(1);
subplot(2,1,1);
plot(mysignal); 
title('Mysignal Graph');  %Time domain graph
xlabel('Time');
ylabel('Amplitude');
subplot(2,1,2);
plot(f,abs(mysignal_fft(1:nf/2+1)));   %fft graph
xlabel('Frequency');
ylabel('Amplitude');
figure(2)
specgram(mysignal,nf,fs);  %Specgram of the mysignal
%sound(mysignal,fs);

n=length(mysignal);
tn=n/fs;
freq=2000;
t=linspace(0,tn,n);
noise_1=0.1*sin(2*pi*freq*t);
noise=reshape(noise_1,[length(mysignal),1]);

noise_fft=fft(noise,nf);  %fft of the mysignal
f=(fs/2)*linspace(0,1,nf/2+1);
figure(3);
subplot(2,1,1);
plot(noise); 
title('Mysignal Graph');  %Time domain graph
xlabel('Time');
ylabel('Amplitude');
subplot(2,1,2);
plot(f,abs(noise_fft(1:nf/2+1)));   %fft graph
xlabel('Frequency');
ylabel('Amplitude');
figure(4)
specgram(noise,nf,fs);  %Specgram of the mysignal

new_signal=mysignal+noise;

new_signal_fft=fft(new_signal,nf);  %fft of the mysignal
f=(fs/2)*linspace(0,1,nf/2+1);
figure(5);
subplot(2,1,1);
plot(new_signal); 
title('Mysignal Graph');  %Time domain graph
xlabel('Time');
ylabel('Amplitude');
subplot(2,1,2);
plot(f,abs(new_signal_fft(1:nf/2+1)));   %fft graph
xlabel('Frequency');
ylabel('Amplitude');
figure(6)
specgram(new_signal,nf,fs);  %Specgram of the mysignal


[a2 b2]=butter(3,[1950 2050]/(fs/2),'stop');
y2=filter(a2,b2,new_signal); 
figure(7);
subplot(2,1,1);
plot(y2);
title('Animal 2: Freq Range: 3500 - 6000 Hz');
xlabel('Time');
ylabel('Amplitude');
subplot(2,1,2);
specgram(y2,nf,fs);


