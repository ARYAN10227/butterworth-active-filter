"""Component selection for a 1 kHz 4th-order Butterworth LPF (two unity-gain Sallen-Key stages)."""
import numpy as np, itertools
fc = 1000.0; w0 = 2*np.pi*fc
Qs = [1/(2*np.cos(np.pi/8)), 1/(2*np.cos(3*np.pi/8))]   # 0.5412, 1.3066
E12 = [1.0,1.2,1.5,1.8,2.2,2.7,3.3,3.9,4.7,5.6,6.8,8.2]
E96 = [round(10**(i/96),2) for i in range(96)]
caps = [m*d for d in (1e-9,10e-9,100e-9) for m in E12]
def snap(x, series):
    dec = 10**np.floor(np.log10(x)); vals = [m*dec for m in series]+[series[0]*dec*10]
    return min(vals, key=lambda v: abs(np.log(v/x)))
def stage(R1,R2,C1,C2):  # C1 = feedback cap (to output), C2 = cap to ground
    return 1/np.sqrt(R1*R2*C1*C2)/(2*np.pi), np.sqrt(R1*R2*C1*C2)/(C2*(R1+R2))
best=[]
for Q in Qs:
    cands=[]
    for C1,C2 in itertools.product(caps,caps):
        if C1/C2 < 4*Q*Q: continue
        s = 1/(w0*Q*C2); p = 1/(w0**2*C1*C2)
        d = s*s-4*p
        R1 = (s-np.sqrt(d))/2; R2 = s-R1   # solve R1+R2=s, R1*R2=p
        if not (2e3 < R1 < 100e3 and 2e3 < R2 < 100e3): continue
        R1s, R2s = snap(R1,E96), snap(R2,E96)
        f,q = stage(R1s,R2s,C1,C2)
        err = abs(f/fc-1)+abs(q/Q-1)
        cands.append((err,R1s,R2s,C1,C2,f,q))
    cands.sort(); best.append(cands[0])
    e,R1,R2,C1,C2,f,q = cands[0]
    print(f"Target Q={Q:.4f}: R1={R1/1e3:.2f}k R2={R2/1e3:.2f}k C1={C1*1e9:.1f}n C2={C2*1e9:.1f}n -> f0={f:.1f} Hz, Q={q:.4f}")
np.save("values.npy", np.array([b[1:5] for b in best]))
