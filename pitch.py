#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 20:08:32 2020

@author: rkingeski
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.io import wavfile

fs, audio = wavfile.read('./audio.wav')
 
x = audio[:,1]

frames = 60;
overlap = 50;

N = len(x)

nframe = round(frames  * fs / 1000) #convert time to samples
noverlap = round(overlap * fs / 1000)

#sizes for the cepstral window
t1=math.floor(fs*0.002) # 2ms 
t2=math.floor(fs*0.03) # 30ms

w = np.hamming(nframe) #hamming window applied in the frames;
L = 2**math.ceil(math.log2(abs(nframe))) #size of FFT


## PITCH 
 
i = 0
pos=1
F0 =[]
C=[]

while (pos+nframe < N):
     frame = x[pos:pos+nframe]
     #cn1= np.convolve(frame,w)
     cn1 = frame * w
     y = np.fft.fft(cn1, n=L)
     y1 = (abs(y))**2
     y2 = np.log(y1.T)
     y3= np.fft.ifft(y2,n=L)
     cn2 = abs(y3)

     C.append(cn2)
     px = np.argmax(abs(cn2[t1:t2]))
     #px = max(abs(cn2))
     f0 = fs/(t1+px)
     print(px)
     F0.append(f0)
     
     #if En[pos] < threshold:
     #    F0[i]=math.nan
     

     pos = pos + (nframe - noverlap);
     i = i + 1;
 

#T = [round(nframe/2):(nframe-noverlap):N-1-round(nframe/2)]/fs;

T = np.linspace(round(nframe/2),N-1-round(nframe/2),len(F0))


F0d=np.diff(F0)/((frames-overlap)/1000);
F02d=np.diff(F0d)/((frames-overlap)/1000);

Fdd=abs(F0d)
M=len(F0)

for ni in range(len(Fdd)):
    if Fdd[ni] > 3000:
      F0[ni]=math.nan
      F0d[ni]=math.nan
      F02d=math.nan


for nj in range(len(F0)):
    if F0[nj]>320:
        F0[nj]=math.nan

 
#F0= smooth(F0,'moving',3)
#F0= smooth(F0,'moving',2)

plt.plot(T,F0)
