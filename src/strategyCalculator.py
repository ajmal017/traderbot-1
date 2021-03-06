import time

import indicators.indicators as ind
import indicators.ATRcalc as atrcalc
import os.path as path
import pandas as pd
import importlib

from comparator import Comparator
from analyser import Analyser

class StrategyCalculator():
    def __init__(self, tickerName):
        self.tickerName = tickerName
        self.comparator = Comparator(self.tickerName)
        self.analyser = Analyser(self.tickerName, self.comparator)
    
    def inform(self, df):
        # print("Calculating Strategy for " + str(self.tickerName) + " at " + str(timeStamp) + "...")
        ### TO-DO: Develop strategies to calculate
        
        ##
        ## Inform Analyser to do the interval Analysis first
        ## This is before the pseudotrades to ensure no clashes
        self.analyser.intervalAnalysis(df.head(1))

        #1. Calculate ATR for potential trade
        atr = atrcalc.ATRcalc(df)
        indi = ind.Indicator()
        
        Results = indi.beginCalc(df, self.tickerName, atr)

        for i in Results:
            if Results[i] != 0:
                self.analyser.PseudoTrade(df,i, Results[i], atr)

            ### for testing
            # self.analyser.PseudoTrade(df,i, Results[i], atr)
            ###
        ### END TO-DO
        # print("Calculated Strategy for " + str(self.tickerName) + " at " + str(timeStamp))
        self.comparator.compare(Results, atr)
        
        