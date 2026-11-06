import numpy as np
from scipy import signal
R1a,R2a,C1a,C2a = 6.81e3,36.5e3,15e-9,6.8e-9
R1b,R2b,C1b,C2b = 12.1e3,43.2e3,22e-9,2.2e-9
def sk(R1,R2,C1,C2): return [1],[R1*R2*C1*C2, C2*(R1+R2), 1]
na,da = sk(R1a,R2a,C1a,C2a); nb,db = sk(R1b,R2b,C1b,C2b)
H_real = (np.polymul(na,nb), np.polymul(da,db))
H_ideal = signal.butter(4, 2*np.pi*1000, analog=True)
f = np.logspace(1,5,2000); w=2*np.pi*f
_,hr = signal.freqs(*H_real,w); _,hi = signal.freqs(*H_ideal,w)
gr,gi = 20*np.log10(abs(hr)),20*np.log10(abs(hi))
for fl in (100,500,1000,2000,5000,10000):
    i=np.argmin(abs(f-fl)); print(f"{fl:>6} Hz  chosen-values {gr[i]:8.3f} dB   ideal-Butterworth {gi[i]:8.3f} dB")
m = f<=10e3; print("max |diff| up to 10 kHz: %.3f dB" % np.max(abs(gr-gi)[m]))
# compare against ngspice ideal-opamp run
d=np.loadtxt("ac_ideal.txt"); fs=d[:,0]; gs=d[:,1]
gm=np.interp(fs,f,gr); sel=(fs>=10)&(fs<=10e3)
print("SPICE(ideal) vs transfer-function model, max diff to 10 kHz: %.4f dB" % np.max(abs(gs[sel]-gm[sel])))
