import moose
import rdesigneur as rd
import matplotlib.pyplot as plt
import numpy as np

Em = -0.065
stim_start = 0.05
stimamp = -25e-12
elecDt = 5e-5
elecPlotDt = 5e-5
RM_soma = 0.11696
CM_soma = 1e-2
RA_soma = 1.18
RM_dend = 0.11696
CM_dend = 1e-2
RA_dend = 1.18

rdes = rd.rdesigneur(
    elecDt = elecDt,
    elecPlotDt = elecPlotDt,
    cellProto = [['ballAndStick', 'soma', 10.075e-6, 10.075e-6, 4e-6, 500e-6, 10]],
    # passiveDistrib = [['soma', 'CM', f'{CM_soma}', 'RM', f'{RM_soma}', 'RA', f'{RA_soma}', 'Em', f'{Em}', 'initVm', f'{Em}'],
    #     ['dend#', 'CM', f'{CM_dend}', 'RM', f'{RM_dend}', 'RA', f'{RA_dend}', 'Em', f'{Em}', 'initVm', f'{Em}']],
    stimList = [['soma', '1', '.', 'inject', f'(t>={stim_start} && t<0.5) * {stimamp}']],
    # stimList = [['soma', '1', '.', 'inject', f'(t>{stim_start}) * sin(3.14159265359*(t-{stim_start})^2) * {stimamp}']],
    plotList = [['soma', '1', '.', 'Vm', 'Soma membrane potential'],
        ['soma', '1', '.', 'inject', 'Stimulus current']],
)

rdes.buildModel()
moose.reinit()
moose.start(1)
rdes.display()

moose.delete('model')
moose.delete('library')

rdes = rd.rdesigneur(
    elecDt = elecDt,
    elecPlotDt = elecPlotDt,
    cellProto = [['ballAndStick', 'soma', 10.075e-6, 10.075e-6, 4e-6, 500e-6, 10]],
    # passiveDistrib = [['soma', 'CM', f'{CM_soma}', 'RM', f'{RM_soma}', 'RA', f'{RA_soma}', 'Em', f'{Em}', 'initVm', f'{Em}'],
    #     ['dend#', 'CM', f'{CM_dend}', 'RM', f'{RM_dend}', 'RA', f'{RA_dend}', 'Em', f'{Em}', 'initVm', f'{Em}']],
    stimList = [['soma', '1', '.', 'inject', f'(t>={stim_start} && t<0.5) * {stimamp}']],
    # stimList = [['soma', '1', '.', 'inject', f'(t>{stim_start}) * sin(3.14159265359*(t-{stim_start})^2) * {stimamp}']],
    plotList = [['soma', '1', '.', 'Vm', 'Soma membrane potential'],
        ['soma', '1', '.', 'inject', 'Stimulus current']],
)

rdes.buildModel()
moose.reinit()
moose.start(1)
rdes.display()