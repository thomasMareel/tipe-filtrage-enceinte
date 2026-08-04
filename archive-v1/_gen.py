import math, cmath

# ---------- BODE Butterworth 2nd ordre ----------
Q=1/math.sqrt(2); fc=100.0
XL,XR=110,920; FMIN,FMAX=10.0,1000.0
GTOP,GBOT,YGT,YGB=6.0,-42.0,40,190
PT,PB,YPT,YPB=180.0,-180.0,250,410
L10=math.log10
def X(f): return XL+(L10(f)-L10(FMIN))/(L10(FMAX)-L10(FMIN))*(XR-XL)
def YG(g): g=min(max(g,GBOT),GTOP); return YGT+(GTOP-g)/(GTOP-GBOT)*(YGB-YGT)
def YP(p): p=min(max(p,PB),PT); return YPT+(PT-p)/(PT-PB)*(YPB-YPT)
N=240; fs=[10.0*10**(2*i/(N-1)) for i in range(N)]
def poly(vals,Yf): return " ".join("%.1f,%.1f"%(X(a),Yf(b)) for a,b in zip(fs,vals))
glp=[];ghp=[];plp=[];php=[]
for f in fs:
    x=f/fc;jx=1j*x;D=1+(1/Q)*jx+(jx)**2;Hl=1/D;Hh=(jx**2)/D
    glp.append(20*math.log10(abs(Hl)));ghp.append(20*math.log10(abs(Hh)))
    plp.append(math.degrees(cmath.phase(Hl)));php.append(math.degrees(cmath.phase(Hh)))
def uw(ds):
    o=[];off=0;pv=None
    for d in ds:
        v=d+off
        if pv is not None:
            while v-pv>180:off-=360;v-=360
            while v-pv<-180:off+=360;v+=360
        o.append(v);pv=v
    return o
plp=uw(plp);php=uw(php)
ticks=[10,20,30,40,50,70,100,200,300,400,500,700,1000];lab={10:"10",20:"20",50:"50",100:"100",200:"200",500:"500",1000:"1 k"}
tk=""
for t in ticks:
    xt=X(t);big=t in lab
    tk+='<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="var(--ink-soft)" stroke-width="%s"/>'%(xt,YPB,xt,YPB+(10 if big else 7),1.5 if big else 1)
    if big: tk+='<text x="%.1f" y="%d" fill="var(--ink-soft)" font-size="15" text-anchor="middle" font-family="JetBrains Mono">%s</text>'%(xt,YPB+30,lab[t])
gr=""
for t in [10,100,1000]:
    xt=X(t);gr+='<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="var(--trait)" stroke-width="1" opacity="0.5"/><line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="var(--trait)" stroke-width="1" opacity="0.5"/>'%(xt,YGT,xt,YGB,xt,YPT,xt,YPB)
