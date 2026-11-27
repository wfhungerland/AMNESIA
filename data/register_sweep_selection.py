"""Share of displaced groups followed within ten years by a targeted broad measure, all groups and outside textiles,
computed from the stored panel. Reproduces Table D.1 for Japan and Korea from the panel before the sweep.
Call: python3 data/register_sweep_selection.py data/population_panel.csv
"""
import sys,pandas as pd
for f in sys.argv[1:]:
  P=pd.read_csv(f,dtype={"code":str})
  for t,d,a,b in (("JP","s1",1963,1989),("KR","s1",1968,1992),("KR","s3",1997,2009),("CN","s3",1993,2009),("CN","hs4",2009,2023)):
   for excl in (False,True):
    g=P[(P.challenger==t)&(P.data==d)]
    if excl: g=g[~g.code.str[:2].isin(["65","84"]) if d!="hs4" else ~g.code.str[:2].isin([str(x) for x in range(50,64)])]
    n=k=k2=0
    for c,h in g.groupby("code"):
      cy=h.crossover_year.iloc[0]
      if pd.isna(cy) or not a<=cy<=b or cy==h.year.min(): continue
      n+=1; w=(h.year>=cy)&(h.year<cy+10); k+=int(((h.broad==1)&w).any()); k2+=int(((h.broad_x301==1)&w).any())
    print(f.split('/')[-1],t,d,"notex" if excl else "all",n,round(k/n,2),round(k2/n,2))
