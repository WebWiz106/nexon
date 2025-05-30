
class BookingItem:
    def __init__(self, roomType, qty):
        self.roomType = roomType
        self.qty = qty

    def to_dict(BookingItem):
        return {
            "RoomType": BookingItem.roomType,
            "Qty": BookingItem.qty
        }

    def from_dict(bookingItem_dict):
        return BookingItem(
            roomType=bookingItem_dict.get("RoomType"),
            qty=bookingItem_dict.get("Qty")
        )
