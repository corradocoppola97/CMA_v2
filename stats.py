import torch
from matplotlib import pyplot as plt
import os
import numpy as np
seeds = [10,100,1000,10000]
dataset_list = [ds[:-4] for ds in os.listdir('dataset')]
big_datasets = ['BlogFeedback', 'Covtype', 'Protein', 'Skin NonSkin', 'YearPredictionMSD']
small_datasets = [d for d in dataset_list if d not in big_datasets]
os.chdir('prove_reg')
architectures = ['S','M','L','XL','XXL','XXXL','4XL']
all_probs = [(ds,net) for ds in dataset_list for net in architectures]
import plotly.graph_objs as go

def average_nfev(architectures, dataset_list, flagtitle):
    d = {}
    CMA = []
    for seed in seeds:
        for ds in dataset_list:
            for architecture in architectures:
                file = 'history_cma_'+architecture+'_'+ds+'_seed_'+str(seed)+'.txt'
                stats = torch.load(file)
                avg_nfev = stats['nfev']/(len(stats['train_loss'])-1)
                CMA.append(avg_nfev)

    NMCMA = []
    for seed in seeds:
        for ds in dataset_list:
            for architecture in architectures:
                file = 'history_nmcma_'+architecture+'_'+ds+'_seed_'+str(seed)+'.txt'
                stats = torch.load(file)
                avg_nfev = stats['nfev']/(len(stats['train_loss'])-1)
                NMCMA.append(avg_nfev)

    d['CMA'] = np.array(CMA)
    d['NMCMA'] = np.array(NMCMA)
    fig = go.Figure()
    fig.add_trace(go.Box(y=d['CMA'], name='CMA',marker_color='blue'))
    fig.add_trace(go.Box(y=d['NMCMA'], name='NMCMA', marker_color='red'))
    fig.update_layout(width=400, height=400,
                      title=flagtitle,
                      title_x=0.5,
                      yaxis_title="nfev",
                      font=dict(
                          family="Courier New, monospace",
                          size=12,
                          color="RebeccaPurple"
                      ))
    fig.write_image('images\\Avg_nfev_'+flagtitle+ '_' +'.png')





def linesearch_failures(architectures, dataset_list, flagtitle):
    d = {}

    CMA = []
    for seed in seeds:
        for ds in dataset_list:
            for architecture in architectures:
                file = 'history_cma_'+architecture+'_'+ds+'_seed_'+str(seed)+'.txt'
                stats = torch.load(file)
                ls_failures = len([_ for _ in stats['Exit'] if _ in {'13b','13c'}])
                CMA.append(ls_failures)

    NMCMA = []
    for seed in seeds:
        for ds in dataset_list:
            for architecture in architectures:
                file = 'history_nmcma_'+architecture+'_'+ds+'_seed_'+str(seed)+'.txt'
                stats = torch.load(file)
                ls_failures = len([_ for _ in stats['Exit'] if _ in {'16','10'}])
                NMCMA.append(ls_failures)

    d['CMA'] = np.array(CMA)
    d['NMCMA'] = np.array(NMCMA)
    fig = go.Figure()
    fig.add_trace(go.Box(y=d['CMA'], name='CMA',marker_color='blue'))
    fig.add_trace(go.Box(y=d['NMCMA'], name='NMCMA', marker_color='red'))
    fig.update_layout(width=400, height=400,
                      title=flagtitle,
                      title_x=0.5,
                      yaxis_title="LS failures",
                      font=dict(
                          family="Courier New, monospace",
                          size=12,
                          color="RebeccaPurple"
                      ))
    fig.write_image('images\\Avg_LSfail_'+flagtitle+'.png')


def acceptance_inner_cycle(architectures, dataset_list, flagtitle):
    d = {}

    CMA = []
    for seed in seeds:
        for ds in dataset_list:
            for architecture in architectures:
                file = 'history_cma_'+architecture+'_'+ds+'_seed_'+str(seed)+'.txt'
                stats = torch.load(file)
                avg_accepted = len(stats['accepted'])/(len(stats['train_loss'])-1)
                CMA.append(avg_accepted)

    NMCMA = []
    for seed in seeds:
        for ds in dataset_list:
            for architecture in architectures:
                file = 'history_nmcma_'+architecture+'_'+ds+'_seed_'+str(seed)+'.txt'
                stats = torch.load(file)
                avg_accepted = len(stats['accepted'])/(len(stats['train_loss'])-1)
                NMCMA.append(avg_accepted)

    d['CMA'] = np.array(CMA)
    d['NMCMA'] = np.array(NMCMA)
    fig = go.Figure()
    fig.add_trace(go.Box(y=d['CMA'], name='CMA',marker_color='blue'))
    fig.add_trace(go.Box(y=d['NMCMA'], name='NMCMA', marker_color='red'))
    fig.update_layout(width=400, height=400,
                      title=flagtitle,
                      title_x=0.5,
                      yaxis_title="IC accepted",
                      font=dict(
                          family="Courier New, monospace",
                          size=12,
                          color="RebeccaPurple"
                      ))
    fig.write_image('images\\Avg_ICacc_'+flagtitle+'.png')