xfc=X(fc)
asy_lp="%.1f,%.1f %.1f,%.1f %.1f,%.1f"%(X(FMIN),YG(0),X(fc),YG(0),X(FMAX),YG(-40))
asy_hp="%.1f,%.1f %.1f,%.1f %.1f,%.1f"%(X(FMIN),YG(-40),X(fc),YG(0),X(FMAX),YG(0))
bode=('<svg viewBox="0 0 1000 470" font-family="Inter,sans-serif" role="img" aria-label="Bode Butterworth 2nd ordre calcule">'
+gr
+'<text x="55" y="36" fill="var(--ink-soft)" font-size="15">G (dB)</text>'
+'<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--ink-soft)" stroke-width="1.5"/>'%(XL,YGT,XL,YGB)
+'<g stroke="var(--trait)" stroke-width="1"><line x1="%d" y1="%.1f" x2="%d" y2="%.1f"/><line x1="%d" y1="%.1f" x2="%d" y2="%.1f"/><line x1="%d" y1="%.1f" x2="%d" y2="%.1f"/></g>'%(XL,YG(0),XR,YG(0),XL,YG(-20),XR,YG(-20),XL,YG(-40),XR,YG(-40))
+'<g fill="var(--ink-soft)" font-size="13" text-anchor="end"><text x="%d" y="%.1f">0</text><text x="%d" y="%.1f">-20</text><text x="%d" y="%.1f">-40</text></g>'%(XL-8,YG(0)+5,XL-8,YG(-20)+5,XL-8,YG(-40)+5)
+'<polyline points="%s" fill="none" stroke="var(--accent)" stroke-width="1.4" stroke-dasharray="5 5" opacity="0.55"/>'%asy_lp
+'<polyline points="%s" fill="none" stroke="var(--accent2)" stroke-width="1.4" stroke-dasharray="5 5" opacity="0.55"/>'%asy_hp
+'<polyline points="%s" fill="none" stroke="var(--accent)" stroke-width="3.5"/>'%poly(glp,YG)
+'<polyline points="%s" fill="none" stroke="var(--accent2)" stroke-width="3.5"/>'%poly(ghp,YG)
+'<circle cx="%.1f" cy="%.1f" r="5" fill="var(--warn)"/><text x="%.1f" y="%.1f" fill="var(--warn)" font-size="14">-3 dB</text>'%(xfc,YG(-3),xfc+12,YG(-3)-4)
+'<text x="%.1f" y="%.1f" fill="var(--ink-soft)" font-size="14">-12 dB/oct</text>'%(X(430),YG(-26))
+'<text x="%.1f" y="%.1f" fill="var(--ink-soft)" font-size="12.5" font-family="JetBrains Mono">- - asymptotes</text>'%(X(10.5),YG(3))
+'<text x="48" y="%d" fill="var(--ink-soft)" font-size="15">phi (deg)</text>'%(YPT-8)
+'<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--ink-soft)" stroke-width="1.5"/>'%(XL,YPT,XL,YPB)
+'<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="var(--trait)" stroke-width="1"/>'%(XL,YP(0),XR,YP(0))
+'<g fill="var(--ink-soft)" font-size="13" text-anchor="end"><text x="%d" y="%.1f">+180</text><text x="%d" y="%.1f">0</text><text x="%d" y="%.1f">-180</text></g>'%(XL-8,YP(180)+12,XL-8,YP(0)+5,XL-8,YP(-180))
+'<polyline points="%s" fill="none" stroke="var(--accent)" stroke-width="3.5"/>'%poly(plp,YP)
+'<polyline points="%s" fill="none" stroke="var(--accent2)" stroke-width="3.5"/>'%poly(php,YP)
+'<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--ink-soft)" stroke-width="1.5"/>'%(XL,YPB,XR,YPB)
+tk
+'<text x="%d" y="%d" fill="var(--ink-soft)" font-size="14" text-anchor="end" font-family="JetBrains Mono">f (Hz)</text>'%(XR,YPB+48)
+'<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="var(--accent)" stroke-width="1.3" stroke-dasharray="4 4"/>'%(xfc,YGT,xfc,YPB)
+'<text x="%.1f" y="%d" fill="var(--accent)" font-size="15" text-anchor="middle" font-weight="700" font-family="Space Grotesk">f_c = 100 Hz</text>'%(xfc,YPB+48)
+'</svg>')

# ---------- IMPEDANCE HP (modele) ----------
Re=6.5; Le=1.2e-3; Res=44.0; fsr=40.0; Les=0.1; Ces=1/((2*math.pi*fsr)**2*Les)
zXL,zXR=110,900; zF0,zF1=20.0,500.0; Zmax=56.0; zYT,zYB=45,295
def zX(f): return zXL+(L10(f)-L10(zF0))/(L10(zF1)-L10(zF0))*(zXR-zXL)
def zY(z): z=min(max(z,0),Zmax); return zYB-(z/Zmax)*(zYB-zYT)
def Zof(f):
    w=2*math.pi*f
    Zmot=1/(1/Res+1/(1j*w*Les)+1j*w*Ces)
    return abs(Re+1j*w*Le+Zmot)
