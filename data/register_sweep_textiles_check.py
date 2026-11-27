"""Compares the Japan-Korea panel before and after the register sweep, with and without textile groups (SITC 65, 84).
Call: python3 data/register_sweep_textiles_check.py <old panel csv> data/population_panel.csv
"""
import sys,warnings;warnings.filterwarnings("ignore")
import numpy as np,pandas as pd,statsmodels.api as sm,statsmodels.formula.api as smf
for f in sys.argv[1:]:
  P=pd.read_csv(f,dtype={"code":str})
  for lab,excl in (("all",False),("no textiles 65/84",True)):
    jk=P[P.challenger.isin(["JP","KR"])&(P.data=="s1")&(P.at_risk==1)].copy()
    if excl: jk=jk[~jk.code.str[:2].isin(["65","84"])]
    jk["yc"]=jk.year.astype(str)+jk.challenger; jk["grp"]=jk.challenger+"_"+jk.code
    for c,v in (("lx_ch","x_ch"),("lm_us","m_us"),("lx_us","x_us")): jk[c]=np.log1p(jk[v]/1e6)
    jk["lr"]=np.clip(np.log((jk.x_ch+1e5)/(jk.x_us+1e5)),-5,5)
    r=[]
    for rhs,t in (("post + C(yc)","post"),("post + lx_ch + lm_us + C(yc)","post"),("lr + lx_ch + lm_us + C(yc)","lr")):
      m=smf.glm(f"broad ~ {rhs}",data=jk,family=sm.families.Poisson()).fit(cov_type="cluster",cov_kwds={"groups":pd.factorize(jk.grp)[0]},maxiter=200)
      b,se=m.params[t],m.bse[t]; k=np.log(2) if t=="lr" else 1
      r.append(f"{t}:{np.exp(k*b):.2f}({np.exp(k*(b-1.96*se)):.2f}-{np.exp(k*(b+1.96*se)):.2f})")
    print(f.split('/')[-1],lab,"starts",int(jk.broad.sum()),"pre",int(jk[jk.post==0].broad.sum()),r)
