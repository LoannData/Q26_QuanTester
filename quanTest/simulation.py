#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os 
import importlib
import datetime as dt 

from quanTest.analysis import ANALYSIS  
from quanTest.writer import WRITER 
from quanTest.diagnostics import TIMER

class SIMULATION(ANALYSIS, WRITER) :
    """ 
    ===============================================================
    Q26 - QuanTester module - SIMULATION(ANALYSIS, WRITER) object. 
    ===============================================================
    Object type : class(class, class)

    Initialisation attributes : 
        - PORTFOLIO   [class] 
        - PRICE_TABLE [class]

    Main Attributes : 
        - portfolio   [PORTFOLIO]                 : PORTFOLIO()    # Object containing informations about the portfolio 
        - priceTable  [PRICE_TABLE]               : PRICE_TABLE()  # Object containing aggregated, tabulated and synchronized prices 
        - portfolio.historicalDataTimeframe[int]  # Integer value of the base simulation timeframe normalized by the 1-minute unit 

    Secondary Attributes : 
        - startIndex   [int] : 0    
            - Simulation start index in the data stored in the priceTable attribute 
        - stopIndex    [int] : 9999999999999999  
            - Simulation stop index in the data stored in the priceTable attribute (inf = goes to the end of the data array)
        - subLoopModel [str] : "ohlc standard"
            - Model that drive how do we make evolve the price at timescales smaller that the timescale of a base candle. 
            - Models : 
            - "ohlc standard" : open -> high -> low -> close order, 4 steps model 
            - "close only"    : close only, 1 step model (fastest)
        - maxHstDataSize [int] : 1000 
            - Integer defining the max size of the emulated historical data buffer which will be available for trading strategies 

    Strategy Attributes : 
        - strategyPath [str] : None 
            - Absolute path to the strategy python file 
        - strategyFile [str] : None 
            - Name of the startegy python file (without the .py extension) 
        - strategy [python module] : None 
            - The imported strategy will be stored here 

    Runtime evolving attributes : 
        - emulatedPriceTable [dict] : None 
            - Historical data table emulated an available for the trading strategy. The objective is to avoid the ahead bias. 
    
    Log attributes : 
        - verbose [bool] : False 
            - If True, this parameter shows additionnal informations during the simulation. 
        - portfolio.verbose [bool] = verbose 
            - Same but for the portfolio attribute 
        - logEvery [int] : 100 
            - This parameter allows to define the regularity at which the simulation shows its advancement state and 
              activates the show() function in the strategy.STRATEGY object. 
    
    Description : 
        The SIMULATION allows to perform the trading strategy backtest. 
    
    To-do list : 
        - Comment all the functions of the SIMULATION class 

    """  

    def __init__(self, PORTFOLIO_LIST, PRICE_TABLE) : 
        # MAIN PARAMETERS 
        self.portfolio   = PORTFOLIO_LIST  # List of the initialized portfolio 
        self.priceTable  = PRICE_TABLE

        for i in range(len(self.portfolio)) : 
            self.portfolio[i].historicalDataTimeframe = int(self.priceTable.priceList[0].baseTimeframe/dt.timedelta(minutes = 1))

        # SECONDARY PARAMETERS
        self.startIndex     = 0 
        self.stopIndex      = 999999999999999 
        self.subLoopModel   = "ohlc standard"#"close only"#
        self.maxHstDataSize = 1000

        # STRATEGY PARAMETERS
        self.strategyPath = list() 
        self.strategyFile = list()
        self.strategy     = list()

        # RUNTIME EVOLVING PARAMETERS 
        self.emulatedPriceTable = None 


        # LOG PARAMETERS 
        self.verbose  = False 
        for i in range(len(self.portfolio)) : 
            self.portfolio[i].verbose = self.verbose 
        self.logEvery = 100 

        return 

    ###############################################################
    # BACKTEST OPERATIONS
    ###############################################################

    def importStrategy(self) : 
        
        for i in range(len(self.strategyFile)) : 
            sys.path.append(self.strategyPath[i]) 
            strategy = importlib.import_module(self.strategyFile[i])
            self.strategy.append(strategy.STRATEGY())

        return 

    
    def parametersCheck(self) : 
        print ("Everything is fine, the simulation can be launched !")
        print ("This functionnality is not working for instance and need to be coded")
        return

    def run(self, mode = "sequential", idx = None) : 
        
        if mode == "sequential" : 
        
            # We initiate the simulation 
            i = self.startIndex 
            iMax = min(self.priceTable.len(), self.stopIndex)
            while i <= iMax : 
    
                # 1. We update the price value in the portfolio 
                #t1 = TIMER(name = "Price update")
                self.updatePrices(i, mode = "sequential") 
                #t1.stop()
    
                # 2. We calculate the EMULATED_PRICE_TABLE object that only contains past data 
                #t2 = TIMER(name = "History emulation")
                self.updateEmulatedHistory(i, mode = "sequential")
                #t2.stop()
    
                # 3. We enter in the sub loop where strategies are executed 
                #t3 = TIMER(name = "Strategy execution")
                self.subLoop(mode = "sequential") 
                #t3.stop()
    
                self.simulationState(i, iMax, mode = "sequential") 
                #print ("i = ",i,"/",iMax)
                # We increment the simulation 
                i += 1
        
        if mode == "linear" : 
            
            for j in range(len(self.portfolio)) : 
                print ("===========================")
                print ("SIMULATION : ",j,"/",len(self.portfolio))
                print ("===========================")
                
                # We initiate the simulation 
                i = self.startIndex 
                iMax = min(self.priceTable.len(), self.stopIndex)
                while i <= iMax : 
        
                    # 1. We update the price value in the portfolio 
                    #t1 = TIMER(name = "Price update")
                    self.updatePrices(i, mode = "linear", idx = j) 
                    #t1.stop()
        
                    # 2. We calculate the EMULATED_PRICE_TABLE object that only contains past data 
                    #t2 = TIMER(name = "History emulation")
                    self.updateEmulatedHistory(i, mode = "linear", idx = j)
                    #t2.stop()
        
                    # 3. We enter in the sub loop where strategies are executed 
                    #t3 = TIMER(name = "Strategy execution")
                    self.subLoop(mode = "linear", idx = j) 
                    #t3.stop()
        
                    self.simulationState(i, iMax, mode = "linear", idx = j) 
                    #print ("i = ",i,"/",iMax)
                    # We increment the simulation 
                    i += 1
                    
        if mode == "unique" : 
            
            print ("===========================")
            print ("SIMULATION : ",idx,"/",len(self.portfolio))
            print ("===========================")
            
            # We initiate the simulation 
            i = self.startIndex 
            iMax = min(self.priceTable.len(), self.stopIndex)
            while i <= iMax : 
    
                # 1. We update the price value in the portfolio 
                #t1 = TIMER(name = "Price update")
                self.updatePrices(i, mode = "linear", idx = idx) 
                #t1.stop()
    
                # 2. We calculate the EMULATED_PRICE_TABLE object that only contains past data 
                #t2 = TIMER(name = "History emulation")
                self.updateEmulatedHistory(i, mode = "linear", idx = idx)
                #t2.stop()
    
                # 3. We enter in the sub loop where strategies are executed 
                #t3 = TIMER(name = "Strategy execution")
                self.subLoop(mode = "linear", idx = idx) 
                #t3.stop()
    
                self.simulationState(i, iMax, mode = "linear", idx = idx) 
                #print ("i = ",i,"/",iMax)
                # We increment the simulation 
                i += 1

                
        print ("Simulation terminated")
    
    def updatePrices(self, index, mode = None, idx = None) : 
        """ 
        Function that define the SYMBOL prices in the portfolio as a function of the given index 
        """
        
        if mode == "sequential" : 
            
            currentPriceTable = self.priceTable.iloc(index)
            
            for j in range(len(self.portfolio)) : 
                for key in list(self.portfolio[j].symbols.keys()) : 
                    symbol = self.portfolio[j].symbols.get(key) 
                    for skey in list(currentPriceTable.get(key).keys()) : 
                        if skey != "market status" : 
                            setattr(symbol, skey, currentPriceTable.get(key).get(skey))
                        if skey == "market status" : 
                            setattr(symbol, "marketState", currentPriceTable.get(key).get(skey))
                            
        if mode == "linear" : 
            
            currentPriceTable = self.priceTable.iloc(index)

            for key in list(self.portfolio[idx].symbols.keys()) : 
                symbol = self.portfolio[idx].symbols.get(key) 
                for skey in list(currentPriceTable.get(key).keys()) : 
                    if skey != "market status" : 
                        setattr(symbol, skey, currentPriceTable.get(key).get(skey))
                    if skey == "market status" : 
                        setattr(symbol, "marketState", currentPriceTable.get(key).get(skey))
    
    
    
    
    
    
    
    
    def updateEmulatedHistory(self, index, mode = None, idx = None) : 
        """ 
        Function that provide an emulated historical data array according the provided index 
        """ 
        if mode == "sequential" : 
        
            array = dict()
    
            if index - 1 < 0 : index = 1 
            # We update the array for every base data symbols 
            for j in range(len(self.portfolio)) : 
                for key in list(self.portfolio[j].symbols.keys()) : 
                    index_ = index#self.priceTable.priceList[0].index[index]
                    #index_ = self.priceTable.priceList[0].index.index(index)
                    array.update({key : self.priceTable.array(key, max(0, index_ - self.maxHstDataSize), index_, format = "dictionnary")})
                    # This is perfectly working like this MF ! 
            
            # We then update the array for every existing sampled data 
            for price in self.priceTable.priceList : 
                if price.sampled : 
                    index_ = price.index[index]
                    #print (index_)
                    array.update({price.name : self.priceTable.array(price.name, max(0, index_ - self.maxHstDataSize), index_, format = "dictionnary")})
                    
    
            self.emulatedPriceTable = array 
            for i in range(len(self.portfolio)) : 
                self.portfolio[i].setHistoricalData(self.emulatedPriceTable)
                
        if mode == "linear" : 
        
            array = dict()
    
            if index - 1 < 0 : index = 1 
            # We update the array for every base data symbols 
            for key in list(self.portfolio[idx].symbols.keys()) : 
                index_ = index#self.priceTable.priceList[0].index[index]
                #index_ = self.priceTable.priceList[0].index.index(index)
                array.update({key : self.priceTable.array(key, max(0, index_ - self.maxHstDataSize), index_, format = "dictionnary")})
                # This is perfectly working like this MF ! 
            
            # We then update the array for every existing sampled data 
            for price in self.priceTable.priceList : 
                if price.sampled : 
                    index_ = price.index[index]
                    #print (index_)
                    array.update({price.name : self.priceTable.array(price.name, max(0, index_ - self.maxHstDataSize), index_, format = "dictionnary")})
                    
    
            self.emulatedPriceTable = array 
            self.portfolio[idx].setHistoricalData(self.emulatedPriceTable)


    
    def executeStrategy(self, index = None) : 
        """ 

        """
        self.strategy[index].run(self.portfolio[index])
        pass 

    
    def subLoop(self, mode = None, idx = None) : 
        """ 

        """
        if mode == "sequential" : 
        
            for j in range(len(self.portfolio)) : 
                # 1. We retrieve the sub-loop price sequences 
                symbolPricesBid, symbolPricesAsk, size = self.subLoopModels(index = j)
        
                # 2. We apply the sub-loop 
                for i in range(size) : 
                    for key in list(symbolPricesBid.keys()) : 
                        self.portfolio[j].symbols.get(key).setCurrentPrice(bidprice = symbolPricesBid.get(key)[i], 
                                                                           askprice = symbolPricesAsk.get(key)[i])
                    self.executeStrategy(index = j) 
                    self.portfolio[j].update()
                    
        if mode == "linear" : 
        
            # 1. We retrieve the sub-loop price sequences 
            symbolPricesBid, symbolPricesAsk, size = self.subLoopModels(index = idx)
    
            # 2. We apply the sub-loop 
            for i in range(size) : 
                for key in list(symbolPricesBid.keys()) : 
                    self.portfolio[idx].symbols.get(key).setCurrentPrice(bidprice = symbolPricesBid.get(key)[i], 
                                                                         askprice = symbolPricesAsk.get(key)[i])
                self.executeStrategy(index = idx) 
                self.portfolio[idx].update()



    
    def subLoopModels(self, index = None) : 
        """ 
        Function that manage the evolution of the price at time scales lower than a candle scale one 
        """
        # 1. We define a symbolPrice sequence dict 
        symbolPricesAsk = dict()
        symbolPricesBid = dict()
        size = 0
        for key in list(self.portfolio[index].symbols.keys()) : 
            #symbol = self.portfolio.symbols.get(key) 
            symbolPricesAsk.update({key : list()}) 
            symbolPricesBid.update({key : list()})

        # 2. We apply the different sub-scale models 
        if self.subLoopModel == "close only"    : 
            size = 1 

            for key in list(symbolPricesAsk.keys()) : 
                symbolPricesAsk.get(key).append(self.portfolio[index].symbols.get(key).askclose)
            
            for key in list(symbolPricesBid.keys()) : 
                symbolPricesBid.get(key).append(self.portfolio[index].symbols.get(key).bidclose)

        if self.subLoopModel == "ohlc standard" : 
            size = 4
            
            for key in list(symbolPricesAsk.keys()) : 
                symbolPricesAsk.get(key).append(self.portfolio[index].symbols.get(key).askopen)
                symbolPricesAsk.get(key).append(self.portfolio[index].symbols.get(key).askhigh)
                symbolPricesAsk.get(key).append(self.portfolio[index].symbols.get(key).asklow)
                symbolPricesAsk.get(key).append(self.portfolio[index].symbols.get(key).askclose)

            for key in list(symbolPricesBid.keys()) : 
                symbolPricesBid.get(key).append(self.portfolio[index].symbols.get(key).bidopen)
                symbolPricesBid.get(key).append(self.portfolio[index].symbols.get(key).bidhigh)
                symbolPricesBid.get(key).append(self.portfolio[index].symbols.get(key).bidlow)
                symbolPricesBid.get(key).append(self.portfolio[index].symbols.get(key).bidclose)
            
            #print (list(symbolPricesAsk.keys()))
        
        # 3. We return the two sub-loop prices 
        return symbolPricesBid, symbolPricesAsk, size


    def simulationState(self, k, iMax, mode = None, idx = None) : 
        
        if mode == "sequential" : 
            
            if (k % self.logEvery == 0) : 
                print ("i = ",float(k)/iMax*100," %")
                # self.showEquityCurve()
                for i in range(len(self.strategy)) : 
                    self.strategy[i].show(self.portfolio[i])
                    
        if mode == "linear" : 
            
            if (k % self.logEvery == 0) : 
                print ("Simulation : ",idx," - i = ",float(k)/iMax*100," %")
                self.strategy[idx].show(self.portfolio[idx])





