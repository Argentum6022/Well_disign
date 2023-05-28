from matplotlib import pyplot as plt

H=[500,1000,1500,2000,2500,3000]
Pre=[4.9,9.8,14.7,19.6,24.5,28.5]
H_course=40
H_conductor=300


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
    H_fig=H.copy()
    Ka_fig=Ka.copy()
    Kfr_fig=Kfr.copy()
    j=0
    s=0
    for l in range(len(Ka_fig)-1):
        if Ka_fig[l]!=Ka_fig[l+1]:
            s+=1
    while j<=n+s:                                  # Выравнивание графика пластовых давлений
        try:
                Ka_fig.insert(j+1,Ka_fig[j])
                H_fig.insert(j+1,H_fig[j+1])
        except:
                print('error1')
        j+=2
    Ka_fig.insert(0, Ka_fig[0])
    H_fig.insert(0, 0)


    plt.plot(Ka_fig,H_fig,'m',label='P пластовое',lw=3)
    k=0
    while k<=n+s:                                     # Выравнивание графика давлений насыщения
        try:
                Kfr_fig.insert(k+1,Kfr_fig[k])
        except:
                print('error2')
        k+=2
    Kfr_fig.insert(0, Kfr_fig[0])
    for p in Kfr_fig:
        Kgr.append(p*1.2)
    for k in range(len(H_fig)):
        if H_fig[k]<=1200:
            Kaz.append(Ka_fig[k]*1.1)
            Kfrz.append(Kfr_fig[k]*0.9)
        elif H_fig[k]>1200:
            Kaz.append(Ka_fig[k]*1.05)
            Kfrz.append(Kfr_fig[k]*0.95)

    plt.plot(Kfr_fig,H_fig,'c',label='P насыщения',lw=3)
    plt.plot(Kgr,H_fig,'r',label='P гидроразрыва',lw=3)
    plt.plot(Kaz,H_fig,'g',label='P граничное',lw=3)
    plt.plot(Kfrz,H_fig,'b',label='P граничное',lw=3)
    plt.title("График совмещенных давлений")
    plt.ylabel('Глубина спуска колонн, м')
    plt.xlabel('Градиент давлений, МПа/100м')

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
            plt.plot(K_well, H_well, ':r', label='Интервал бурения', lw=4)
            plt.fill(K_well, H_well, 'r',alpha=0.2)

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
    plt.plot(K_well, H_well, ':r', label='Интервал бурения', lw=4)
    plt.fill(K_well, H_well, 'r', alpha=0.2)
    plt.minorticks_on()

    plt.xlim([min(Ka)-0.1,max(Kgr)+0.1])
    plt.ylim([-100,H[-1]+200])
    plt.legend()
    plt.gca().invert_yaxis()
    plt.grid(which='major')
    plt.grid(which='minor', linestyle=':')
    plt.tight_layout()
    plt.show()


    intervals+=2
    H_intervals[0]=H_course
    H_intervals.insert(1,H_conductor)
    return H_intervals,intervals

a=CPG(H,Pre,H_course,H_conductor)
print(a)
