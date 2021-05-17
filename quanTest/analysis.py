#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt 

class ANALYSIS : 



    def showEquityCurve(self, 
                        y_scale = "linear", # See : https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.yscale.html
                        y_lim   = None, 
                        x_label = "# of transaction", 
                        y_label = "Equity Curve" 
                        ) : 

        y = self.portfolio.equityCurve

        fig, ax = plt.subplots()
        l1, = ax.plot(y)

        if y_lim is not None : 
            ax.set_ylim(y_lim[0], y_lim[1])

        ax.set_yscale(y_scale)

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label) 

        plt.show()
