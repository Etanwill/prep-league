

from collections import defaultdict


class Bank:
    def __init__(self):
        self.account = defaultdict(list)
        self.outgoing = defaultdict(int)
        self.payments = {}
        self.payment_counter = 0
        self.balance_history = defaultdict(list)
        # Store the timestamp when an account was merged away.
        self.merged_at = {}


    def _process_payments(self, timestamp):
            # Process due payments in due-time order,
            # then payment-number order.
            due_payments = sorted(
                [
                    payment
                    for payment in self.payments.values()
                    if payment["status"] == "pending"
                    and payment["due_time"] <= timestamp
                ],
                key=lambda p: (p["due_time"], p["number"])
            )
    
            for payment in due_payments:
                account_id = payment["account_id"]
                amount = payment["amount"]
    
                # The account must exist and have enough money.
                if (
                    account_id in self.account
                    and self.account[account_id][0] >= amount
                ):
                    self.account[account_id][0] -= amount
                    self.outgoing[account_id] += amount
                    payment["status"] = "executed"
                else:
                    payment["status"] = "skipped"

    def _record_balance(self, timestamp, account_id):
        balance = self.account[account_id][0]
        self.balance_history[account_id].append(
            (timestamp, balance)
        )
    

    def create_account(self, timestamp, account_id) -> bool:
        self._process_payments(timestamp)
        if account_id in self.account:
            return False
        self.account[account_id] = [0, timestamp]
        return True

    def deposit(self, timestamp, account_id, amount) -> int | None:
        self._process_payments(timestamp)
        if account_id not in self.account:
            return None
        self.account[account_id][0] += amount
        return self.account[account_id][0]

    def transfer(self, timestamp, source_id, target_id, amount) -> int | None:
        self._process_payments(timestamp)
        if source_id not in self.account or target_id not in self.account:
            return None
        if source_id == target_id or self.account[source_id][0] < amount:
            return None
        self.account[source_id][0] -= amount
        self.account[target_id][0] += amount
        self.outgoing[source_id] += amount
        return self.account[target_id][0]

    def top_spenders(self,timestamp, n) -> list[str]:
        self._process_payments(timestamp)
        sorted_accounts = [f"{key}({val})" for key, val in sorted(self.outgoing.items(), key = lambda x: (x[1], x[0]), reverse=True)]
        return sorted_accounts[:n]

    

    def schedule_payment(
        self, timestamp, account_id, amount, delay
    ) -> str | None:
        self._process_payments(timestamp)

        if account_id not in self.account:
            return None

        self.payment_counter += 1
        payment_id = f"payment{self.payment_counter}"

        self.payments[payment_id] = {
            "id": payment_id,
            "number": self.payment_counter,
            "account_id": account_id,
            "amount": amount,
            "due_time": timestamp + delay,
            "status": "pending"
        }

        return payment_id

    def cancel_payment(
        self, timestamp, account_id, payment_id
    ) -> bool:
        self._process_payments(timestamp)

        if account_id not in self.account:
            return False

        if payment_id not in self.payments:
            return False

        payment = self.payments[payment_id]

        if payment["account_id"] != account_id:
            return False

        if payment["status"] != "pending":
            return False

        payment["status"] = "cancelled"
        return True

    def merge_accounts(
        self, timestamp, account_id_1, account_id_2
    ) -> bool:
        self._process_payments(timestamp)

        if (
            account_id_1 not in self.account
            or account_id_2 not in self.account
        ):
            return False

        if account_id_1 == account_id_2:
            return False

        # Add account 2's balance to account 1.
        self.account[account_id_1][0] += (
            self.account[account_id_2][0]
        )

        # Combine their outgoing totals.
        self.outgoing[account_id_1] += (
            self.outgoing[account_id_2]
        )

        # Transfer account 2's pending payments to account 1.
        for payment in self.payments.values():
            if (
                payment["account_id"] == account_id_2
                and payment["status"] == "pending"
            ):
                payment["account_id"] = account_id_1

        # Record account 1's balance immediately after merging.
        self._record_balance(timestamp, account_id_1)

        # Mark account 2 as merged and remove it from active accounts.
        self.merged_at[account_id_2] = timestamp
        del self.account[account_id_2]
        self.outgoing.pop(account_id_2, None)

        return True