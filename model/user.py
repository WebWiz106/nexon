from model.accessScope import AccessScope, AssignedLocation


class User:

    def __init__(
        self,
        emailId,
        displayName,
        accesskey,
        createdAt,
        role,
        assigned_location,
        isAdmin,
        userName=None,
        accessScope=None,
        ndid=None,
    ):

        def to_bool(val):
            return str(val).lower() == "true"

        # values checking
        if not emailId:
            raise ValueError("Email Id is required")

        self.ndid = ndid
        self.emailId = emailId
        self.displayName = displayName
        self.userName = userName
        self.role = role
        self.accesskey = accesskey
        self.createdAt = createdAt
        self.isAdmin = to_bool(isAdmin)
        self.accessScope = accessScope
        self.assigned_location = assigned_location

    def to_dict(user):
        print(User)

        return {
            "ndid": user.ndid,
            "emailId": user.emailId,
            "displayName": user.displayName,
            "userName": user.userName,
            "accesskey": user.accesskey,
            "createdAt": user.createdAt,
            "role": user.role,
            "isAdmin": user.isAdmin,
            "accessScope": user.accessScope.to_dict() if user.accessScope else {},
            "assigned_location": [loc.to_dict() for loc in user.assigned_location],
        }

        # if user.accessScope is not None:
        #     result["accessScope"] = user.accessScope.to_dict()

        # return result

    @staticmethod
    def from_dict(user_dict):
        # print(user_dict)

        assigned_locations = [
            AssignedLocation.from_dict(loc)
            for loc in user_dict.get("assigned_location", [])
        ]

        access_scope_data = user_dict.get("accessScope")
        access_scope = (
            AccessScope.from_dict(access_scope_data)
            if access_scope_data and isinstance(access_scope_data, dict)
            else None
        )
        return User(
            ndid=user_dict.get("ndid"),
            emailId=user_dict.get("emailId"),
            displayName=user_dict.get("displayName"),
            userName=user_dict.get("userName"),
            accesskey=user_dict.get("accesskey"),
            createdAt=user_dict.get("createdAt"),
            role=user_dict.get("role"),
            isAdmin=user_dict.get("isAdmin"),
            accessScope=access_scope,
            assigned_location=assigned_locations,
        )
