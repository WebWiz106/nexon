class DashboardMealPlan:
    def __init__(self, hId, ndid, planId, packageName,packageDesc,packagePrice,packageImage,planStart,planEnd,isPerRoom,planCreatedAt):
        self.hId = hId
        self.ndid = ndid
        self.planId = planId
        self.packageName = packageName
        self.packageDesc = packageDesc
        self.packagePrice = packagePrice
        self.packageImage =packageImage
        self.planStart = planStart
        self.planEnd = planEnd
        self.isPerRoom = isPerRoom=="true"
        self.planCreatedAt = planCreatedAt


    def to_dict(mealplan):
        return {
            "hId": mealplan.hId,
            "ndid": mealplan.ndid,
            "planId": mealplan.planId,
            "packageName": mealplan.packageName,
            "packageDesc": mealplan.packageDesc,
            "packagePrice": mealplan.packagePrice,
            "packageImage": mealplan.packageImage,
            "planStart": mealplan.planStart,
            "planEnd": mealplan.planEnd,
            "isPerRoom": mealplan.isPerRoom,
            "planCreatedAt": mealplan.planCreatedAt
        }

    def from_dict(mealplan):
        return DashboardMealPlan(
            hId=mealplan.get("hId"),
            ndid=mealplan.get("ndid"),
            planId=mealplan.get("planId"),
            packageName=mealplan.get("packageName"),
            packageDesc=mealplan.get("packageDesc"),
            packagePrice=mealplan.get("packagePrice"),
            packageImage=mealplan.get("packageImage"),
            planStart=mealplan.get("planStart"),
            planEnd=mealplan.get("planEnd"),
            isPerRoom=mealplan.get("isPerRoom"),
            planCreatedAt=mealplan.get("planCreatedAt")
        )
