""" Brokerage Calculator for Zerodha, Upstox, PayTM & Tradeplus """

import streamlit as st

GST = 18

RIGHT_ALIGN_TAG = "text-align:right;"
LEFT_ALIGN_TAG = "text-align:left;"
CENTER_ALIGN_TAG = "text-align:center;"


def calc_charges(broker, instrtype, instrkey,rates,buy,sell,qty):
    buyamt = buy*qty
    sellamt = sell*qty
    turnover = buyamt+sellamt

    #st.write(broker+':',instrtype) #,instrkey)
    if qty>0 and (buy>0 or sell > 0):
        if broker.upper() in ["ZERODHA","PAYTM","UPSTOX"] and instrkey!=1:
            brokeragerate = (rates[broker]["Brokerage"][instrkey])/2
            buybrokerage = buyamt / 100 * ( 0.03 if broker.upper()=="ZERODHA" else 0.05)
            buybrokerage = brokeragerate if buybrokerage > brokeragerate else buybrokerage
            sellbrokerage = sellamt / 100 * ( 0.03 if broker.upper()=="ZERODHA" else 0.05)
            sellbrokerage = brokeragerate if sellbrokerage > brokeragerate else sellbrokerage
            if instrkey==3:
                brokerage = brokeragerate * 2
            else:
                brokerage = buybrokerage+sellbrokerage
        else:
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
brokers = ["Zerodha", "UpStox", "TradePlus", "PayTM"]
rates = { "Zerodha":    { "Brokerage": [40,0,40,40], 
                          "STT": [0.025,0.1,0.01,0.05],
                          "ExchTrnChrg": [0.00345,0.00345,0.002,0.053],
                          "ClearingChrg": [0,0,0,0],
                          "SEBIChrg": [0.0001,0.0001,0.0001,0.0001],
                          "StampDuty": [0.003,0.015,0.002,0.003],
                        },
           "UpStox":    { "Brokerage": [40,0,40,40], 
                          "STT": [0.025,0.1,0.01,0.05],
                          "ExchTrnChrg": [0.00345,0.00345,0.002,0.053],
                          "ClearingChrg": [0,0,0,0],
                          "SEBIChrg": [0.00005,0.00005,0.00005,0.00005],
                          "StampDuty": [0.003,0.015,0.002,0.003],
                        },
           "TradePlus": { "Brokerage": [18,0,18,0], 
                          "STT": [0.025,0.1,0.01,0.05],
                          "ExchTrnChrg": [0.00345,0.00345,0.002,0.053],
                          "ClearingChrg": [0,0,0,0],
                          "SEBIChrg": [0.0001,0.0001,0.0001,0.0001],
                          "StampDuty": [0.003,0.015,0.002,0.003],
                        },
           "PayTM":    { "Brokerage": [20,0,20,20], 
                          "STT": [0.025,0.1,0.01,0.05],
                          "ExchTrnChrg": [0.00345,0.00345,0.002,0.053],
                          "ClearingChrg": [0,0,0,0],
                          "SEBIChrg": [0.00005,0.00005,0.00005,0.00005],
                          "StampDuty": [0.003,0.015,0.002,0.003],
                        }
        }
         

st.title("Trade P&L Calculator")

inp,dummy,outp1,sep,outp2,dummy1,dummy2 = st.beta_columns((1.7,0.2,1.5,0.1,1,2.2,2.2))

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

outp1.write('Brokerage')
outp1.write("STT")
outp1.write("Exch.Trn. Chrg")
outp1.write("Clearing Chrg")
outp1.write("GST")
outp1.write("SEBI Chrg")
outp1.write("Stamp Duty")
#outp1.markdown("""~~~""")

sep.write(': ')
sep.write(": ")
sep.write(": ")
sep.write(": ")
sep.write(": ")
sep.write(": ")
sep.write(": ")
#sep.markdown("""---""")

for charge in charges:
    out_html = '<p style="text-align:right;">'+str(charge)+'</p>'
    outp2.write(out_html, unsafe_allow_html=True)
#outp2.markdown("""---""")

outp1.write('<p style="font-size:110%"><b>Tot Charges</b></p>', unsafe_allow_html=True)
outp1.markdown("""---""")
sep.write(': ')
sep.markdown("""---""")

totcharges_html = '<p style="color:Blue;text-align:right;"><b>'+f"{totcharges:,.2f}"+'</b></p>'

outp2.write(totcharges_html, unsafe_allow_html=True)
outp2.markdown("""---""")
outp1.write('<p style="font-size:115%"><b>P/L</b></p>', unsafe_allow_html=True)
if pl>0:
    pl_html = '<p style="text-align:right;color:green;font-size:115%"><b>'+f"{pl:,.2f}"+'</b></p>'
elif pl<0:
    pl_html = '<p style="text-align:right;color:red"><b>'+f"{pl:,.2f}"+'</b></p>'
else:
    pl_html = '<p style="text-align:right><b>'+f"{pl:,.2f}"+'</b></p>'

outp2.write(pl_html, unsafe_allow_html=True)
sep.write(': ')
# sep.markdown("""---""")
# outp1.markdown("""---""")
# outp2.markdown("""---""")
