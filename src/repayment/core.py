from dataclasses import dataclass, field
from datetime import datetime
from dateutil.relativedelta import relativedelta

import numpy_financial as npf


@dataclass
class Transaction:
    month_id: int = 0
    principal: float = 0.0
    interest: float = 0.0
    installment: float = 0.0

    def round(self, precision: int = 2):
        self.principal = round(self.principal, precision)
        self.interest = round(self.interest, precision)
        self.installment = round(self.installment, precision)

    def data(self) -> tuple[int, float, float, float]:
        return (self.month_id, self.principal, self.interest, self.installment)

    @staticmethod
    def default_next_month_date(date: datetime) -> datetime:
        if date.day > 28:
            date = datetime(year=date.year, month=date.month, day=28)
        return date + relativedelta(months=1)

    @staticmethod
    def pivot(items: list["Month | Quarter | Year"]):
        tr = Transaction()
        for item in items:
            data = item.tr.data() if isinstance(item, Month) else item.pivot()
            month_id, principal, interest, installment = data
            tr.month_id = month_id
            tr.principal += principal
            tr.interest += interest
            tr.installment += installment
        tr.round()
        return tr.data()


@dataclass
class Month:
    monthly_interest_rate: float
    next_installment: float
    date: datetime
    balance: float
    tr: Transaction = field(default_factory=Transaction)
    next_month: "Month | None" = None
    prev_month: "Month | None" = None
    next_date: callable = Transaction.default_next_month_date

    def __post_init__(self):
        self.update_month()

    def update_month(self):
        if self.tr.month_id == 0:
            self.balance = round(self.balance, 2)
        else:
            self.tr.interest = round(abs(self.balance) * self.monthly_interest_rate, 2)
            if abs(self.balance) + self.tr.interest <= self.next_installment:
                self.tr.principal = -self.balance
                self.balance = 0
            else:
                self.tr.principal = max(
                    0, self.next_installment - round(self.tr.interest, 2)
                )
                self.balance += self.tr.principal
            self.balance = round(self.balance, 2)
            self.tr.installment = self.tr.interest + self.tr.principal

    def create_next_month(self):
        if self.balance == 0:
            return None
        tr = Transaction(
            month_id=self.tr.month_id + 1,
            principal=self.tr.principal,
            interest=self.tr.interest,
            installment=self.tr.installment,
        )
        next_month_date = self.next_date(self.date)
        return Month(
            monthly_interest_rate=self.monthly_interest_rate,
            next_installment=self.next_installment,
            date=next_month_date,
            balance=self.balance,
            tr=tr,
            prev_month=self,
        )


@dataclass
class Quarter:
    quarter: int
    m1: Month | None = None
    m2: Month | None = None
    m3: Month | None = None
    month_list: list[Month] = field(default_factory=list)

    def add_month(self, month: Month):
        self.month_list.append(month)

    def pivot(self):
        return Transaction.pivot(self.month_list)


@dataclass
class Year:
    year: int
    q1: Quarter = field(default_factory=lambda: Quarter(1))
    q2: Quarter = field(default_factory=lambda: Quarter(2))
    q3: Quarter = field(default_factory=lambda: Quarter(3))
    q4: Quarter = field(default_factory=lambda: Quarter(4))
    quarter_list: list[Quarter] = field(default_factory=list)

    def add_month(self, month: Month):
        quarter_number = (month.date.month - 1) // 3 + 1
        month_in_quarter = (month.date.month - 1) % 3 + 1
        quarter: Quarter = getattr(self, f"q{quarter_number}")

        if month_in_quarter == 1:
            quarter.m1 = month
        elif month_in_quarter == 2:
            quarter.m2 = month
        elif month_in_quarter == 3:
            quarter.m3 = month
        else:
            raise ValueError("Invalid month in quarter")

        if quarter not in self.quarter_list:
            self.quarter_list.append(quarter)

        quarter.add_month(month)

    def pivot(self):
        return Transaction.pivot(self.quarter_list)


@dataclass
class Repayment:
    interest_rate: float
    monthly_installment: float
    initial_balance: float
    start_date: datetime
    years: list[Year] = field(default_factory=list)
    cache: dict = field(default_factory=dict)
    max_interest_installment_ratio: float = 0.90
    effective_interest_rate: float | None = None

    def __post_init__(self):
        monthly_interest = self.interest_rate * -self.initial_balance / 12
        interest_installment_ratio = monthly_interest / self.monthly_installment

        # Log 1.a
        log_post_init = dict()
        log_post_init["interest_installment_ratio"] = interest_installment_ratio
        log_post_init["monthly_installment"] = self.monthly_installment
        # -------

        if interest_installment_ratio > self.max_interest_installment_ratio:
            self.monthly_installment = round(
                (1.0 + monthly_interest) / self.max_interest_installment_ratio
            )

            # Log 1.b
            log_post_init["max_ii_ratio"] = self.max_interest_installment_ratio
            log_post_init["new_ii_ratio"] = monthly_interest / self.monthly_installment
            log_post_init["valid_m_installment"] = self.monthly_installment
            # -------

        self.cache["log__Repayment"] = {"__post_init__": log_post_init}  # Log 1

    def calculate_effective_interest_rate(self):
        cash_flows = []
        cash_flows.append(self.initial_balance)
        for year in self.years:
            for quarter in year.quarter_list:
                for month in quarter.month_list:
                    cash_flows.append(month.tr.installment)
        irr = npf.irr(cash_flows)
        effective_interest_rate = (1 + irr) ** 12 - 1
        return effective_interest_rate

    def add_month(self, month: Month):
        year_number = month.date.year
        year = next((y for y in self.years if y.year == year_number), None)
        if not year:
            year = Year(year=year_number)
            self.years.append(year)
        year.add_month(month)

    def generate_schedule(self):
        current_month = Month(
            monthly_interest_rate=self.interest_rate / 12,
            next_installment=self.monthly_installment,
            date=self.start_date,
            balance=self.initial_balance,
        )
        while current_month:
            self.add_month(current_month)
            current_month = current_month.create_next_month()
        self.effective_interest_rate = self.calculate_effective_interest_rate()

    def pivot(self):
        return Transaction.pivot(self.years)