M=240; zfs=[zF0*10**(L10(zF1/zF0)*i/(M-1)) for i in range(M)]
zpts=" ".join("%.1f,%.1f"%(zX(f),zY(Zof(f))) for f in zfs)
fpk=max(zfs,key=Zof); zpk=Zof(fpk)
zt=[20,30,50,70,100,200,300,500];zlab={20:"20",50:"50",100:"100",200:"200",500:"500"}
ztk=""
for t in zt:
    xt=zX(t);big=t in zlab
    ztk+='<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="var(--ink-soft)" stroke-width="%s"/>'%(xt,zYB,xt,zYB+(10 if big else 7),1.5 if big else 1)
    if big: ztk+='<text x="%.1f" y="%d" fill="var(--ink-soft)" font-size="15" text-anchor="middle" font-family="JetBrains Mono">%s</text>'%(xt,zYB+30,zlab[t])
zimp=('<svg viewBox="0 0 1000 360" font-family="Inter,sans-serif" role="img" aria-label="Impedance HP modele">'
+'<text x="55" y="40" fill="var(--ink-soft)" font-size="15">|Z| (ohm)</text>'
+'<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--ink-soft)" stroke-width="1.5"/>'%(zXL,zYT-5,zXL,zYB)
+'<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--ink-soft)" stroke-width="1.5"/>'%(zXL,zYB,zXR,zYB)
+'<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="var(--accent2)" stroke-width="1.4" stroke-dasharray="7 6"/>'%(zXL,zY(8),zXR,zY(8))
+'<text x="%d" y="%.1f" fill="var(--accent2)" font-size="14" text-anchor="start">8 ohm nominal</text>'%(zXL+10,zY(8)-9)
+'<polyline points="%s" fill="none" stroke="var(--accent)" stroke-width="4"/>'%zpts
+'<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%d" stroke="var(--accent)" stroke-width="1.2" stroke-dasharray="4 4"/>'%(zX(fpk),zY(zpk),zX(fpk),zYB)
+'<text x="%.1f" y="%.1f" fill="var(--accent)" font-size="15" text-anchor="middle" font-weight="700" font-family="Space Grotesk">f_s</text>'%(zX(fpk),zY(zpk)-10)
+'<text x="%.1f" y="%.1f" fill="var(--ink-soft)" font-size="13">pic de resonance</text>'%(zX(fpk)+14,zY(zpk)+6)
+'<text x="%.1f" y="%.1f" fill="var(--ink-soft)" font-size="13" text-anchor="end">monte avec f (L_e) ↗</text>'%(zXR-2,zY(Zof(430))-16)
+ztk
+'<text x="%d" y="%d" fill="var(--ink-soft)" font-size="14" text-anchor="end" font-family="JetBrains Mono">f (Hz)</text>'%(zXR,zYB+48)
+'<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="var(--warn)" stroke-width="1.2" stroke-dasharray="4 4"/>'%(zX(100),zYT-5,zX(100),zYB)
+'<circle cx="%.1f" cy="%.1f" r="4" fill="var(--warn)"/>'%(zX(100),zY(Zof(100)))
+'<text x="%.1f" y="%.1f" fill="var(--warn)" font-size="13" text-anchor="start" font-family="Space Grotesk">à 100 Hz : Z ≈ %d ohm</text>'%(zX(100)+10,zY(Zof(100))-8,round(Zof(100)))
+'</svg>')

import re
html=open("presentation-finale.html",encoding="utf-8").read()
if "<!--BODE_SVG-->" in html:
    html=html.replace("<!--BODE_SVG-->",bode).replace("<!--Z_SVG-->",zimp)
else:
    html=re.sub(r'<svg[^>]*aria-label="Bode Butterworth[^"]*"[^>]*>.*?</svg>', lambda m: bode, html, flags=re.DOTALL)
    html=re.sub(r'<svg[^>]*aria-label="Impedance HP[^"]*"[^>]*>.*?</svg>', lambda m: zimp, html, flags=re.DOTALL)
open("presentation-finale.html","w",encoding="utf-8").write(html)
print("OK injecte. f_s=%.1f Hz pic=%.1f ohm  Z(100)=%.1f ohm"%(fpk,zpk,Zof(100)))
