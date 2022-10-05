import moose
import rdesigneur as rd
import matplotlib.pyplot as plt
import brute_curvefit
import numpy as np

Em = -0.065
stim_start = 0.05
stimamp = -25e-12
elecDt = 5e-5
elecPlotDt = 5e-5
RM_soma = 0.11696
CM_soma = 1e-2 ##somatic capacitance is 3.19e-12F
RA_soma = 1.18
RM_dend = 1.86794368
CM_dend = 0.02411617
RA_dend = 1.18

def get_Vmsinglecompt():
    if moose.exists('model'):
        moose.delete('model')
    if moose.exists("Graphs"):
        moose.delete("Graphs")
    if moose.exists("library"):
        moose.delete("library")

    rdes = rd.rdesigneur(
        elecDt = elecDt,
        elecPlotDt = elecPlotDt,
        passiveDistrib = [['soma', 'Cm', f'{138e-12}', 'Rm', f'{168e6}', 'Em', f'{Em}', 'initVm', f'{Em}'],],
        stimList = [['soma', '1', '.', 'inject', f'(t>={stim_start} && t<0.5) * {stimamp}']],
        # stimList = [['soma', '1', '.', 'inject', f'(t>{stim_start}) * sin(3.14159265359*(t-{stim_start})^2) * {stimamp}']],
        plotList = [['soma', '1', '.', 'Vm', 'Soma membrane potential'],
            ['soma', '1', '.', 'inject', 'Stimulus current']],
    )

    # Setup clock table to record time
    clk = moose.element("/clock")
    moose.Neutral("Graphs")
    plott = moose.Table("/Graphs/plott")
    moose.connect(plott, "requestOut", clk, "getCurrentTime")

    rdes.buildModel()
    moose.reinit()
    moose.start( 1 )
    Vmvec = moose.element("/model/graphs/plot0").vector
    tvec = moose.element("/Graphs/plott").vector
    Ivec = moose.element("/model/graphs/plot1").vector

    return [tvec, Ivec, Vmvec]

def get_Vm(RA_soma=RA_soma, RM_dend=RM_dend,CM_dend=CM_dend,RA_dend=RA_dend):
    if moose.exists('model'):
        moose.delete('model')
    if moose.exists("Graphs"):
        moose.delete("Graphs")
    if moose.exists("library"):
        moose.delete("library")

    rdes = rd.rdesigneur(
        elecDt = elecDt,
        elecPlotDt = elecPlotDt,
        cellProto = [['ballAndStick', 'soma', 10.075e-6, 10.075e-6, 4e-6, 500e-6, 10]],
        passiveDistrib = [['soma', 'CM', f'{CM_soma}', 'RM', f'{RM_soma}', 'RA', f'{RA_soma}', 'Em', f'{Em}', 'initVm', f'{Em}'],
            ['dend#', 'CM', f'{CM_dend}', 'RM', f'{RM_dend}', 'RA', f'{RA_dend}', 'Em', f'{Em}', 'initVm', f'{Em}']],
        stimList = [['soma', '1', '.', 'inject', f'(t>={stim_start} && t<0.5) * {stimamp}']],
        # stimList = [['soma', '1', '.', 'inject', f'(t>{stim_start}) * sin(3.14159265359*(t-{stim_start})^2) * {stimamp}']],
        plotList = [['soma', '1', '.', 'Vm', 'Soma membrane potential'],
            ['soma', '1', '.', 'inject', 'Stimulus current']],
    )

    # Setup clock table to record time
    clk = moose.element("/clock")
    moose.Neutral("Graphs")
    plott = moose.Table("/Graphs/plott")
    moose.connect(plott, "requestOut", clk, "getCurrentTime")

    rdes.buildModel()
    moose.reinit()
    moose.start( 1 )
    Vmvec = moose.element("/model/graphs/plot0").vector
    tvec = moose.element("/Graphs/plott").vector
    Ivec = moose.element("/model/graphs/plot1").vector

    return [tvec, Ivec, Vmvec]

def get_scaledpasproperties(ttt=[1,2,3], RM_dend=RM_dend):
    tvec, Ivec, Vmvec = get_Vm(RA_soma=RA_soma, RM_dend=RM_dend,CM_dend=CM_dend,RA_dend=RA_dend)

    #### Calculate input resistance and capacitance#############################################
    E_rest = np.median(Vmvec[tvec>0.6])
    def chargingm25_1(t, R,tau):
        return (
            E_rest - R * 25e-12 * (1 - np.exp(-t / tau))
        )
    tempv = Vmvec[(tvec >= stim_start) & (tvec <= stim_start + 0.2)]

    RCfitted_chm25, errorm25 = brute_curvefit.brute_scifit(
        chargingm25_1,
        np.linspace(0, 0.2, len(tempv)),
        tempv,
        restrict=[[5e6, 0], [1000e6, 0.1]],
        ntol=1000,
        printerrors=False,
        parallel=False,
    )
    Rin, Cin = RCfitted_chm25[0], RCfitted_chm25[1]/RCfitted_chm25[0]

    # print(f'{Cin=}', f'{Rin=}', f'{RCfitted_chm25=}', f'{errorm25=}',)

    # plt.figure()
    # plt.plot(np.linspace(0, 0.2, len(tempv)), tempv)
    # plt.plot(np.linspace(0, 0.2, len(tempv)), chargingm25_1(np.linspace(0, 0.2, len(tempv)), *RCfitted_chm25))
    #################################################

    return [Rin*1e-6, Cin*1e12]


# act_pas = [168, 138]
# # get_Vm(RA_soma=RA_soma, RM_dend=RM_dend,CM_dend=CM_dend,RA_dend=RA_dend)
# # get_Vm(RA_soma=RA_soma, RM_dend=RM_dend,CM_dend=CM_dend,RA_dend=RA_dend)
# fitted, error = brute_curvefit.brute_scifit(
#         get_scaledpasproperties,
#         [1,2,3],
#         act_pas,
#         restrict=[[0.5], [4]],
#         ntol=1000,
#         returnnfactor=0.01,
#         maxfev=1000,
#         printerrors=True,
#         parallel=True,
#         savetofile=False,
#     )

# print(f'fitted = {fitted}', f'error={error}')

# fitted = [1e-5, 1.96,0.02,1e-5] ##If the RA is too low 
fitted = [1.2]
print(get_scaledpasproperties([1,2,3], *fitted))
tvec, Ivec, Vmvec = get_Vm(RM_dend=fitted[0])
tvec_o, Ivec_o, Vmvec_o = get_Vmsinglecompt()
plt.plot(tvec, Vmvec, label='fitted')
plt.plot(tvec_o, Vmvec_o, label='full morphology single compt equivalent')
plt.legend()
plt.show()



