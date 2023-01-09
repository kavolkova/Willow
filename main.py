import csv
import sys
import hashlib

class House:
  def __init__(self, owner, address, area, neighborhood, zipcode, beds, baths, washer_dryer, air_conditioning, outdoor_space, parking, acreage, num_floors, type, furnished, energy_efficiency,storage_space, price = 0, listed = False,likes=0):
    #ints
    self.price = int(price) #if no price is listed, will be 0 unti westimate is calculated
    self.area = int(area)
    self.beds = int(beds)
    self.baths = int(baths)
    self.outdoor_space = int(outdoor_space)
    self.acreage = int(acreage)
    self.num_floors = int(num_floors)
    self.storage_space = int(storage_space)
    self.ppsf = 750
    self.ppsf_outdoor = self.ppsf/2

    #strings
    self.owner = owner
    self.address = address
    self.zipcode = zipcode
    self.neighborhood = neighborhood
    self.type= type
    self.energy_efficiency = energy_efficiency

    #booleans
    self.washer_dryer = washer_dryer
    self.air_conditioning = air_conditioning
    self.furnished = furnished
    self.parking = parking
    self.listed = False

  def westimate(self):
    with open('ppsfs.csv') as df:
        data = csv.reader(df)
        for row in data:
            if row[0] == self.neighborhood:
                self.ppsf = int(row[1])
    self.ppsf_outdoor = self.ppsf/2
    self.price = self.ppsf*self.area + self.ppsf_outdoor*self.outdoor_space
    if self.washer_dryer:
        self.price += 2000
    if self.air_conditioning:
        self.price += 5000
    if self.furnished:
        self.price += self.ppsf*50
    if self.parking:
        self.price += 5000




class User():
  def __init__(self, username, password, type=""):
    self.username = username
    self.password = str(hashlib.sha256(password.encode()).hexdigest())


houselist = {}

vanderbilt_414 = House('state', '414 Vanderbilt Ave', 774, 'Fort Greene', 11238, 4, 4, True, True, 50, False, 1, 4, 'House', False, 'D', 20)
houselist["vanderbilt_414"] = vanderbilt_414
vanderbilt_414.westimate()
print(vanderbilt_414.price)

riverterrace_2_9F = House('state','2 River Terrace, 9F',300,'Battery Park City',10282,3,4,True,True,30,False,1,4,'Apartment',False,'C',20)
houselist["riverterrace_2_9F"] = riverterrace_2_9F
# riverterrace_2_9F.westimate()
# print(riverterrace_2_9F.price())



# housesearch = input("please type in the name of the street, street number, and apartment number if needed, all separated with underscores.")
# if housesearch in houselist.keys():
#     print(f"welcome to the page for {housesearch}.")
#     houselist[housesearch].westimate()
#     print(houselist[housesearch].price())
# else:
#     print(houselist)
#     print('epic fail')
