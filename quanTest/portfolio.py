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

import numpy as np 
import pandas as pd 
import datetime as dt 

import quanTest.financialTools as financialTools
from quanTest.order import ORDER
from quanTest.position import POSITION
from quanTest.system import SYSTEM 

from quanTest.models.slippage import SLIPPAGE


class PORTFOLIO(SLIPPAGE, SYSTEM) : 
    """!
    ===============================================================
    Q26 - QuanTester module - PORTFOLIO object. 
    ===============================================================
    ### Description :
        
        This class is dedicated in initializing a trading PORTFOLIO. 
    
    ### Examples :
    
    ### Planned developments :
    
    ### Known bugs :
    
    \dontinclude[
    Do do list : 
        - 
    ] 
        

    """  

    def __init__(self, 
                 initialDeposit                  = 10000,                # The initial client deposit 
                 leverage                        = 1,                    # The leverage value (margin = initialDeposit*leverage)
                 currency                        = "USD",                # The currency 
                 positions                       = "long & short",       # "long", "short" or "long & short"
                 marginCallTreeshold             = 100,                  # If marginLevel < marginCallTreeshold : Warning (no more trading allowed)
                 marginMinimum                   = 50,                   # If marginLevel < marginMinimum : Automatically close all losing positions 
                 minimumBalance                  = 200,                  # If balance < minimumBalance : No more trading allowed 
                 maximumProfit                   = 10000,                # If balance - inialDeposit > maximumProfit : No more trading allowed 
                 maximumDrawDown                 = 70,                   # If drawDown < maximumDrawDown : No more trading allowed 
                 maximumConsecutiveLoss          = 5000,                 # If valueLossSerie > maximumConsecutiveLoss : No more trading allowed 
                 maximumConsecutiveGain          = 10000,                # If valueGainSerie > maximumConsecutiveGain : No more trading allowed 
                 maximumNumberOfConsecutiveGains = 30) :                 # If numberLossSerie > maximumNumberOfConsecutiveGains : No more trading allowed 
            
        # Initial parameters (static)
        ## ### Initial client desposit amount  
        # **Type** : float/integer \n 
        # **Defaut value** : 10000 \n 
        # **Description** : \n
        # Determine the initial portfolio value  
        self.initialDeposit                         = initialDeposit 
        ##! \private 
        # **Type** : float/integer \n 
        # **Description** : \n 
        # The initial available portfolio margin 
        self.initialAvailableMargin                 = initialDeposit
        ## ### Portfolio leverage 
        # **Type** : float/integer \n 
        # **Defaut value** : 1 \n 
        # **Description** : \n 
        # A selected leverage. 
        self.leverage                               = leverage 
        ## ### Portfolio Currency
        # **Type** : string \n 
        # **Defaut value** : "USD" \n 
        # **Description** : \n 
        # The portfolio devise. 
        # !!!This feature is not implemented yet, the only available devise in 
        # USD for instance!!!
        self.currency                               = currency 

        # Constraint parameters (static, but can evolve if needed)
        ## ### Allowed positions types 
        # **Type** : string \n 
        # **Defaut value** : "long & short" \n 
        # **Description** : \n 
        # If "long", only long positions are allowed, if "short", only short 
        # positions are allowed. If "long & short", both direction positions 
        # are allowed. !!! Not working yet !!! For instance "long & short" is 
        # the only possible value. 
        self.positions                              = positions 
        ## ### Margin call treeshold 
        # **Type** : float \n 
        # **Defaut value** : 100 \n 
        # **Description** : \n 
        # Defines the treeshold below which the trading is deactivated for 
        # the current portfolio. The margin rate is expressed as a percentage. 
        # If marginLevel < marginCallTreeshold : Warning (no more trading allowed)
        self.marginCallTreeshold                    = marginCallTreeshold
        ## ### Margin Minimum treeshold 
        # **Type** : float \n 
        # **Defaut value** : 50 \n 
        # **Description** : \n 
        # Defines the treeshold below which the simulator starts to automatically 
        # close the most losing positions, and this until the portfolio 
        # margin goes up to the minimum allowed value. The value is expressed 
        # as a percentage. 
        self.marginMinimum                          = marginMinimum 
        ## ### Minimum balance 
        # **Type** : integer/float \n 
        # **Defaut value** : 200 \n 
        # **Description** : \n 
        # If the portfolio balance goes below the minimum allowed balance,
        # the trading is deactivated.
        self.minimumBalance                         = minimumBalance 
        ## ### Maximum allowed profit 
        # **Type** : integer/float \n 
        # **Defaut value** : 1000 \n 
        # **Description** : \n 
        # If the current portfolio makes more profit than the maximum 
        # allowed profit, the trading is deactivated. 
        self.maximumProfit                          = maximumProfit 
        ## ### Maximum allowed drawdown 
        # **Type** : integer/float \n 
        # **Defaut value** : 70 \n 
        # **Description** : \n 
        # If the current looses generate a drawdown percentage higher than the 
        # maximum allowed, the trading is deactivated.
        self.maximumDrawDown                        = maximumDrawDown
        ## ### Maximum consecutive loss 
        # **Type** : integer/float \n 
        # **Defaut value** : 5000 \n 
        # **Description** : \n 
        # If the portfolio meet a consecutive loss higher than the maximum 
        # allowed consecutive loss, the trading is deactivated. 
        self.maximumConsecutiveLoss                 = maximumConsecutiveLoss 
        ## ### Maximum consecutive gain 
        # **Type** : integer/float \n 
        # **Defaut value** : 10000 \n 
        # **Description** : \n 
        # If the portfolio meet a consecutive gain higher than the maximum 
        # allowed consecutive gain, the trading is deactivated. 
        self.maximumConsecutiveGain                 = maximumConsecutiveGain 
        ## ### Maximum number consecutive gain
        # **Type** : integer \n 
        # **Defaut value** : 30 \n 
        # **Description** : \n 
        # If the portfolio meet a a number of consecutive gain higher than the maximum 
        # allowed number of consecutive gain, the trading is deactivated. 
        self.maximumNumberOfConsecutiveGains        = maximumNumberOfConsecutiveGains

        # Simulation parameters (dynamic) 
        ## ### Portfolio balance 
        # **Type** : integer/float \n 
        # **Simulation variable** \n 
        # **Description** : \n
        # The balance of cash available to the portfolio all along the simulation.  
        self.balance                                = self.initialDeposit 
        ## ### Available margin 
        # **Type** : integer/float \n 
        # **Simulation variable** 
        # **Description** : \n
        # The portfolio available margin all along the simulation. 
        self.availableMargin                        = self.initialAvailableMargin 
        ## ### Used margin 
        # **Type** : integer/float \n 
        # **Simulation variable** \n 
        # **Description** : \n 
        # The portfolio used margin all along the simulation. 
        self.usedMargin                             = 0. 
        ## ### Equity balance 
        # **Type** : integer/float \n 
        # **Simulation variable** \n 
        # **Description :** \n 
        # The portfolio equity all along the simulation. The equity variable 
        # represents the portfolio balance but also takes in account the 
        # instant potential gains/loses of the currently actyive positions. 
        self.equity                                 = self.initialAvailableMargin
        ## ### Margin level
        # **Type** : float \n 
        # **Simulation variable** \n 
        # **Description :** \n 
        # The margin level is defined by : availableMargin / usedMargin * 100
        # and is expressed as a percentage. 
        self.marginLevel                            = np.inf 
        ## ### Open positions list 
        # **Type** : list(class POSITION) \n 
        # **Simulation variable** \n 
        # **Description :** \n 
        # This list stores all the currently active POSITION taken by the 
        # current portfolio. 
        self.openPositions                          = list()
        ## ### Closed positions list 
        # **Type** : list(class POSITION) \n 
        # **Simulation variable** \n 
        # **Description :** \n 
        # This list stores all the POSITIONs that have been closed by the 
        # current portfolio or automatically by the simulated broker. 
        self.closedPositions                        = list()
        ## ### Pending orders list 
        # **Type** : list(class ORDER) \n 
        # **Simulation variable** \n 
        # **Description :** \n 
        # Every submitted ORDER is stored here. If conditions are met, the order 
        # is executed. It means that it is removed from this list and placed 
        # in the executedOrders list, and a POSITION object is generated in the 
        # openPositions list. 
        self.pendingOrders                          = list() 
        ## ### Executed orders list 
        # **Type** : list(class ORDER) \n 
        # **Simulation variable** \n
        # **Description :** \n 
        # Every executed or cancelled order is stored here. This list allows 
        # to have an history of every portfolio trading action. 
        self.executedOrders                         = list() 
        ## ### Portfolio equity curve 
        # **Type** : list(float) \n 
        # **Simulation variable** \n 
        # **Description** : \n 
        # This list represent the value of the portfolio equity at each time 
        # a position is closed. It is in particular involved in the calculation 
        # of the portfolio current draw down and other gain/loss series. 
        self.equityCurve                            = list([initialDeposit])
        ## ### Current value loss serie 
        # **Type** : float \n 
        # **Simulation variable** \n 
        # **Description** : \n 
        # Current value loss serie. 0 if the last transaction was a gain. 
        self.currentValueLossSerie                  = 0.
        ## ### Current value gain serie 
        # **Type** : float \n 
        # **Simulation variable** \n 
        # **Description** : \n 
        # Current value gain serie. 0 if the last transaction was a loss. 
        self.currentValueGainSerie                  = 0. 
        ## ### Current drawdown 
        # **Type** : float \n 
        # **Simulation variable** \n 
        # **Description** : \n 
        # The current drawdown is calculated as a percentage value of the 
        # portfolio balance. 
        self.currentDrawDown                        = 0. 
        ## ### Current maximum number of consecutive gains 
        # **Type** : integer \n 
        # **Simulation variable** \n 
        # **Description** : \n 
        # Each time a new gain is registered, this variable is incremented by 
        # an unitary value. If the last transation was a loss, this variable 
        # becomes 0. 
        self.currentMaximumNumberOfConsecutiveGains = 0 

        # Symbol objects  
        ## ### Symbols 
        # **Type** : dictionnary(string : class SYMBOL) \n 
        # **Description** : \n 
        # This variable stores all the SYMBOL objects involved in the 
        # simulation. 
        self.symbols                                = dict() 

        # Historical data price 
        ##! 
        # ### Historical available data price 
        # **Type** : dictionnary(symbolName : dictionnary(price : list(value))) \n 
        # **Simulation variable** \n 
        # **Description** : \n 
        # This variable contains all the historical data price available to 
        # the portfolio according the actual time date. This is the place 
        # where historical data price can be accessed from STRATEGY classes. 
        # This variable is structured as follows : 
        # \code{.py}
        # {Symbol Name 1: {askopen : list(float), 
        #                  askhigh : list(float), 
        #                  asklow  : list(float), 
        #                  askclose: list(float), 
        #                  bidopen : list(float), 
        #                  bidhigh : list(float), 
        #                  bidlow  : list(float), 
        #                  bidclose: list(float), 
        #                  volume  : list(float), 
        #                  time    : list(datetime)}, 
        # Symbol Name 2 : ...}
        # \endcode
        self.historicalDataPrice                    = None 
        ## ### Simulation data timeframe
        # **Type** : integer \n  
        # **Description** : \n 
        # Timeframe (in minutes unit) of the not-resampled simulation data.
        self.historicalDataTimeframe                = None # [int] in minutes 

        # Trading authorisation 
        ## ### Trading authorisation 
        # **Type** : boolean \n 
        # **Description** : \n 
        # If False, trading is unauthorised. 
        self.tradeAuthorisation                     = True 
        
        # Debug attributes 
        ## ### Verbose, debug mode 
        # **Type** : boolean \n 
        # **Description** : \n 
        # If True, a lot of technical informations are printed during the 
        # simulation. 
        self.verbose                                = True 
        
        
        ## ### Backtest log file 
        # **Type** : string \n 
        # **Default value** : None \n 
        # **Description** : 
        # Path+name to a file dedicated to store all the actions done by 
        # the backtester.
        self.trading_log_path             = None 
        
        ## ### Backtest first file write mode 
        # **Type** : bool \n 
        # **Default value** : None \n 
        # **Description** : 
        # If True and log file already exists, the backtest 
        # system will overwrite it. 
        self.trading_log_first_write_mode = None 
        
        self.log_step_every = 100 
        
        
        self.trading_log_actions = ["portfolio initialization",
                                    "portfolio step",
                                    "place order", 
                                    "close position", 
                                    "edit stoploss order", 
                                    "edit takeprofit order", 
                                    "cancel order", 
                                    "get active positions", 
                                    "get historical data", 
                                    "get last price", 
                                    "portfolio error", 
                                    "strategy message"]
        
        
        # Models 
        ##! \private 
        self.slippageMdl                            = None 
        
        return 
    

    
    # Functions to be used at an higher level 
    def addSymbol(self, 
                  symbol) :  # SYMBOL object 
        """! 
        **Description :** 
            
            Function allowing to add a new SYMBOL object in the portfolio 
            symbols dictionnary.
        
        **Parameters :** 
            
            - symbol [class SYMBOL()] : A SYMBOL object 
        
        **Returns :** 
            
            None 
        """ 
        self.symbols.update({symbol.symbolName : symbol})

    @SYSTEM.placeOrder
    def placeOrder(self, 
                   symbolName,
                   action     = "long",      # "long" or "short"
                   orderType  = "MKT",       # Order kind : "MKT", "MIT", "LMT"
                   volume     = 0.1,         # Volume 
                   stoploss   = None,          
                   takeprofit = None, 
                   lmtPrice   = None, 
                   auxPrice   = None) : 
        """!
        **Description :** 
            
            This function allows to place an order, the symbol name being 
            provided. Three types of orders can be placed : market, market if 
            touched and limit order. For every placed order, three orders are 
            placed, the immediately desired transaction and two pending orders 
            simulating the stoploss and takeprofit values. If stoploss and/or 
            takeprofit is not required, the user can put an extraordinary value 
            so that the security pending orders will never be triggered. 
        
        **Parameters :** 
            
            - symbolName [string] : 
                Name of the symbol as registered in the portfolio. 
            - action [string] = "long" : 
                "long" or "short", direction of the position.
            - orderType [string] = "MKT" : 
                "MKT" (Market) : The order is placed as soon as possible. 
                "MIT" (Market If Touched) : 
                    If action = "long", the order is executed if price < lmtprice 
                    If action = "short", the order is executed if price > lmtPrice 
                "LMT" (Limit) : 
                    If action = "long", the order is executed if price > lmtPrice 
                    If action = "short", the order is executed if price < lmtPrice 
            - volume [float] = 0.1 : 
                Volume of the asset to be traded in the unit defined by the 
                associated SYMBOL object in the portfolio symbol dictionnary. 
            - stoploss [float] : 
                Stoploss value 
            - takeprofit [float] : 
                Takeprofit value 
            - lmtPrice [float] : 
                Secondary price value which becomes usefull in case of 
                MIT or LMT order 
            - auxPrice [float] : 
                This variable is not used for instance 
        
        **Returns :** 
            
            If the order is correctly placed, the function returns a list of 
            three ORDER objects where the first element is the desired 
            transction while the second and the third are the stoploss and 
            takeprofit orders respectively. 
            Else, the function returns a list of Falses, of size 3.
        """
    
        
        symbol = self.symbols.get(symbolName)

        #print(symbol.__dict__)
        
        if symbol is not None and self.tradeAuthorisation : 

            orderList = self.createOrder(symbolName = symbolName, 
                                         action     = action,          # "long" or "short"
                                         orderType  = orderType,       # Order kind : "MKT", "MIT", "LMT"
                                         volume     = volume,          # Volume 
                                         stoploss   = stoploss,          
                                         takeprofit = takeprofit, 
                                         lmtPrice   = lmtPrice, 
                                         auxPrice   = auxPrice)

            self.checkPendingOrder(symbol, 
                                   orderList[0])
            
            return orderList 
        
        else : 
            
            #print ("Order not placed")
            return [False, False, False]
    
    @SYSTEM.editSLOrder
    def editSLOrder(self, 
                    symbolName, 
                    order, 
                    stoploss = None) : 
        """! 
        **Description :** 
            
            This function allows to edit the stoploss value of a placed order. 
            To do it, the user has to provide the stoploss ORDER object (not the 
            main ORDER object), and the new stoploss value. 
        
        **Parameters :** 
            
            - symbolName [string] : 
                Name of the symbol 
            - order [class ORDER()] : 
                The pending stoploss ORDER object that have been placed 
            - stoploss [float] : 
                The new stoploss value 
            
        
        **Returns :** 
            
            None 
        """
        if stoploss is not None : 
            orderID  = order.orderID 
            parentID = order.parentID
            if parentID is not None : 
                pendingOrderIndex = None 
                for i in range(len(self.pendingOrders)) : 
                    if (self.pendingOrders[i].orderID == orderID) : 
                        pendingOrderIndex = i 
                if pendingOrderIndex is not None : 
                    self.pendingOrders[pendingOrderIndex].lmtPrice = stoploss 

    @SYSTEM.editTPOrder
    def editTPOrder(self, 
                    symbolName, 
                    order, 
                    takeprofit = None) : 
        """! 
        **Description :** 
            
            This function allows to edit the takeprofit value of a placed order. 
            To do it, the user has to provide the takeprofit ORDER object (not the 
            main ORDER object), and the new takeprofit value. 
        
        **Parameters :** 
            
            - symbolName [string] : 
                Name of the symbol 
            - order [class ORDER()] : 
                The pending takeprofit ORDER object that have been placed 
            - takeprofit [float] : 
                The new takeprofit value 
            
        
        **Returns :** 
            
            None 
        """
        if takeprofit is not None : 
            orderID  = order.orderID 
            parentID = order.parentID
            if parentID is not None : 
                pendingOrderIndex = None 
                for i in range(len(self.pendingOrders)) : 
                    if (self.pendingOrders[i].orderID == orderID) : 
                        pendingOrderIndex = i 
                if pendingOrderIndex is not None : 
                    self.pendingOrders[pendingOrderIndex].lmtPrice = takeprofit 
    
    @SYSTEM.cancelOrder
    def cancelOrder(self, 
                    symbolName, 
                    order) : 
        """! 
        **Description :** 
            
            This function allows to cancel an ORDER that have been placed but 
            not executed yet given the symbol name and the pending ORDER. 
            If the ORDER is a parent order, the parent ORDER AND the children 
            ORDERs will be cancelled. If the ORDER is a children ORDER, only 
            the provided order will be cancelled. 
        
        **Parameters :** 
            
            - symbolName [string] : 
                Name of the symbol 
            - order [class ORDER()] : 
                The ORDER object that have been placed 
        
        **Returns :** 
            
            None 
        """

        inPendingOrders = False 
        for o in self.pendingOrders : 
            if order.orderID == o.orderID : 
                inPendingOrders = True 
        
        if inPendingOrders : 
        
            # Case where the order is a parent one 
            if order.parentID is None : 

                stillAnOrder = True 
                while (stillAnOrder) : 
                    pendingOrderIndex = None
                    for i in range(len(self.pendingOrders)) : 
                        if self.pendingOrders[i].orderID == order.orderID or self.pendingOrders[i].parentID == order.orderID : 
                            pendingOrderIndex = i 
                    if pendingOrderIndex is not None : 
                        self.executedOrders.append(self.pendingOrders[pendingOrderIndex])
                        del self.pendingOrders[pendingOrderIndex]
                    else : 
                        stillAnOrder = False 



            else : 
                stillAnOrder = True 
                while (stillAnOrder) : 
                    pendingOrderIndex = None
                    for i in range(len(self.pendingOrders)) : 
                        if self.pendingOrders[i].orderID == order.orderID or self.pendingOrders[i].parentID == order.orderID : 
                            pendingOrderIndex = i 
                    if pendingOrderIndex is not None : 
                        self.executedOrders.append(self.pendingOrders[pendingOrderIndex])
                        del self.pendingOrders[pendingOrderIndex]
                    else : 
                        stillAnOrder = False 

        
                                         
    @SYSTEM.closePosition
    def closePosition(self,
                      symbolName, 
                      order) : 
        """! 
        **Description :** 
            
            This function allows to close a POSITION object, the symbol name 
            and the main ORDER object (the one which allowed to open the 
            POSITION object) being provided. 
        
        **Parameters :** 
            
            - symbolName [string] : 
                Name of the symbol 
            - order [class ORDER()] : 
                The ORDER object that have been placed 
        
        **Returns :** 
            
            None 
        """
        
        symbol = self.symbols.get(symbolName)

        if symbol is not None : 

            orderID = order.orderID
            # We retrive the position in the portfolio 
            openPositionIndex = None 
            for i in range(len(self.openPositions)) : 
                if self.openPositions[i].orderID == orderID : 
                    openPositionIndex = i 
            
            if openPositionIndex is None : 
                self.error("Error when retrieving the position")
                return False
            else : 
                self.updatePosition(symbol, self.openPositions[openPositionIndex])
                self.updatePortfolio()
                position = self.openPositions[openPositionIndex]
                

                # We create an order to close the current position 
                orderS           = ORDER()
                orderS.symbolName= symbolName
                orderS.parentID  = position.orderID 
                orderS.action    = "short" if position.action == "long" else "long" 
                orderS.orderType = "MKT" 
                orderS.volume    = position.volume 

                # We execute the order 
                return self.executeOrder(symbol, 
                                         orderS, 
                                         type = "close") 
        else : 
            return False 
    
    @SYSTEM.getActivePositions
    def getActivePositions(self, 
                           symbolName) : 
        """! 
        **Description :** 
            
            Returns the list of currently active positions given a symbol name. 
        
        **Parameters :** 
            
            - symbolName [string] :
                Name of the symbol
        
        **Returns :** 
            
            List of active POSITION objects.  
        """

        activePositions = list()
        for pos in self.openPositions : 
            if pos.symbol == symbolName : 
                activePositions.append(pos)
        
        return activePositions

    ###################################################################
    # Security check functions. 
    ###################################################################
    def checkExecuteOrder(self, 
                          symbol, 
                          order) : 
        """! \private 
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """

        executeOrder = True 
        # A. We check if we have the global trading authorisation 
        if not self.tradeAuthorisation : 
            self.error("Order cannot be executed. Trading un-authorised")
            executeOrder = False 
        # B. We check if the order action is authorised by the portfolio 
        if not order.action in self.positions : 
            self.error("Order action "+order.action+" is not allowed by the portfolio parameters")
            executeOrder = False 

        # 1. We check if we have the request margin 
        if order.requestMargin > self.availableMargin : 
            self.error("Order cannot be executed. The request margin is higher than the available margin")
            executeOrder = False 
        if self.marginLevel < symbol.marginPercentage : 
            self.error("Order cannot be executed. Available margin lower than the limit margin", 
                       kwargs = {"SYMBOL MARGIN %": symbol.marginPercentage, 
                                 "MARGIN LEVEL"   : self.marginLevel, 
                                 "MARGIN CALL TREESHOLD" : self.marginCallTreeshold, 
                                 "AVAILABLE MARGIN" : self.availableMargin, 
                                 "USED MARGIN": self.usedMargin})
            executeOrder = False 
        # 2. We check if the volume responds to the constraints 
        if order.volume > symbol.maximalVolume or order.volume < symbol.minimalVolume : 
            self.error("Order cannot be executed. The volume amount is not right.", 
                       kwargs = {"ORDER NAME"      : order.symbolName, 
                                 "ORDER VOLUME"    : order.volume, 
                                 "SYMBOL MiN VOLUME": symbol.minimalVolume, 
                                 "SYMBOL MaX VOLUME": symbol.maximalVolume})
            executeOrder = False 
        # 3. We check if the volume step responds to the constrains 
        if round(order.volume / symbol.volumeStep, 8) != round(order.volume / symbol.volumeStep, 0) :
            self.error("Order cannot be executed. The volume step is not right")
            executeOrder = False
        # 4. We check if the market is open or not 
        if symbol.marketState == "closed" : 
            self.error("Order cannot be executed. The market is closed")
            executeOrder = False 
        if symbol.marketState == "sell only" and order.action == "long" : 
            self.error("Order cannot be executed. Only sell orders are allowed")
            executeOrder = False 
        if symbol.marketState == "buy only" and order.action == "short" : 
            self.error("Order cannot be executed. Only buy orders are allowed")
            executeOrder = False 
        
        return executeOrder 
    

    def tradingAuthorisation(self) : 
        """! \private 
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """
        
        locAuthorisation = True 

        # 1. The available margin is lower than the margin call treeshold 
        if self.marginLevel < self.marginCallTreeshold : 
            self.error("The available margin is lower than the margin call treeshold", 
                       kwargs = {"MARGIN LEVEL"          : self.marginLevel, 
                                 "MARGIN CALL TREESHOLD" : self.marginCallTreeshold, 
                                 "AVAILABLE MARGIN"      : self.availableMargin, 
                                 "USED MARGIN"           : self.usedMargin})
            locAuthorisation = False   
        # 2. If the balance is lower than the minimum allowed 
        if self.balance < self.minimumBalance : 
            self.error("The balance is lower than the minimum allowed", 
                       kwargs = {"BALANCE"              : self.balance, 
                                 "MINIMUM BALANCE"      : self.minimumBalance})
            locAuthorisation = False 
        # 3. If the profit made is higher than the maximum profit 
        if self.getProfit(option = "balance") > self.maximumProfit : 
            self.error("The profit made is higher than the maximum profit")
            locAuthorisation = False 
        # 4. If the drawDown is higher than the maximum drawdown 
        if self.currentDrawDown >= self.maximumDrawDown : 
            self.error("The drawdown is higher than the maximum drawdown")
            locAuthorisation = False 
        # 5. If the consecutive losses amount is higher than the maximum consecutive losses 
        if self.currentValueLossSerie >= self.maximumConsecutiveLoss : 
            self.error("The consecutive losses amount is higher than the maximum consecutive losses")
            locAuthorisation = False 
        # 6. If the consecutive gains amount is higher than the maximum consecutive gains 
        if self.currentValueGainSerie >= self.maximumConsecutiveGain : 
            self.error("The consecutive gains amount is higher than the maximum consecutive gains")
            locAuthorisation = False 
        # 7. If the consecutive gains number is higher than the maximum number of consecutive gains 
        if self.currentMaximumNumberOfConsecutiveGains >= self.maximumNumberOfConsecutiveGains : 
            self.error("The consecutive gains number is higher than the maximum number of consecutive gains")
            locAuthorisation = False 


        # We associate the trading authorisation to the result of the security checks 
        self.tradeAuthorisation = locAuthorisation

    def checkMarginMinimum(self) :
        """! \private 
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """
        # If the margin level is below the minimum rate 
        # we close all the worse positions until the margin level becomes 
        # higher than this minimum 
        while self.marginLevel <= self.marginMinimum and len(self.openPositions) > 0 : 
            
            minProfit   = np.inf
            indexLowest = None 
            # We retrieve the position that has the worse profit 
            for i in range(len(self.openPositions)) : 
                if self.openPositions[i].profit < minProfit : 
                    minProfit   = self.openPositions[i].profit 
                    indexLowest = i
            
            # We close this position 
            if indexLowest is not None : 
                #print ("Closed position because bad margin level")
                self.closePosition(self.openPositions[indexLowest].symbol, self.openPositions[indexLowest])
            
            

    ###################################################################
    # Evolving parameters functions 
    ###################################################################
    def getProfit(self, option = "balance") : 
        """! \private 
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """
        """ 
        Returns the portfolio profit. 
        If option = balance : returns balance (t) - balance (t = 0) 
        If option = margin  : return availableMargin (t) - balance (t) 
        """
        if option == "balance" : 
            return self.balance - self.initialDeposit 
        if option == "margin" : 
            return self.availableMargin - self.balance 

    def getMaxDrawDown(self) :
        """! \private 
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """ 
        """ 
        Returns the current drawdown value in percentage. 
        """
        diff = (max(self.equityCurve) - self.equityCurve[-1])/max(self.equityCurve)
        if diff > self.currentDrawDown : 
            return diff 
        else : 
            return self.currentDrawDown

    ###################################################################
    # Parametric functions. Cannot be used at an higher level 
    ###################################################################
    
    def createOrder(self, 
                    symbolName = None,  
                    action     = "long",      # "long" or "short"
                    orderType  = "MKT",       # Order kind : "MKT", "MIT", "LMT"
                    volume     = 0.1,         # Volume 
                    stoploss   = None,          
                    takeprofit = None, 
                    lmtPrice   = None, 
                    auxPrice   = None ) : 
        """! \private 
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """ 


        # We create the ORDER parent object 
        orderParent           = ORDER() 
        orderParent.symbolName=symbolName
        orderParent.action    = action 
        orderParent.orderType = orderType 
        orderParent.volume    = volume 
        orderParent.lmtPrice  = lmtPrice

        # We create the ORDER stoploss object 
        orderSL           = ORDER()
        orderSL.symbolName= symbolName
        orderSL.parentID  = orderParent.orderID 
        orderSL.action    = "short" if orderParent.action == "long" else "long" 
        orderSL.orderType = "LMT" 
        orderSL.volume    = volume 
        orderSL.lmtPrice  = stoploss
        
        # We create the ORDER takeprofit object 
        orderTP           = ORDER()
        orderTP.symbolName= symbolName
        orderTP.parentID  = orderParent.orderID 
        orderTP.action    = "short" if orderParent.action == "long" else "long" 
        orderTP.orderType = "MIT" 
        orderTP.volume    = volume 
        orderTP.lmtPrice  = takeprofit

        # We place these orders in the pending order list 
        self.pendingOrders.append(orderParent)
        self.pendingOrders.append(orderSL)
        self.pendingOrders.append(orderTP)

        return [orderParent, orderSL, orderTP]

    
    def executeOrder(self, 
                     symbol,           # SYMBOL object
                     order,            # ORDER object to execute  
                     type   = "open"   # Two kind of orders execution : "open" (a position), "close" (a position)
                     ) :     
        """! \private 
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """

        if type == "open" and self.checkExecuteOrder(symbol, order) : 

            # We first calculate the request margin to operate 
            type = symbol.marginRequestMethod 
            contractSize = symbol.contractSize
            openPrice    = symbol.askprice if order.action == "long" else symbol.bidprice
            openPrice    = self.generateSlippage(openPrice) # Slippage model 
             
            tickPrice    = None 
            tickSize     = None 
            leverage     = self.leverage

            requestMargin = financialTools.requestMargin(type, 
                                                         order.volume, 
                                                         contractSize, 
                                                         openPrice, 
                                                         tickPrice, 
                                                         tickSize, 
                                                         leverage) 
            
            #print ("request margin = ",requestMargin)
            

            # We secondly calculate the total price
            totalPrice = requestMargin*self.leverage 

            # Third we calculate the loan made by the broker 
            brokerLoan = totalPrice - requestMargin 

            # Fourth, we calculate the transaction fees 
            #commission = financialTools.transactionFees(symbol, 
            #                                            "BUY", 
            #                                            volume)
            commission = 0. 

            if (requestMargin + commission > self.availableMargin) :
                self.error("Cannot execute order : Request Margin + Commision > Available Margin", 
                           kwargs = {"REQUEST MARGIN"     : requestMargin, 
                                     "COMMISSION"         : commission, 
                                     "AVAILABLE MARGIN"   : self.availableMargin})
                return
        
            # Fifth, we operate the transaction 
            self.balance         -= requestMargin + commission
            self.usedMargin      += requestMargin 
            if self.usedMargin < 0. : self.usedMargin       = 0.
            self.availableMargin -= requestMargin + commission
            self.marginLevel      = np.divide(self.availableMargin, self.usedMargin)*100.

            # Sixth, we edit the ORDER object 

            # Attributes filled at execution 
            order.totalPrice    = totalPrice  
            order.requestMargin = requestMargin 
            order.brokerLoan    = brokerLoan 
            order.commission    = commission 
            order.executionPrice= openPrice 
            order.executionDate = symbol.time
            order.comment       = ""

            # Execution status
            order.executed      = True  

            # Seventh, we create a POSITION object and move the placed order in the executed list 
            pendingOrderIndex = None 
            for i in range(len(self.pendingOrders)) : 
                if order.orderID == self.pendingOrders[i].orderID :  
                    pendingOrderIndex = i 
            if pendingOrderIndex is not None : 
                self.executedOrders.append(self.pendingOrders[pendingOrderIndex])
                del self.pendingOrders[pendingOrderIndex]
            

            locPos                = POSITION() 
            locPos.orderID        = order.orderID
            locPos.symbol         = symbol.symbolName 
            locPos.volume         = order.volume 
            locPos.action         = order.action 
            locPos.executionPrice = openPrice 
            locPos.executionDate  = symbol.time 
            locPos.brokerLoan     = brokerLoan 
            locPos.requestMargin  = requestMargin

            locPos.possibleClosePrice = symbol.bidprice if order.action == "long" else symbol.askprice
            locPos.possibleCloseDate  = symbol.time 
            absoluteProfit            = locPos.possibleClosePrice*order.volume*symbol.contractSize - brokerLoan - requestMargin
            absoluteProfit_           = absoluteProfit if order.action == "long" else -absoluteProfit
            locPos.profit             = absoluteProfit_

            locPos.comment            = "" 

            self.openPositions.append(locPos)

        if type == "close" : 

            if order.parentID is not None : 

                # We retrieve the position associated to the order 
                openPositionIndex = None 
                for i in range(len(self.openPositions)) : 
                    if self.openPositions[i].orderID == order.parentID : 
                        openPositionIndex = i 
                
                if openPositionIndex is None : 
                    self.error("Error when retrieving the position associated to the closing order")
                else : 

                    order.executed = True

                    self.openPositions[openPositionIndex].possibleClosePrice = symbol.bidprice if order.action == "short" else symbol.askprice
                    self.openPositions[openPositionIndex].possibleClosePrice    = self.generateSlippage(self.openPositions[openPositionIndex].possibleClosePrice) # Slippage model 
                    self.openPositions[openPositionIndex].possibleCloseDate  = symbol.time 
                    absoluteProfit = self.openPositions[openPositionIndex].possibleClosePrice*order.volume*symbol.contractSize - self.openPositions[openPositionIndex].brokerLoan - self.openPositions[openPositionIndex].requestMargin
                    absoluteProfit_ = absoluteProfit if order.action == "short" else - absoluteProfit 
                    self.openPositions[openPositionIndex].profit = absoluteProfit_
                    
                    self.openPositions[openPositionIndex].closed = True 

                    # We operate the transaction 
                    requestMargin = self.openPositions[openPositionIndex].requestMargin
                    commission = 0. 

                    self.balance         += absoluteProfit_ + requestMargin + commission
                    self.usedMargin      -= requestMargin #+ absoluteProfit_ 
                    if self.usedMargin < 0.   : self.usedMargin = 0. 
                    self.availableMargin += requestMargin #+ absoluteProfit_ 
                    self.marginLevel      = np.divide(self.availableMargin, self.usedMargin)*100.

                    # We move the closed order and order associated pending order 
                    self.closedPositions.append(self.openPositions[openPositionIndex]) 
                    del self.openPositions[openPositionIndex]

                    isOrder = True
                    while (isOrder) : 
                        pendingOrderIndex = None 
                        for i in range(len(self.pendingOrders)) : 
                            if order.parentID == self.pendingOrders[i].parentID : 
                                pendingOrderIndex = i 
                        if pendingOrderIndex is not None : 
                            self.executedOrders.append(self.pendingOrders[pendingOrderIndex])
                            del self.pendingOrders[pendingOrderIndex]
                        if pendingOrderIndex is None : 
                            isOrder = False 

                    # We update some statistics of the porfolio

                    # 1. We update the equity curve 
                    self.equityCurve.append(self.equity)

                    # 2. We update the drawdown calculation 
                    self.currentDrawDown = self.getMaxDrawDown() 

                    # 3. We update the current value loss serie 
                    if absoluteProfit_ < 0 : 
                        self.currentValueLossSerie += -absoluteProfit_ 
                        self.currentValueGainSerie = 0. 
                        self.currentMaximumNumberOfConsecutiveGains = 0
                    if absoluteProfit_ > 0 : 
                        self.currentValueGainSerie += absoluteProfit_ 
                        self.currentValueLossSerie = 0. 
                        self.currentMaximumNumberOfConsecutiveGains += 1

            else : 
                self.error("Error. The order has no parent order")

                
 
            
    def checkPendingOrder(self, 
                          symbol, 
                          order) : 
        """! \private 
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """ 
        openPositionIndex = None 
        for i in range(len(self.openPositions)) : 
            if self.openPositions[i].orderID == order.orderID or self.openPositions[i].orderID == order.parentID :
                openPositionIndex = i 

        if openPositionIndex is not None : 
            self.updatePosition(symbol, self.openPositions[openPositionIndex])
            self.updatePortfolio()
        else : 
            pass 
        
        # If the order is the child of another order 
        if order.parentID is not None : 
            # Check if the parent of the order have been executed 
            isParentExecuted = False  
            for parent in self.openPositions : 
                if parent.orderID == order.parentID : 
                    isParentExecuted = True 
            if isParentExecuted : 
                # We check the current pending order 
                if order.orderType == "MIT": 
                    # Execute the order if : 
                    if order.action == "short" and symbol.askprice >= order.lmtPrice : 
                        self.executeOrder(symbol, order, type = "close") # Here we actualise the portfolio properties 


                    if order.action == "long" and symbol.bidprice <= order.lmtPrice : 
                        self.executeOrder(symbol, order, type = "close") # Here we actualise the portfolio properties 

                    
                if order.orderType == "LMT" : 
                    # Execute the order if : 
                    if order.action == "short" and symbol.askprice <= order.lmtPrice : 
                        self.executeOrder(symbol, order, type = "close") # Here we actualise the portfolio properties 

                    if order.action == "long" and symbol.bidprice >= order.lmtPrice : 
                        self.executeOrder(symbol, order, type = "close") # Here we actualise the portfolio properties 

        # If the order is a parent order 
        else : 
            if order.orderType == "MKT" : 
                self.executeOrder(symbol, order) # Here we actualise the portfolio properties 

            if order.orderType == "MIT" : 
                # Execute the order if : 
                if order.action == "short" and symbol.askprice >= order.lmtPrice : 
                    self.executeOrder(symbol, order) # Here we actualise the portfolio properties 


                if order.action == "long" and symbol.bidprice <= order.lmtPrice : 
                    self.executeOrder(symbol, order) # Here we actualise the portfolio properties 

            if order.orderType == "LMT" : 
                # Execute the order if : 
                if order.action == "short" and symbol.askprice <= order.lmtPrice : 
                    self.executeOrder(symbol, order) # Here we actualise the portfolio properties 

                if order.action == "long" and symbol.bidprice >= order.lmtPrice : 
                    self.executeOrder(symbol, order) # Here we actualise the portfolio properties 

    #########################################################################################
    # UPDATE FUNCTIONS
    #########################################################################################

    def updatePosition(self, 
                       symbol, 
                       position) : 
        """! \private 
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """

        position.possibleClosePrice =  symbol.bidprice if position.action == "long" else symbol.askprice 
        position.possibleCloseDate  =  symbol.time 
        absoluteProfit              =  position.possibleClosePrice*position.volume*symbol.contractSize - position.brokerLoan - position.requestMargin
        absoluteProfit_             =  absoluteProfit if position.action == "long" else -absoluteProfit
        position.profit             =  absoluteProfit_



    def updatePortfolio(self) :
        """! \private 
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """
        for position in self.openPositions : 
             self.availableMargin = self.balance + position.profit 
             self.marginLevel = np.divide(self.availableMargin, self.usedMargin)*100.
             self.equity      = self.availableMargin + self.usedMargin



    def update(self) : 
        """! \private 
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """

        # 1. We first update all the currently active positions 
        for key in list(self.symbols.keys()) : 
            symbol = self.symbols.get(key)
            for position in self.openPositions : 
                self.updatePosition(symbol, position)

        # 2. We then update the available margin and the margin level 
        self.updatePortfolio()
        
        # 3. We check for the security systems 
        self.tradingAuthorisation()
        self.checkMarginMinimum()

        # 4. We check for the pending orders 
        for key in list(self.symbols.keys()) : 
            symbol = self.symbols.get(key) 
            for order in self.pendingOrders : 
                if order.symbolName == key : 
                    self.checkPendingOrder(symbol, order) 
        
        # 5. We update the available margin and the margin level another time 
        self.updatePortfolio()
        
        # 6. We calculate the statistics 
        # No needs for instance. Statistics are calculated at each position close 

        # 7. We check again for the security systems 
        self.tradingAuthorisation()
        self.checkMarginMinimum()


    ###################################################################
    # Historical data price functions  
    ###################################################################
    def setHistoricalData(self, historicalData) : 
        """! \private 
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """

        self.historicalDataPrice = historicalData

    @SYSTEM.getHistoricalData
    def getHistoricalData(self, 
                          symbolName, 
                          dateIni, 
                          dateEnd, 
                          timeframe, 
                          onlyOpen = True) : 
        """!
        **Description :** 
            
            This function returns the historical dataset available to the 
            portfolio according the different constraints provided as a 
            parameter. 
        
        **Parameters :** 
            
            - symbolName [string] : 
                Name of the symbol 
            - dateIni [datetime/integer] : 
                If datetime: The initial dataset datetime value 
                If integer: The number of price candle in the past, 0 being the 
                            last available candle. 
                Note : dateIni and dateEnd have to have the same type 
            - dateEnd [datetime/integer] : 
                If datetime: The latest dataset datetime value 
                If integer: The number of price candle in the past, 0 being the 
                            last available candle. 
                Note : dateIni and dateEnd have to have the same type  
            - timeframe [integer] : 
                Timeframe sampling of the historical data in minute unit. 
                0 means the simulation base timeframe. 
                Note : The requested timeframe have to have been prepared 
                       in the simulation header. 
        
        **Returns :** 
            
            The function returns a dictionnary of the following shape : 
                
                {askopen : list(float), 
                 askhigh : list(float), 
                 asklow  : list(float), 
                 askclose: list(float), 
                 bidopen : list(float), 
                 bidhigh : list(float), 
                 bidlow  : list(float), 
                 bidclose: list(float), 
                 volume  : list(float), 
                 time    : list(datetime)}
                
        """ 
        # Case where the timeframe is provided as 0 
        if timeframe == 0 or timeframe == self.historicalDataTimeframe: 
            pass 
        else : 
            symbolName += "_"+str(timeframe)
            


        if not onlyOpen : 

            historicalData = self.historicalDataPrice.get(symbolName)
            df = pd.DataFrame(historicalData)



            if (type(dateIni) == type(dt.datetime(2020, 1, 10, 10, 10)) and type(dateIni) == type(dateEnd)) : 
                df = df.set_index("date") 
                df = df[dateIni : dateEnd]
            if (type(dateIni) == int and type(dateIni) == type(dateEnd)) : 
                if dateEnd == 0: 
                    df = df[-dateIni:]
                else : 
                    df = df[-dateIni:-dateEnd]
            dictDf = df.to_dict(orient="list")
            for i in range(len(dictDf.get("date"))) : 
                dictDf.get("date")[i] = dictDf.get("date")[i].to_pydatetime()
            
            return dictDf 
        
        else : 

            historicalData = self.historicalDataPrice.get(symbolName)

            #print("Historical data = ",self.historicalDataPrice)

            # !!! This step have to be optimized !!! (too slow)
            historicalData_ = dict()
            for key in list(historicalData.keys()) : 
                historicalData_.update({key : list()})
            for i in range(len(historicalData.get("market status"))) : 
                if historicalData.get("market status")[i] == "open" : 
                    for key in list(historicalData_.keys()) : 
                        historicalData_.get(key).append(historicalData.get(key)[i])


            df = pd.DataFrame(historicalData_)
            if (type(dateIni) == dt.datetime(2020, 1, 10, 10, 10) and type(dateIni) == type(dateEnd)) : 
                df = df.set_index("date") 
                df = df[dateIni : dateEnd]
            if (type(dateIni) == int and type(dateIni) == type(dateEnd)) : 
                if dateEnd == 0: 
                    df = df[-dateIni:]
                else : 
                    df = df[-dateIni:-dateEnd]
            dictDf = df.to_dict(orient="list")
            for i in range(len(dictDf.get("date"))) : 
                dictDf.get("date")[i] = dictDf.get("date")[i].to_pydatetime()
            
            return dictDf 


    @SYSTEM.getLastPrice 
    def getLastPrice(self, symbolName) : 
        """! 
        **Description :** 
            
            This function returns the last simulation price available to the 
            portfolio given the name of the symbol. 
            Note : In certain cases, because of the subloop models, the 
                   portfolio can return prices from the future that have 
                   theoretically not been released yet. To avoid this 
                   potential time ahead-bias, please for any action from 
                   the STRATEGY object, use only the askprice/bidprice to 
                   know the last existing price. 
                   If the subLoopModel is "close only", everything is fine, 
                   there is no risk of time ahead bias. 
        
        **Parameters :** 
            
            - symbolName [string] : 
                Name of the symbol 
        
        **Returns :** 
            
            This function returns a dictionnary of the following shape : 
                
            {"askopen" : float, 
             "askhigh" : float, 
             "asklow"  : float, 
             "askclose": float, 
             "askprice": float,
             "bidopen" : float, 
             "bidhigh" : float, 
             "bidlow"  : float, 
             "bidclose": float,
             "bidprice": float, 
             "date"    : datetime, 
             "volume"  : float, 
             "market state" : string ("open" or "closed") }
                
        """ 
        price = {
            "askopen" : self.symbols.get(symbolName).askopen, 
            "askhigh" : self.symbols.get(symbolName).askhigh, 
            "asklow"  : self.symbols.get(symbolName).asklow, 
            "askclose": self.symbols.get(symbolName).askclose, 
            "askprice": self.symbols.get(symbolName).askprice,
            "bidopen" : self.symbols.get(symbolName).bidopen, 
            "bidhigh" : self.symbols.get(symbolName).bidhigh, 
            "bidlow"  : self.symbols.get(symbolName).bidlow, 
            "bidclose": self.symbols.get(symbolName).bidclose,
            "bidprice": self.symbols.get(symbolName).bidprice, 
            "date"    : self.symbols.get(symbolName).time, 
            "volume"  : self.symbols.get(symbolName).volume, 
            "market state" : self.symbols.get(symbolName).marketState   
        }
        return price 
    
    ###################################################################
    # Portfolio system functions 
    ###################################################################
    @SYSTEM.message 
    def message(self, messageStr, category = "Strategy Message", kwargs = dict()) : 
        
        if self.verbose : 
            print (category)
            print (messageStr) 
            for key in list(kwargs.keys()) : 
                print (key+": "+str(kwargs[key])) 
                
        return 
    
    @SYSTEM.error
    def error(self, errorStr, category = "Portfolio Error.", kwargs = dict()) : 
        
        if self.verbose : 
            print (category)
            print (errorStr) 
            for key in list(kwargs.keys()) : 
                print (key+": "+str(kwargs[key])) 
        
        return 
    
    @SYSTEM.step
    def newTurn(self, index_, portfolio_state = None, simulation_state = None) : 
        
        return 
    
    @SYSTEM.init
    def initiate(self, simulation = None, portfolio = None) : 
        
        return self.trading_log_first_write_mode
        
        
    
    