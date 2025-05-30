class ChangedPrice:
    def __init__(self, weekend, weekday):
        self.weekend = weekend
        self.weekday = weekday

    def to_dict(room):
        return {
            "weekend": room.weekend,
            "weekday": room.weekday
        }

    def from_dict(changedprice):
        return ChangedPrice(
            weekend=changedprice.get("weekend"),
            weekday=changedprice.get("weekday")
        )
