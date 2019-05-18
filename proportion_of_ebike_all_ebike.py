# -*- coding: utf-8 -*-

"""
simulation model with different number of e-bikes
"""


import Sim_random_pick_CRN_751
from datetime import timedelta as td
from datetime import datetime as time
from copy import deepcopy

start_time = time(2017,7,1,hour= 18)
end_time=start_time+ td(weeks=50)
initial_stations=eval(open(("stations_initial_751.txt")).read())

for bikestation in initial_stations.keys():
    initial_stations[bikestation]['ecap']= initial_stations[bikestation]['cap']
    initial_stations[bikestation]['bike']=0
    initial_stations[bikestation]['cap']=0
    initial_stations[bikestation]['edock'] = initial_stations[bikestation]['ecap']

initial_stations_copy = deepcopy(initial_stations)

propotion_of_ebike_list=[0.6]

for num_ebike in propotion_of_ebike_list:
    for station in initial_stations.keys():
        initial_stations[station]['ebike']=round(initial_stations[station]['ecap']*num_ebike)
    gc=Sim_random_pick_CRN_751.GlobalClock(start_time,end_time,initial_stations)
    print('propotion_ebike: ',num_ebike)
    gc.clockAdvance()

    w_demandlost=list(gc.week_demandlost.values())[2:]

    w_three_trip_error=list(gc.week_three_trip_error.values())[2:]

    w_ebike_return_full=list(gc.week_ebike_return_full.values())[2:]

    w_average_SOC=list(gc.week_average_SOC.values())[2:]

    w_out_of_battery=list(gc.week_out_of_battery.values())[2:]

    w_num_etrip=list(gc.week_num_etrip.values())[2:]

    w_demandlost_causedby_battery=list(gc.week_demandlost_causedby_battery)[2:]

    x=range(0,len(w_demandlost))

    with open('simdata/ebikes_'+str(num_ebike)+'.csv','w') as f:
        f.write('week,ebike_return_error,lost_demand,out_of_battery_trips,lost_demand_causedby_battery,three_error,ebike_trips\n')
        for week in x:
            f.write(str(week+1)+','+str(w_ebike_return_full[week])+','+str(w_demandlost[week])+','+str(w_out_of_battery[week])+','+str(w_demandlost_causedby_battery[week])+','+str(w_three_trip_error[week])+','+str(w_num_etrip[week])+'\n')
    steady = {}
    for i in gc.stations.keys():
        temp={}
        temp['ebike'] = len(gc.stations[i].ebike)
        temp['ecap'] = gc.stations[i].ebike_cap
        temp['edock'] = gc.stations[i].edock
        temp['bike'] = 0
        temp['cap'] = 0
        steady[i] = temp
    f = open("steady_states_751/steady_ebikes_initial_"+str(num_ebike)+".txt","w")
    f.write(str(steady))
    f.close()

    initial_stations = deepcopy(initial_stations_copy)

