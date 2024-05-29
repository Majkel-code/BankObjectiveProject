import os
from datetime import date, datetime

from users.credits.credit_construkt import CreditConstruct
from users.credits.credit_reader import CreditReader
from users.user_authorization.user_reader import UsersReader


class CreditMaker(CreditConstruct):
    def __init__(self) -> None:
        """
        Initializes a new instance of the CreditMaker class.

        This constructor sets up the necessary attributes for the CreditMaker class. It initializes the following attributes:
        - `credit_income_info`: A dictionary containing information about a credit income. It has the following keys:
            - "FROM_ACC": The account number from which the credit income originates.
            - "SENDER": The sender of the credit income.
            - "TO_ACC": The account number to which the credit income is sent.
            - "RECEIVER": The receiver of the credit income.
            - "AMOUNT": The amount of the credit income.
            - "DATE": The date of the credit income.
            - "TIME": The time of the credit income.
            - "TITLE": The title of the credit income.
            - "DESC": The description of the credit income.

        Parameters:
        - None

        Returns:
        - None
        """
        super().__init__()
        self.credit_income_info = {
            "FROM_ACC": "9999 9999 9999 9999",
            "SENDER": "CORONA BANK S.A",
            "TO_ACC": None,
            "RECEIVER": None,
            "AMOUNT": None,
            "DATE": None,
            "TIME": None,
            "TITLE": "POZYCZKA GOTOWKOWA",
            "DESC": "Wszelkie informacje dostepne na naszej infolini lub w panelu urzytkownika",
        }

    def take_current_time(self):
        """
        Returns the current time in the format "%H:%M:%S".
            :return: The current time as a string.

        """
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        return current_time

    def take_credit_dates(self, credit_months: int):
        """
        Function returns the current date and the date after a specified number of months.

        Args:
            credit_months (int): Number of months to add to the current date.

        Returns:
            list: Pair of dates [current, future].
        """

        # Get the current date
        current_date = date.today()
        end_date = date(
            current_date.year + (current_date.month + credit_months - 1) // 12,
            (current_date.month + credit_months - 1) % 12 + 1,
            current_date.day,
        )

        return [current_date, end_date]

    def calculate_months_between_dates(self, start_date: str, end_date: str):
        """
        Function to calculate the number of months between two dates.

        Args:
            start_date: A datetime object representing the start date.
            end_date: A datetime object representing the end date.

        Returns:
            The difference in months between the two dates as an int.
        """
        start_data_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        start_year = start_data_obj.year
        start_month = start_data_obj.month
        end_year = end_date_obj.year
        end_month = end_date_obj.month

        year_difference = end_year - start_year
        month_difference = end_month - start_month

        if month_difference < 0:
            year_difference -= 1
            month_difference += 12

        return year_difference * 12 + month_difference

    def calculate_loan(self, interest_rate, loan_amount, loan_term):
        """
        Calculates the loan, interest, and total repayment amount.

        Args:
            interest_rate: Monthly interest rate (in percent).
            loan_amount: Loan amount (in PLN).
            loan_term: Loan term in months.

        Returns:
            total_interest: Total interest to be paid (in PLN).
            actual_apr: Actual Annual Percentage Rate (APR) (in percent).
            total_repayment: Total amount to be repaid (in PLN).
            monthly_payment: Monthly payment amount (in PLN).
            schedule: List of monthly_payment
        """

        # Monthly payment
        monthly_payment = (
            loan_amount
            * (interest_rate * (1 + interest_rate) ** loan_term)
            / ((1 + interest_rate) ** loan_term - 1)
        )

        # Total interest
        total_interest = monthly_payment * loan_term - loan_amount

        # Actual Annual Percentage Rate (APR)
        actual_apr = (total_interest / loan_amount) / (loan_term / 12) * 100

        # Total amount to be repaid
        total_repayment = loan_amount + total_interest

        schedule = []
        for month in range(loan_term):
            schedule.append(round(monthly_payment, 2))
        rates_sum = sum(schedule)
        if rates_sum < total_repayment:
            last_rate = total_repayment - rates_sum
            schedule[-1] = round(schedule[-1] + last_rate, 2)

        return (
            round(total_interest, 2),
            round(actual_apr, 2),
            round(total_repayment, 2),
            round(monthly_payment, 2),
            schedule,
        )

    def recalculate_loan(self, schedule, amount, start_month: str, end_month: str, actual_amount):
        """
        Recalculates the loan after a prepayment.

        Args:
            schedule: List of monthly_payment.
            amount: Prepayment amount (in PLN).
            start_month: credit start date. Y-M-D.
            end_month: credit end date. Y-M-D.
            actual_amount: Actual loan amount.

        Returns:
            schedule: List of left monthly_payment.
            months_left: loan months left
            actual_amount: Actual loan amount after excess payment
        """
        months_left = self.calculate_months_between_dates(start_month, end_month)
        if not isinstance(schedule, list):
            raise TypeError("Schedule must be a list and amount must be a float.")
        if isinstance(amount, int) or isinstance(amount, float):
            if len(schedule) == 0:
                raise ValueError("Schedule cannot be empty.")

            if amount < 0:
                raise ValueError("Amount cannot be less than zero.")

            for i in range(len(schedule) - 1, -1, -1):
                if schedule[i] < amount:
                    amount -= schedule[i]
                    actual_amount -= schedule[i]
                    del schedule[i]
                    months_left -= 1

            if amount > 0 and len(schedule) > 0:
                schedule[-1] -= amount
                schedule[-1] = round(schedule[-1], 2)
                actual_amount -= amount

            return schedule, months_left, round(actual_amount, 2)

    def send_credit_income(self, id, user, amount):
        """
        Sends credit income to a user.

        Args:
            id (int): The ID of the user.
            user (dict): The user information.
            amount (float): The amount of credit income.

        Returns:
            dict: The result of adding the credit amount to the user's account.
        """
        self.credit_income_info["TO_ACC"] = user["DATA"]["ACC_NUM"]
        self.credit_income_info["RECEIVER"] = f'{user["DATA"]["NAME"]} {user["DATA"]["L_NAME"]}'
        self.credit_income_info["AMOUNT"] = amount
        self.credit_income_info["DATE"] = self.credit_struc["START_DATE"]
        self.credit_income_info["TIME"] = self.take_current_time()
        data = self.credit_income_info
        return self.add_credit_amount_to_account(id, data)

    def send_credit_outcome(self, id, data):
        """
        Sends the credit outcome to the user with the given ID.

        Args:
            id (int): The ID of the user.
            data (dict): The data containing the credit outcome information.

        Returns:
            The result of calculating the excess credit for the user.
        """
        return self.calculate_excess_credit(id, data)

    def setup_credit_calculation(
        self, excess_amount: int = None, operation: str = "REGULAR", **kwargs
    ):
        """
        Sets up the credit calculation based on the provided parameters.

        Args:
            excess_amount (int, optional): The excess amount to be recalculated. Defaults to None.
            operation (str, optional): The type of operation. Defaults to "REGULAR".
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The result of the credit calculation.

                - "STATUS" (bool): Indicates whether the operation was successful.
                - "ERROR" (str or None): If the operation was not successful, this key contains an error message. Otherwise, it is None.
                - "DATA" (str or None): If the operation was not successful, this key contains an error message. Otherwise, it is None.

        Raises:
            Exception: If there is an error while saving the credit.
        """
        credit_config = self.load_credit_config()
        interest_rate = credit_config["RRSO"] / 12 / 100
        if operation == "REGULAR":
            (
                total_interest,
                actual_apr,
                total_repayment,
                monthly_payment,
                schedule,
            ) = self.calculate_loan(interest_rate, kwargs["credit"], kwargs["months"])
            user_data = UsersReader().take_user_data(kwargs["id"])
            if user_data["STATUS"]:
                if not CreditReader().return_credit_data(kwargs["id"])["STATUS"]:
                    self.credit_struc["ID"] = kwargs["id"]
                    self.credit_struc["NAME"] = user_data["DATA"]["NAME"]
                    self.credit_struc["L_NAME"] = user_data["DATA"]["L_NAME"]
                    self.credit_struc["START_DATE"] = self.take_credit_dates(kwargs["months"])[
                        0
                    ].strftime("%Y-%m-%d")
                    self.credit_struc["CREDIT_AMOUNT"] = total_repayment
                    self.credit_struc["CREDIT_MONTHLY"] = monthly_payment
                    self.credit_struc["CREDIT_INTEREST"] = total_interest
                    self.credit_struc["END_DATE"] = self.take_credit_dates(kwargs["months"])[
                        1
                    ].strftime("%Y-%m-%d")
                    self.credit_struc["SCHEDULE"] = schedule

                    if os.path.exists(f"{self.credit_path}/{kwargs['id']}.json"):
                        return {"STATUS": False, "ERROR": "You have active credit!", "DATA": None}
                    else:
                        try:
                            self.credit_file["credits"].append(self.credit_struc)
                            if self.create_credit_file(id=kwargs["id"])["STATUS"]:
                                return self.send_credit_income(
                                    id=kwargs["id"], user=user_data, amount=kwargs["credit"]
                                )
                        except Exception as e:
                            print(e)
                            return {"STATUS": False, "ERROR": "Unabe to save credit!", "DATA": e}

        elif operation == "EXCESS":
            user_id = UsersReader().find_id(kwargs["from_acc"])["DATA"]
            take_credit_data = CreditReader().return_credit_data(user_id)
            user_data = UsersReader().take_user_data(user_id)
            if take_credit_data["STATUS"] and user_data["STATUS"]:
                print(take_credit_data["DATA"]["credits"][0]["START_DATE"])

                updated_schedule, months_left, left_amount = self.recalculate_loan(
                    schedule=take_credit_data["DATA"]["credits"][0]["SCHEDULE"],
                    amount=excess_amount,
                    start_month=take_credit_data["DATA"]["credits"][0]["START_DATE"],
                    end_month=take_credit_data["DATA"]["credits"][0]["END_DATE"],
                    actual_amount=take_credit_data["DATA"]["credits"][0]["CREDIT_AMOUNT"],
                )

                self.credit_struc["ID"] = user_id
                self.credit_struc["NAME"] = user_data["DATA"]["NAME"]
                self.credit_struc["L_NAME"] = user_data["DATA"]["L_NAME"]
                self.credit_struc["START_DATE"] = self.take_credit_dates(months_left)[0].strftime(
                    "%Y-%m-%d"
                )
                self.credit_struc["CREDIT_AMOUNT"] = left_amount
                self.credit_struc["CREDIT_MONTHLY"] = take_credit_data["DATA"]["credits"][0][
                    "CREDIT_MONTHLY"
                ]
                self.credit_struc["CREDIT_INTEREST"] = take_credit_data["DATA"]["credits"][0][
                    "CREDIT_INTEREST"
                ]
                self.credit_struc["END_DATE"] = self.take_credit_dates(months_left)[1].strftime(
                    "%Y-%m-%d"
                )
                self.credit_struc["SCHEDULE"] = updated_schedule
                try:
                    self.credit_file["credits"].append(self.credit_struc)
                    if self.edit_credit_file(user_id)["STATUS"]:
                        return self.send_credit_outcome(id=user_id, data=kwargs)
                except Exception as e:
                    return {"STATUS": False, "ERROR": "Unabe to save credit!", "DATA": e}
            else:
                return {"STATUS": False, "ERROR": "Unabe to excess credit!"}
