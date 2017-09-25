# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 15:26:28 2016

@author: Somokai
"""

def stripper(file, name):
    lines = file.read().split(' ')
    temp = []
    i = 0   
    while i < len(lines):
        if lines[i] != '':
            temp.append(lines[i].strip())
        i += 1
    lines = temp
    file = open(name +'.txt', 'w+')
    for item in lines:
        file.write(item)
        file.write('\n')
    file.close()
   
folder = 'Mis_50_Inner_Ring/Trial_2'
usr = 'uberg'

w_rangel = 151
w_rangeu = 153

stellar = open('C:/Users/'+usr+'/Dropbox/Research/HD100453/Plots/Fits_Images_PA_220/'+folder+'/stellar.txt')
stripper(stellar, 'stellar_arr')
stellar.close()
thermal = open('C:/Users/'+usr+'/Dropbox/Research/HD100453/Plots/Fits_Images_PA_220/'+folder+'/thermal.txt')
stripper(thermal, 'thermal_arr')
thermal.close()
'''total = open('C:/Users/'+usr+'/Dropbox/Research/HD100453/Plots/Fits_Images_PA_220/'+folder+'/total.txt')
stripper(total, 'total_arr')
total.close()
scattered = open('C:/Users/'+usr+'/Dropbox/Research/HD100453/Plots/Fits_Images_PA_220/'+folder+'/scattered.txt')
stripper(scattered, 'scattered_arr')
scattered.close()
wavelength = open('C:/Users/'+usr+'/Dropbox/Research/HD100453/Plots/Fits_Images_PA_220/'+folder+'/wavelength.txt')
stripper(wavelength, 'wavelength_arr')
wavelength.close()'''

