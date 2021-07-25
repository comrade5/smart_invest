import yahoo_fin.stock_info as si
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import common as cm

company_ticker = 'AAPL'
tax_rate = 0.25
market_risk_premium = 0.0523
long_term_growth = 0.01
debt_return = 0.01

income_statement = si.get_income_statement(company_ticker)
balance_sheet = si.get_balance_sheet(company_ticker)
stats = si.get_stats_valuation(company_ticker)

# Ger CAGR and EBIT margin for the past 5 years ! Better to calculate free cash flow rather that using EBIT
totEbit = [(ebit/1000) for ebit in income_statement.loc['ebit']][::-1]
totRev = [(rev/1000) for rev in income_statement.loc['totalRevenue']][::-1]
latest_rev = totRev[len(totRev)-1]
earliest_rev = totRev[0]

# Getting CAGR
rev_CAGR = ((latest_rev/earliest_rev)**(float(1/(len(totRev)))))-1

# EBIT margin
EBIT_margin_lst = []
for y in range(0, len(income_statement.columns)):
    EBIT_margin = totEbit[y] / totRev[y]
    EBIT_margin_lst.append(EBIT_margin)
avg_EBIT_margin = sum(EBIT_margin_lst) / len(EBIT_margin_lst)

forecast_df = pd.DataFrame(columns=['Year' + str(i) for i in range(1,7)])

rev_forecast_lst = []
for i in range(1,7):
    if i != 6:
        rev_forecast = latest_rev*(1+rev_CAGR)**i
    else:
        rev_forecast = latest_rev*(1+rev_CAGR)**(i-1)*(1+long_term_growth)
    rev_forecast_lst.append(int(rev_forecast))
forecast_df.loc[0] = rev_forecast_lst
EBIT_forecast_lst = []
for i in range(0,6):
    EBIT_forecast = rev_forecast_lst[i]*avg_EBIT_margin
    EBIT_forecast_lst.append(int(EBIT_forecast))
forecast_df.loc[1] = EBIT_forecast_lst

# *** Calculating CAMP ***
risk_free_rate = si.get_data('^TNX').iloc[-1][0]/100
equity_beta = cm.get_beta(company_ticker)
equity_return = risk_free_rate + equity_beta * (market_risk_premium)

# *** Calculating WACC ***
market_cap = cm.get_market_cap(company_ticker)

# Getting the net debt
balance_sheet_site = "https://finance.yahoo.com/quote/" + company_ticker + \
                     "/balance-sheet?p=" + company_ticker
balance_sheet_html = requests.get(url=balance_sheet_site, headers = {'User-agent': 'Mozilla/5.0'})
balance_sheet_soup = bs(balance_sheet_html.text, 'html.parser')
balance_sheet_table = balance_sheet_soup.find('div', class_='D(tbrg)')
net_debt_lst = []
net_debt_row = balance_sheet_table.find('div', attrs={'title':'Net Debt'}).parent.parent
for value in net_debt_row.find_all('div'):
    value = value.text
    value = value.replace(',','')
    net_debt_lst.append(value)
net_debt_int = int(net_debt_lst[3])

# finding WACC
company_value = market_cap + net_debt_int
WACC = market_cap/company_value * equity_return + net_debt_int/company_value * debt_return * (1-tax_rate)
print(WACC)

discounted_EBIT_lst = []

for year in range(0,5):
    discounted_EBIT = forecast_df.iloc[1,year]/(1+WACC)**(year+1)
    discounted_EBIT_lst.append(int(discounted_EBIT))

terminal_value = forecast_df.iloc[1,5]/(WACC-long_term_growth)
PV_terminal_value = int(terminal_value/(1+WACC)**5)

enterprise_value = sum(discounted_EBIT_lst)+PV_terminal_value
equity_value = enterprise_value-net_debt_int
print('Equity value', equity_value)

'''
    The two main issues at play here are firstly that the somewhat questionable assumptions 
    on which the model is built are simply unreasonable for certain companies. 
    Secondly, the model output is highly sensitive to the WACC input data 
    due to the approach used to calculate the terminal company value. 
    A more appropriate approach would be to apply an EBIT or EBITDA multiple 
    based on comparable companies, as this entails a lower sensitivity of the 
    program output to the WACC and the terminal growth rate.
'''