#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#############################################################
SIMULATION CONFIGURATION FILE
#############################################################
This file contains all the header informations necessary to 
initialize a backtest. 

Please, read carefully all the explanations and report any 
bugs found in this file. 
"""

""" 
===============================================================================
MODULE IMPORTATION STEP
===============================================================================
This step is dedicated to specify the path at which the Q26 BackTester module 
is stored on your machine and to import the different important objects : 
    - SYMBOL            : This object correponds to the "broker" identity of 
                          the symbol to be backtested. 
    - PORTFOLIO         : This object corresponds to the portfolio to be 
                          simulated. 
    - PRICE/PRICE_TABLE : These objects refers to the datasets. 
    - SIMULATION        : This object corresponds to the simulation algorithm 
                          itself.
"""
# Usual modules importations 
import sys, os 
import numpy as np 
import pandas as pd 
import datetime as dt 
import matplotlib.pyplot as plt 
import pprint
import copy 

# Relative or absolute path to Q26_BacktestSystem folder
backTesterModulePath = "../"            
sys.path.append(backTesterModulePath)

# Q26 BacktestSystem class importations 
from quanTest.symbol     import SYMBOL
from quanTest.portfolio  import PORTFOLIO 
from quanTest.data       import PRICE 
from quanTest.data       import PRICE_TABLE
from quanTest.simulation import SIMULATION


""" 
===============================================================================
INITIALIZATION STEP : DATA PRICE PREPARATION
===============================================================================
"""

# We define the path to the dataset
path  = "./"
path += "exampleDataFile.csv"
# We create an object PRICE and give it a name 
price = PRICE("EUR.USD") 
# We associate the name of the columns in the datafile with 
# the properties of the PRICE object.
# In the specific case of the exampleDataFile.csv dataset, we do not have 
# any information of ask/bid price, so we consider by default that ask = bid 
# in the reading process. This will lead to a spread = 0.
price.setColumnsTitle(askOpen        ="open", 
                      askHigh        ="high",
                      askLow         ="low",
                      askClose       ="close", 
                      bidOpen        ="open",   
                      bidHigh        ="high",
                      bidLow         ="low",
                      bidClose       ="close",
                      dateFormat     ="%Y.%m.%d %H:%M", 
                      volume         ="vol",
                      splitDaysHours =True,  
                      days           ="date", 
                      hours          ="hour")
# We read the data
price.read(path)
# We define the timeframe associated to the loaded data 
price.setBaseTimeframe(timeframe = dt.timedelta(minutes = 1))
# We fill the missing data according to a data filling model 
price.fillMissingData()


# If necessary, we can shift our data 
price.shiftMarketTime(timeshift = 0)
# We can define the time zone in which data have been scraped (UTC+...)
price.dataTimeZone   = 0
# We can define the timezone in which the market is located (UTC+...)
price.marketTimeZone = 0
# We can define market opening/closing hours in the format "HH:MM"
# Note : If the market never close, the opening hour is "00:00"
#        while the closing hour is "24:00".
price.marketOpeningHour = "00:00"
price.marketClosingHour = "24:00"
# If the market has a mid day break or others breaks during the day 
# write it in the format : "HH:MM-HH:MM"
price.marketLunch    = None
marketBreakList      = list()
# Days of the week the market is open - 0 : Monday -> 6 : Sunday 
price.daysOfWeek = [0, 1, 2, 3, 4]
# Soon ... vacations 
# Function that define if the market is open/close 
price.setMarketState() 

# From the price object, it is possible to define another exact same object 
# thanks to the deepcopy function
price_H1 = copy.deepcopy(price)
# Here this dataset object is resampled to be used in the simulation. 
# The resampling process is exactly the same as you can see 
# on trading platforms. 
price_H1.resampleData("01:00", name = "EUR.USD_H1")

# We generate our data table which will be involved in the simulation 
table = PRICE_TABLE([price, price_H1]) 
# In the case where we have more than 1 not resampled price, 
# the synchronize function will be necessary. 
table.synchronize()

""" 
===============================================================================
INITIALIZATION STEP : SYMBOL PROPERTIES IN THE BROKER FRAME
===============================================================================
Note : Fees are not yet implemented 
"""

symbol = SYMBOL(symbolName              = "EUR.USD",
                contractSize            = 100000, 
                marginCurrency          = "USD",    # Can be any existing currency (only USD is working for instance)
                profitCalculationMethod = "Forex",  # "CFD", "Forex", "Stock", "CFD-Index"
                marginRequestMethod     = "Forex",  # "CFD", "Forex", "Stock", "CFD-Index"
                marginPercentage        = 100, 
                execution               = "Market", 
                minimalVolume           = 0.01, 
                maximalVolume           = 100.0, 
                volumeStep              = 0.01, 
                precision               = 5,        # Price precision (3 means 1 point = 0.001)
                exchangeType            = "Point",  # "Point", "Percentage"
                exchangeLong            = 6.88, 
                exchangeShort           = 0.63)

""" 
===============================================================================
INITIALIZATION STEP : PORTFOLIO PROPERTIES
===============================================================================
"""

# We initialize our portfolio 
p = PORTFOLIO(initialDeposit                  = 100000,                # The initial client deposit 
              leverage                        = 30,                    # The leverage value (margin = initialDeposit*leverage)
              currency                        = "USD",                 # The currency 
              positions                       = "long & short",        # "long", "short" or "long & short"
              marginCallTreeshold             = 100,                   # If marginLevel < marginCallTreeshold : Warning (no more trading allowed)
              marginMinimum                   = 50,                    # If marginLevel < marginMinimum : Automatically close all losing positions 
              minimumBalance                  = 50000,                 # If balance < minimumBalance : No more trading allowed 
              maximumProfit                   = 100000,                # If balance - inialDeposit > maximumProfit : No more trading allowed 
              maximumDrawDown                 = 70,                    # If drawDown < maximumDrawDown : No more trading allowed 
              maximumConsecutiveLoss          = 50000,                 # If valueLossSerie > maximumConsecutiveLoss : No more trading allowed 
              maximumConsecutiveGain          = 50000,                 # If valueGainSerie > maximumConsecutiveGain : No more trading allowed 
              maximumNumberOfConsecutiveGains = 30)

# We add the symbol identity we created inside the portfolio object 
p.addSymbol(symbol)

""" 
===============================================================================
SIMULATION STEP
===============================================================================
"""
# We initialize the simulation object 
sim = SIMULATION([p], table)

sim.subLoopModel = "close only"
sim.maxHstDataSize = 2000
sim.startIndex = 2000
# sim.stopIndex  = 2010
sim.logEvery = 1000


# Relative or absolute pathe to the strategy file
# and strategy class importation  
sim.strategyPath = ["./"]
sim.strategyFile = ["strategyExample"]
sim.importStrategy()

# Check of the simulation parameters (not yet working)
sim.parametersCheck()

# Run of the simulation 
sim.run(mode = "linear")


""" 
===============================================================================
RESULTS STEP
===============================================================================
"""
# We write the results in a csv file 
sim.writeClosedPositionsFile(index = 0)
# We plot the equity curve 
sim.showEquityCurve(index = [0])

