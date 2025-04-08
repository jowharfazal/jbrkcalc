""" Trade P/L Calculator for Zerodha/Finvasia/Tradeplus/PayTM """

import streamlit as st

st.set_page_config(page_title="Trade P/L calculator",page_icon='rupees_symbol_1.ico') #':chart:')

GST = 18

def calc_charges(broker, instrtype, instrkey,rates,buy,sell,qty):
    buyamt = buy*qty
    sellamt = sell*qty
    turnover = buyamt+sellamt

    #st.write(broker+':',instrtype) #,instrkey)
    if qty>0 and (buy>0 or sell > 0):
        if broker.upper() in ["ZERODHA","PAYTM"] and instrkey!=1:
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
    brokerage = round(brokerage,2)
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

    if instrtype == 'Deliv':
        brokerage = 15.3
    return [brokerage,stt,round(exchtrnchrg+clearingchrg,2),gst,sebicharg,stampduty]


instrtypes = ['Intraday', 'Deliv', 'Futures', 'Options']
instrtypesdict = {'Intraday':0, 'Deliv':1, 'Futures':2, 'Options':3}
brokers = ["Finvasia", "Trade+", "PayTM","Zerodha" ]
rates = { "Finvasia":    { "Brokerage": [5,5,5,5], 
                          "STT": [0.026,0.1,0.0125,0.065],
                          "ExchTrnChrg": [0.00345,0.00345,0.002,0.053],
                          "ClearingChrg": [0,0,0,0],
                          "SEBIChrg": [0.00005,0.00005,0.00005,0.00005],
                          "StampDuty": [0.003,0.015,0.002,0.003],
                        },
           "Trade+": { "Brokerage": [9,0.1,0.1,0.1], 
                          "STT": [0.026,0.1,0.0125,0.065],
                          "ExchTrnChrg": [0.00345,0.00345,0.002,0.053],
                          "ClearingChrg": [0,0,0.016,0.025],
                          "SEBIChrg": [0.0001,0.0001,0.0001,0.0001],
                          "StampDuty": [0.003,0.015,0.002,0.003],
                        },
           "PayTM":    { "Brokerage": [18,0,18,18], 
                          "STT": [0.026,0.1,0.0125,0.065],
                          "ExchTrnChrg": [0.00345,0.00345,0.002,0.053],
                          "ClearingChrg": [0,0,0,0],
                          "SEBIChrg": [0.00005,0.00005,0.00005,0.00005],
                          "StampDuty": [0.003,0.015,0.002,0.003],
                        },
           "Zerodha":    { "Brokerage": [40,0,40,40], 
                          "STT": [0.026,0.1,0.0125,0.065],
                          "ExchTrnChrg": [0.00345,0.00345,0.002,0.053],
                          "ClearingChrg": [0,0,0,0],
                          "SEBIChrg": [0.0001,0.0001,0.0001,0.0001],
                          "StampDuty": [0.003,0.015,0.002,0.003],
                        }
        }
         

st.title("Trade P/L Calculator")

broker = st.radio("Broker", brokers, index=2, horizontal=True)
instrtype = st.radio("Type of Instrument", instrtypes, index=3, horizontal=True)
# st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

inp,dummy,outp1,sep,outp2,dummy1,dummy2 = st.columns((1.6,0.2,1.5,0.1,1.3,2.3,2.1))

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

breakeven = round(totcharges/qty,2) if qty>0 else 0

if instrtype=='Deliv':
    outp1.write('<p style="font-size:85%">Brkrg./DP.Chrg</p>', unsafe_allow_html=True)
else:
    outp1.write('<p style="font-size:85%">Brokerage</p>', unsafe_allow_html=True)
    
outp1.write('<p style="font-size:85%">STT</p>', unsafe_allow_html=True)
outp1.write('<p style="font-size:85%">Exch+Clearing</p>', unsafe_allow_html=True)
outp1.write('<p style="font-size:85%">GST</p>', unsafe_allow_html=True)
outp1.write('<p style="font-size:85%">SEBI Chrg</p>', unsafe_allow_html=True)
outp1.write('<p style="font-size:85%">Stamp Duty</p>', unsafe_allow_html=True)
outp1.write('<p style="font-size:85%">Break-even</p>', unsafe_allow_html=True)

sep.write('<p style="font-size:85%">:</p>', unsafe_allow_html=True)
sep.write('<p style="font-size:85%">:</p>', unsafe_allow_html=True)
sep.write('<p style="font-size:85%">:</p>', unsafe_allow_html=True)
sep.write('<p style="font-size:85%">:</p>', unsafe_allow_html=True)
sep.write('<p style="font-size:85%">:</p>', unsafe_allow_html=True)
sep.write('<p style="font-size:85%">:</p>', unsafe_allow_html=True)
sep.write('<p style="font-size:85%">:</p>', unsafe_allow_html=True)

for charge in charges:
    out_html = '<p style="text-align:right;font-size:85%">'+str(charge)+'</p>'
    outp2.write(out_html, unsafe_allow_html=True)

out_html = '<p style="text-align:right;font-size:85%;color:Yellow">'+str(breakeven)+'</p>'
outp2.write(out_html, unsafe_allow_html=True)

outp1.write('<p style="font-size:100%"><b>Tot Charges</b></p>', unsafe_allow_html=True)
sep.write(': ')

totcharges_html = '<p style="color:Yellow;text-align:right;"><b>'+f"{totcharges:,.2f}"+'</b></p>'

outp2.write(totcharges_html, unsafe_allow_html=True)
outp1.write('<p style="font-size:115%"><b>P/L</b></p>', unsafe_allow_html=True)
if pl>0:
    pl_html = '<p style="text-align:right;font-size:115%;"><b>'+f"{pl:,.2f}"+'</b></p>'
elif pl<0:
    pl_html = '<p style="text-align:right;font-size:115%;"><b>'+f"{pl:,.2f}"+'</b></p>'
else:
    pl_html = '<p style="text-align:right><b>'+f"{pl:,.2f}"+'</b></p>'

sep.write(': ')
outp2.write(pl_html, unsafe_allow_html=True)
