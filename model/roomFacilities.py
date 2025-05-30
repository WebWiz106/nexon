class RoomFacility:
    def __init__(self, wifi,television,airConditonar,hairdryers,coffeeMakers,directDial,tableWithChair,alarmclock, electronicLocker,fridge,bathroomWithShower,freeBreakfast,kidEquipment,Balcony,Bath,View,FlatscreenTV,Privatepool,Electrickettle,Spabath,RoomAmenities,Cots,Clothesrack,FoldupBed,SofaBed,Trashcans,Heatedpool,Infinitypool,Plungepool,Poolcover,Pooltowels,Rooftoppool,Dressingroom,Fan,Fireplace,Heating,Iron,Ironingfacilities,Hottub,Mosquitonet,PrivateEntrance,Sofa,Soundproofing,SeatingArea,Pantspress,Washingmachine,Desk,Hypoallergenic,Cleaningproducts,Pajamas,Yukata,Adapter,Featherpillow,Non_feather_pillow,Bathroom,Privatebathroom,Shared_bathroom,Toilet_paper,Bidet,Bath_shower,Bathrobe,Free_toiletries,Additional_toilet,Hairdryer,Shared_toilet,Sauna,Shower,Slippers,Toilet,Additional_bathroom,Toothbrush,Shampoo,Conditioner,Cd_player,Dvd_player,Fax,Radio,Satellitechannels,Telephone,Tv,Smartphone,Streamingservice_like_Netflix,Dining_table,Bottle_of_water,Chocolate_or_cookies,Fruits,Barbecue,Oven,Stovetop,Toaster,Dishwasher,Outdoor_furniture,Minibar,Kitchen,Key_card_access,Lockers,Key_access,Alarm_clock,Wake_up_service,Linen,Blanket,Extra_blankets,Pillow,Towels,Patio,City_view,Garden_view,Lake_view,Landmark_view,Mountain_view,Pool_view,River_view,Sea_view,Hearingaccessible,Adaptedbath,Raisedtoilet,Loweredsink,Showerchair,Entertainment_family_services,Baby_safety_gates,Books,DVDs,Smokealarm,Fire_extinguisher,Safety_features,Air_purifiers,Physicaldistancing,Handsanitiser):
        self.wifi = wifi
        self.television = television
        self.airConditonar = airConditonar
        self.hairdryers = hairdryers        
        self.coffeeMakers = coffeeMakers
        self.directDial = directDial
        self.tableWithChair = tableWithChair
        self.alarmclock = alarmclock
        self.electronicLocker = electronicLocker
        self.fridge = fridge
        self.bathroomWithShower = bathroomWithShower
        self.freeBreakfast = freeBreakfast
        self.kidEquipment = kidEquipment
        self.Balcony = Balcony
        self.Bath = Bath
        self.View = View
        self.FlatscreenTV = FlatscreenTV
        self.Privatepool = Privatepool
        self.Electrickettle = Electrickettle
        self.Spabath = Spabath
        self.RoomAmenities = RoomAmenities
        self.Cots = Cots
        self.Clothesrack=Clothesrack
        self.FoldupBed = FoldupBed
        self.SofaBed = SofaBed
        self.Trashcans = Trashcans
        self.Heatedpool = Heatedpool
        self.Infinitypool = Infinitypool
        self.Plungepool = Plungepool
        self.Poolcover = Poolcover
        self.Pooltowels = Pooltowels
        self.Rooftoppool = Rooftoppool
        self.Dressingroom = Dressingroom
        self.Fan = Fan
        self.Fireplace = Fireplace
        self.Heating = Heating
        self.Iron = Iron
        self.Ironingfacilities = Ironingfacilities
        self.Hottub = Hottub
        self.Mosquitonet = Mosquitonet
        self.PrivateEntrance = PrivateEntrance
        self.Sofa = Sofa
        self.Soundproofing = Soundproofing
        self.SeatingArea = SeatingArea
        self.Pantspress = Pantspress
        self.Washingmachine = Washingmachine
        self.Desk = Desk
        self.Hypoallergenic = Hypoallergenic
        self.Cleaningproducts = Cleaningproducts
        self.Pajamas = Pajamas
        self.Yukata = Yukata
        self.Adapter = Adapter
        self.Featherpillow = Featherpillow
        self.Non_feather_pillow = Non_feather_pillow
        self.Bathroom = Bathroom
        self.Privatebathroom = Privatebathroom
        self.Shared_bathroom = Shared_bathroom
        self.Toilet_paper = Toilet_paper
        
        self.Bidet = Bidet
        self.Bath_shower = Bath_shower
        self.Bathrobe = Bathrobe
        self.Free_toiletries = Free_toiletries
        self.Additional_toilet = Additional_toilet
        self.Hairdryer = Hairdryer
        self.Shared_toilet = Shared_toilet
        self.Sauna = Sauna
        self.Shower = Shower
        self.Slippers = Slippers
        self.Toilet = Toilet
        self.Additional_bathroom = Additional_bathroom
        self.Toothbrush = Toothbrush
        self.Shampoo = Shampoo
        self.Conditioner = Conditioner
        self.Cd_player = Cd_player
        self.Dvd_player = Dvd_player
        self.Fax = Fax

        self.Radio = Radio
        self.Satellitechannels = Satellitechannels
        self.Telephone = Telephone
        self.Tv = Tv
        self.Smartphone = Smartphone
        self.Streamingservice_like_Netflix = Streamingservice_like_Netflix
        self.Dining_table = Dining_table
        self.Bottle_of_water = Bottle_of_water
        self.Chocolate_or_cookies = Chocolate_or_cookies
        self.Fruits = Fruits
        self.Barbecue = Barbecue
        self.Oven = Oven
        self.Stovetop = Stovetop
        self.Toaster = Toaster
        self.Dishwasher = Dishwasher
        self.Outdoor_furniture = Outdoor_furniture
        self.Minibar = Minibar
        self.Kitchen = Kitchen

        self.Key_card_access = Key_card_access
        self.Lockers = Lockers
        self.Key_access = Key_access
        self.Alarm_clock = Alarm_clock
        self.Wake_up_service = Wake_up_service
        self.Linen = Linen
        self.Blanket = Blanket
        self.Extra_blankets = Extra_blankets
        self.Pillow = Pillow
        self.Towels = Towels
        self.Patio = Patio
        self.City_view = City_view
        self.Garden_view = Garden_view
        self.Lake_view = Lake_view
        self.Landmark_view = Landmark_view
        self.Mountain_view = Mountain_view
        self.Pool_view = Pool_view
        self.River_view = River_view
        
        self.Sea_view = Sea_view
        self.Hearingaccessible = Hearingaccessible
        self.Adaptedbath = Adaptedbath
        self.Raisedtoilet = Raisedtoilet
        self.Loweredsink = Loweredsink
        self.Showerchair = Showerchair
        self.Entertainment_family_services = Entertainment_family_services
        self.Baby_safety_gates = Baby_safety_gates
        self.Books = Books
        self.DVDs = DVDs
        self.Smokealarm = Smokealarm
        self.Fire_extinguisher = Fire_extinguisher
        self.Safety_features = Safety_features
        self.Air_purifiers = Air_purifiers
        self.Physicaldistancing = Physicaldistancing
        self.Handsanitiser = Handsanitiser


    def to_dict(roomfacility):
        return {
            "wifi" : roomfacility.wifi,
            "television" : roomfacility.television,
            "airConditonar": roomfacility.airConditonar,
            "hairdryers" : roomfacility.hairdryers,        
            "coffeeMakers" : roomfacility.coffeeMakers,
            "directDial" : roomfacility.directDial,
            "tableWithChair" : roomfacility.tableWithChair,
            "alarmclock" : roomfacility.alarmclock,
            "electronicLocker" : roomfacility.electronicLocker,
            "fridge" : roomfacility.fridge,
            "bathroomWithShower" : roomfacility.bathroomWithShower,
            "freeBreakfast" : roomfacility.freeBreakfast,
            "kidEquipment" : roomfacility.kidEquipment,
            "Balcony": roomfacility.Balcony,
            "Bath": roomfacility.Bath,
            "View" : roomfacility.View,
            "FlatscreenTV" : roomfacility.FlatscreenTV,
            "Privatepool": roomfacility.Privatepool,
            "Electrickettle" : roomfacility.Electrickettle,
            "Spabath" : roomfacility.Spabath,
            "RoomAmenities" : roomfacility.RoomAmenities,
            "Cots" : roomfacility.Cots,
            "Clothesrack":roomfacility.Clothesrack,
            "FoldupBed" : roomfacility.FoldupBed,
            "SofaBed" : roomfacility.SofaBed,
            "Trashcans" : roomfacility.Trashcans,
            "Heatedpool" : roomfacility.Heatedpool,
            "Infinitypool" : roomfacility.Infinitypool,
            "Plungepool" : roomfacility.Plungepool,
            "Poolcover" : roomfacility.Poolcover,
            "Pooltowels" : roomfacility.Pooltowels,
            "Rooftoppool" : roomfacility.Rooftoppool,
            "Dressingroom" : roomfacility.Dressingroom,
            "Fan" : roomfacility.Fan,
            "Fireplace" : roomfacility.Fireplace,
            "Heating" : roomfacility.Heating,
            "Iron" : roomfacility.Iron,
            "Ironingfacilities" : roomfacility.Ironingfacilities,
            "Hottub" : roomfacility.Hottub,
            "Mosquitonet" : roomfacility.Mosquitonet,
            "PrivateEntrance" : roomfacility.PrivateEntrance,
            "Sofa" : roomfacility.Sofa,
            "Soundproofing" : roomfacility.Soundproofing,
            "SeatingArea" : roomfacility.SeatingArea,
            "Pantspress" : roomfacility.Pantspress,
            "Washingmachine" : roomfacility.Washingmachine,
            "Desk": roomfacility.Desk,
            "Hypoallergenic" : roomfacility.Hypoallergenic,
            "Cleaningproducts" : roomfacility.Cleaningproducts,
            "Pajamas": roomfacility.Pajamas,
            "Yukata" : roomfacility.Yukata,
            "Adapter": roomfacility.Adapter,
            "Featherpillow" : roomfacility.Featherpillow,
            "Non_feather_pillow" : roomfacility.Non_feather_pillow,
            "Bathroom" : roomfacility.Bathroom,
            "Privatebathroom" : roomfacility.Privatebathroom,
            "Shared_bathroom" : roomfacility.Shared_bathroom,
            "Toilet_paper" : roomfacility.Toilet_paper,            
            "Bidet" : roomfacility.Bidet,
            "Bath_shower" : roomfacility.Bath_shower,
            "Bathrobe" : roomfacility.Bathrobe,
            "Free_toiletries" : roomfacility.Free_toiletries,
            "Additional_toilet" : roomfacility.Additional_toilet,
            "Hairdryer" : roomfacility.Hairdryer,
            "Shared_toilet" : roomfacility.Shared_toilet,
            "Sauna" : roomfacility.Sauna,
           "Shower" : roomfacility.Shower,
            "Slippers" : roomfacility.Slippers,
            "Toilet": roomfacility.Toilet,
            "Additional_bathroom" : roomfacility.Additional_bathroom,
            "Toothbrush" : roomfacility.Toothbrush,
            "Shampoo": roomfacility.Shampoo,
            "Conditioner": roomfacility.Conditioner,
            "Cd_player" : roomfacility.Cd_player,
           "Dvd_player" : roomfacility.Dvd_player,
            "Fax": roomfacility.Fax,
            "Radio": roomfacility.Radio,
            "Satellitechannels" : roomfacility.Satellitechannels,
            "Telephone" : roomfacility.Telephone,
            "Tv" : roomfacility.Tv,
            "Smartphone": roomfacility.Smartphone,
            "Streamingservice_like_Netflix" : roomfacility.Streamingservice_like_Netflix,
            "Dining_table" : roomfacility.Dining_table,
            "Bottle_of_water": roomfacility.Bottle_of_water,
            "Chocolate_or_cookies" : roomfacility.Chocolate_or_cookies,
            "Fruits" : roomfacility.Fruits,
            "Barbecue": roomfacility.Barbecue,
            "Oven": roomfacility.Oven,
            "Stovetop": roomfacility.Stovetop,
            "Toaster" : roomfacility.Toaster,
            "Dishwasher" : roomfacility.Dishwasher,
            "Outdoor_furniture" : roomfacility.Outdoor_furniture,
            "Minibar": roomfacility.Minibar,
            "Kitchen" : roomfacility.Kitchen,
            "Key_card_access" : roomfacility.Key_card_access,
            "Lockers" : roomfacility.Lockers,
            "Key_access": roomfacility.Key_access,
            "Alarm_clock" : roomfacility.Alarm_clock,
            "Wake_up_service" : roomfacility.Wake_up_service,
            "Linen" : roomfacility.Linen,
            "Blanket": roomfacility.Blanket,
            "Extra_blankets" : roomfacility.Extra_blankets,
            "Pillow": roomfacility.Pillow,
            "Towels" : roomfacility.Towels,
            "Patio" : roomfacility.Patio,
            "City_view" : roomfacility.City_view,
            "Garden_view": roomfacility.Garden_view,
            "Lake_view" : roomfacility.Lake_view,
            "Landmark_view" : roomfacility.Landmark_view,
            "Mountain_view" : roomfacility.Mountain_view,
            "Pool_view" : roomfacility.Pool_view,
            "River_view" : roomfacility.River_view,
            "Sea_view": roomfacility.Sea_view,
            "Hearingaccessible" : roomfacility.Hearingaccessible,
            "Adaptedbath" : roomfacility.Adaptedbath,
            "Raisedtoilet" : roomfacility.Raisedtoilet,
            "Loweredsink" : roomfacility.Loweredsink,
            "Showerchair" : roomfacility.Showerchair,
            "Entertainment_family_services": roomfacility.Entertainment_family_services,
            "Baby_safety_gates" : roomfacility.Baby_safety_gates,
            "Books": roomfacility.Books,
            "DVDs": roomfacility.DVDs,
            "Smokealarm": roomfacility.Smokealarm,
            "Fire_extinguisher" : roomfacility.Fire_extinguisher,
            "Safety_features" : roomfacility.Safety_features,
            "Air_purifiers" : roomfacility.Air_purifiers,
            "Physicaldistancing": roomfacility.Physicaldistancing,
            "Handsanitiser": roomfacility.Handsanitiser
        }

    def from_dict(roomfacility):
        return RoomFacility(
            wifi = "wifi" in roomfacility,
            television ="television" in roomfacility,
            airConditonar= "airConditonar" in roomfacility,
            hairdryers = "hairdryers" in roomfacility,        
            coffeeMakers = "coffeeMakers" in roomfacility,
            directDial = "directDial" in roomfacility,
            tableWithChair = "tableWithChair" in roomfacility,
            alarmclock = "alarmclock" in roomfacility,
            electronicLocker = "electronicLocker" in roomfacility,
            fridge ="fridge" in roomfacility,
            bathroomWithShower="bathroomWithShower" in roomfacility,
            freeBreakfast = "freeBreakfast" in roomfacility,
            kidEquipment = "kidEquipment" in roomfacility,
            Balcony="Balcony" in roomfacility,
            Bath="Bath" in roomfacility,
            View= "View" in roomfacility,
            FlatscreenTV = "FlatscreenTV" in roomfacility,
            Privatepool= "Privatepool" in roomfacility,
            Electrickettle= "Electrickettle" in roomfacility,
            Spabath = "Spabath" in roomfacility,
            RoomAmenities = "RoomAmenities" in roomfacility,
            Cots = "Cots" in roomfacility,
            Clothesrack="Clothesrack" in roomfacility,
            FoldupBed = "FoldupBed" in roomfacility,
            SofaBed = "SofaBed" in roomfacility,
            Trashcans = "Trashcans" in roomfacility,
            Heatedpool = "Heatedpool" in roomfacility,
            Infinitypool = "Infinitypool" in roomfacility,
            Plungepool = "Plungepool" in roomfacility,
            Poolcover = "Poolcover" in roomfacility,
            Pooltowels = "Pooltowels" in roomfacility,
            Rooftoppool = "Rooftoppool" in roomfacility,
            Dressingroom = "Dressingroom" in roomfacility,
            Fan = "Fan" in roomfacility,
            Fireplace = "Fireplace" in roomfacility,
            Heating = "Heating" in roomfacility,
            Iron ="Iron" in roomfacility,
            Ironingfacilities = "Ironingfacilities" in roomfacility,
            Hottub = "Hottub" in roomfacility,
            Mosquitonet = "Mosquitonet" in roomfacility,
            PrivateEntrance ="PrivateEntrance" in roomfacility,
            Sofa = "Sofa" in roomfacility,
            Soundproofing = "Soundproofing" in roomfacility,
            SeatingArea = "SeatingArea" in roomfacility,
            Pantspress = "Pantspress" in roomfacility,
            Washingmachine = "Washingmachine" in roomfacility,
            Desk= "Desk" in roomfacility,
            Hypoallergenic= "Hypoallergenic" in roomfacility,
            Cleaningproducts = "Cleaningproducts" in roomfacility,
            Pajamas= "Pajamas" in roomfacility,
            Yukata = "Yukata" in roomfacility,
            Adapter= "Adapter" in roomfacility,
            Featherpillow = "Featherpillow" in roomfacility,
            Non_feather_pillow= "Non_feather_pillow" in roomfacility,
            Bathroom = "Bathroom" in roomfacility,
            Privatebathroom = "Privatebathroom" in roomfacility,
            Shared_bathroom= "Shared_bathroom" in roomfacility,
            Toilet_paper = "Toilet_paper" in roomfacility,            
            Bidet= "Bidet" in roomfacility,
            Bath_shower = "Bath_shower" in roomfacility,
            Bathrobe= "Bathrobe" in roomfacility,
            Free_toiletries = "Free_toiletries" in roomfacility,
            Additional_toilet= "Additional_toilet" in roomfacility,
            Hairdryer = "Hairdryer" in roomfacility,
            Shared_toilet = "Shared_toilet" in roomfacility,
            Sauna = "Sauna" in roomfacility,
            Shower = "Shower" in roomfacility,
            Slippers = "Slippers" in roomfacility,
            Toilet= "Toilet" in roomfacility,
            Additional_bathroom = "Additional_bathroom" in roomfacility,
            Toothbrush ="Toothbrush" in roomfacility,
            Shampoo= "Shampoo" in roomfacility,
            Conditioner= "Conditioner" in roomfacility,
            Cd_player= "Cd_player" in roomfacility,
           Dvd_player = "Dvd_player" in roomfacility,
            Fax= "Fax" in roomfacility,
            Radio= "Radio" in roomfacility,
            Satellitechannels= "Satellitechannels" in roomfacility,
            Telephone= "Telephone" in roomfacility,
            Tv= "Tv" in roomfacility,
            Smartphone= "Smartphone" in roomfacility,
            Streamingservice_like_Netflix= "Streamingservice_like_Netflix" in roomfacility,
            Dining_table= "Dining_table" in roomfacility,
            Bottle_of_water= "Bottle_of_water" in roomfacility,
            Chocolate_or_cookies="Chocolate_or_cookies" in roomfacility,
            Fruits= "Fruits" in roomfacility,
            Barbecue="Barbecue" in roomfacility,
            Oven= "Oven" in roomfacility,
            Stovetop= "Stovetop" in roomfacility,
            Toaster= "Toaster" in roomfacility,
            Dishwasher= "Dishwasher" in roomfacility,
            Outdoor_furniture= "Outdoor_furniture" in roomfacility,
            Minibar= "Minibar" in roomfacility,
            Kitchen="Kitchen"in roomfacility,
            Key_card_access= "Key_card_access" in roomfacility,
            Lockers= "Lockers" in roomfacility,
            Key_access="Key_access" in roomfacility,
            Alarm_clock="Alarm_clock" in roomfacility,
            Wake_up_service= "Wake_up_service" in roomfacility,
            Linen= "Linen" in roomfacility,
            Blanket= "Blanket" in roomfacility,
            Extra_blankets= "Extra_blankets" in roomfacility,
            Pillow= "Pillow" in roomfacility,
            Towels= "Towels" in roomfacility,
            Patio= "Patio" in roomfacility,
            City_view= "City_view" in roomfacility,
            Garden_view= "Garden_view" in roomfacility,
            Lake_view= "Lake_view" in roomfacility,
            Landmark_view= "Landmark_view" in roomfacility,
            Mountain_view= "Mountain_view" in roomfacility,
            Pool_view="Pool_view" in roomfacility,
            River_view= "River_view" in roomfacility,
            Sea_view= "Sea_view" in roomfacility,
            Hearingaccessible= "Hearingaccessible" in roomfacility,
            Adaptedbath= "Adaptedbath" in roomfacility,
            Raisedtoilet ="Raisedtoilet" in roomfacility,
            Loweredsink= "Loweredsink" in roomfacility,
            Showerchair= "Showerchair" in roomfacility,
            Entertainment_family_services= "Entertainment_family_services" in roomfacility,
            Baby_safety_gates= "Baby_safety_gates" in roomfacility,
            Books ="Books" in roomfacility,
            DVDs="DVDs" in roomfacility,
            Smokealarm= "Smokealarm" in roomfacility,
            Fire_extinguisher= "Fire_extinguisher"in roomfacility,
            Safety_features= "Safety_features" in roomfacility,
            Air_purifiers="Air_purifiers" in roomfacility,
            Physicaldistancing= "Physicaldistancing" in roomfacility,
            Handsanitiser= "Handsanitiser" in roomfacility
        )
