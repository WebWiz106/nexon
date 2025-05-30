class PromoCode:
    # "promo", {"PromoId": "NA", "Code": "NA", "Discount": "NA"}),
    def __init__(self, PromoId, Code, Discount):
        self.PromoId = PromoId
        self.Code = Code
        self.Discount = Discount

    def to_dict(promocode):
        return {
            "PromoId": promocode.PromoId,
            "Code": promocode.Code,
            "Discount": promocode.Discount
        }

    def from_dict(package_dict):
        return PromoCode(
            PromoId=package_dict.get("PromoId"),
            Code=package_dict.get("Code"),
            Discount=package_dict.get("Discount")
        )
