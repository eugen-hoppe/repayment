from datetime import datetime

from src.core import Repayment
from src.report import PDF


repayment_schedule = Repayment(
    start_date=datetime(2024, 8, 1),
    initial_balance=-5000.0,
    interest_rate=0.0345,
    monthly_installment=30.0,
)


if __name__ == "__main__":
    repayment_schedule.generate_schedule()
    PDF.generate_repayment(repayment_schedule, "repayment_en.pdf")
    PDF.generate_repayment(repayment_schedule, "repayment_de.pdf", language="DE")
