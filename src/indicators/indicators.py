
from talib import MACDFIX, RSI, EMA
import os

import pandas as pd
class Indicator:

    
    # indicatorlist = ['ichimoku200', 'macdRSI']    
    def beginCalc(self, df, tickerName, atr):
        ## FILL THIS IN AS MORE INDICATORS ARE ADDED
        indicatorlist = ['ichimoku200','macdRSI']

        # Step 1: Find out if analysis csv exists
        
        if not os.path.exists('./database/' + tickerName + '/IndicatorScore.csv'):
            columnNames = indicatorlist
            frame = pd.DataFrame(columns=columnNames)
            frame.loc[len(frame)] = 100
            frame.loc[len(frame)] = 0
            frame.loc[len(frame)] = 1
            frame.to_csv('./database/' + tickerName + '/IndicatorScore.csv')
        else:
            columnCheck = pd.read_csv('./database/' + tickerName + '/IndicatorScore.csv', index_col=0)
            for i in indicatorlist:
                if not i in columnCheck.columns:
                    avg = columnCheck.mean(axis = 1)
                    columnCheck.insert(len(columnCheck.columns), i, avg)
            columnCheck.to_csv('./database/' + tickerName + '/IndicatorScore.csv')
        resultsDict = {}

        for i in indicatorlist:
            fnRun = getattr(self, i)
            output = fnRun(df)
            resultsDict[i] = output
            
        return resultsDict
    
    def ichimoku200(self,df):
        ## Step 1: 
        #####PLACEHOLDER
        # df = pd.read_csv('./database/AAPL.csv')
        #####END_PLACEHOLDER
        df = df.dropna()
        ###1. Getting Parameters

        ##a. Senkou Span B Ahead
        Currentfifty_two = df.head(52)
        Currentfifty_two_high = Currentfifty_two['high'].max()
        Currentfifty_two_low = Currentfifty_two['low'].min()
        AheadSenkouB = (Currentfifty_two_high + Currentfifty_two_low) / 2
        # print("SenkouBAhead\n", AheadSenkouB)

        ##b. Current Kijun-Sen
        Currenttwenty_six = Currentfifty_two.head(26)
        Currenttwenty_six_high = Currenttwenty_six['high'].max()
        Currenttwenty_six_low = Currenttwenty_six['low'].min()
        CurrentKijun = (Currenttwenty_six_high + Currenttwenty_six_low) / 2
        # print("Kijun-Sen\n" , CurrentKijun)

        ##c. Current Tenkan-Sen
        Currentnine = Currenttwenty_six.head(9)
        Currentnine_high = Currentnine['high'].max()
        Currentnine_low = Currentnine['low'].min()
        CurrentTenkan = (Currentnine_high + Currentnine_low)/2

        # print("Tenkan-Sen\n", CurrentTenkan)

        ##d. Senkou Span A Ahead
        AheadSenkouA = (CurrentKijun + CurrentTenkan) / 2
        # print("SenkouAAhead\n", AheadSenkouA)

        ##e. Senkou Span B Current
        Pastfifty_two = df.iloc[26:].head(52)
        Pastfifty_two_high = Pastfifty_two['high'].max()
        Pastfifty_two_low = Pastfifty_two['low'].min()
        CurrentSenkouB = (Pastfifty_two_high + Pastfifty_two_low) / 2
        # print("SenkouBCurrent\n", CurrentSenkouB)

        ##f. Past Kijun-Sen
        Pasttwenty_six = Pastfifty_two.head(26)
        Pasttwenty_six_high = Pasttwenty_six['high'].max()
        Pasttwenty_six_low = Pasttwenty_six['low'].min()
        PastKijun = (Pasttwenty_six_low + Pasttwenty_six_high) / 2
        # print("PastKijun-Sen\n",PastKijun)

        ##g. Past Tenkan-Sen
        Pastnine = Pasttwenty_six.head(9)
        Pastnine_high = Pastnine['high'].max()
        Pastnine_low = Pastnine['low'].min()
        PastTenkan = (Pastnine_high + Pastnine_low) / 2
        # print("PastTenkan-Sen\n", PastTenkan)

        ##h. Senkou Span A Current
        CurrentSenkouA = (PastKijun + PastTenkan) / 2
        # print("SenkouACurrent\n", CurrentSenkouA)


        ##i. Senkou Span B Past
        PastPastfifty_two = df.iloc[52:].head(52)
        PastPastfifty_two_high = PastPastfifty_two['high'].max()
        PastPastfifty_two_low = PastPastfifty_two['low'].min()
        PastSenkouB = (PastPastfifty_two_high + PastPastfifty_two_low) / 2

        ##j. Past Past Kijun - Sen
        PastPasttwenty_six = PastPastfifty_two.head(26)
        PastPasttwenty_six_high = PastPasttwenty_six['high'].max()
        PastPasttwenty_six_low = PastPasttwenty_six['low'].min()
        PastPastKijun = (PastPasttwenty_six_low + PastPasttwenty_six_high) / 2

        ##k. Past Past Tenkan-Sen
        PastPastnine = PastPasttwenty_six.head(9)
        PastPastnine_high = PastPastnine['high'].max()
        PastPastnine_low = PastPastnine['low'].min()
        PastPastTenkan = (PastPastnine_high + PastPastnine_low) / 2

        ##l. Senkou Span A Past
        PastSenkouA = (PastPastKijun + PastPastTenkan) / 2

        


        ##m. 200EMA
        emaInput = df.head(200)
        EMAclose = emaInput['close'].values
        ema = EMA(EMAclose, timeperiod=200)
        # print("EMA\n", ema[-1])

        ##n. current price action
        priceaction = df.head(1)
        pricehigh = priceaction['high'].values[0]
        pricelow = priceaction['low'].values[0]
        priceclose = priceaction['close'].values[0]
        ### IMPT CHIKOU SPAN = PRICE CLOSE

        # print("pricehigh\n", pricehigh)
        # print("pricelow\n", pricelow)
        
        ### 2. Analysing using Data Provided
        ##tenkan-kijun crossover type
            ## -1 means negative crossover
            ## 1 means positive crossover
            ## 0 means both

        if CurrentTenkan > CurrentKijun: crossover = 1
        elif CurrentTenkan < CurrentKijun: crossover = -1
        else: crossover = 0


        ##ahead cloud colour
            ## -1 means red cloud
            ## 1 means green cloud
            ## 0 means both

        if AheadSenkouA > AheadSenkouB: AheadCloud = 1
        elif AheadSenkouA < AheadSenkouB: AheadCloud = -1
        else: AheadCloud = 0

        ##market-ema type
            ## 1 means low > 200EMA
            ## -1 means high < 200EMA
            ## 0 means otherwise

        if pricelow > ema[-1]: marketEMA = 1
        elif pricehigh < ema[-1]: marketEMA = -1
        else: marketEMA = 0

        ##market-cloud type
            ## 1 means close is above current cloud, and close (lagging span) above the past cloud too
            ## -1 means close is below current cloud, and close (lagging span) below the past cloud too
            ## 0 means otherwise (absolutely no trading)

        if  priceclose > max(CurrentSenkouA,CurrentSenkouB) and priceclose > max(PastSenkouB,PastSenkouA):
            marketCloud = 1
        elif priceclose < max(CurrentSenkouB, CurrentSenkouA) and priceclose < max(PastSenkouA, PastSenkouB):
            marketCloud = -1
        else: marketCloud = 0



        if marketCloud == 1 and marketEMA >= 0 and AheadCloud >= 0 and crossover >= 0:
            position = 1 ##long
        elif marketCloud == -1 and marketEMA <=0 and AheadCloud <= 0 and crossover <= 0:
            position = -1 ##short
        else: position = 0 ## no position

        return position

    def macdRSI(self,df):
        #####PLACEHOLDER
        # df = pd.read_csv('./database/AAPL.csv')
        #####END_PLACEHOLDER
        df = df.dropna()

        ###1. Getting Parameters
        ##a. RSI
        rsiInput = df.head(15)
        RSIclose = rsiInput['close'].values
        rsi = RSI(RSIclose,timeperiod=14)
        # print("RSI\n", rsi[-1])

        ##b. MACD
        macdInput = df.head(34)
        MACDclose = macdInput['close'].values
        macd, macdsignal, macdhist = MACDFIX(MACDclose, signalperiod = 9)
        # print("MACD\n", macd[-1])
        # print("Signal\n", macdsignal[-1])

        ##c. 200EMA
        emaInput = df.head(200)
        EMAclose = emaInput['close'].values
        ema = EMA(EMAclose, timeperiod=200)

        # print("EMA\n", ema[-1])

        ##d. current price action
        priceaction = df.head(1)
        pricehigh = priceaction['high'].values[0]
        pricelow = priceaction['low'].values[0]
        # print("pricehigh\n", pricehigh)
        # print("pricelow\n", pricelow)


        ###2. Analysing using the data provided

        ##macd-signal crossover type
        ## -1 means negative crossover
        ## 1 means positive crossover
        ## 0 means both
        if macd[-1] > macdsignal[-1]: crossover = 1
        elif macd[-1] < macdsignal[-1]: crossover = -1
        else: crossover = 0

        ##market-ema type
        ## 1 means low > 200EMA
        ## -1 means high < 200EMA
        ## 0 means otherwise

        if pricelow > ema[-1]: marketEMA = 1
        elif pricehigh < ema[-1]: marketEMA = -1
        else: marketEMA = 0



        ##RSI-TYPE
        ##TO-DO


        ##OUTPUT
        if marketEMA == 1 and crossover >= 0: position = 1
        elif marketEMA == -1 and crossover <=0: position = -1
        else: position = 0

        return position


