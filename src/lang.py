LANGUAGES = {
    "EN": {
        "title": "Repayment Plan",
        "payment_date": "Payment Date",
        "loan_amount": "Loan Amount",
        "interest_rate": "Interest Rate",
        "interest_rate_effective": "Interest Rate (Effective)",
        "installment": "Installment",
        "id": "ID",
        "date": "Date",
        "balance": "Balance",
        "principal": "Principal",
        "interest": "Interest",
        "total": "Total",
    },
    "DE": {
        "title": "Tilgungsplan",
        "payment_date": "Auszahlungsdatum",
        "loan_amount": "Darlehensbetrag",
        "interest_rate": "Nom. Zinssatz",
        "interest_rate_effective": "Eff. Zinssatz",
        "installment": "Ratenzahlung",
        "id": "ID",
        "date": "Datum",
        "balance": "Restschuld",
        "principal": "Tilgung",
        "interest": "Zinsen",
        "total": "Gesamt",
    },
}


def format_number(value, language="EN"):
    if language == "DE":
        formatted_value = (
            f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
    else:
        formatted_value = f"{value:,.2f}"
    return formatted_value
