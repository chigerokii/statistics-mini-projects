"""Графики для README. Запуск из корня репозитория: python scripts/make_figures.py"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
BLUE='#2b6cb0'; LIGHT='#90cdf4'; GREY='#a0aec0'; ORANGE='#dd6b20'
plt.rcParams.update({'font.size':10,'axes.titlesize':12,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,
                     'axes.grid':True,'grid.alpha':.25,'axes.axisbelow':True,'legend.frameon':False})
f=lambda x,d=0: f'{x:,.{d}f}'.replace(',',' ').replace('.',',')
rng=np.random.default_rng(42)
# ---------- A/B ----------
a=pd.read_csv('ab-test-average-check/data/ab.csv'); a.columns=a.columns.str.lower()
a=a.drop_duplicates(); both=a.groupby('user_id').variant_name.nunique(); a=a[a.user_id.isin(both[both==1].index)]
q1,q3=a.revenue.quantile([.25,.75]); a=a[(a.revenue>q1-1.5*(q3-q1))&(a.revenue<q3+1.5*(q3-q1))]
res={}
for g,s in a.groupby('variant_name').revenue:
    boots=[rng.choice(s.values,len(s)).mean() for _ in range(3000)]
    res[g]=(s.mean(),*np.percentile(boots,[2.5,97.5]))
diff=[rng.choice(a[a.variant_name=='variant'].revenue.values,len(a[a.variant_name=='variant'])).mean()-rng.choice(a[a.variant_name=='control'].revenue.values,len(a[a.variant_name=='control'])).mean() for _ in range(3000)]
fig,axes=plt.subplots(1,2,figsize=(11,3.8),gridspec_kw={'width_ratios':[1.3,1]})
for g,c in [('control',GREY),('variant',BLUE)]:
    axes[0].hist(a[a.variant_name==g].revenue,bins=40,alpha=.6,color=c,label=g)
axes[0].set_title('Распределение чека по группам'); axes[0].set_xlabel('Чек'); axes[0].legend()
lo,hi=np.percentile(diff,[2.5,97.5]); m=np.mean(diff)
axes[1].hist(diff,bins=40,color=LIGHT); axes[1].axvline(0,color='#4a5568',lw=1.2)
axes[1].axvspan(lo,hi,color=BLUE,alpha=.15,label='95% интервал')
axes[1].set_title('Разница средних чеков (bootstrap)'); axes[1].set_xlabel('variant − control'); axes[1].legend(); axes[1].set_yticks([])
fig.suptitle(f'Ноль внутри интервала [{f(lo,3)}; {f(hi,3)}]: изменение не повлияло на средний чек',fontweight='bold')
fig.tight_layout(); fig.savefig('images/ab_test.png',dpi=130,bbox_inches='tight'); plt.close()
print('AB',res,lo,hi)
# ---------- Страхование ----------
i=pd.read_excel('insurance-risk-measures/data/auto_insurance.xlsx'); i.columns=i.columns.str.lower()
i['state']=i.state.str.replace('STATE ','штат ')
st=i.groupby('state').paid.agg(var95=lambda x:np.percentile(x,95),mean='mean',n='size').sort_values('var95')
fig,ax=plt.subplots(figsize=(8,4.6))
top=st.var95.nlargest(1).index
b=ax.barh(st.index,st.var95,color=[ORANGE if s in top else LIGHT for s in st.index])
ax.bar_label(b,[f(v,0) for v in st.var95],padding=3,fontsize=9)
ax.set_xlabel('VaR 95%: выплата, которую превышают только 5% случаев, $')
ax.set_title('По VaR 95% самый рисковый штат 12'); ax.set_xlim(0,st.var95.max()*1.15)
fig.tight_layout(); fig.savefig('images/var_by_state.png',dpi=130); plt.close()
g=i.groupby('gender').paid
meas=pd.DataFrame({'СКО':g.std(),'Отрицательная\nполудисперсия*':g.apply(lambda x:np.sqrt(np.mean(np.maximum(x.mean()-x,0)**2))),
                   'Положительная\nполудисперсия*':g.apply(lambda x:np.sqrt(np.mean(np.maximum(x-x.mean(),0)**2))),'VaR 95%':g.quantile(.95),'Средняя выплата':g.mean()})
rel=(meas.loc['F']/meas.loc['M']-1)*100
fig,ax=plt.subplots(figsize=(8,3.4))
b=ax.bar(rel.index,rel.values,color=BLUE); ax.bar_label(b,[f'+{f(v,0)}%' if v>0 else f'{f(v,0)}%' for v in rel],padding=3)
ax.axhline(0,color='#4a5568',lw=.8); ax.set_ylabel('Женщины vs мужчины, %'); ax.set_ylim(0,rel.max()*1.25)
ax.set_title('У женщин все меры риска выше, но разница небольшая: 1–8%'); ax.tick_params(axis='x',labelsize=9)
fig.text(0.01,0.01,'* корень из полудисперсии, чтобы шкала совпадала с выплатами',fontsize=8,color='#718096')
fig.tight_layout(rect=(0,0.06,1,1)); fig.savefig('images/risk_by_gender.png',dpi=130,bbox_inches='tight'); plt.close()
print(st.round(0)); print(meas.round(1)); print(rel.round(1))