def final_step_size(architectures, dataset_list, flagtitle):
    d = {}

    CMA = []
    for seed in seeds:
        for ds in dataset_list:
            for architecture in architectures:
                file = 'history_cma_' + architecture + '_' + ds + '_seed_' + str(seed) + '.txt'
                stats = torch.load(file)
                zeta_final = stats['step_size'][-1]
                CMA.append(zeta_final)

    NMCMA = []
    for seed in seeds:
        for ds in dataset_list:
            for architecture in architectures:
                file = 'history_nmcma_' + architecture + '_' + ds + '_seed_' + str(seed) + '.txt'
                stats = torch.load(file)
                zeta_final = stats['step_size'][-1]
                NMCMA.append(zeta_final)

    IG = []
    for seed in seeds:
        for ds in dataset_list:
            for architecture in architectures:
                file = 'history_ig_' + architecture + '_' + ds + '_seed_' + str(seed) + '.txt'
                stats = torch.load(file)
                zeta_final = stats['step_size'][-1]
                IG.append(zeta_final)

    d['CMA'] = np.array(CMA)
    d['NMCMA'] = np.array(NMCMA)
    d['IG'] = np.array(IG)
    fig = go.Figure()
    fig.add_trace(go.Box(y=d['CMA'], name='CMA',marker_color='blue'))
    fig.add_trace(go.Box(y=d['NMCMA'], name='NMCMA', marker_color='red'))
    fig.add_trace(go.Box(y=d['IG'], name='IG', marker_color='green'))
    fig.update_layout(width=400, height=400,
                      title=flagtitle,
                      title_x=0.5,
                      yaxis_title="final_zeta",
                      font=dict(
                          family="Courier New, monospace",
                          size=12,
                          color="RebeccaPurple"
                      ))
    fig.write_image('images\\final_stepsize_'+flagtitle+'.png')


if __name__ == '__main__':
    average_nfev(['S','M','L','XL'],small_datasets,'SmallData_SmallNet')
    average_nfev(['XXL','XXXL','4XL'],big_datasets,'BigData_BigNet')
    average_nfev(['S','M','L','XL'],big_datasets,'BigData_SmallNet')
    average_nfev(['XXL','XXXL','4XL'],small_datasets,'SmallData_BigNet')

    linesearch_failures(['S','M','L','XL'],small_datasets,'SmallData_SmallNet')
    linesearch_failures(['XXL','XXXL','4XL'],big_datasets,'BigData_BigNet')
    linesearch_failures(['S','M','L','XL'],big_datasets,'BigData_SmallNet')
    linesearch_failures(['XXL','XXXL','4XL'],small_datasets,'SmallData_BigNet')

    acceptance_inner_cycle(['S','M','L','XL'],small_datasets,'SmallData_SmallNet')
    acceptance_inner_cycle(['XXL','XXXL','4XL'],big_datasets,'BigData_BigNet')
    acceptance_inner_cycle(['S','M','L','XL'],big_datasets,'BigData_SmallNet')
    acceptance_inner_cycle(['XXL','XXXL','4XL'],small_datasets,'SmallData_BigNet')

    final_step_size(['S','M','L','XL'],small_datasets,'SmallData_SmallNet')
    final_step_size(['XXL','XXXL','4XL'],big_datasets,'BigData_BigNet')
    final_step_size(['S','M','L','XL'],big_datasets,'BigData_SmallNet')
    final_step_size(['XXL','XXXL','4XL'],small_datasets,'SmallData_BigNet')

"""        linesearch_failures(arch, small_datasets, 'small')
        linesearch_failures(arch, big_datasets, 'big')
        acceptance_inner_cycle(arch, small_datasets, 'small')
        acceptance_inner_cycle(arch, big_datasets, 'big')
        final_step_size(arch,small_datasets,'small')
        final_step_size(arch,big_datasets,'big')"""
