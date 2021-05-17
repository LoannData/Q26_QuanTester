#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd 
import datetime as dt 
import numpy as np 
from quanTest import utils 

class PRICE : 

    def __init__(self, name) : 

        # Base properties 
        self.name       = name
        
        # Variables that allow to identify by default the name of the columns in the csv file 
        self.askOpen_    = "askopen"
        self.askHigh_    = "askhigh"
        self.askLow_     = "asklow"
        self.askClose_   = "askclose"

        self.bidOpen_    = "bidopen"
        self.bidHigh_    = "bidhigh"
        self.bidLow_     = "bidlow"
        self.bidClose_   = "bidclose"

        self.date_       = "time" 
        self.dateFormat_ = "%Y-%m-%d %H:%M:%S"
        self.volume_     = "volume"


        self.path        = None

        # Names of each list on the object PRICE
        self.askOpenTitle  = "askopen"
        self.askHighTitle  = "askhigh"
        self.askLowTitle   = "asklow"
        self.askCloseTitle = "askclose"

        self.bidOpenTitle  = "bidopen"
        self.bidHighTitle  = "bidhigh"
        self.bidLowTitle   = "bidlow"
        self.bidCloseTitle = "bidclose"

        self.dateTitle     = "time" 
        self.dateFormat    = "%Y-%m-%d %H:%M:%S"
        self.volumeTitle   = "volume"

        # Price object main properties 
        self.baseTimeframe = None
        # Local market time zone
        self.dataTimeZone      = 0 # UTC+...
        self.marketTimeZone    = 0 # UTC+...
        # Hours defined in the local market time zone 
        self.marketOpeningHour = "00:00"
        self.marketLunch       = None    # The format of this variable is : "HH:MM-HH:MM"
        self.marketBreakList   = list()  # The format of this variable is : ["HH:MM-HH:MM", "..."]
        self.marketClosingHour = "23:59"

        # Initial, file structure 
        self.askOpen  = list()
        self.askHigh  = list()
        self.askLow   = list() 
        self.askClose = list()

        self.bidOpen  = list()
        self.bidHigh  = list()
        self.bidLow   = list() 
        self.bidClose = list()

        self.date     = list() 
        self.volume   = list()

        # Other important lists 
        self.marketStatus = list()    # Can be : "closed", "open"

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
        """  
        This function allows to define the columns names in the file. 
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
        """ 
        Function that reads the csv file
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
        """ 
        Function allowing to define the base timeframe of the PRICE object.
        """
        if type(timeframe) == type(dt.timedelta(minutes = 1)) : 
            self.baseTimeframe = timeframe 
        else : 
            print ("Error. Bad timeframe reference format.")
    
    def fillMissingData(self, 
                        model = "constant") : 
        """ 
        Function that allows to fill the missing data so that it exists a price data candle for 
        every time step from the beginning to the end of the dataframe. 
        Different filling models can be used : 
            - "constant" : This model just fill the candles using the last knew price (the standard model, to be used when data quality is good)
            - other models to be defined ... 

        """
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
        """ 
        Function that allows to shift the market hours to make it fit with 
        UTC+0 time if this is not already the case 
        """
        self.date = list(np.array(self.date) + dt.timedelta(hours = timeshift)) 
    
    def setMarketTimeZone(self, 
                          timezone = 0) : 
        """ 
        Function that allows to define the price time data time zone 
        according to UTC+0. 
        """
        self.marketTimeZone = timezone 
    
    def setDataTimeZone(self, 
                        timezone = 0) : 
        """ 
        Function that allows to define the timezone in which the data is printed 
        """
        self.dataTimeZone = timezone

    def setMarketState(self) : 
        
        for i in range(len(self.date)) : 

            locHour   = "0"+str(self.date[i].hour) if  self.date[i].hour < 10 else str(self.date[i].hour) 
            locMinute = "0"+str(self.date[i].minute) if self.date[i].minute < 10 else str(self.date[i].minute)
            hourOfTheDay = locHour+":"+locMinute

            # We shift the hour of the day to have it in a local reference timeframe 
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

class PRICE_TABLE : 

    def __init__(self, priceList) : 
        self.priceList = priceList  # Here price list is a list of the objects PRICE to be synchronized 
        self.synchronized = False 
    
    def synchronize(self) : 

        # 1. We cut the useless edges of the data 
        lateGeneralBeginning = self.priceList[0].date[0]
        earlyGeneralEnd      = self.priceList[0].date[-1] 

        for i in range(1, len(self.priceList)) : 

            if lateGeneralBeginning > self.priceList[i].date[0] : 
                lateGeneralBeginning = self.priceList[i].date[0]
            
            if earlyGeneralEnd > self.priceList[i].date[-1] : 
                earlyGeneralEnd = self.priceList[i].date[-1]

        # 2. We fill the missing data 
        for i in range(len(self.priceList)) : 

            self.priceList[i].fillMissingData(model = "constant")
            self.priceList[i].setMarketState() 
        
        self.synchronized = True 
    
    def iloc(self, index) : 
        table = dict() 
        for price in self.priceList : 
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

        if self.synchronized : 

            return len(self.priceList[0].date)
        
        else : 

            print ("Data not synchronzed yet, cannot return any length")



    def array(self, name, indexIni, indexEnd, format = "dictionnary") : 
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
            locIndexIni = price.date.index(indexIni) 
            locIndexEnd = price.date.index(indexEnd) 

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





