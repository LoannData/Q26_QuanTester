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

class POSITION : 
    """!
    ===============================================================
    Q26 - QuanTester module - POSITION object. 
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
        # Main attributes 
        ## ### Order ID 
        # **Type** : integer \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # ID of the parent order that generated the POSITION. 
        self.orderID            = None      # ID of the parent order that generated the position
        ## ### Symbol name 
        # **Type** : string \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Name of the symbol on which the POSITION is active.  
        self.symbol             = None      # Symbol name  
        ## ### Asset volume 
        # **Type** : float \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Current owned volume of the asset. 
        self.volume             = None      # Current owned volume of the asset 
        ## ### Action position 
        # **Type** : string \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Position direction ("long" or "short"). 
        self.action             = None      # Position direction ("long" or "short")

        ## ### Execution price  
        # **Type** : float \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Execution price at position opening. 
        self.executionPrice     = None       # Execution price at position opening  
        ## ### Execution date  
        # **Type** : datetime \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Execution date at position opening. 
        self.executionDate      = None       # Execution date at position opening 
        ## ### Broker Loan  
        # **Type** : float \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Broker loan at position opening (to be reimbursed). 
        self.brokerLoan         = None       # Broker loan at position opening (to be reimbursed) 
        ## ### Paid Margin 
        # **Type** : float \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Margin paid by the user to open this position.
        self.requestMargin      = None       # Margin paid by the user to open this position
        ## ### Potential close price 
        # **Type** : float \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Potential price if close now.
        self.possibleClosePrice = None       # Potential price if close now 
        ## ### Potential close date 
        # **Type** : datetime \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Potential date if close now.
        self.possibleCloseDate  = None       # Potential date if close now 
        ## ### Potential profit 
        # **Type** : float \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Potential profit if close now.
        self.profit             = None       # Potential profit if close now 

        ## ### User comment 
        # **Type** : string \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # User can write a comment if he close the position manually.
        self.comment            = None       # Comment 

        ## ### Position status 
        # **Type** : boolean \n 
        # **Defaut value** : False \n 
        # **Description** : \n 
        # True if the POSITION is closed. 
        self.closed             = False      # Is the position closed 

        
