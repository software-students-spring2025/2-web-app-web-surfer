from mongoengine import Document, StringField, IntField, EmailField, ReferenceField, DateTimeField, FloatField
from datetime import datetime
from mongoengine import connect

connect('SWE_Project2_Rental_Software', host='mongodb://localhost:27017/SWE_Project2_Rental_Software')

#user-information table
class UserInformation(Document):
    meta = {'collection': 'user_information'}
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    usertype = IntField(required=True)  # 1 for admin, 0 for guest
    avatar = StringField()
    email = EmailField(required=True, unique=True)

#policies table
class Policy(Document):
    meta = {'collection': 'policies'}
    # 1 for yes, 0 for no
    pet_allowed = IntField(required=True)  
    guarantor_accepted = IntField(required=True)  
    smoke_free = IntField(required=True)  

#home features table
class HomeFeature(Document):
    meta = {'collection': 'home_features'}
    # 1 for yes, 0 for no
    centralair = IntField(required=True)
    dishwasher = IntField(required=True)
    hardwoodfloor = IntField(required=True)
    view = IntField(required=True)
    privateoutdoor = IntField(required=True)
    washerdryer = IntField(required=True)
    fridge = IntField(required=True)
    oven = IntField(required=True)

#building amenities table
class BuildingAmenity(Document):
    meta = {'collection': 'building_amenities'}
    # 1 for yes, 0 for no
    doorman = IntField(required=True)
    bikeroom = IntField(required=True)
    elevator = IntField(required=True)
    laundry = IntField(required=True)
    gym = IntField(required=True)
    packageroom = IntField(required=True)
    parking = IntField(required=True)
    concierge = IntField(required=True)
    library = IntField(required=True)

#buildings table
class Building(Document):
    meta = {'collection': 'buildings'}
    name = StringField(required=True)
    address = StringField(required=True)
    num_unit = IntField(required=True)
    about_info = StringField()

#houses table
class House(Document):
    meta = {'collection': 'houses'}
    building = ReferenceField(Building)
    apt_num = StringField(required=True)
    price = FloatField(required=True)
    bedroom = StringField(required=True)
    bathroom = StringField(required=True)
    area = StringField(required=True)
    available_date = DateTimeField(required=True)
    address = StringField(required=True)
    posted_admin = ReferenceField(UserInformation)
    about_info = StringField()
    policy = ReferenceField(Policy)
    home_feature = ReferenceField(HomeFeature)
    amenities = ReferenceField(BuildingAmenity)
    picture = StringField()


#wishlists table
class Wishlist(Document):
    meta = {'collection': 'wishlists'}
    user = ReferenceField(UserInformation, required=True)
    house = ReferenceField(House, required=True)


# 初始化数据的函数
def init_test_data():
    # 检查是否已经存在数据
    if UserInformation.objects.count() == 0:
        # 插入用户数据
        user_admin = UserInformation(
            username="Bob",
            password="1234567",
            usertype=1,
            avatar="...",
            email="bb123@gmail.com"
        ).save()

        user_guest = UserInformation(
            username="Alex",
            password="1234567",
            usertype=0,
            avatar="...",
            email="a1234@gmail.com"
        ).save()

    if Policy.objects.count() == 0:
        # 插入政策数据
        policy = Policy(
            pet_allowed=1,
            guarantor_accepted=1,
            smoke_free=0
        ).save()

    if HomeFeature.objects.count() == 0:
        # 插入房屋特征数据
        home_feature = HomeFeature(
            centralair=1,
            dishwasher=1,
            hardwoodfloor=1,
            view=1,
            privateoutdoor=1,
            washerdryer=1,
            fridge=1,
            oven=1
        ).save()

    if BuildingAmenity.objects.count() == 0:
        # 插入建筑设施数据
        amenities = BuildingAmenity(
            doorman=1,
            bikeroom=1,
            elevator=1,
            laundry=0,
            gym=1,
            packageroom=0,
            parking=1,
            concierge=0,
            library=1
        ).save()

    if Building.objects.count() == 0:
        # 插入建筑数据
        building = Building(
            name="Jackson Park",
            address="28-16 Jackson Ave, Long Island City, NY 11101",
            num_unit=219,
            about_info="20xx built"
        ).save()

        # 只有在所有必要的关联数据都存在时才插入房屋数据
        if all([user_admin, policy, home_feature, amenities]):
            house = House(
                building=building,
                apt_num="#316",
                price=1000.00,
                bedroom="1",
                bathroom="1",
                area="xxxx",
                available_date=datetime(2025, 5, 16),
                address="28-16 Jackson Ave, Long Island City, NY 11101",
                posted_admin=user_admin,
                about_info="Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
                policy=policy,
                home_feature=home_feature,
                amenities=amenities,
                picture="..."
            ).save()

# 调用初始化函数
init_test_data()
