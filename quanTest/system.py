#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 10:34:01 2021

@author: loann
"""

import json 
import time 
import datetime as dt 






class SYSTEM : 
    
    def write_log(self, action, nargs, args, kwargs, result) : 
        if action in self.trading_log_actions : 
            arguments = dict() 
            arguments.update({"sys. local time" : str(dt.datetime.now())})
            arguments.update({"sys. action"     : action})
            for key in list(nargs.keys()) : 
                arguments.update({key : args[nargs[key]]})
            arguments.update(kwargs)
            arguments.update({"client response" : result})
            with open(self.trading_log_path, "a") as json_file : 
                json.dump(arguments, json_file)
                json_file.write("\n")
                
    def init_write_log(self, action, nargs, args, kwargs, mode = "a") : 
        if action in self.trading_log_actions : 
            arguments = dict() 
            arguments.update({"sys. local time" : str(dt.datetime.now())})
            arguments.update({"sys. action"     : action})
            for key in list(nargs.keys()) : 
                arguments.update({key : args[nargs[key]]})
            arguments.update(kwargs)
            with open(self.trading_log_path, mode) as json_file : 
                json.dump(arguments, json_file)
                json_file.write("\n")
                
    # System action functions 
    def init(function): 
        def func(self, *args, **kwargs) : 
            result = function(self, *args, **kwargs)
            nargs = {}
            args = list(args)
            self.init_write_log("portfolio initialization", nargs, args, kwargs, mode = result)
            return result 
        return func 
    
    def message(function): 
        def func(self, *args, **kwargs) : 
            result = function(self, *args, **kwargs)
            nargs = {"message" : 0}
            args = list(args)
            self.write_log("strategy message", nargs, args, kwargs, str(result))
            return result 
        return func 
                
    def error(function): 
        def func(self, *args, **kwargs) : 
            result = function(self, *args, **kwargs)
            nargs = {"error" : 0}
            args = list(args)
            self.write_log("portfolio error", nargs, args, kwargs, str(result))
            return result 
        return func 
    
    def step(function): 
        def func(self, *args, **kwargs) : 
            result = function(self, *args, **kwargs)
            nargs = {"sys. step" : 0}
            args = list(args)
            self.write_log("portfolio step", nargs, args, kwargs, str(result))
            return result 
        return func 
            
    # Order action functions 
    
    def placeOrder(function) : 
        def func(self, *args, **kwargs) : 
            result = function(self, *args, **kwargs)
            nargs = {"symbolName" : 0}
            self.write_log("place order", nargs, args, kwargs, str(result))
            return result 
        return func 
    
    def closePosition(function) : 
        def func(self, *args, **kwargs) : 
            result = function(self, *args, **kwargs)
            nargs = {"symbolName" : 0, 
                     "orderID"    : 1}
            args = list(args)
            args[1] = args[1].orderID
            self.write_log("close position", nargs, args, kwargs, str(result))
            return result 
        return func 
    
    def editSLOrder(function): 
        def func(self, *args, **kwargs) : 
            result = function(self, *args, **kwargs)
            nargs = {"symbolName" : 0,
                     "orderID"    : 1}
            args = list(args)
            args[1] = args[1].orderID
            self.write_log("edit stoploss order", nargs, args, kwargs, str(result))
            return result 
        return func 
    
    def editTPOrder(function): 
        def func(self, *args, **kwargs) : 
            result = function(self, *args, **kwargs)
            nargs = {"symbolName" : 0,
                     "orderID"    : 1}
            args = list(args)
            args[1] = args[1].orderID
            self.write_log("edit takeprofit order", nargs, args, kwargs, str(result))
            return result 
        return func 
    
    def cancelOrder(function): 
        def func(self, *args, **kwargs) : 
            result = function(self, *args, **kwargs)
            nargs = {"symbolName" : 0,
                     "orderID"    : 1}
            args = list(args)
            args[1] = args[1].orderID
            self.write_log("cancel order", nargs, args, kwargs, str(result))
            return result 
        return func 
    
    def getActivePositions(function):
        def func(self, *args, **kwargs) : 
            result = function(self, *args, **kwargs)
            for i in range(len(result)): 
                result[i] = result[i].orderID
            nargs = {"symbolName" : 0}
            args = list(args)
            self.write_log("get active positions", nargs, args, kwargs, str(result))
            return result 
        return func 
    
    # Data functions 
    
    def getHistoricalData(function) : 
        def func(self, *args, **kwargs) : 
            result = function(self, *args, **kwargs)
            nargs = {"symbolName" : 0,
                     "date ini"   : 1, 
                     "date end"   : 2, 
                     "timeframe"  : 3}
            args = list(args)
            self.write_log("get historical data", nargs, args, kwargs, "None")
            return result 
        return func 
    
    def getLastPrice(function) : 
        def func(self, *args, **kwargs) : 
            result = function(self, *args, **kwargs)
            nargs = {"symbolName" : 0}
            args = list(args)
            self.write_log("get last price", nargs, args, kwargs, str(result))
            return result 
        return func 
    
    

    
        


