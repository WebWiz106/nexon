from model.roomFacilities import RoomFacility
from model.changedprice import ChangedPrice

class Room:
    def __init__(self, hId, ndid, roomType, roomName, roomDescription, roomSubheading, child, adult, noOfRooms, roomTypeName, price, isWeekendFormat, changedPrice, roomImage,roomFacilities,roomNumbers,inMaintanance,roomTag):
        self.hId = hId
        self.ndid = ndid
        self.roomType = roomType
        self.roomName = roomName
        self.roomDescription = roomDescription
        self.roomSubheading = roomSubheading
        self.child = child
        self.adult = adult
        self.noOfRooms = noOfRooms
        self.roomTypeName = roomTypeName
        self.price = price
        self.isWeekendFormat = isWeekendFormat
        self.changedPrice = changedPrice
        self.roomImage = roomImage
        self.roomFacilities = roomFacilities
        self.roomNumbers = roomNumbers
        self.inMaintanance = inMaintanance
        self.roomTag = roomTag

    def to_dict(room):
        return {
            "hId": room.hId,
            "ndid": room.ndid,
            "roomType": room.roomType,
            "roomName": room.roomName,
            "roomDescription": room.roomDescription,
            "roomSubheading": room.roomSubheading,
            "child": room.child,
            "adult": room.adult,
            "noOfRooms": room.noOfRooms,
            "roomTypeName": room.roomTypeName,
            "price": room.price,
            "isWeekendFormat": room.isWeekendFormat=="true",
            "changedPrice": ChangedPrice.to_dict(room.changedPrice),
            "roomImage": room.roomImage,
            "roomFacilities": RoomFacility.to_dict(room.roomFacilities),
            "roomNumbers":room.roomNumbers,
            "inMaintanance":room.inMaintanance,
            "roomTag":room.roomTag
        }

    def from_dict(room):
        return Room(
            hId=room.get("hId"),
            ndid=room.get("ndid"),
            roomType=room.get("roomType"),
            roomName=room.get("roomName"),
            roomDescription=room.get("roomDescription"),
            roomSubheading=room.get("roomSubheading"),
            child=room.get("child"),
            adult=room.get("adult"),
            noOfRooms=room.get("noOfRooms"),
            roomTypeName=room.get("roomTypeName"),
            price=room.get("price"),
            isWeekendFormat=room.get("isWeekendFormat"),
            changedPrice=ChangedPrice.from_dict(room.get("changedPrice")),
            roomImage=room.get("roomImage"),
            roomFacilities=RoomFacility.from_dict(room.get("roomFacilities")),
            roomNumbers = room.get("roomNumbers",[]),
            inMaintanance = room.get("inMaintanance",[]),
            roomTag = room.get("roomTag","")
        )
