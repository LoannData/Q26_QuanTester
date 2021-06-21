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
import pandas as pd 
import datetime as dt 
import numpy as np 
import copy 
from quanTest import utils 

class PRICE : 
    """!
    ===============================================================
    Q26 - QuanTester module - PRICE object. 
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

    def __init__(self, name) : 

        # Base properties 
        ## ### Dataset name  
        # **Type** : string \n 
        # **Description** : \n 
        # Dataset name. The dataset name should be the exact same of 
        # a SYMBOL name embedded in the PORTFOLIO.
        self.name       = name
        
        # Variables that allow to identify by default the name of the columns in the csv file 
        ##! \private
        self.askOpen_    = "askopen"
        ##! \private
        self.askHigh_    = "askhigh"
        ##! \private
        self.askLow_     = "asklow"
        ##! \private
        self.askClose_   = "askclose"

        ##! \private
        self.bidOpen_    = "bidopen"
        ##! \private
        self.bidHigh_    = "bidhigh"
        ##! \private
        self.bidLow_     = "bidlow"
        ##! \private
        self.bidClose_   = "bidclose"

        ##! \private
        self.date_       = "time" 
        ##! \private
        self.dateFormat_ = "%Y-%m-%d %H:%M:%S"
        ##! \private
        self.volume_     = "volume"

        ##! \private
        self.path        = None

        # Names of each list on the object PRICE
        ##! \private
        self.askOpenTitle  = "askopen"
        ##! \private
        self.askHighTitle  = "askhigh"
        ##! \private
        self.askLowTitle   = "asklow"
        ##! \private
        self.askCloseTitle = "askclose"

        ##! \private
        self.bidOpenTitle  = "bidopen"
        ##! \private
        self.bidHighTitle  = "bidhigh"
        ##! \private
        self.bidLowTitle   = "bidlow"
        ##! \private
        self.bidCloseTitle = "bidclose"

        ##! \private
        self.dateTitle     = "time" 
        ##! \private
        self.dateFormat    = "%Y-%m-%d %H:%M:%S"
        ##! \private
        self.volumeTitle   = "volume"

        # Price object main properties
        ##! \private 
        self.baseTimeframe = None
        # Local market time zone
        ## ### Dataset time zone   
        # **Type** : int \n 
        # **Defaut value** : 0 \n 
        # **Description** : \n 
        # Time zone at which the data have been aggregated. 
        # UTC+...
        self.dataTimeZone      = 0 # UTC+...
        ## ### Exchange market time zone    
        # **Type** : int \n 
        # **Defaut value** : 0 \n 
        # **Description** : \n 
        # Exchange market time zone.  
        # UTC+...
        self.marketTimeZone    = 0 # UTC+...
        # Hours defined in the local market time zone 
        ## ### Market opening hour    
        # **Type** : string \n 
        # **Defaut value** : "00:00" \n 
        # **Description** : \n 
        # Market opening hour in the local market time zone.
        # The variable format should follow : "HH:MM"
        self.marketOpeningHour = "00:00"
        ## ### Market lunch hour    
        # **Type** : string \n 
        # **Defaut value** : None \n 
        # **Description** : \n 
        # Lunch period in the local market hour. 
        # The variable format should follow : "HH:MM-HH:MM". If no lunch, let 
        # this variable to None. 
        self.marketLunch       = None    # The format of this variable is : "HH:MM-HH:MM"
        ## ### Market breaks list    
        # **Type** : list(string) \n 
        # **Defaut value** : list() \n 
        # **Description** : \n 
        # List of the different breaks during a day.  
        # The variable format should follow : ["HH:MM-HH:MM", "...", ... ]. 
        # If there are no breaks within the day, let this variable as an empty list. 
        self.marketBreakList   = list()  # The format of this variable is : ["HH:MM-HH:MM", "..."]
        ## ### Market closing hour    
        # **Type** : string \n 
        # **Defaut value** : "24:00" \n 
        # **Description** : \n 
        # Market closing hour in the local market time zone.
        # The variable format should follow : "HH:MM".
        # Note : If the market never close, the close hour should be : "24:00"
        self.marketClosingHour = "24:00"
        # Days of week where the market is open 
        ## ### Days of week open market    
        # **Type** : list(integer) \n 
        # **Defaut value** : [0, 1, 2, 3, 4, 5, 6] \n 
        # **Description** : \n 
        # List of days in the week the market is usually open. 
        # 0 : Monday -> 6 : Sunday
        self.daysOfWeek        = [0, 1, 2, 3, 4, 5, 6] # [#day of the week from 0 to 6]
        # List of dates where the market can be closed (vacancies ...)
        # To be done ..... 
        ## ### Market vacations list    
        # **Type** : list() \n 
        # **Defaut value** : list()\n 
        # **Description** : \n 
        # List of vacations all along the simulation time. Note : this variable 
        # is not working yet. 
        self.vacations         = list()

        # Initial, file structure 
        ## ### Data list     
        # **Type** : list(float) \n 
        # **Defaut value** : list() \n 
        # **Description** : \n 
        # Open ask data list.  
        self.askOpen  = list()
        ## ### Data list     
        # **Type** : list(float) \n 
        # **Defaut value** : list() \n 
        # **Description** : \n 
        # High ask data list.  
        self.askHigh  = list()
        ## ### Data list     
        # **Type** : list(float) \n 
        # **Defaut value** : list() \n 
        # **Description** : \n 
        # Low ask data list.  
        self.askLow   = list() 
        ## ### Data list     
        # **Type** : list(float) \n 
        # **Defaut value** : list() \n 
        # **Description** : \n 
        # Close ask data list.  
        self.askClose = list()

        ## ### Data list     
        # **Type** : list(float) \n 
        # **Defaut value** : list() \n 
        # **Description** : \n 
        # Open bid data list.  
        self.bidOpen  = list()
        ## ### Data list     
        # **Type** : list(float) \n 
        # **Defaut value** : list() \n 
        # **Description** : \n 
        # High bid data list.  
        self.bidHigh  = list()
        ## ### Data list     
        # **Type** : list(float) \n 
        # **Defaut value** : list() \n 
        # **Description** : \n 
        # Low bid data list.  
        self.bidLow   = list() 
        ## ### Data list     
        # **Type** : list(float) \n 
        # **Defaut value** : list() \n 
        # **Description** : \n 
        # Close bid data list.  
        self.bidClose = list()

        ## ### Data list     
        # **Type** : list(datetime) \n 
        # **Defaut value** : list() \n 
        # **Description** : \n 
        # Date list.  
        self.date     = list() 
        
        ## ### Data list     
        # **Type** : list(float) \n 
        # **Defaut value** : list() \n 
        # **Description** : \n 
        # Volume list.  
        self.volume   = list()

        # Other important lists 
        ## ### Data list     
        # **Type** : list(string) \n 
        # **Defaut value** : list() \n 
        # **Description** : \n 
        # Market status list. It can be : "closed" or "open" 
        self.marketStatus = list()    # Can be : "closed", "open"

        # Other informations 
        ## ### Is re-sampled data ?      
        # **Type** : boolean \n 
        # **Defaut value** : False \n 
        # **Description** : \n 
        # False if original data. True is sampled from sub resolution data   
        self.sampled = False # False if original data. True is sampled from sub resolution data 
        ##! \private ### Data list     
        # **Type** : list(integer) \n 
        # **Defaut value** : list() \n 
        # **Description** : \n 
        # Index list.  
        self.index   = list()

    def createCopy(self) : 
        """!  
        **Description :** 
            
            Returns a deep copy of current PRICE object
        
        **Parameters :** 
            
            None 
        
        **Returns :** 
            
            PRICE object 
        """
        return copy.deepcopy(self)

    def setColumnsTitle(self, 
                        askOpen    = None, 
                        askHigh    = None, 
                        askLow     = None, 
                        askClose   = None, 
                        bidOpen    = None, 
                        bidHigh    = None, 
                        bidLow     = None, 
                        bidClose   = None, 
                        date       = None,
                        dateFormat = None, 
                        volume     = None, 

                        splitDaysHours    = False, # Case where days and hours infos are not on the same column 
                        days              = None, 
                        hours             = None) : 
        """!  
        **Description :** 
            
            This function allows to define the columns names in the file.  
        
        **Parameters :** 
            
            - askOpen [str] = None : 
                ask open datafile column name 
            - askHigh [str] = None : 
                ask high datafile column name 
            - askLow [str] = None : 
                ask low datafile column name 
            - askClose [str] = None : 
                ask close datafile column name 
            - bidOpen [str] = None : 
                bid open datafile column name 
            - bidHigh [str] = None : 
                bid high datafile column name 
            - bidLow [str] = None : 
                bid low datafile column name 
            - bidClose [str] = None : 
                bid close datafile column name 
            - date [str] = None : 
                date datafile column name. Only if days and hours are specified in 
                the same column. Example : 2021-03-18 23:57:12 
            - dateFormat [str] = None : 
                date format associated to the date strings in the datafile. 
                See more here : https://docs.python.org/3.6/library/datetime.html#strftime-and-strptime-behavior 
                Note : Even if days and hours are separated, the date format should be defined as if they were 
                only separated by a space. 
            - volume [str] = None : 
                volume datafile column name 
            - splitDaysHours [bool] = False :
                put True if days and hours are not in the same column in the datafile. 
            - days [str] = None : 
                days datafile column name. Only if splitDaysHours = True 
            - hours [str] = None : 
                hours datafile column name. Only if splitDaysHours = True
        
        **Returns :** 
            
            None 
        """
        if askOpen is not None : 
            self.askOpen_ = askOpen 
        if askHigh is not None : 
            self.askHigh_ = askHigh 
        if askLow is not None : 
            self.askLow_ = askLow 
        if askClose is not None : 
            self.askClose_ = askClose 
        if bidOpen is not None : 
            self.bidOpen_ = bidOpen 
        if bidHigh is not None : 
            self.bidHigh_ = bidHigh 
        if bidLow is not None : 
            self.bidLow_ = bidLow 
        if bidClose is not None : 
            self.bidClose_ = bidClose 
        if date is not None : 
            self.date_ = date 
        if dateFormat is not None : 
            self.dateFormat = dateFormat
        if volume is not None : 
            self.volume_ = volume 
        
        if splitDaysHours : 
            self.date_ = "split---"+days+"---"+hours
    
    def read(self, path) : 
        """!  
        **Description :** 
            
            Reads the historical dataset, given its path. The dataset have to 
            be a csv file. 
        
        **Parameters :** 
            
            path [str] : 
                The dataset path+name
        
        **Returns :** 
            
            None
        """
        
        df = pd.read_csv(path)

        try : 
            self.askOpen  = list(df[self.askOpen_])
        except : 
            pass 
        try : 
            self.askHigh  = list(df[self.askHigh_])
        except : 
            pass 
        try : 
            self.askLow   = list(df[self.askLow_])
        except : 
            pass 
        try : 
            self.askClose = list(df[self.askClose_])
        except : 
            pass 
        try : 
            self.bidOpen  = list(df[self.bidOpen_])
        except : 
            pass 
        try : 
            self.bidHigh  = list(df[self.bidHigh_])
        except : 
            pass 
        try : 
            self.bidLow   = list(df[self.bidLow_])
        except : 
            pass 
        try : 
            self.bidClose = list(df[self.bidClose_])
        except : 
            pass 
        try : 
            if not "split" in self.date_ : 
                tempDate      = list(df[self.date_])
                self.date     = [dt.datetime.strptime(x, self.dateFormat) for x in tempDate] 
            else : 
                locDate = self.date_.split("---")
                days_  = locDate[1] 
                hours_ = locDate[2]
                tempDays      = list(df[days_])
                tempHours     = list(df[hours_]) 
                self.date = list() 
                for i in range(len(tempDays)) : 
                    self.date.append(dt.datetime.strptime(tempDays[i]+" "+tempHours[i], self.dateFormat))
        except : 
            print ("An error occured")
            pass 
        try : 
            self.volume   = list(df[self.volume_])
        except : 
            pass 
    
    def setBaseTimeframe(self, 
                         timeframe = dt.timedelta(minutes = 1)) : 
        """!  
        **Description :** 
            
            Function allowing to define the base timeframe of the PRICE object.
        
        **Parameters :** 
            
            - timeframe [datetime.timedelta] = timedelta(minutes = 1) 
        
        **Returns :** 
            
            None 
        """
        
        if type(timeframe) == type(dt.timedelta(minutes = 1)) : 
            self.baseTimeframe = timeframe 
        else : 
            print ("Error. Bad timeframe reference format.")
    
    def fillMissingData(self, 
                        model = "constant") : 
        """!  
        **Description :** 
            
            Function that allows to fill the missing data so that it exists a price data candle for 
            every time step from the beginning to the end of the dataframe. 
            Note : More models will be implemented in a close future...

        
        **Parameters :** 
            
            - model [str] = "constant" : 
                - "constant" : Fill the candles using the last known price 
                               (the standard model, to be used when data quality is good) 
        
        **Returns :** 
            
            None 
        """

        if not self.sampled :

            filledAskOpen  = list() 
            filledAskHigh  = list()
            filledAskLow   = list()
            filledAskClose = list()

            filledBidOpen  = list() 
            filledBidHigh  = list()
            filledBidLow   = list()
            filledBidClose = list()

            filledDate     = list() 
            filledVolume   = list()

        

            if model == "constant" : 
                

                iniTime = self.date[0] 
                endTime = self.date[-1] 

                varTime = iniTime 
                varIndex = 0 
                while varTime <= endTime and varIndex < len(self.date): 
                    filledAskOpen.append(self.askOpen[varIndex])
                    filledAskHigh.append(self.askHigh[varIndex])
                    filledAskLow.append(self.askLow[varIndex])
                    filledAskClose.append(self.askClose[varIndex])

                    filledBidOpen.append(self.bidOpen[varIndex])
                    filledBidHigh.append(self.bidHigh[varIndex])
                    filledBidLow.append(self.bidLow[varIndex])
                    filledBidClose.append(self.bidClose[varIndex])

                    filledDate.append(varTime)
                    filledVolume.append(self.volume[varIndex])

                    if self.date[varIndex] == varTime : 
                        varIndex += 1 
                    
                    else :  
                        pass

                    # We increment the time variable from the base time delta 
                    varTime += self.baseTimeframe 

        
            self.askOpen  = filledAskOpen 
            self.askHigh  = filledAskHigh 
            self.askLow   = filledAskLow 
            self.askClose = filledAskClose

            self.bidOpen  = filledBidOpen 
            self.bidHigh  = filledBidHigh 
            self.bidLow   = filledBidLow 
            self.bidClose = filledBidClose

            self.date     = filledDate 
            self.volume   = filledVolume



    def shiftMarketTime(self, 
                        timeshift = 0) : 
        """!  
        **Description :** 
            
            Function that allows to shift the market hours to make it fit with 
            UTC+0 time if this is not already the case. 
        
        **Parameters :** 
            
            - timeshift [int] = 0 : 
                timeshift in hours
        
        **Returns :** 
            
            None 
        """
        self.date = list(np.array(self.date) + dt.timedelta(hours = timeshift)) 
    
    def setMarketTimeZone(self, 
                          timezone = 0) : 
        """!  
        **Description :** 
            
            Allows to define the price time data time zone 
            according to UTC+0. 
        
        **Parameters :** 
            
            - timezone [int] = 0 : 
                market time zone in hours
        
        **Returns :** 
            
            None 
        """

        self.marketTimeZone = timezone 
    
    def setDataTimeZone(self, 
                        timezone = 0) : 
        """!  
        **Description :** 
            
            Function that allows to define the timezone in which the data is printed 
        
        **Parameters :** 
            
            - timezone [int] = 0 : 
                timezone in which the data will be printed
        
        **Returns :** 
            
            None 
        """
        self.dataTimeZone = timezone

    def setMarketState(self) : 
        """!  
        **Description :** 
            
            Once defined the time zones, the open/close/breaks hours, this function 
            fill the marketState list with "open" or "closed" for every candle. 
        
        **Parameters :** 
            
            None
        
        **Returns :** 
            
            None 
        """

        for i in range(len(self.date)) : 

            if self.date[i].weekday() not in self.daysOfWeek : 
                self.marketStatus.append("closed") 
            else : 
                locHour   = "0"+str(self.date[i].hour) if  self.date[i].hour < 10 else str(self.date[i].hour) 
                locMinute = "0"+str(self.date[i].minute) if self.date[i].minute < 10 else str(self.date[i].minute)
                hourOfTheDay = locHour+":"+locMinute

                # We shift the hour of the day to have it in a local reference timeframe 
                h_dtz = int(locHour) 
                h_ut0 = h_dtz - self.dataTimeZone 
                if h_ut0 < 0 : 
                    h_ut0 = 24 + h_ut0  
                if h_ut0 > 23 : 
                    h_ut0 = 24 - h_ut0
                h_mtz = h_ut0 + self.marketTimeZone 
                if h_mtz > 23 : 
                    h_mtz = 24 - h_mtz 
                if h_mtz < 0 : 
                    h_mtz = 24 + h_mtz

                locHour   = "0"+str(h_mtz) if  h_mtz < 10 else str(h_mtz) 
                hourOfTheDay = locHour+":"+locMinute
                #print ("hOD : ",hourOfTheDay, ", h_dtz = ",h_dtz,", h_ut0 = ",h_ut0,", h_mtz = ",h_mtz)

                # We test the local hour of the day 
                locMarketState = "open" 
                if utils.compareHour(hourOfTheDay, "<=", self.marketOpeningHour) : 
                    locMarketState = "closed"
                if utils.compareHour(hourOfTheDay, ">=", self.marketClosingHour) : 
                    locMarketState = "closed"
                if self.marketLunch is not None : 
                    marketLunch = self.marketLunch.split("-")
                    beginLunch  = marketLunch[0]
                    endLunch    = marketLunch[1]
                    if utils.compareHour(hourOfTheDay, ">=", beginLunch) and utils.compareHour(hourOfTheDay, "<=", endLunch) : 
                        locMarketState = "closed"
                if len(self.marketBreakList) > 0 : 
                    for j in range(len(self.marketBreakList)) : 
                        marketBreak = self.marketBreakList[j].split("-")
                        beginBreak  = marketBreak[0]
                        endBreak    = marketBreak[1]
                        if utils.compareHour(hourOfTheDay, ">=", beginBreak) and utils.compareHour(hourOfTheDay, "<=", endBreak) : 
                            locMarketState = "closed"
                self.marketStatus.append(locMarketState) 
            
    def setBaseIndex(self) : 
        """!  \private
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None
        
        **Returns :** 
            
            None 
        """

        #if not self.sampled :

        self.index.append(-1) 

        for i in range (len(self.marketStatus)) : 

            if self.marketStatus[i] == "open" : 
                self.index.append(self.index[-1] + 1)
            else : 
                self.index.append(self.index[-1])
    
        del self.index[0]



    def timeDaySampler(self, 
                       baseTimeframe, 
                       timeframe) :
        """!  \private
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None
        
        **Returns :** 
            
            None 
        """

        marketOpeningHour = self.marketOpeningHour 
        marketClosingHour = self.marketClosingHour 
        marketLunch       = self.marketLunch 
        marketBreakList   = self.marketBreakList 


        dateList    = list() 
        dateListEnd = list()
        
        # 1. We start with the market open hour 
        dateList.append(marketOpeningHour) 
        dateListEnd.append(operation(dateList[-1], "+", operation(timeframe, "-", baseTimeframe)))
        currentTime = dateList[0] 
        
        marketBreakList_ = marketBreakList.copy() 
        
        if marketLunch is not None : 
            marketBreakList_.append(marketLunch)
        
        if len(marketBreakList_) > 0 : 
            # We check that the end of the period is not inside a break 
            insideBreak = False 
            breakIndexList = list()
            for i in range(len(marketBreakList_)) : 
                if (operation(dateListEnd[-1], ">=", marketBreakList_[i].split("-")[0]) and
                    #operation(dateListEnd[-1], "<", marketBreakList_[i].split("-")[1]) and 
                    operation(dateList[-1], "<", marketBreakList_[i].split("-")[0])): 
                    breakIndexList.append(i)
                    insideBreak = True 
            if insideBreak : 
                earlyIndex = breakIndexList[0] 
                for i in range (1, len(breakIndexList)) : 
                    if operation(marketBreakList_[breakIndexList[i]].split("-")[0], "<", marketBreakList_[earlyIndex].split("-")[0]) : 
                        earlyIndex = breakIndexList[i] 
                dateListEnd[-1] = operation(marketBreakList_[earlyIndex].split("-")[0], "-", baseTimeframe)
                #dateList[-1] = marketBreakList_[earlyIndex].split("-")[1]
        
        while operation(currentTime, "<", marketClosingHour): 
            
            # We add a new period 
            #dateList.append(operation(currentTime, "+", timeframe)) 
            dateList.append(operation(dateListEnd[-1], "+", baseTimeframe))
            dateListEnd.append(operation(dateList[-1], "+", operation(timeframe, "-", baseTimeframe)))
            
            
            if len(marketBreakList_) > 0 : 
                # We check that the end of the period is not inside a break 
                insideBreak = False 
                breakIndexList = list()
                for i in range(len(marketBreakList_)) : 
                    
                    if (operation(dateListEnd[-1], ">=", marketBreakList_[i].split("-")[0]) and
                        #operation(dateListEnd[-1], "<", marketBreakList_[i].split("-")[1]) and 
                        operation(dateList[-1], "<", marketBreakList_[i].split("-")[0])): 
                        
                        breakIndexList.append(i)
                        insideBreak = True 
                if insideBreak : 
                    earlyIndex = breakIndexList[0] 
                    for i in range (1, len(breakIndexList)) : 
                        if operation(marketBreakList_[breakIndexList[i]].split("-")[0], "<", marketBreakList_[earlyIndex].split("-")[0]) : 
                            earlyIndex = breakIndexList[i] 
                    dateListEnd[-1] = operation(marketBreakList_[earlyIndex].split("-")[0], "-", baseTimeframe)
                    #dateList[-1] = marketBreakList_[earlyIndex].split("-")[1]
                
                # We check that the begining of the period is not inside a break 
                insideBreak = False 
                breakIndexList = list()
                for i in range(len(marketBreakList_)) : 
                    if (operation(dateList[-1], ">=", marketBreakList_[i].split("-")[0]) and 
                        operation(dateList[-1], "<", marketBreakList_[i].split("-")[1])) : 
                        breakIndexList.append(i)
                        insideBreak = True 
                
                if insideBreak : 
                    lateIndex = breakIndexList[0] 
                    for i in range (1, len(breakIndexList)) : 
                        if operation(marketBreakList_[breakIndexList[i]].split("-")[1], ">", marketBreakList_[lateIndex].split("-")[1]) : 
                            lateIndex = breakIndexList[i] 
                            
                    dateList[-1]    = marketBreakList_[lateIndex].split("-")[1]
                    dateListEnd[-1] = operation(dateList[-1], "+", operation(timeframe, "-", baseTimeframe))
                    
                    # We check that the end of the period is not inside a break 
                    insideBreak = False 
                    breakIndexList = list()
                    for i in range(len(marketBreakList_)) : 
                        
                        if (operation(dateListEnd[-1], ">=", marketBreakList_[i].split("-")[0]) and
                            #operation(dateListEnd[-1], "<", marketBreakList_[i].split("-")[1]) and 
                            operation(dateList[-1], "<", marketBreakList_[i].split("-")[0])): 
                            
                            breakIndexList.append(i)
                            insideBreak = True 
                    if insideBreak : 
                        earlyIndex = breakIndexList[0] 
                        for i in range (1, len(breakIndexList)) : 
                            #print(marketBreakList_[i].split("-")[0])
                            if operation(marketBreakList_[breakIndexList[i]].split("-")[0], "<", marketBreakList_[earlyIndex].split("-")[0]) : 
                                earlyIndex = breakIndexList[i] 
                        dateListEnd[-1] = operation(marketBreakList_[earlyIndex].split("-")[0], "-", baseTimeframe)
                        #print(dateListEnd[-1])
                        #dateList[-1] = marketBreakList_[earlyIndex].split("-")[1]
            
            
            currentTime = dateList[-1]
            
            if operation(dateList[-1], ">=", marketClosingHour) : 
                del dateList[-1] 
                del dateListEnd[-1]
            if operation(dateListEnd[-1], ">", marketClosingHour) : 
                dateListEnd[-1] = operation(marketClosingHour, "-", baseTimeframe) 
        
        candlesList = list() 
        for i in range(len(dateList)) : 
            candlesList.append((dateList[i]+"-"+dateListEnd[i]))
        
        return candlesList

    def resampleData(self, newTimeFrame, name = None) : 
        """!  
        **Description :** 
            
            This function allows to re-sample candle data following the typical sampling method 
            used by trading platforms. Once resampled, the PRICE object obtains the status 
            sampled = True. 
        
        **Parameters :** 
            
            - newTimeFrame [str] : 
                New sampling timeframe in format : "HH:MM". The new sampling timeframe has to be 
                time larger than the before sampling timeframe. 
            - name [str] = None : 
                To make the data readable in the standard way by the STRATEGY classes 
                via the function .getHistoricalData, the name of the sampled data should be 
                the exact same as the corresponding SYMBOL name and the base dataset name. 
        
        **Returns :** 
            
            None 
        """

        # 0. We transform the base timeframe attribute into a readable format 
        baseTf_lst = str(self.baseTimeframe).split(":") 
        baseTf_h = int(baseTf_lst[0]) 
        baseTf_m = int(baseTf_lst[1]) 

        if baseTf_h < 10 : 
            baseTf_h = "0"+str(baseTf_h)
        else: 
            baseTf_h = str(baseTf_h)
        if baseTf_m < 10 : 
            baseTf_m = "0"+str(baseTf_m)
        else: 
            baseTf_m = str(baseTf_m)

        baseTf = baseTf_h+":"+baseTf_m 

        # We generate a day time sampler hours list 
        dayCandleList = self.timeDaySampler(baseTf, newTimeFrame)

        # We create a pandas dataframe from our data and pass date as index 
        df = pd.DataFrame({"askOpen" : self.askOpen, 
                        "askHigh" : self.askHigh, 
                        "askLow"  : self.askLow, 
                        "askClose": self.askClose, 
                        "bidOpen" : self.bidOpen, 
                        "bidHigh" : self.bidHigh, 
                        "bidLow"  : self.bidLow, 
                        "bidClose": self.bidClose, 
                        "date"    : self.date, 
                        "volume"  : self.volume, 
                        "market status" : self.marketStatus})


        df.set_index("date", inplace = True)


        dfList = list()

        # We iterate over old sampled data over every day 
        currentDay = df.index[0].date()

        lastDay = df.index[-1].date()
        while currentDay <= lastDay : 
            subDf = df[dt.datetime.combine(currentDay, dt.time(hour = 0, minute = 0)) : dt.datetime.combine(currentDay, dt.time(hour = 23, minute = 59))]
            dfList.append(subDf)
            currentDay += dt.timedelta(days = 1)


        sampledData = list()
        for i in range(len(dfList)) : 
            isMarketOpen = False 
            # 1. We check if it exists an open phase of the market 
            if "open" in list(dfList[i]["market status"]) : 
                isMarketOpen = True 
            
            if isMarketOpen : 
                # 2. We aggregate the data 
                currentDay = dfList[i].index[0].date()
                for j in range(len(dayCandleList)) : 
                    timeIni, timeEnd = dayCandleList[j].split("-")[0], dayCandleList[j].split("-")[1]
                    t_ini = dt.time(hour = int(timeIni.split(":")[0]), minute = int(timeIni.split(":")[1]))
                    t_end = dt.time(hour = int(timeEnd.split(":")[0]), minute = int(timeEnd.split(":")[1]))
                    
                    sampledData.append(dfList[i][dt.datetime.combine(currentDay, t_ini) : dt.datetime.combine(currentDay, t_end)])


        # We create new data lists which will contain future data sampling 
        askOpen  = list()
        askHigh  = list()
        askLow   = list() 
        askClose = list()

        bidOpen  = list()
        bidHigh  = list()
        bidLow   = list() 
        bidClose = list()

        date_     = list() 
        volume    = list()
        
        for i in range(len(sampledData)) : 
            if len(sampledData[i]) > 0 : 
                askOpen.append(sampledData[i]["askOpen"].iloc[0])
                askHigh.append(max(sampledData[i]["askHigh"]))
                askLow.append(min(sampledData[i]["askLow"])) 
                askClose.append(sampledData[i]["askClose"].iloc[-1])
                
                bidOpen.append(sampledData[i]["bidOpen"].iloc[0])
                bidHigh.append(max(sampledData[i]["bidHigh"]))
                bidLow.append(min(sampledData[i]["bidLow"])) 
                bidClose.append(sampledData[i]["bidClose"].iloc[-1])
                
                date_.append(sampledData[i].index[0].to_pydatetime())
                volume.append(sum(sampledData[i]["volume"]))

            #if len(index) > 0 : 
            #    index.append(self.date.index(date_[-1], index[-1]))
            #else : 
            #    index.append(self.date.index(date_[-1]))
            

        index     = list() 
        j = 0 
        for i in range(len(self.date)) : 
            if j+1 < len(date_) : 
                #print (self.date[i], date_[j], date_[j+1])
                if self.date[i] < date_[j] and j == 0 : 
                    index.append(-1)
                elif (self.date[i] >= date_[j] and self.date[i] <= date_[j+1]) : 
                    index.append(j)
                    #print (True)
                else : 
                    index.append(j+1)
                    j += 1
            
        self.askOpen = askOpen 
        self.askHigh = askHigh 
        self.askLow  = askLow 
        self.askClose= askClose

        self.bidOpen = bidOpen 
        self.bidHigh = bidHigh 
        self.bidLow  = bidLow 
        self.bidClose= bidClose 

        #print (date_[6])




        self.date    = date_ 
        self.index   = index 
        
        self.volume  = volume  

        self.sampled = True 


        self.marketStatus = list()

        self.setBaseTimeframe(timeframe = dt.timedelta(hours = int(newTimeFrame.split(":")[0]), minutes = int(newTimeFrame.split(":")[1])))
        #print(self.date[6])

        if name is not None : 
            self.name = name+"_"+str(int(newTimeFrame.split(":")[0])*60 + int(newTimeFrame.split(":")[1])) 
        else : 
            self.name += "_resampled"+str(int(newTimeFrame.split(":")[0])*60 + int(newTimeFrame.split(":")[1])) 
        

class PRICE_TABLE : 
    """!
    ===============================================================
    Q26 - QuanTester module - PRICE_TABLE object. 
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

    def __init__(self, priceList) : 
        ## ### Dataset name  
        # **Type** : list(class PRICE) \n 
        # **Description** : \n 
        # List of PRICE objects 
        self.priceList = priceList  # Here price list is a list of the objects PRICE to be synchronized 
        ## ### PRICEs synchronization state  
        # **Type** : boolean \n 
        # **Defaut value** : False \n 
        # **Description** : \n 
        # Synchronization state of the base PRICE objects 
        self.synchronized = False 
    
    def synchronize(self) : 
        """!  
        **Description :** 
            
            This function allows to synchronize the base data PRICEs. 
        
        **Parameters :** 
            
            None
        
        **Returns :** 
            
            None 
        """

        # 1. We cut the useless edges of the data 
        lateGeneralBeginning = self.priceList[0].date[0]
        earlyGeneralEnd      = self.priceList[0].date[-1] 

        for i in range(1, len(self.priceList)) : 

            if lateGeneralBeginning > self.priceList[i].date[0] : 
                lateGeneralBeginning = self.priceList[i].date[0]
            
            if earlyGeneralEnd > self.priceList[i].date[-1] : 
                earlyGeneralEnd = self.priceList[i].date[-1]

        # 2. We fill the missing data 
        for i in range(len(self.priceList)) : 

            self.priceList[i].fillMissingData(model = "constant")
            self.priceList[i].setMarketState() 
            self.priceList[i].setBaseIndex()
        
        self.synchronized = True 
    
    def iloc(self, index, exceptSampled = True) : 
        """!  \private
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None
        
        **Returns :** 
            
            None 
        """
        table = dict() 
        for price in self.priceList : 
            
            toUpdate = True 
            if exceptSampled : 
                if price.sampled : 
                    toUpdate = False 
                
            if toUpdate : 
                if index < len(price.date) : 
                    table.update({price.name : {
                        "askopen"       : price.askOpen[index],
                        "askhigh"       : price.askHigh[index],
                        "asklow"        : price.askLow[index],
                        "askclose"      : price.askClose[index],
                        "bidopen"       : price.bidOpen[index], 
                        "bidhigh"       : price.bidHigh[index], 
                        "bidlow"        : price.bidLow[index], 
                        "bidclose"      : price.bidClose[index], 
                        "time"          : price.date[index], 
                        "volume"        : price.volume[index], 
                        "market status" : price.marketStatus[index] 
                    }})
                else : 
                    print ("Index out of range for symbol : ", price.name)
                    index = -1 
                    table.update({price.name : {
                        "askopen"       : price.askOpen[index],
                        "askhigh"       : price.askHigh[index],
                        "asklow"        : price.askLow[index],
                        "askclose"      : price.askClose[index],
                        "bidopen"       : price.bidOpen[index], 
                        "bidhigh"       : price.bidHigh[index], 
                        "bidlow"        : price.bidLow[index], 
                        "bidclose"      : price.bidClose[index], 
                        "time"          : price.date[index], 
                        "volume"        : price.volume[index], 
                        "market status" : price.marketStatus[index] 
                    }})
        return table 
    
    def len(self) : 
        """!  \private
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None
        
        **Returns :** 
            
            None 
        """

        if self.synchronized : 

            return len(self.priceList[0].date)
        
        else : 

            print ("Data not synchronzed yet, cannot return any length")



    def array(self, name, indexIni, indexEnd, format = "dictionnary") : 
        """!  \private
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None
        
        **Returns :** 
            
            None 
        """
        price = None 
        for i in range(len(self.priceList)) : 
            if self.priceList[i].name == name : 
                price = self.priceList[i] 

        if type(indexIni) == type(1) and type(indexEnd) == type(1) : 

            array_ = {"askopen"       : price.askOpen[indexIni : indexEnd],
                    "askhigh"         : price.askHigh[indexIni : indexEnd],
                    "asklow"          : price.askLow[indexIni : indexEnd],
                    "askclose"        : price.askClose[indexIni : indexEnd],
                    "bidopen"         : price.bidOpen[indexIni : indexEnd], 
                    "bidhigh"         : price.bidHigh[indexIni : indexEnd], 
                    "bidlow"          : price.bidLow[indexIni : indexEnd], 
                    "bidclose"        : price.bidClose[indexIni : indexEnd], 
                    "date"            : price.date[indexIni : indexEnd], 
                    "volume"          : price.volume[indexIni : indexEnd], 
                    "market status"   : price.marketStatus[indexIni : indexEnd]}

        if type(indexIni) == type(dt.datetime(2021, 1, 12, 12, 12)) and type(indexEnd) == type(dt.datetime(2021, 1, 12, 12, 12)) : 

            locIndexIni_ = min(price.date, key=lambda x: abs(x - indexIni))
            locIndexEnd_ = min(price.date, key=lambda x: abs(x - indexEnd))

            locIndexIni = price.date.index(locIndexIni_) 
            locIndexEnd = price.date.index(locIndexEnd_) 

            if locIndexIni_ > indexIni : 
                locIndexIni -= 1
            if locIndexEnd_ > indexEnd : 
                locIndexEnd -= 1 

            array_ = {"askopen"       : price.askOpen[locIndexIni : locIndexEnd],
                    "askhigh"         : price.askHigh[locIndexIni : locIndexEnd],
                    "asklow"          : price.askLow[locIndexIni : locIndexEnd],
                    "askclose"        : price.askClose[locIndexIni : locIndexEnd],
                    "bidopen"         : price.bidOpen[locIndexIni : locIndexEnd], 
                    "bidhigh"         : price.bidHigh[locIndexIni : locIndexEnd], 
                    "bidlow"          : price.bidLow[locIndexIni : locIndexEnd], 
                    "bidclose"        : price.bidClose[locIndexIni : locIndexEnd], 
                    "date"            : price.date[locIndexIni : locIndexEnd], 
                    "volume"          : price.volume[locIndexIni : locIndexEnd], 
                    "market status"   : price.marketStatus[locIndexIni : locIndexEnd]}

        if format == "dictionnary" : 
            return array_
        if format == "dataframe" : 
            df = pd.DataFrame(data = array_)
            return df 

    def isSampled(self, priceName) : 
        """!  \private
        **Description :** 
            
            None
        
        **Parameters :** 
            
            None
        
        **Returns :** 
            
            None 
        """
        locIndex = None 
        for i in range(len(self.priceList)) : 
            price = self.priceList[i]
            if price.name == priceName : 
                locIndex = i
        return self.priceList[locIndex].sampled




