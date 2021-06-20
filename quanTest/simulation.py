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
import sys, os 
import importlib
import datetime as dt 

from quanTest.analysis import ANALYSIS  
from quanTest.writer import WRITER 
from quanTest.diagnostics import TIMER

class SIMULATION(ANALYSIS, WRITER) :
    """!
    ===============================================================
    Q26 - QuanTester module - SIMULATION(ANALYSIS, WRITER) object. 
    ===============================================================
    ### Description :
    
    ### Examples :
    
    ### Planned developments :
    
    ### Known bugs :
    
    \dontinclude[
    Do do list : 
        - Add random ohlc model 
    ] 
        

    """  

    def __init__(self, PORTFOLIO_LIST, PRICE_TABLE) : 
        # MAIN PARAMETERS
        
        ## ### PORTFOLIO class object. 
        # **Type** : class PORTFOLIO() \n 
        # **Description** : \n
        # This object contains the portfolio informations 
        self.portfolio   = PORTFOLIO_LIST  
        ## ### PRICE_TABLE class object. 
        # **Type** : class PRICE_TABLE() \n 
        # **Description** : \n
        # This object contains the global price dataset. 
        self.priceTable  = PRICE_TABLE

        for i in range(len(self.portfolio)) : 
            self.portfolio[i].historicalDataTimeframe = int(self.priceTable.priceList[0].baseTimeframe/dt.timedelta(minutes = 1))

        # SECONDARY PARAMETERS
        ## ### Intial index of the simulation. 
        # **Type :** integer \n
        # **Defaut value** : 0 \n
        # **Description** : \n
        # This index corresponds to the first available index in the 
        # datasets dedicated to simulate the price evolution.  
        self.startIndex     = 0 
        ## ### Ending index of the simulation.  
        # **Type :** integer \n
        # **Defaut value** : 99999999999999 \n
        # **Description** : \n
        # This index corresponds to the last available index in the 
        # datasets dedicated to simulate the price evolution. 
        self.stopIndex      = 999999999999999 
        ## ### Model used to cross prices below the candle resolution 
        # **Type** : string  \n
        # **Values** : 
        #   - "ohlc standard" : Prices are presented in the following order, 
        #                       open -> high -> low -> close 
        #   - "close only"    : Only close price is presented 
        #
        # **Description :** \n
        # The backtest simulation is defined by presenting a succession of 
        # candle sampled price, each candle being defined by : Open, High, 
        # Low, Close. The models define how the prices are successively 
        # presented to the portfolio at timescales below the candle resolution. 
        self.subLoopModel   = "ohlc standard"#"close only"#
        ## ### Historical data buffer size 
        # **Type** : integer \n
        # **Defaut value** : 1000  \n
        # **Description** : \n
        # This value defines the size of the buffer allowed to store any 
        # historical data price to be accessible by the trading strategies 
        # the function : getHistoricalData. 
        self.maxHstDataSize = 1000

        # STRATEGY PARAMETERS
        ## ### Strategy path list 
        # **Type** : list[string] \n 
        # **Defaut value** : list() \n
        # **Description** : \n 
        # This list contains all the paths to the trading strategy to be used 
        # in the simulation. In case of Monte Carlo type simulations of one 
        # trading strategy with parameter variations, the same path have to be 
        # inserted the number of times as the number of variations of the 
        # strategy parameters to be simulated. 
        self.strategyPath = list() 
        ## ### Strategy file list 
        # **Type** : list[string] \n 
        # **Defaut value** : list() \n
        # **Description** : \n 
        # This list contains all the strategy file names (without the .py extension). 
        # It follows the same structure as for the strategy path list. 
        self.strategyFile = list()
        ## ### Strategy module list 
        # **Type** : list[python module] \n 
        # **Defaut value** : list() \n 
        # **Description** : \n 
        # This list contains all the imported strategy modules. In case of a  
        # simulation with one strategy have been duplicated, every strategy element 
        # in this list is independant. 
        self.strategy     = list()

        # RUNTIME EVOLVING PARAMETERS 
        ##! \private 
        # **Description** : 
        # Variable containing the emulated data price which allows to avoid 
        # time ahead biases. 
        self.emulatedPriceTable = None 


        # LOG PARAMETERS 
        ## ### Debug mode 
        # **Type** : boolean \n 
        # **Defaut value** : False \n 
        # **Description** : 
        # If True, the simulation will print a lot of debug informations. \n
        # Warning : This parameter is not fully functionnal yet. 
        self.verbose  = False 
        for i in range(len(self.portfolio)) : 
            self.portfolio[i].verbose = self.verbose 
        ## ### Log frequency 
        # **Type** : integer \n 
        # **Defaut value** : 100 \n 
        # **Description** : 
        # If logEvery = 100, each 100 timestep (without considering subcandle timesteps) 
        # the code will print the simulation advancement and run the function .show() in 
        # each strategy.STRAGEY() class. 
        self.logEvery = 100 

        return 

    """! \dontinclude[
    ###############################################################
    # BACKTEST OPERATIONS
    ###############################################################
    ]""" 


    def importStrategy(self) : 
        """! 
        **Description :** 
            
            This function allows to import strategy files as a strategy module. 
            If a given strategy is imported number of times (the strategyFiles and 
            strategyPath lists contain a multiplicity of the same file/path), the 
            imported strategy modules are independent one from each others. 
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """
        
        for i in range(len(self.strategyFile)) : 
            sys.path.append(self.strategyPath[i]) 
            strategy = importlib.import_module(self.strategyFile[i])
            self.strategy.append(strategy.STRATEGY())

        return 

    
    def parametersCheck(self) : 
        """! 
        **Description** : 
            
            This function checks that everything is fine before running the 
            simulation. 
            !!! This function is not working yet !!! 
            
        **Parameters :** 
        
            None 
            
        **Returns :** 
        
            None 
            
        \dontinclude[
            To be done : 
                - Think about the different control steps ]
        """ 
        print ("Everything is fine, the simulation can be launched !")
        print ("This functionnality is not working for instance and need to be coded")
        return

    def run(self, mode = "sequential", idx = None) : 
        """! 
        **Description :** 
        
            Main function of the simulation. This function initiate the time 
            loop where at each time step, a new price is presented to the 
            portfolio. 
        
        **Parameters :** 
        
            - mode [int] = "sequential" : Drives the way for the simulation to 
                                          be done. The different parameters are : 
                                              - "sequential" : every couple portfolio/strategy is updated at each time step 
                                              - "linear" : the algorithm simulate sequentially each couple portfolio/strategy 
                                              - "unique" : given an idx index, only the couple indexed by idx is simulated 
            - idx [int] = None : If mode == "unique", this parameters represent the index of the couple portfolio/strategy 
                                 to be backtested.
        
        **Returns** : 
            
            None 
        
        \dontinclude[
            To be done : 
                - Find a way to parallelise simulation inside this function]
        
        """ 
        
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
        """! \private
        **Description :** 
            
            Function that define the SYMBOL prices in the portfolio as a 
            function of the given index. 
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        
        Do be done : 
            - Detail more the description of this function. 
        
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
        """! \private
        **Description :** 
            
            Function that provide an emulated historical data array according the provided index 
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
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
        """! \private
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """
        self.strategy[index].run(self.portfolio[index])
        pass 

    
    def subLoop(self, mode = None, idx = None) : 
        """! \private
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
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
        """! \private 
        **Description :** 
            
            Function that manage the evolution of the price at time scales lower than a candle scale one 
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
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
        """! \private  
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """
        
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





