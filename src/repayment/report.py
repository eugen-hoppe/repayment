from fpdf import FPDF, XPos, YPos
from datetime import datetime

from .core import Repayment
from .lang import LANGUAGES, format_number


FONT_FAMILY = "Roboto"
FONT_SIZE_TITLE = 12
FONT_SIZE_BODY = 8
FONT_SIZE_OVERVIEW = 10
CELL_HEIGHT = 3
CELL_HEIGHT_OVERVIEW = 5
HEADER_CELL_WIDTH = 30
SPACING_SMALL = 1
SPACING_MEDIUM = 3
SPACING_LARGE = 5
MARGIN_LEFT = 20
MARGIN_RIGHT = 10
MARGIN_TOP = 10
MARGIN_BOTTOM = 10
TB_BORDER = 0
DEFAULT_CURRENCY = ("Euro", "EUR", "€")
DEFAULT_LANGUAGE = "EN"


class PDF(FPDF):
    def __init__(self, language: str, currency: tuple[str, ...]):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=MARGIN_BOTTOM)
        self.set_margins(MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT)
        self.language = language
        self.texts = LANGUAGES[self.language]
        self.currency = currency[0]
        self.currency_sign = currency[-1]

        self.add_font(FONT_FAMILY, "", "src/fonts/Roboto-Regular.ttf")
        self.add_font(FONT_FAMILY, "B", "src/fonts/Roboto-Bold.ttf")

    def format_number(self, value) -> str:
        return format_number(value, self.language)

    def chapter_title(self, title):
        self.set_font(FONT_FAMILY, "B", FONT_SIZE_TITLE)
        self.cell(0, CELL_HEIGHT, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        self.ln(SPACING_SMALL)
        self.line(MARGIN_LEFT, self.get_y(), self.w - HEADER_CELL_WIDTH, self.get_y())
        self.ln(SPACING_SMALL)

    def chapter_total(self, total):
        self.set_font(FONT_FAMILY, "B", FONT_SIZE_BODY)
        self.cell(HEADER_CELL_WIDTH // 3, CELL_HEIGHT, "", 0, align="R")
        self.cell(HEADER_CELL_WIDTH, CELL_HEIGHT, "", 0, align="R")
        self.cell(HEADER_CELL_WIDTH, CELL_HEIGHT, "", 0, align="R")
        self.cell(
            HEADER_CELL_WIDTH,
            CELL_HEIGHT,
            f"{self.format_number(total[1])} {self.currency_sign}",
            TB_BORDER,
            align="R",
        )
        self.cell(
            HEADER_CELL_WIDTH,
            CELL_HEIGHT,
            f"{self.format_number(total[2])} {self.currency_sign}",
            TB_BORDER,
            align="R",
        )
        self.cell(
            HEADER_CELL_WIDTH,
            CELL_HEIGHT,
            f"{self.format_number(total[3])} {self.currency_sign}",
            TB_BORDER,
            align="R",
        )
        self.ln(SPACING_LARGE)

    def chapter_year_total(self, year_total):
        self.ln(SPACING_MEDIUM)
        self.line(
            MARGIN_LEFT + HEADER_CELL_WIDTH // 3 + HEADER_CELL_WIDTH,
            self.get_y(),
            self.w - HEADER_CELL_WIDTH,
            self.get_y(),
        )
        self.ln(SPACING_SMALL)
        self.set_font(FONT_FAMILY, "B", FONT_SIZE_BODY)
        self.cell(HEADER_CELL_WIDTH // 3, CELL_HEIGHT, "", 0, align="R")
        self.cell(HEADER_CELL_WIDTH, CELL_HEIGHT, "", 0, align="R")
        self.cell(
            HEADER_CELL_WIDTH,
            CELL_HEIGHT,
            f"{self.format_number(year_total[4])} {self.currency_sign}",
            0,
            align="R",
        )
        self.cell(
            HEADER_CELL_WIDTH,
            CELL_HEIGHT,
            f"{self.format_number(year_total[1])} {self.currency_sign}",
            TB_BORDER,
            align="R",
        )
        self.cell(
            HEADER_CELL_WIDTH,
            CELL_HEIGHT,
            f"{self.format_number(year_total[2])} {self.currency_sign}",
            TB_BORDER,
            align="R",
        )
        self.cell(
            HEADER_CELL_WIDTH,
            CELL_HEIGHT,
            f"{self.format_number(year_total[3])} {self.currency_sign}",
            TB_BORDER,
            align="R",
        )
        self.ln(SPACING_LARGE)

    def final_total(self, total):
        self.ln(SPACING_LARGE)
        for _ in range(0, 2):
            self.ln(SPACING_SMALL)
            self.line(
                MARGIN_LEFT + HEADER_CELL_WIDTH // 3 + HEADER_CELL_WIDTH,
                self.get_y(),
                self.w - HEADER_CELL_WIDTH,
                self.get_y(),
            )
        self.ln(SPACING_SMALL)
        self.set_font(FONT_FAMILY, "B", FONT_SIZE_BODY)
        self.cell(HEADER_CELL_WIDTH // 3, CELL_HEIGHT, "", 0, align="R")
        self.cell(HEADER_CELL_WIDTH, CELL_HEIGHT, "", 0, align="R")
        self.cell(HEADER_CELL_WIDTH, CELL_HEIGHT, "", 0, align="R")
        self.cell(
            HEADER_CELL_WIDTH,
            CELL_HEIGHT,
            f"{self.format_number(total[1])} {self.currency}",
            TB_BORDER,
            align="R",
        )
        self.cell(
            HEADER_CELL_WIDTH,
            CELL_HEIGHT,
            f"{self.format_number(total[2])} {self.currency}",
            TB_BORDER,
            align="R",
        )
        self.cell(
            HEADER_CELL_WIDTH,
            CELL_HEIGHT,
            f"{self.format_number(total[3])} {self.currency}",
            TB_BORDER,
            align="R",
        )
        self.ln(SPACING_MEDIUM)

    def overview(
        self,
        start_date: datetime,
        initial_balance: float,
        interest_rate: float,
        interest_rate_effective: float,
        next_installment: float,
    ):
        self.add_page()
        self.set_font(FONT_FAMILY, "B", FONT_SIZE_TITLE * 1.5)
        self.cell(
            0,
            CELL_HEIGHT_OVERVIEW,
            self.texts["title"],
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
            align="L",
        )
        self.ln(SPACING_MEDIUM)

        self.set_font(FONT_FAMILY, "", FONT_SIZE_OVERVIEW)

        headers = [
            self.texts["payment_date"],
            self.texts["loan_amount"],
            self.texts["interest_rate"],
            self.texts["interest_rate_effective"],
            self.texts["installment"],
        ]
        values = [
            (
                start_date.strftime("%Y-%m-%d")
                if self.language == "EN"
                else start_date.strftime("%d.%m.%Y")
            ),
            f"{self.format_number(abs(initial_balance))} {self.currency}",
            f"{self.format_number(interest_rate * 100)} %",
            f"{self.format_number(interest_rate_effective * 100)} %",
            f"{self.format_number(next_installment)} {self.currency}",
        ]

        col_width = HEADER_CELL_WIDTH // 3 + HEADER_CELL_WIDTH
        col_value_width = 50

        for header, value in zip(headers, values):
            self.cell(
                col_width,
                CELL_HEIGHT_OVERVIEW,
                f"{header}:",
                new_x=XPos.RIGHT,
                new_y=YPos.TOP,
                align="R",
            )
            self.cell(
                col_value_width,
                CELL_HEIGHT_OVERVIEW,
                value,
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
                align="L",
            )

        self.ln(SPACING_LARGE)

    def chapter_body(self, data):
        self.set_font(FONT_FAMILY, "", FONT_SIZE_BODY)
        for row in data:
            self.cell(
                HEADER_CELL_WIDTH // 3, CELL_HEIGHT, str(row[0]), TB_BORDER, align="R"
            )
            self.cell(HEADER_CELL_WIDTH, CELL_HEIGHT, str(row[5]), TB_BORDER, align="R")
            self.cell(
                HEADER_CELL_WIDTH,
                CELL_HEIGHT,
                f"{self.format_number(row[4])} {self.currency_sign}",
                TB_BORDER,
                align="R",
            )
            self.cell(
                HEADER_CELL_WIDTH,
                CELL_HEIGHT,
                f"{self.format_number(row[1])} {self.currency_sign}",
                TB_BORDER,
                align="R",
            )
            self.cell(
                HEADER_CELL_WIDTH,
                CELL_HEIGHT,
                f"{self.format_number(row[2])} {self.currency_sign}",
                TB_BORDER,
                align="R",
            )
            self.cell(
                HEADER_CELL_WIDTH,
                CELL_HEIGHT,
                f"{self.format_number(row[3]):} {self.currency_sign}",
                TB_BORDER,
                align="R",
            )
            self.ln()
        self.ln(SPACING_SMALL)

    @staticmethod
    def generate_repayment(
        repayment_schedule: Repayment,
        filename: str,
        language=DEFAULT_LANGUAGE,
        currency=DEFAULT_CURRENCY,
    ) -> None:

        pdf = PDF(language=language, currency=currency)
        pdf.overview(
            start_date=repayment_schedule.start_date,
            initial_balance=repayment_schedule.initial_balance,
            interest_rate=repayment_schedule.interest_rate,
            interest_rate_effective=repayment_schedule.effective_interest_rate,
            next_installment=repayment_schedule.monthly_installment,
        )
        total_principal = 0.0
        total_interest = 0.0
        total_installment = 0.0
        for year in repayment_schedule.years:
            num_rows = sum(len(quarter.month_list) for quarter in year.quarter_list)
            required_height = (
                (num_rows + len(year.quarter_list)) * CELL_HEIGHT
                + SPACING_SMALL * len(year.quarter_list)
                + SPACING_MEDIUM
            )

            if pdf.get_y() + required_height * 1.2 > pdf.h - MARGIN_BOTTOM:
                pdf.add_page()

            year_title = f"{year.year}"
            pdf.chapter_title(year_title)

            headers = [
                pdf.texts["id"],
                pdf.texts["date"],
                pdf.texts["balance"],
                pdf.texts["principal"],
                pdf.texts["interest"],
                pdf.texts["installment"],
            ]
            pdf.set_font(FONT_FAMILY, "B", FONT_SIZE_BODY)
            for header in headers:
                pdf.cell(
                    (
                        HEADER_CELL_WIDTH // 3
                        if header == headers[0]
                        else HEADER_CELL_WIDTH
                    ),
                    CELL_HEIGHT,
                    header,
                    TB_BORDER,
                    align="R",
                )
            pdf.ln()

            year_principal = 0.0
            year_interest = 0.0
            year_installment = 0.0

            for quarter in year.quarter_list:
                data = []
                for month in quarter.month_list:
                    data.append(
                        [
                            month.tr.month_id,
                            month.tr.principal,
                            month.tr.interest,
                            month.tr.installment,
                            month.balance,
                            (
                                month.date.strftime("%Y-%m-%d")
                                if language == "EN"
                                else month.date.strftime("%d.%m.%Y")
                            ),
                        ]
                    )
                pdf.chapter_body(data)

                quarter_pivot = quarter.pivot()
                total_principal += quarter_pivot[1]
                total_interest += quarter_pivot[2]
                total_installment += quarter_pivot[3]

                year_principal += quarter_pivot[1]
                year_interest += quarter_pivot[2]
                year_installment += quarter_pivot[3]

                pdf.chapter_total([*quarter_pivot, month.balance])

            year_total = (0, year_principal, year_interest, year_installment)
            pdf.chapter_year_total([*year_total, month.balance])
            pdf.ln(SPACING_LARGE)

        final_total = (0, total_principal, total_interest, total_installment)
        pdf.final_total([*final_total, month.balance])

        pdf.output(filename)