def operation(h1, operator, h2) : 
    h1_ = h1 
    h2_ = h2
    
    h1 = h1.split(":")
    h1_hour, h1_minute = int(h1[0]), int(h1[1])
    h2 = h2.split(":") 
    h2_hour, h2_minute = int(h2[0]), int(h2[1]) 
    

    if operator == "+" : 
        h3_hour, h3_minute = None, None 
        h3 = None 
        
        h3_hour   = h1_hour + h2_hour 
        h3_minute = h1_minute + h2_minute 
        
        while h3_minute >= 60 : 
            h3_minute -= 60 
            h3_hour   += 1 

        
        if h3_hour   < 10 and h3_hour >= 0 : 
            h3_hour   = "0"+str(h3_hour) 
        else : 
            h3_hour = str(h3_hour)
        if h3_minute < 10 : 
            h3_minute = "0"+str(h3_minute)
        else : 
            h3_minute = str(h3_minute)
            
        h3 = h3_hour+":"+h3_minute
        
        return h3
    
    if operator == "-" : 
        h3_hour, h3_minute = None, None 
        h3 = None  
        
        h3_hour   = h1_hour - h2_hour 
        h3_minute = h1_minute - h2_minute 
        
        while h3_minute < 0 : 
            h3_minute  = 60 - abs(h3_minute) 
            h3_hour   -= 1
        
        if abs(h3_hour)   < 10 and h3_hour >= 0 : 
            h3_hour   = "0"+str(h3_hour) 
        elif abs(h3_hour)   < 10 and h3_hour < 0 : 
            h3_hour   = "-0"+str(h3_hour) 
        else : 
            h3_hour = str(h3_hour)
        if h3_minute < 10 : 
            h3_minute = "0"+str(h3_minute)
        else : 
            h3_minute = str(h3_minute)
            
        h3 = h3_hour+":"+h3_minute
        
        return h3
        
    
    if operator == "<" : 
        
        if h1_hour < h2_hour : 
            return True 
        if h1_hour > h2_hour : 
            return False 
        if h1_hour == h2_hour : 
            if h1_minute < h2_minute : 
                return True 
            else : 
                return False 
    
    if operator == ">" : 
        
        if h1_hour > h2_hour : 
            return True 
        if h1_hour < h2_hour : 
            return False 
        if h1_hour == h2_hour : 
            if h1_minute > h2_minute : 
                return True 
            else : 
                return False 
            
    if operator == ">=" : 
        
        if h1_hour > h2_hour : 
            return True 
        if h1_hour < h2_hour : 
            return False 
        if h1_hour == h2_hour : 
            if h1_minute >= h2_minute : 
                return True 
            else : 
                return False 
    
    if operator == "min" : 
        
        if h1_hour < h2_hour : 
            return h1_ 
        if h1_hour > h2_hour : 
            return h2_
        if h1_hour ==  h2_hour : 
            if h1_minute < h2_minute : 
                return h1_ 
            else : 
                return h2_
