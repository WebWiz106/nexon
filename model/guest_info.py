from model.country import Country
class GuestInfo:
    def __init__(self, guestName, emailId, phone, city, country, address=None):
        self.guestName = guestName
        self.emailId = emailId
        self.phone = phone
        self.city = city
        self.country = country
        self.address = address

    def to_dict(GuestInfo):
        return {
            "guestName": GuestInfo.guestName,
            "EmailId": GuestInfo.emailId,
            "Phone": GuestInfo.phone,
            "City": GuestInfo.city,
            "Country": Country.to_dict(GuestInfo.country),
            "address": GuestInfo.address
        }

    def from_dict(guestInfo_dict):
        return GuestInfo(
            guestName=guestInfo_dict.get("guestName"),
            emailId=guestInfo_dict.get("EmailId"),
            phone=guestInfo_dict.get("Phone"),
            city=guestInfo_dict.get("City"),
            country=Country.from_dict(guestInfo_dict.get("Country")),
            address=guestInfo_dict.get("address")
        )
