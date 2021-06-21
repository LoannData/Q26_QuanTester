#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""! 
=============================================================
Q26 - QuanTester Python File
=============================================================

\dontinclude[
    Every function need to have a description header following this 
    template : 
        
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
            
            ]

""" 

import matplotlib.pyplot as plt 
import numpy as np
import datetime as dt 

class ANALYSIS : 
    """!
    ===============================================================
    Q26 - QuanTester module - ANALYSIS herited class 
    ===============================================================
    ### Description :
        
        This class is an heritage of the SIMULATION class so the 
        member functions can be directly used on SIMULATION() objects. 
        
    ### Examples :
    
    ### Planned developments :
    
    ### Known bugs :
    
    \dontinclude[
    Do do list : 
    ] 
        

    """ 



    def showEquityCurve(self, 
                        index     = [], 
                        labels    = list(),
                        xTime     = False,
                        y_scale   = "linear", # See : https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.yscale.html
                        y_lim     = None, 
                        x_lim     = None,
                        x_label   = "# of transaction", 
                        y_label   = "Equity Curve", 
                        x_rotation= 45, 
                        subCurve  = None, 
                        linestyle = "-",
                        marker    = None
                        ) :
        """! 
        **Description :** 
            
            This function allows to show the equity curves as a function of 
            the trade number or the time. 
        
        **Parameters :** 
            
            - index [list(int)] = list() : 
                List of index of portfolios one want to plot their equity curve 
            - labels [list(int)] = list() : 
                List of labels associated to the indexes 
            - xTime [bool] = False : 
                If True, the x-axis correspond to the time at which every position 
                have been closed. False correspond to the number of transaction. 
            - y_scale [string] = "linear" : 
                See https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.yscale.html for more 
            - y_lim [list(float)] = None : 
                y_lim = [y_min, y_max] price axis limits 
            - x_lim [list(float if !xTime else datetime)] = None : 
                x_lim = [x_min, x_max] time/#of transaction axis limits 
            - x_label [str] = "# of transaction" 
            - y_label [str] = "Equity curve" 
            - x_rotation [int] = 45 : 
                x labels rotation in degrees 
            - subCurve [list(int)] = None: 
                subCurve = [y_min, y_max] variable which allows to cut the y values. 
            - linestyle [str] = "-" 
            - marker [str] = None 
        
        **Returns :** 
            
            - fig : The figure which can be saved. 
            - ax 
        """
        
        
        fig, ax = plt.subplots()
        
        if len(index) == 0 : 
            index = list(np.linspace(0, len(self.portfolio)-1, num = len(self.portfolio)-1, dtype = int))
        for i in range(len(index)) : 
            y = self.portfolio[index[i]].equityCurve.copy()
            if subCurve is not None : 
                y = y[subCurve[0] : subCurve[1]]
            
            x = list(np.linspace(0, len(y), len(y)))
            if xTime : 
                x = list()
                for j in range(len(self.portfolio[index[i]].closedPositions)) : 
                    if self.portfolio[index[i]].closedPositions[j].closed : 
                        x.append(self.portfolio[index[i]].closedPositions[j].possibleCloseDate)
                del y[0]
            
            if len(labels) > 0 and i < len(labels): 
                l1, = ax.plot(x, y, ls = linestyle, marker = marker, label = labels[i])
            else : 
                l1, = ax.plot(x, y, ls = linestyle, marker = marker)

        if y_lim is not None : 
            ax.set_ylim(y_lim[0], y_lim[1])
        if x_lim is not None : 
            ax.set_xlim(x_lim[0], x_lim[1])

        ax.set_yscale(y_scale)

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label) 
        

        for tick in ax.get_xticklabels():
            tick.set_rotation(x_rotation)
        
        if len(labels) > 0 : 
            ax.legend()
            
        return fig, ax 
        # plt.show()
