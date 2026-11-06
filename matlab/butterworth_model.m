% Transfer-function model of the two Sallen-Key stages vs. an ideal 4th-order Butterworth
% Unity-gain Sallen-Key LPF: H(s) = 1 / (R1 R2 C1 C2 s^2 + C2 (R1+R2) s + 1)
fc = 1e3; w0 = 2*pi*fc;
R1a=6.81e3; R2a=36.5e3; C1a=15e-9; C2a=6.8e-9;   % stage A
R1b=12.1e3; R2b=43.2e3; C1b=22e-9; C2b=2.2e-9;   % stage B
sk = @(R1,R2,C1,C2) tf(1,[R1*R2*C1*C2, C2*(R1+R2), 1]);
Ha = sk(R1a,R2a,C1a,C2a); Hb = sk(R1b,R2b,C1b,C2b); H = Ha*Hb;
[b,a] = butter(4, w0, 's'); Hbw = tf(b,a);
for s = {Ha,Hb}
    [wn,z] = damp(s{1}); fprintf('f0 = %.1f Hz, Q = %.4f\n', wn(1)/2/pi, 1/(2*z(1)));
end
f = logspace(1,5,2000); w = 2*pi*f;
g  = 20*log10(squeeze(abs(freqresp(H,w))));
gb = 20*log10(squeeze(abs(freqresp(Hbw,w))));
fprintf('Max deviation from ideal Butterworth up to 10 kHz: %.3f dB\n', max(abs(g(f<=1e4)-gb(f<=1e4))));
fprintf('-3 dB frequency: %.1f Hz\n', interp1(g, f, -3.0103));
semilogx(f,g,'LineWidth',2); hold on; semilogx(f,gb,'--','LineWidth',1.5); grid on
xlabel('Frequency (Hz)'); ylabel('Gain (dB)'); legend('Chosen E-series values','Ideal Butterworth');
title('4th-order Butterworth LPF, f_c = 1 kHz');
