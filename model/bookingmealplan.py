class BookingMealPlan:
    def __init__(self, PackageId, PackageName, PackagePrice, PackageType):
        self.PackageId = PackageId
        self.PackageName = PackageName
        self.PackagePrice = PackagePrice
        self.PackageType = PackageType

    def to_dict(mealplan):
        return {
            "PackageId": mealplan.PackageId,
            "PackageName": mealplan.PackageName,
            "PackagePrice": mealplan.PackagePrice,
            "PackageType": mealplan.PackageType
        }

    def from_dict(mealplan):
        return BookingMealPlan(
            PackageId=mealplan.get("PackageId"),
            PackageName=mealplan.get("PackageName"),
            PackagePrice=mealplan.get("PackagePrice"),
            PackageType=mealplan.get("PackageType")
        )
