import yahoo_fin.stock_info as si
import pandas as pd
import CustomExceptions as ce

def get_val_table(ticker):
    val = si.get_stats_valuation(ticker)
    val = val.iloc[:, :2]
    val.columns = ["Attribute", "Recent"]
    return val

def get_beta(ticker):
    " Beta is the measure of the vulnerability \
    of the company by the market "

    try:
        quote = si.get_quote_table(ticker)
        res = float(quote["Beta (5Y Monthly)"])
        if pd.isna(res):
            raise ce.ValueIsNotPresent()
    except ce.ValueIsNotPresent:
        return "Value is not found!"
    else:
        return res

def get_eps(ticker):
    " Earnings per share of 12 month"

    try:
        quote = si.get_quote_table(ticker)
        res = float(quote["EPS (TTM)"])
        if pd.isna(res):
            raise ce.ValueIsNotPresent()
    except ce.ValueIsNotPresent:
        return "Value is not found!"
    else:
        return res

def get_market_cap(ticker):
    " Market capitalization in thousands "

    try:
        quote = si.get_quote_table(ticker)
        res = float(quote['Market Cap'][:-1])
        if pd.isna(res):
            raise ce.ValueIsNotPresent()
    except ce.ValueIsNotPresent:
        return "Value is not found!"
    else:
        return res * 1e+9

def get_enterprise_value(ticker):
    " The real price of the company in thousands"
    try:
        val = get_val_table(ticker)
        res = float(val[val.Attribute.
                        str.contains("Enterprise Value")].iloc[0, 1][:-1])
        if pd.isna(res):
            raise ce.ValueIsNotPresent()
    except ce.ValueIsNotPresent:
        return "Value is not found!"
    else:
        return res * 1e+9

def get_trailing_PE(ticker):
    " Trailing P/E is calculated by dividing the \
    current market value, or share price, by the \
    earnings per share over the previous 12 months. "

    try:
        val = get_val_table(ticker)
        res = float(val[val.Attribute.
                    str.contains("Trailing P/E")].iloc[0, 1])
        if pd.isna(res):
            raise ce.ValueIsNotPresent()
    except ce.ValueIsNotPresent:
        return "Value is not found!"
    else:
        return res

def get_forward_PE(ticker):
    " The forward P/E ratio estimates a company's \
    likely earnings per share for the next 12 months."

    try:
        val = get_val_table(ticker)
        res = float(val[val.Attribute.
                        str.contains("Forward P/E")].iloc[0, 1])
        if pd.isna(res):
            raise ce.ValueIsNotPresent()
    except ce.ValueIsNotPresent:
        return "Value is not found!"
    else:
        return res

def get_PEG_ratio(ticker):
    " The PEG ratio is a company's Price/Earnings \
    ratio divided by its earnings growth rate over \
    a period of time (5 years expected)"

    try:
        val = get_val_table(ticker)
        res = float(val[val.Attribute.
                        str.contains("PEG Ratio")].iloc[0, 1])
        if pd.isna(res):
            raise ce.ValueIsNotPresent()
    except ce.ValueIsNotPresent:
        return "Value is not found!"
    else:
        return res

def get_price_to_sales(ticker):
    " The price-to-sales ratio shows how much the \
    market values every dollar of the company's sales "

    try:
        val = get_val_table(ticker)
        res = float(val[val.Attribute.
                        str.contains("Price/Sales")].iloc[0, 1])
        if pd.isna(res):
            raise ce.ValueIsNotPresent()
    except ce.ValueIsNotPresent:
        return "Value is not found!"
    else:
        return res

def get_price_to_book(ticker):
    " A P/B ratio analysis is an important \
    part of an overall value investing approach. "

    try:
        val = get_val_table(ticker)
        res = float(val[val.Attribute.
                        str.contains("Price/Book")].iloc[0, 1])
        if pd.isna(res):
            raise ce.ValueIsNotPresent()
    except ce.ValueIsNotPresent:
        return "Value is not found!"
    else:
        return res

def get_EV_by_EBITDA(ticker):
    " Just like the P/E ratio (price-to-earnings), the lower \
    the EV/EBITDA, the cheaper the valuation for a company. "

    try:
        val = get_val_table(ticker)
        res = float(val[val.Attribute.
                        str.contains("Enterprise Value/Revenue")].iloc[0, 1])
        if pd.isna(res):
            raise ce.ValueIsNotPresent()
    except ce.ValueIsNotPresent:
        return "Value is not found!"
    else:
        return res

def get_EV_by_Revenue(ticker):
    " The lower the better, in that, a lower EV/R \
    multiple signals a company is undervalued "

    try:
        val = get_val_table(ticker)
        res = float(val[val.Attribute.
                        str.contains("Enterprise Value/EBITDA")].iloc[0, 1])
        if pd.isna(res):
            raise ce.ValueIsNotPresent()
    except ce.ValueIsNotPresent:
        return "Value is not found!"
    else:
        return res

# TODO: Find all the formulas