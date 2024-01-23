
import datetime

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  
    WHITE = 4 

def latest_financial_index(data: dict):
    financials = data.get("data", {}).get("financials")
    if financials is not None:
        for index, financial in enumerate(financials):
            if financial.get("nature") == "STANDALONE":
                return index
    return 0

def total_revenue(data: dict, financial_index):
    financials = data.get("data", {}).get("financials")
    if financials is not None and 0 <= financial_index < len(financials):
        pnl_data = financials[financial_index].get("lineItems", {}).get("pnl", {})
        return pnl_data.get("netRevenue", 0)
    return 0


def total_borrowing(data: dict, financial_index):
    bs_data = data["financials"][financial_index]["lineItems"]["bs"]
    long_term_borrowings = bs_data.get("longTermBorrowings", 0)
    short_term_borrowings = bs_data.get("shortTermBorrowings", 0)
    total_borrowings = long_term_borrowings + short_term_borrowings

    total_rev = total_revenue(data, financial_index)
    return total_borrowings / total_rev if total_rev != 0 else 0

def iscr(data: dict, financial_index):
    pnl_data = data["financials"][financial_index]["lineItems"]["pnl"]
    interest_expenses = pnl_data.get("interestExpenses", 0)
    profit_before_tax = pnl_data.get("profitBeforeTax", 0)
    depreciation = pnl_data.get("depreciation", 0)

    return (profit_before_tax + depreciation + 1) / (interest_expenses + 1)

def iscr_flag(data: dict, financial_index):
    iscr_value = iscr(data, financial_index)
    return FLAGS.GREEN if iscr_value >= 2 else FLAGS.RED

def total_revenue_5cr_flag(data: dict, financial_index):
    total_rev = total_revenue(data, financial_index)
    return FLAGS.GREEN if total_rev >= 50000000 else FLAGS.RED

def borrowing_to_revenue_flag(data: dict, financial_index):
    borrowing_to_rev_ratio = total_borrowing(data, financial_index)
    return FLAGS.GREEN if borrowing_to_rev_ratio <= 0.25 else FLAGS.AMBER

