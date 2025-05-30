class BookingPackage:
    def __init__(self, packageId, packageName, packagePrice, specialRequest):
        self.packageId = packageId
        self.packageName = packageName
        self.packagePrice = packagePrice
        self.specialRequest = specialRequest

    def to_dict(package):
        return {
            "packageId": package.packageId,
            "packageName": package.packageName,
            "packagePrice": package.packagePrice,
            "specialRequest": package.specialRequest
        }

    def from_dict(package_dict):
        return BookingPackage(
            packageId=package_dict.get("packageId"),
            packageName=package_dict.get("packageName"),
            packagePrice=package_dict.get("packagePrice"),
            specialRequest=package_dict.get("specialRequest")
        )
