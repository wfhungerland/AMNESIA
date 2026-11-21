"""Ergaenzt die Hansard-Auswertung: Deutschland-Nennung im Abstand von hoechstens 30 Woertern zu Wettbewerbswoertern. Laeuft nach hansard_salience.py, nur auf dem Zwischenspeicher."""
import re, hashlib, pandas as pd
from pathlib import Path
C=Path('data/raw/hansard'); s=pd.read_csv('data/ds1_hansard_sections.csv')
T=re.compile(r"\b(german|germany|germans|prussia|prussian|zollverein)\b",re.I)
K=re.compile(r"\b(competition|competitor|competitors|compete|competing|dumping|dumped|unfair|bount\w*|subsid\w*|undersell\w*|cheap|cheaper|imitat\w*|rival\w*)\b",re.I)
def txt(u):
    f=C/(hashlib.sha1(u.encode()).hexdigest()+'.html'); h=f.read_text(errors='replace') if f.exists() else ''
    h=re.sub(r'(?s)<(script|style|head).*?</\1>',' ',h); return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',h)).split()
def comp(u):
    w=txt(u); ti=[i for i,x in enumerate(w) if T.search(x)]; ki=[i for i,x in enumerate(w) if K.search(x)]
    return any(abs(a-b)<=30 for a in ti for b in ki)
s['germany_competition']=[comp(u) if m else False for u,m in zip(s.url,s.mentions_target)]
s.to_csv('data/ds1_hansard_sections.csv',index=False)
y=pd.read_csv('data/ds1_hansard_salience.csv')
g=s.groupby('year').germany_competition.sum().rename('econ_germany_competition')
y=y.drop(columns=[c for c in ['econ_germany_competition','competition_share'] if c in y]).merge(g,on='year',how='left')
y['competition_share']=(y.econ_germany_competition/y.econ_sections).round(4)
y.to_csv('data/ds1_hansard_salience.csv',index=False)
y['p']=pd.cut(y.year,[1849,1869,1886,1895,1902,1914],labels=['1850-69','1870-86','1887-95','1896-1902','1903-14'])
print(y.groupby('p',observed=True).agg(nennung=('salience_share','mean'),wettbewerb=('competition_share','mean'),n_wettb=('econ_germany_competition','sum')).round(3))
