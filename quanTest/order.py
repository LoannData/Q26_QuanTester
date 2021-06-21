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

import random

class ORDER : 
    """!
    ===============================================================
    Q26 - QuanTester module - ORDER object. 
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

    def __init__(self) : 
        # Standard order attributes 
        ## ### Symbol name 
        # **Type** : string \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Name of the symbol subject to the transaction 
        self.symbolName    = None         # name of the symbpol associated to the order 
        ## ### Order ID 
        # **Type** : integer \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # To each ORDER is associated a random integer. This reference number should not be 
        # edited by the user. 
        self.orderID       = None         # Reference ID of the order 
        ## ### Parent order ID 
        # **Type** : integer \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Typically, children orders are pending orders placed as security 
        # orders when a parent order have been placed. The parent order haven 
        # parentID value but children orders have a parentOrder value corresponding 
        # to the orderID value of the parent order. 
        self.parentID      = None         # Reference ID of an order parent of this order 
        ## ### Action 
        # **Type** : string \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Order direction : "long" or "short". 
        self.action        = None         # "long" or "short"
        ## ### Order type 
        # **Type** : string \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # "MKT" (Market), "LMT" (Limit), "MIT" (Market If Touched)
        self.orderType     = None         # "MKT" (Market), "LMT" (Limit), "MIT" (Market If Touched) 
        ## ### Volume of asset 
        # **Type** : float \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Volume of asset to be traded in symbol lot size unit. 
        self.volume        = None         # Volume of the asset to be traded 
        ## ### Limit price 
        # **Type** : float \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Limit price dedicated to trigger LMT and/or MIT orders when conditions are met. 
        self.lmtPrice      = None         # Particular price for LMT and MIT orders
        ## ### Cancel date 
        # **Type** : datetime \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Date at which, if the order hasn't been executed yet, will be canceled 
        self.cancelDate    = None         # Date at which, if the order hasn't been executed yet, will be canceled 

        # Attributes filled at execution 
        ## ### Total price 
        # **Type** : float \n 
        # **Filled at execution** \n 
        # **Description** : \n 
        # Price paid by the user+broker to access to the volume of asset 
        # requested. 
        self.totalPrice    = None  
        ## ### Request margin 
        # **Type** : float \n 
        # **Filled at execution** \n 
        # **Description** : \n 
        # Margin requested by the broker to access to the asked asset volume. 
        self.requestMargin = 0 
        ## ### Broker Loan 
        # **Type** : float \n 
        # **Filled at execution** \n 
        # **Description** : \n
        # In case of a leverage > 1, loan value of the broker to access the 
        # asked asset volume. 
        self.brokerLoan    = None 
        ## ### Commission 
        # **Type** : float \n 
        # **Filled at execution** \n
        # **Description** : \n 
        # Potential fee paid at execution. 
        self.commission    = None 
        ## ### Execution price 
        # **Type** : float \n 
        # **Filled at execution** \n 
        # **Description** : \n 
        # Exact execution price. 
        self.executionPrice= None 
        ## ### Execution date 
        # **Type** : datetime \n 
        # **Filled at execution** \n 
        # **Description** : \n 
        # Exact execution date. 
        self.executionDate = None 
        ## ### Comment 
        # **Type** : string \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Comment inputed by the user. 
        self.comment       = None 

        # Execution status
        ## ### Execution status 
        # **Type** : boolean \n 
        # **Defaut value** : False \n 
        # **Description**  : \n 
        # If executed, this status becomes True. In case of a cancelled order, 
        # the ORDER object is placed in PORTFOLIO.executedOrders list but its 
        # execution status remains False. 
        self.executed      = False 

        # Initialization functions 
        self.initializeOrderID()
    
    #############################################################
    # INITIALISATION FUNCTIONS 
    #############################################################
    def initializeOrderID(self) : 
        """! \private 
        
        """
        n = 20 
        numList = "" 
        for i in range(n) : 
            numList += str(random.randint(0,9))
        self.orderID = int(numList)
    
    #############################################################
    # OTHER FUNCTIONS
    #############################################################
    

         

