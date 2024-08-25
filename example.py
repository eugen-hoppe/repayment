from datetime import datetime

from src.repayment.core import Repayment
from src.repayment.report import PDF


FONTS = "src/repayment/fonts"


repayment = Repayment(
    start_date=datetime(2024, 8, 1),
    initial_balance=-5000.0,
    interest_rate=0.0345,
    monthly_installment=30.0,
)


if __name__ == "__main__":
    repayment.generate_schedule()
    PDF.generate_repayment(repayment, "repayment_en.pdf", fonts_path=FONTS)
    PDF.generate_repayment(
        repayment, "repayment_de.pdf", language="DE", fonts_path=FONTS
    )
    repayment.display_year(0)
    repayment.display_year(1)
    repayment.display_year(-1)
