# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 18:25:26 2020

@author: А
"""

import math
import xlrd
from prettytable import PrettyTable
import matplotlib.pyplot as plt
from scipy.stats.kde import gaussian_kde
from numpy import linspace, hstack
from pylab import plot, show, hist
import pandas as pd

class Work1:
    def __init__(self, Array):
        self.N=len(Array)
        print ("Num of elements: " + str(self.N))
        self.m = 1 + math.log2(self.N)
        self.m = self.Rounding(self.m)
        print ("Num of groups: " + str(self.m))
        self.Group(self.N, self.m)
        self.Kernel()
        
    def Group(self, N, m):
        self.Del = (max(Array) - min(Array))/m
        self.Del = self.Rounding(self.Del)
        print("Gap is " + str(self.Del))
        
        self.C = []
        self.C.append(min(Array))
        print ("C1 is " + str(self.C[0]))
        self.i = 0
        while self.i < m:
            self.C.append(self.Borders(self.C[self.i], self.Del))
            print ("C" + str(self.i+2) + " is " + str(self.C[self.i+1]))
            self.i=self.i+1
        
        self.CA = []
        self.i = 0
        while self.i < m:
            self.CA.append(self.Average_in_gap(self.C[self.i], self.C[self.i+1]))
            print ("Average " + str(self.i+1) + " - " + str(self.i+2) + " is " + str(self.CA[self.i]))
            self.i=self.i+1
        
        self.F = []
        self.i = 0
        while self.i < m:
            self.F.append(self.Num_elmnts_in_group(self.C[self.i], self.C[self.i + 1]))
            print("Num elements in group " + str(self.i+1) + " is " + str(self.F[self.i]))
            self.i=self.i+1
            
        self.RelF = []
        self.i = 0
        for self.i in self.F:
            self.RelF.append(self.i / N)
        print ("Relative frequency is ")
        print (self.RelF)
        
        self.GA = []
        self.i = 0
        while self.i < m:
            self.GA.append(self.Group_average(self.C[self.i], self.C[self.i + 1]))
            print("Average in group " + str(self.i+1) + " is " + str(self.GA[self.i]))
            self.i = self.i+1       
        
        self.NumOfGroup = []
        self.Yoha = 0
        while self.Yoha < m:
            self.NumOfGroup.append(self.Yoha+1)
            self.Yoha = self.Yoha + 1
        self.TableCreator(self.C, self.CA, self.GA, self.F, self.RelF, m)
        
        self.PercentRelF = []
        self.K = 0
        for self.K in self.RelF:
            self.PercentRelF.append(self.K*100)
            
        self.K = 0
        self.Den = []
        for self.K in self.RelF:
            self.Den.append(self.K/self.Del)
        self.K = 0
        self.Inter = []
        while self.K < m:
            self.Inter.append("[" + str(self.C[self.K]) + ';' + str(self.C[self.K + 1]) + ")")
            self.K = self.K + 1
            
        print ("Histogramma of frequency")
        self.Histogramma1(self.NumOfGroup, self.F)
        print ("Histograma of relative frequency in %")
        self.Histogramma2(self.NumOfGroup, self.PercentRelF)
        print ("Histograma of estimation of the probability density")
        self.Histogramma3(self.Inter, self.Den)
        
        return 0
    
    def Rounding(self, X):
        if (X - math.floor(X) >= 0.5):
            return (math.ceil(X))
        else:
            return (math.floor(X))
        
    def Borders(self, C1, Del):
        return (C1 + Del)
    
    def Average_in_gap(self, C1, C2):
        return ((C1+C2)/2)
    
    def Num_elmnts_in_group(self, C1, C2):
        self.Count=0
        for self.K in Array:
            if (self.K >= C1) and (self.K < C2):
                self.Count = self.Count+1
        return self.Count
    
    def Group_average(self, C1, C2):
        self.K = 0
        self.Count = 0
        self.Sum = 0
        for self.K in Array:
            if (self.K >= C1) and (self.K < C2):
                self.Sum = self.Sum + self.K
                self.Count = self.Count+1
        return (self.Sum/self.Count)
        
    def TableCreator(self, C, CA, GA, F, RelF, m):
        self.th = ['# of group', 'Interval', 'Interval average', 'Group average', 'Frequency', 'Relative frequency']
        self.DataArray = []
        self.CC = 0
        while self.CC < m:
            self.DataArray.extend([self.CC+1,"[" + str(C[self.CC]) + ";" + str(C[self.CC+1]) + ")", CA[self.CC], GA[self.CC], F[self.CC], RelF[self.CC]])
            self.CC=self.CC+1
        self.col = len(self.th)
        self.table = PrettyTable(self.th)
        self.td = self.DataArray
        while self.td:
            self.table.add_row(self.td[:self.col])
            self.td = self.td[self.col:]
        print (self.table)
        return 0
    
    def Histogramma1(self, Arr1, Arr2):
        plt.title("Histogramma of frequency")
        plt.xlabel("# of group")
        plt.ylabel("Frequency")
        plt.bar(Arr1, Arr2, width = 0.1, color = 'red')
        plt.show()
        return 0
    
    def Histogramma2(self, Arr1, Arr2):
        plt.title("Histograma of relative frequency in %")
        plt.xlabel("# of group")
        plt.ylabel("Relative frequency")
        plt.bar(Arr1, Arr2)
        plt.show()
        return 0
    
    def Histogramma3(self, Arr1, Arr2):
        plt.figure(figsize=(9, 9), constrained_layout=True)
        plt.title("Histograma of estimation of the probability density")
        plt.xlabel("Interval")
        plt.ylabel("Dencity")
        plt.bar(Arr1, Arr2, width = 1)
        plt.show()
        return 0
    
    def Kernel(self):
        AH = pd.read_csv('Auto.txt', sep = "\t", header = 0, index_col = False)
        my_density = gaussian_kde(AH['Power'])
        x = linspace(min(AH['Power']), max(AH['Power']), 1000)
        print ("Kernel Density Estimation:")
        plot(x, my_density(x), 'r')
        return 0
        
        
        
rb=xlrd.open_workbook('auto.xls' ,formatting_info=True)
sheet=rb.sheet_by_index(0)
Array=[]
i=0
for i in range(sheet.nrows):
    row = sheet.row_values(i)
    if i>1:
        Array.append(int(row[1]))
print ("Min " + str(min(Array)))
print ("Max " + str(max(Array)))



Work1(Array)