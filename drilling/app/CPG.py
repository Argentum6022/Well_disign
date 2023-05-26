import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
#H=[100,200,540,750,1300]
#Pre=[1,2,5,8,15]
#H_course=40
#H_conductor=300


def CPG(H,Pre,H_course,H_conductor):
    Pfr=[]
    Ka=[]
    Kfr=[]
    Phs=[]
    Kgr=[]
    Kaz=[]
    Kfrz=[]
    n = len(H)
    for i in range(n):                              # Получение расчётных данных
        Pfr.append(0.0083*H[i]+0.66*Pre[i])
        Phs.append(1000*9.81*H[i]*10**-6)
        Ka.append(round(Pre[i]/Phs[i],3))
        Kfr.append(round(Pfr[i]/Phs[i],3))
    fig =go.Figure()
    H_fig=H.copy()
    Ka_fig=Ka.copy()
    Kfr_fig=Kfr.copy()
    j=0
    s=0
    for l in range(len(Ka_fig)-1):
        if Ka_fig[l]!=Ka_fig[l+1]:
            s+=1
    while j<n+s:                                  # Выравнивание графика пластовых давлений
        try:
                Ka_fig.insert(j+1,Ka_fig[j])
                H_fig.insert(j+1,H_fig[j+1])
        except:
                print('error')
        j+=2
    Ka_fig.insert(0, Ka_fig[0])
    H_fig.insert(0, 0)
    H_fig.append(H_fig[-1]+300)
    Ka_fig.append(Ka_fig[-1])

    fig.add_trace(go.Scatter(x=Ka_fig, y=H_fig,name='P пластовое<sup></sup>'))

    k=0
    while k<n+s:                                     # Выравнивание графика давлений насыщения
        try:
                Kfr_fig.insert(k+1,Kfr_fig[k])
        except:
                print('error')
        k+=2
    Kfr_fig.insert(0, Kfr_fig[0])
    Kfr_fig.append(Kfr_fig[-1])
    for p in Kfr_fig:
        Kgr.append(p*1.2)
    for k in range(len(H_fig)):
        if H_fig[k]<=1200:
            Kaz.append(Ka_fig[k]*1.1)
            Kfrz.append(Kfr_fig[k]*0.9)
        elif H_fig[k]>1200:
            Kaz.append(Ka_fig[k]*1.05)
            Kfrz.append(Kfr_fig[k]*0.95)
    fig.add_trace(go.Scatter(x=Kfr_fig, y=H_fig,name='P насыщения<sup></sup>'))
    fig.add_trace(go.Scatter(x=Kgr, y=H_fig,name='P гидроразрыва<sup></sup>'))
    fig.add_trace(go.Scatter(x=Kaz, y=H_fig,name='P граничное<sup></sup>'))
    fig.add_trace(go.Scatter(x=Kfrz, y=H_fig,name='P граничное<sup></sup>'))
    fig.update_layout(legend_orientation="h",
                title="График совмещенных давлений",
                xaxis_title="Градиент давлений, МПа/100м",
                yaxis_title="Глубина спуска колонн, м",
                margin=dict(l=30, r=30, t=30, b=30))

    intervals=0
    H_intervals=[0]


    for popa in range (1,len(H_fig)-1):
        if Kfrz[popa]<=Kaz[popa] or Kfrz[popa]<=Kaz[popa+1] or Kfrz[popa]<=Kaz[popa-1]:
            H_int = []
            Ka_int = []
            Kfr_int = []
            K_well = []
            H_well = []
            H_intervals.append(H_fig[popa])
            H_int=H_fig[H_fig.index(H_intervals[-2])+1:H_fig.index(H_intervals[-1])+1]
            Ka_int=Kaz[H_fig.index(H_intervals[-2])+1:H_fig.index(H_intervals[-1])+1]
            Kfr_int=Kfrz[H_fig.index(H_intervals[-2])+1:H_fig.index(H_intervals[-1])+1]
            K_min=max(Ka_int)
            K_max=min(Kfr_int)

            H_well.append(H_intervals[-2])
            H_well.append(H_intervals[-1])
            H_well.append(H_intervals[-1])
            H_well.append(H_intervals[-2])
            H_well.append(H_intervals[-2])

            K_well.append(K_min)
            K_well.append(K_min)
            K_well.append(K_max)
            K_well.append(K_max)
            K_well.append(K_min)
            intervals+=1
            fig.add_trace(go.Scatter(x=K_well, y=H_well, name='Интервал бурения<sup></sup>'))

    H_int = []
    Ka_int = []
    Kfr_int = []
    K_well = []
    H_well = []
    H_intervals.append(H_fig[-1])
    H_int = H_fig[H_fig.index(H_intervals[-2]) + 1:H_fig.index(H_intervals[-1]) + 1]
    Ka_int = Kaz[H_fig.index(H_intervals[-2]) + 1:H_fig.index(H_intervals[-1]) + 1]
    Kfr_int = Kfrz[H_fig.index(H_intervals[-2]) + 1:H_fig.index(H_intervals[-1]) + 1]
    K_min = max(Ka_int)
    K_max = min(Kfr_int)

    H_well.append(H_intervals[-2])
    H_well.append(H_intervals[-1])
    H_well.append(H_intervals[-1])
    H_well.append(H_intervals[-2])
    H_well.append(H_intervals[-2])

    K_well.append(K_min)
    K_well.append(K_min)
    K_well.append(K_max)
    K_well.append(K_max)
    K_well.append(K_min)
    intervals += 1
    fig.add_trace(go.Scatter(x=K_well, y=H_well, name='Интервал бурения<sup></sup>'))

    fig.update_yaxes(range=[H[-1]+500,-100 ])                   #Коэффициенты для масштаба?
    fig.update_xaxes(range=[min(Ka)-0.1, max(Kgr)+0.1],side='top')
    fig.show()


    intervals+=2
    H_intervals[0]=H_course
    H_intervals.insert(1,H_conductor)
    return H_intervals,intervals

#a=CPG(H,Pre,H_course,H_conductor)
#print(a)
