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

class SYMBOL : 
    """!
    ===============================================================
    Q26 - QuanTester module - SYMBOL object. 
    ===============================================================
    ### Description :
    
    ### Examples :
    
    ### Planned developments :
    
    ### Known bugs :
    
    \dontinclude[
    Do do list : 
        - 
    ] 
        

    """ 
    
    def __init__(
        self, 
        symbolName              = "GOLD.USD",
        #dataTableName           = None,
        contractSize            = 100, 
        marginCurrency          = "USD", # Can be any existing currency 
        profitCalculationMethod = "CFD", # "CFD", "Forex", "Stock", "CFD-Index"
        marginRequestMethod     = "CFD", # "CFD", "Forex", "Stock", "CFD-Index"
        marginPercentage        = 100, 
        execution               = "Market", 
        minimalVolume           = 0.01, 
        maximalVolume           = 25.0, 
        volumeStep              = 0.01, 
        precision               = 3,        # Price precision (3 means 1 point = 0.001)
        exchangeType            = "Point", # "Point", "Percentage"
        exchangeLong            = 99.5, 
        exchangeShort           = 58.2 
    ) : 
        # These values are static over all the backtest 
        ## ### Symbol name 
        # **Type** : string \n 
        # **Defaut value** : "GOLD.USD" \n 
        # **Description** : \n 
        # Name of the symbol.  
        self.symbolName              = symbolName
        #self.dataTableName           = dataTableName
        ## ### Contract size 
        # **Type** : float \n 
        # **Defaut value** : 100 \n 
        # **Description** : \n 
        # Size of a unitary lot. 
        self.contractSize            = contractSize 
        ## ### Margin currency  
        # **Type** : string \n 
        # **Defaut value** : "USD" \n 
        # **Description** : \n 
        # Currency used to access this symbol. !!!Variable not active for 
        # instance!!!, "USD" is the defaut value. 
        self.marginCurrency          = marginCurrency 
        ## ### Profit calculation method 
        # **Type** : string \n 
        # **Defaut value** : "CFD" \n 
        # **Description** : \n 
        # Unused variable for instance... 
        self.profitCalculationMethod = profitCalculationMethod 
        ## ### Margin request method
        # **Type** : string \n 
        # **Defaut value** : "CFD" \n 
        # **Description** : \n 
        # Way the request margin is calculated as a function of the type of 
        # asset. There are actually 4 different margin request methods : 
        #   - "CFD"   = volume*contractSize*openPrice/leverage 
        #   - "Forex" = volume*contractSize*openPrice/leverage 
        #   - "Stock" = volume*contractSize*openPrice/leverage 
        #   - "CFD-Index" = volume*contractSize/openPrice/tickPrice/tickSize/leverage
        self.marginRequestMethod     = marginRequestMethod 
        ## ### Margin percentage  
        # **Type** : float \n 
        # **Defaut value** : 100 \n 
        # **Description** : \n 
        # If the portfolio margin rate is inferior to this value, a potential 
        # ORDER cannot be executed. 
        self.marginPercentage        = marginPercentage 
        ## ### Execution mode 
        # **Type** : string \n 
        # **Defaut value** : "Market" \n 
        # **Description** : \n 
        # Unused variable for instance... 
        self.execution               = execution 
        ## ### Minimal allowed volume 
        # **Type** : float \n 
        # **Defaut value** : 0.01 \n 
        # **Description** : \n 
        # Minimal volume to allow an order execution. 
        # Unused variable for instance... 
        self.minimalVolume           = minimalVolume 
        ## ### Maximal allowed volum
        # **Type** : float \n 
        # **Defaut value** : 25.0 \n 
        # **Description** : \n 
        # Maximal volume to allow an order execution.
        # Unused variable for instance... 
        self.maximalVolume           = maximalVolume 
        ## ### Volume step
        # **Type** : double \n 
        # **Defaut value** : 0.01 \n 
        # **Description** : \n 
        # An order can be placed only if volume % volume step = 0. 
        # Unused variable for instance... 
        self.volumeStep              = volumeStep
        ## ### Price precision 
        # **Type** : integer \n 
        # **Defaut value** : 3 \n 
        # **Description** : \n 
        # Price precision (3 means 1 point = 0.001)
        # Unused variable for instance... 
        self.precision               = precision
        ## ### Exchange type 
        # **Type** : string \n 
        # **Defaut value** : "Point" \n 
        # **Description** : \n 
        # "Point", "Percentage". 
        # Unused variable for instance... 
        self.exchangeType            = exchangeType 

        # These values are the brokerage fees (swap) and can evolve with time 
        ## ### Exchange long fee  
        # **Type** : double \n 
        # **Defaut value** : 99.5 \n 
        # **Description** : \n 
        # Fees in exchange type unit to pay regulary if the user maintain at least 
        # one long position. 
        # Unused variable for instance... 
        self.exchangeLong            = exchangeLong 
        ## ### Exchange short fee  
        # **Type** : double \n 
        # **Defaut value** : 58.2 \n 
        # **Description** : \n 
        # Fees in exchange type unit to pay regulary if the user maintain at least 
        # one short position. 
        # Unused variable for instance... 
        self.exchangeShort           = exchangeShort
        
        # These values are going to be updated at each new price value. 
        ## ### Variable updated at each time step 
        self.askopen                 = None 
        ## ### Variable updated at each time step 
        self.askhigh                 = None 
        ## ### Variable updated at each time step 
        self.asklow                  = None 
        ## ### Variable updated at each time step 
        self.askclose                = None 
        ## ### Variable updated at each time step 
        # Price to be used as execution price
        self.askprice                = None  
        ## ### Variable updated at each time step 
        self.bidopen                 = None 
        ## ### Variable updated at each time step 
        self.bidhigh                 = None 
        ## ### Variable updated at each time step 
        self.bidlow                  = None 
        ## ### Variable updated at each time step 
        self.bidclose                = None 
        ## ### Variable updated at each time step 
        # Price to be used as execution price 
        self.bidprice                = None 
        ## ### Variable updated at each time step 
        self.volume                  = None 
        ## ### Variable updated at each time step 
        self.time                    = None 
        ## ### Variable updated at each time step 
        self.marketState             = "open" 

        return 
    
    def setCurrentMarketState(
        self, 
        state
    ) : 
        """! \private 
        **Description :** 
            
        Define the current market state : 
            - "open"      : Buy and Sell orders are both allowed 
            - "closed"    : No trading allowed 
            - "buy only"  : Only buy orders allowed 
            - "sell only" : Only sell orders allowed
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """

        self.marketState = state
    
    def setCurrentPrice(
        self, 
        askopen  = None, 
        askhigh  = None, 
        asklow   = None, 
        askclose = None, 
        bidopen  = None, 
        bidhigh  = None, 
        bidlow   = None, 
        bidclose = None,
        volume   = None, 
        time     = None, 
        askprice = None, 
        bidprice = None  
    ) : 
        """! \private 
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            None 
        """
        if askopen is not None : 
            self.askopen = askopen
        if askhigh is not None : 
            self.askhigh = askhigh
        if asklow is not None : 
            self.asklow = asklow 
        if askclose is not None : 
            self.askclose = askclose 
        if bidopen is not None : 
            self.bidopen = bidopen
        if bidhigh is not None : 
            self.bidhigh = bidhigh
        if bidlow is not None : 
            self.bidlow = bidlow 
        if bidclose is not None : 
            self.bidclose = bidclose 
        if volume is not None : 
            self.volume = volume 
        if time is not None : 
            self.time   = time 
        if askprice is not None : 
            self.askprice = askprice 
        if bidprice is not None : 
            self.bidprice = bidprice 


