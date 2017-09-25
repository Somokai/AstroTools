import subprocess
import os
import time
import collections
import numpy as np


def param(p, min, max, outCount):
    value = []
    i = 0
    j = 0
    while i < 10:
        value.append(min+i*(max-min)/10)
        i += 1
    input=[p, value]
    print('The length is' + str(len(input[1])))
    while j < 10:
        initial(input[0], input[1][j], outCount)
        j += 1
        outCount += 1
    return outCount
    
def initial(param, value, outCount):
    f = open('../Plots/mctherm_original.par', 'r')
    file = f.readlines()
    f.close()
    mctherm = collections.OrderedDict()
    for line in file:
        #print(line + '\n')
        linesplit = [l.split('=') for l in line.split('\n')]
        #print(linesplit)
        if len(linesplit[0]) > 2:
            mctherm[linesplit[0][1].strip(' =')] = linesplit[0][0]
    #print(mctherm)
    mctherm[param] = value
    mcnew = []
    #print('here')
    for key, value in mctherm.items():
        l = str(value) + '=' + str(key) + '='
        mcnew.append(l)
    #print(mcnew)
    if outCount >= 1:
        l = '/home/fernanrb/pigpen/Zac/hochunk3d/models/PDS70/Output' + str(outCount)
        print(l)
        os.chdir(l)
        with open('mctherm.par', 'w') as file:
            for item in mcnew:
                file.write("%s\n" % item)
    else:
        l = '/home/fernanrb/pigpen/Zac/hochunk3d/models/PDS70/Output'
        os.chdir(l)     
        
    os.system('condor_submit submit.std')


outC = 0
outC = param('A(1)',2,3,outC)
outC = param('B(1)',1,2,outC)
outC = param('FMASSD1',0,1,outC)



