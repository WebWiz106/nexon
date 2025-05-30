class DashboardPackage:
    def __init__(self, ndid, hId, packageId, packageName, packageDesc, packageInclusion, packageItinerary, packageguests, NoofDays, NoofNight, packagePrice, packageImage, roomTypeProvided, packageStart, packageEnd, packageCreatedAt):
        self.ndid = ndid
        self.hId = hId
        self.packageId = packageId
        self.packageName = packageName
        self.packageDesc = packageDesc
        self.packageInclusion = packageInclusion
        self.packageItinerary = packageItinerary
        self.packageguests = packageguests
        self.NoofDays = NoofDays
        self.NoofNight = NoofNight
        self.packagePrice = packagePrice
        self.packageImage = packageImage
        self.roomTypeProvided = roomTypeProvided
        self.packageStart = packageStart
        self.packageEnd = packageEnd
        self.packageCreatedAt = packageCreatedAt

    def to_dict(package):
        return {
            "ndid": package.ndid,
            "hId": package.hId,
            "packageId": package.packageId,
            "packageName": package.packageName,
            "packageDesc": package.packageDesc,
            "packageId": package.packageId,
            "packageInclusion": package.packageInclusion,
            "packageItinerary": package.packageItinerary,
            "packageguests": package.packageguests,
            "NoofDays": package.NoofDays,
            "NoofNight": package.NoofNight,
            "packagePrice": package.packagePrice,
            "packageImage": package.packageImage,
            "roomTypeProvided": package.roomTypeProvided,
            "packageStart": package.packageStart,
            "packageEnd": package.packageEnd,
            "packageCreatedAt": package.packageCreatedAt

        }

    def from_dict(package_dict):
        return DashboardPackage(
            ndid=package_dict.get("ndid"),
            hId=package_dict.get("hId"),
            packageId=package_dict.get("packageId"),
            packageName=package_dict.get("packageName"),
            packageDesc=package_dict.get("packageDesc"),
            packageInclusion=package_dict.get("packageInclusion"),
            packageItinerary=package_dict.get("packageItinerary"),
            packageguests=package_dict.get("packageguests"),
            NoofDays=package_dict.get("NoofDays"),
            NoofNight=package_dict.get("NoofNight"),
            packagePrice=package_dict.get("packagePrice"),
            packageImage=package_dict.get("packageImage"),
            roomTypeProvided=package_dict.get("roomTypeProvided"),
            packageStart=package_dict.get("packageStart"),
            packageEnd=package_dict.get("packageEnd"),
            packageCreatedAt=package_dict.get("packageCreatedAt"),
        )
