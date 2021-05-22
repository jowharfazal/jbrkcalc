""" Brokerage Calculator for Zerodha & Tradeplus """

import streamlit as st

GST = 18

def calc_charges(broker, instrtype, instrkey,rates,buy,sell,qty):
    buyamt = buy*qty
    sellamt = sell*qty
    turnover = buyamt+sellamt

    #st.write(broker+':',instrtype) #,instrkey)
    if qty>0:
        brokerage = rates[broker]["Brokerage"][instrkey]
    else:
        brokerage = 0
    stt = round(rates[broker]["STT"][instrkey] * ( turnover if instrkey==1 else sellamt ) / 100,2)
    exchtrnchrg = round(rates[broker]["ExchTrnChrg"][instrkey] * turnover / 100,2)
    clearingchrg = round(rates[broker]["ClearingChrg"][instrkey] * turnover / 100,2)
    if qty>0:
        gst = round((brokerage+exchtrnchrg+clearingchrg) * GST / 100,2)
    else:
        gst = 0
    sebicharg = round(rates[broker]["SEBIChrg"][instrkey] * turnover / 100,2)
    stampduty = round(rates[broker]["StampDuty"][instrkey] * buyamt / 100,2)

    # totalcharges = brokerage+stt+exchtrnchrg+clearingchrg+gst+sebicharg+stampduty
    # pl = (sellamt-buyamt-totalcharges


    return [brokerage,stt,exchtrnchrg,clearingchrg,gst,sebicharg,stampduty]

    

instrtypes = ['EQ Intraday', 'EQ Delivery', 'Futures', 'Options']
instrtypesdict = {'EQ Intraday':0, 'EQ Delivery':1, 'Futures':2, 'Options':3}
brokers = ["Zerodha","TradePlus"]
rates = { "Zerodha":    { "Brokerage": [40,0,40,40], 
                          "STT": [0.025,0.1,0.01,0.05],
                          "ExchTrnChrg": [0.00345,0.00345,0.002,0.053],
                          "ClearingChrg": [0,0,0,0],
                          "SEBIChrg": [0.0001,0.0001,0.0001,0.0001],
                          "StampDuty": [0.003,0.015,0.002,0.003],
                        },
           "TradePlus": { "Brokerage": [18,0,18,0], 
                          "STT": [0.025,0.1,0.1,0.05],
                          "ExchTrnChrg": [0.00345,0.00345,0.002,0.053],
                          "ClearingChrg": [0,0,0,0],
                          "SEBIChrg": [0.0001,0.0001,0.0001,0.0001],
                          "StampDuty": [0.003,0.015,0.002,0.003],
                        } 
        }
         

#st.write("Brokerage Calculator")
st.title("Brokerage Calculator")

inp,dummy,outp1,sep,outp2,dummy1,dummy2 = st.beta_columns((1.7,0.9,1.1,0.1,1.1,2.2,2.2))

#broker = inp.radio("Broker", brokers, index=1)
broker = inp.selectbox("Broker", brokers,index=0)

#instrtype = inp.radio("Type of Instrument", instrtypes, index=3)
instrtype = inp.selectbox("Type of Instrument", instrtypes, index=3)

# buy = inp.number_input("Buy",value=0.0,step=0.05)
# sell = inp.number_input("Sell",value=0.0,step=0.05)
# qty = inp.number_input("Qty",value=0,step=1)
buy = inp.text_input("Buy",value=0)
sell = inp.text_input("Sell",value=0)
qty = inp.text_input("Qty",value=0)
try:
    buy = float(buy)
except:
    buy = 0

try:
    sell = float(sell)
except:
    sell = 0

try:
    qty = int(qty)
except:
    qty = 0

charges = calc_charges(broker, instrtype, instrtypesdict[instrtype],rates,buy,sell,qty)
totcharges = round(sum(charges),2)
pl = round((sell-buy)*qty-totcharges,2)

outp1.write('brokerage ')
outp1.write("stt ")
outp1.write("exchtrnchrg ")
outp1.write("clearingchrg ")
outp1.write("gst ")
outp1.write("sebicharg ")
outp1.write("stampduty ")
outp1.markdown("""---""")

sep.write(': ')
sep.write(": ")
sep.write(": ")
sep.write(": ")
sep.write(": ")
sep.write(": ")
sep.write(": ")
sep.markdown("""---""")

for charge in charges:
    outp2.write(charge)
outp2.markdown("""---""")

outp1.write("Tot Charges")
outp1.markdown("""---""")
sep.write(': ')
sep.markdown("""---""")
outp2.write(totcharges)
outp2.markdown("""---""")
outp1.write("P&L")
outp2.write(pl)
sep.write(': ')
sep.markdown("""---""")
outp1.markdown("""---""")
outp2.markdown("""---""")
