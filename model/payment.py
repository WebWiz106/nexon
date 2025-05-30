
class Payment:
    def __init__(self,refNo,paymentProvider,mode,status="PENDING",payId=None):
        self.refNo = refNo
        self.paymentProvider = paymentProvider
        self.mode = mode 
        self.status = status
        self.payId = payId

    def to_dict(Payment):
        return {
            "RefNo":Payment.refNo,
            "PaymentProvider":Payment.paymentProvider,
            "Mode":Payment.mode,
            "Status":Payment.status,
            "payId":Payment.payId
        }
    
    def from_dict(payment_dict):
        return Payment(
            refNo = payment_dict.get("RefNo"),
            paymentProvider = payment_dict.get("PaymentProvider"),
            mode = payment_dict.get("Mode"),
            status = payment_dict.get("Status"),
            payId = payment_dict.get("payId")
        )