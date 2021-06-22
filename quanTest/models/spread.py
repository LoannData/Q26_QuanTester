#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 16:03:51 2021

@author: loann
"""

class SPREAD : 
    """!  
    ===============================================================
    Q26 - QuanTester module - SPREAD object. 
    ===============================================================
    ### Description :
        
        This class contains functions used by PRICE module object 
    
    ### Examples :
    
    ### Planned developments :
    
    ### Known bugs :
    
    \dontinclude[
    Do do list : 
        - 
    ] 
        

    """ 
    
    
    def spreadModel(self, 
                    model       = "constant", 
                    apply       = "bid", # "ask", "both"
                    parameters  = {"spread" : 0.0001} ) : 
        """!  
        **Description :** 
            
            Modify ask and bid prices of a PRICE object according a provided 
            spread model. 
        
        **Parameters :** 
            
            - model [str] = "constant" : 
                To every available model is associated a parameters dictionnary.
                The different available spread models are : 
                    - "constant" : 
                        Consists in a constant widening of the prices. In this case : 
                        parameters = {"spread" [double] : spread value}
            - apply [str] = "bid" : 
                - "bid" -> the spread value is substracted from the bid values 
                - "ask" -> the spread value is added to the ask values 
                - "both" -> the spread value is 50% substracted from the bid values 
                            and 50% added to the ask values.
            - parameters [dict] = None : 
                See model parameter description. 
        
        **Returns :** 
            
            None
            
        """
        
        spread = self.generateSpread(model = model, 
                                     parameters = parameters)
        
        if apply == "bid" : 
            
            for i in range(len(self.date)) : 
                
                self.bidOpen[i] -= spread[i].get("open")
                self.bidHigh[i] -= spread[i].get("high") 
                self.bidLow[i]  -= spread[i].get("low") 
                self.bidClose[i]-= spread[i].get("close") 
        
        if apply == "ask" : 
            
            for i in range(len(self.date)) : 
                
                self.askOpen[i] += spread[i].get("open")
                self.askHigh[i] += spread[i].get("high") 
                self.askLow[i]  += spread[i].get("low") 
                self.askClose[i]+= spread[i].get("close")
        
        if apply == "both" : 
            
            for i in range(len(self.date)) : 
                
                self.bidOpen[i] -= 0.5*spread[i].get("open")
                self.bidHigh[i] -= 0.5*spread[i].get("high") 
                self.bidLow[i]  -= 0.5*spread[i].get("low") 
                self.bidClose[i]-= 0.5*spread[i].get("close") 
                
                self.askOpen[i] += 0.5*spread[i].get("open")
                self.askHigh[i] += 0.5*spread[i].get("high") 
                self.askLow[i]  += 0.5*spread[i].get("low") 
                self.askClose[i]+= 0.5*spread[i].get("close")
    
    def generateSpread(self,
                       model      = None, 
                       parameters = None) : 
        """!  \private 
        **Description :** 
            
            Generate spread value as a function of the provided model 
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            PRICE object 
        """
        
        if model == "constant" : 
            
            spread = list() 
            for i in range(len(self.date)) : 
                
                locSpread = {
                    "open" : parameters.get("spread"), 
                    "high" : parameters.get("spread"), 
                    "low"  : parameters.get("spread"), 
                    "close": parameters.get("spread")
                    }
                spread.append(locSpread)
            
            return spread
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    