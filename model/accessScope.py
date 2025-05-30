class AccessScope:
    def __init__(
        self,
        bookingEngine,
        channelManager,
        cms,
        humanResourceManagement,
        guestRequestManagement,
        enquiriesManagement,
        foodManager,
        frontDesk,
        gatewayManager,
        reservationDesk,
        seoManager,
        socialMedia,
        themes,
        leadgenform,
        conversationaltool,
        eazobot,
        usermanagement,
        emailmarketing,
        whatsappmarketing,
        smsmarketing,
        analyticsandreporting,
    ):
        # self.bookingEngine = bookingEngine == "true"
        # self.channelManager = channelManager == "true"
        # self.cms = cms == "true"
        # self.foodManager = foodManager == "true"
        # self.frontDesk = frontDesk == "true"
        # self.gatewayManager = gatewayManager == "true"
        # self.reservationDesk = reservationDesk == "true"
        # self.seoManager = seoManager == "true"
        # self.socialMedia = socialMedia == "true"
        # self.themes = themes == "true"
        # self.enquiriesManagement = enquiriesManagement == "true"
        # self.guestRequestManagement = guestRequestManagement == "true"
        # self.humanResourceManagement = humanResourceManagement == "true"

        def to_bool(val):
            return str(val).lower() == "true"

        self.bookingEngine = to_bool(bookingEngine)
        self.channelManager = to_bool(channelManager)
        self.cms = to_bool(cms)
        self.foodManager = to_bool(foodManager)
        self.frontDesk = to_bool(frontDesk)
        self.gatewayManager = to_bool(gatewayManager)
        self.reservationDesk = to_bool(reservationDesk)
        self.seoManager = to_bool(seoManager)
        self.socialMedia = to_bool(socialMedia)
        self.themes = to_bool(themes)
        self.enquiriesManagement = to_bool(enquiriesManagement)
        self.guestRequestManagement = to_bool(guestRequestManagement)
        self.humanResourceManagement = to_bool(humanResourceManagement)
        self.leadgenform = to_bool(leadgenform)
        self.conversationaltool = to_bool(conversationaltool)
        self.eazobot = to_bool(eazobot)
        self.usermanagement = to_bool(usermanagement)
        self.emailmarketing = to_bool(emailmarketing)
        self.whatsappmarketing = to_bool(whatsappmarketing)
        self.smsmarketing = to_bool(smsmarketing)
        self.analyticsandreporting = to_bool(analyticsandreporting)

    def to_dict(self):
        print(self)
        return {
            "bookingEngine": self.bookingEngine,
            "channelManager": self.channelManager,
            "cms": self.cms,
            "foodManager": self.foodManager,
            "frontDesk": self.frontDesk,
            "gatewayManager": self.gatewayManager,
            "reservationDesk": self.reservationDesk,
            "seoManager": self.seoManager,
            "socialMedia": self.socialMedia,
            "themes": self.themes,
            "enquiriesManagement": self.enquiriesManagement,
            "guestRequestManagement": self.guestRequestManagement,
            "humanResourceManagement": self.humanResourceManagement,
            "leadgenform": self.leadgenform,
            "conversationaltool": self.conversationaltool,
            "eazobot": self.eazobot,
            "usermanagement": self.usermanagement,
            "emailmarketing": self.emailmarketing,
            "whatsappmarketing": self.whatsappmarketing,
            "smsmarketing": self.smsmarketing,
            "analyticsandreporting": self.analyticsandreporting,
        }

    def from_dict(access_scope):
        return AccessScope(
            bookingEngine=access_scope.get("bookingEngine"),
            channelManager=access_scope.get("channelManager"),
            cms=access_scope.get("cms"),
            foodManager=access_scope.get("foodManager"),
            frontDesk=access_scope.get("frontDesk"),
            gatewayManager=access_scope.get("gatewayManager"),
            reservationDesk=access_scope.get("reservationDesk"),
            seoManager=access_scope.get("seoManager"),
            socialMedia=access_scope.get("socialMedia"),
            themes=access_scope.get("themes"),
            enquiriesManagement=access_scope.get("enquiriesManagement"),
            guestRequestManagement=access_scope.get("guestRequestManagement"),
            humanResourceManagement=access_scope.get("humanResourceManagement"),
            leadgenform=access_scope.get("leadgenform"),
            conversationaltool=access_scope.get("conversationaltool"),
            eazobot=access_scope.get("eazobot"),
            usermanagement=access_scope.get("usermanagement"),
            emailmarketing=access_scope.get("emailmarketing"),
            whatsappmarketing=access_scope.get("whatsappmarketing"),
            smsmarketing=access_scope.get("smsmarketing"),
            analyticsandreporting=access_scope.get("analyticsandreporting"),
        )


class AssignedLocation:

    def __init__(self, hid, accessScope):
        self.hid = hid
        self.accessScope = accessScope

    def to_dict(self):
        return {"hid": self.hid, "accessScope": AccessScope.to_dict(self.accessScope)}

    def from_dict(data):
        return AssignedLocation(
            hid=data.get("hid"),
            accessScope=AccessScope.from_dict(data.get("accessScope")),
        )
