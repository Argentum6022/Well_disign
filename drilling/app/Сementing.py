import math

well_construction=[{'Db': 349.2, 'Dm': 298.5, 'D': 273.1, 'd': 252.7, 's': 10.2, 'size': 273, 'H_intervals': 40},
                   {'Db': 250.8, 'Dm': 215.9, 'D': 193.7, 'd': 174.7, 's': 9.5, 'size': 194, 'H_intervals': 300},
                   {'Db': 171.5, 'Dm': 141.3, 'D': 127, 'd': 112, 's': 7.5, 'size': 127, 'H_intervals': 1500}]
well_type='Газовая'
cement=['До устья','До устья','До устья']

def cementing(well_construction,well_type,cementing):
    plug=20

    V_cementing=0
    #цементирование направления
    V_cementing+=((well_construction[0]['Db']*0.001)**2-(well_construction[0]['D']*0.001)**2)*math.pi*well_construction[0]['H_intervals']*0.25
    V_cementing+=(well_construction[0]['d']*0.001)**2*math.pi*0.25*plug

    #цементирование кондуктора
    V_cementing+=((well_construction[0]['d']*0.001)**2-(well_construction[1]['D']*0.001)**2)*math.pi*well_construction[0]['H_intervals']*0.25
    V_cementing+=((well_construction[1]['Db']*0.001)**2-(well_construction[1]['D']*0.001)**2)*math.pi*(well_construction[1]['H_intervals']-well_construction[0]['H_intervals'])*0.25
    V_cementing+=(well_construction[1]['d']*0.001)**2*math.pi*0.25*plug

    #цементирование оставшихся колонн
    for i in range(2,len(well_construction)):
        if cement[i]==True:
            if well_type == "Нефтяная":
                cement_long = 250
            elif well_type == 'Газовая':
                cement_long = 500
            V_cementing+=(well_construction[i]['d']*0.001)**2*math.pi*0.25*plug
            if (well_construction[i]['H_intervals'] - well_construction[i-1]['H_intervals'])>=cement_long:
                V_cementing += ((well_construction[i]['Db'] * 0.001) ** 2 - (well_construction[i]['D'] * 0.001) ** 2) * math.pi * cement_long * 0.25
            elif   (well_construction[i]['H_intervals'] - well_construction[i-1]['H_intervals'])<cement_long:
                V_cementing += ((well_construction[i]['Db'] * 0.001) ** 2 - (well_construction[i]['D'] * 0.001) ** 2) * math.pi * (well_construction[i]['H_intervals'] - well_construction[i-1]['H_intervals']) * 0.25
                V_cementing += ((well_construction[i-1]['d'] * 0.001) ** 2 - (well_construction[i]['D'] * 0.001) ** 2) * math.pi * (cement_long-(well_construction[i]['H_intervals'] - well_construction[i-1]['H_intervals'])) * 0.25

        elif cement[i]=='До устья':
            V_cementing+=(well_construction[i]['d']*0.001)**2*math.pi*0.25*plug
            V_cementing += ((well_construction[i]['Db'] * 0.001) ** 2 - (well_construction[i]['D'] * 0.001) ** 2) * math.pi * (well_construction[i]['H_intervals'] - well_construction[i - 1]['H_intervals']) * 0.25
            V_cementing += ((well_construction[i - 1]['d'] * 0.001) ** 2 - (well_construction[i]['D'] * 0.001) ** 2) * math.pi * well_construction[i - 1]['H_intervals'] * 0.25

    return round(V_cementing,3)

a=cementing(well_construction,well_type,cement)
print(a)