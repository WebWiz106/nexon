
class Price:
    def __init__(self,principal,tax,total,amountPay=0):
        self.principal = principal
        self.tax = tax # private variable
        self.total = total
        self.amountPay=amountPay

    def to_dict(Price):
        return {
            "Principal":Price.principal,
            "Tax":Price.tax,
            "Total":Price.total,
            "amountPay":Price.amountPay
        }

    def from_dict(price_dict):
        return Price(
            principal=price_dict.get("Principal"),
            tax=price_dict.get("Tax"),
            total=price_dict.get("Total"),
            amountPay=price_dict.get("amountPay"))