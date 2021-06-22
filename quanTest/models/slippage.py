#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 17:24:09 2021

@author: loann
"""

import numpy as np 


class SLIPPAGE : 
    """!  
    ===============================================================
    Q26 - QuanTester module - SLIPPAGE object. 
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
    
    def slippageModel(self, 
                      model = "gaussian relative", 
                      parameters = {"std" : 0.0001}) : 
        """!  
        **Description :** 
            
            Define market slippage model 
        
        **Parameters :** 
            
            - model [str] = "gaussian relative" : 
                The available models are : 
                    - "gaussian relative" : 
                        This model suggests the price meet a random normal fluctuation 
                        caracterised by a standard deviation value. The parameters are : 
                            {"std" : standard deviation as a percentage of the current price}
            - parameters [dict] = {"std" : 0.0001} : 
                See model parameter description. 
        
        **Returns :** 
            
            None
        """
        self.slippageMdl = {"name"       : model, 
                            "parameters" : parameters}
    
    
    def generateSlippage(self, 
                         price) : 
        """! \private 
        **Description :** 
            
            Define market slippage model 
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            PRICE object 
        """
        if self.slippageMdl is not None : 
            
            if self.slippageMdl.get("name") == "gaussian relative" : 
                parameters = self.slippageMdl.get("parameters")
                price = np.random.normal(loc = price, scale = parameters.get("std")*price)
                return price 
            else : 
                print ("Bad slippage model")
        
        else : 
            
            return price 
    
    
    
    