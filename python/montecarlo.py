"""500-run Monte Carlo on the TL072 filter: uniform +/-1% resistors, +/-5% capacitors (same as LTspice mc())."""
import numpy as np, subprocess, re, os, tempfile
rng = np.random.default_rng(7)
nom = dict(R1a=6.81e3,R2a=36.5e3,C1a=15e-9,C2a=6.8e-9,R1b=12.1e3,R2b=43.2e3,C1b=22e-9,C2b=2.2e-9)
base = open("filter_tl072.cir").read()
base = re.sub(r"wrdata.*\n","",base)
f3, g2k = [], []
for run in range(500):
    p = {k: v*(1+rng.uniform(-1,1)*(0.01 if k[0]=="R" else 0.05)) for k,v in nom.items()}
    net = re.sub(r"\.param R1a.*\n\.param R1b.*\n",
        ".param "+" ".join(f"{k}={v:.6g}" for k,v in p.items())+"\n", base)
    net = net.replace("ac dec 200 10 10Meg","ac dec 400 500 3k").replace("meas ac g10k","meas ac g2k find g at=2k\n*")
    with tempfile.NamedTemporaryFile("w",suffix=".cir",delete=False,dir=".") as t: t.write(net)
    out = subprocess.run(["ngspice","-b",t.name],capture_output=True,text=True).stdout; os.unlink(t.name)
    f3.append(float(re.search(r"f3db\s*=\s*(\S+)",out).group(1)))
    g2k.append(float(re.search(r"g2k\s*=\s*(\S+)",out).group(1)))
f3=np.array(f3); np.savetxt("mc_f3db.txt",f3)
dev=(f3/1000-1)*100
print(f"runs={len(f3)} mean fc={f3.mean():.1f} Hz  sigma={f3.std(ddof=1):.1f} Hz ({f3.std(ddof=1)/f3.mean()*100:.2f}%)")
print(f"min {f3.min():.1f} Hz ({dev.min():+.2f}%)  max {f3.max():.1f} Hz ({dev.max():+.2f}%)")
print(f"gain at 2 kHz: mean {np.mean(g2k):.2f} dB, range {min(g2k):.2f} .. {max(g2k):.2f} dB")
