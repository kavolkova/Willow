import csv
import sys

#hey whats up
class House:
  def __init__(self, owner, address, area, neighborhood, zipcode, beds, baths, washer_dryer, air_conditioning, heating, outdoor_space, parking, acreage, num_floors, type, furnished, energy_efficiency,storage_space, price = 0,likes=0):
    #ints
    self.price = int(price) #if no price is listed, will be 0 unti westimate is calculated
    self.area = int(area)
    self.beds = int(beds)
    self.baths = int(baths)
    self.outdoor_space = int(outdoor_space)
    self.acreage = int(acreage)
    self.num_floors = int(num_floors)
    self.storage_space = int(storage_space)

    #strings
    self.owner = owner
    self.address = address
    self.zipcode = zipcode
    self.neighborhood = neighborhood
    self.type= type
    self.energy_efficiency = energy_efficiency

    #booleans
    self.washer_dryer = washer_dryer
    self.air_condintioning = air_conditioning
    self.heating = heating
    self.furnished = furnished
    self.parking = parking

  def westimate(self):
    ppsf = 1000
    with open('ppsfs.csv') as df:
        data = csv.reader(df)
        for row in data:
            if row[0] == self.neighborhood:
                ppsf = int(row[1])
    self.price = ppsf*self.area
    #self.price = ppsf*self.area
    #price +=



class User():
  def __init__(self, username, password, type=""):
    self.username = username
    self.password = password
    self.type = type

  def checklogin(self,username, password):
    if username == self.username:
      if password == self.password:
        return True
    return False

  def selectType(self,type):
    if type == "buyer" or type == "seller":
      self.type = type
    else:
      return False

  def typeMenu(self):
    if self.type == "buyer":
      pass
    else:
      pass

houselist = {}

vanderbilt_414 = House('state', '414 Vanderbilt Ave', 500, 'Fort Greene', 11238, 4, 4, True, True, True, 50, False, 1, 4, 'House', False, 'D', 20)
houselist["vanderbilt_414"] = vanderbilt_414
vanderbilt_414.westimate()
print(vanderbilt_414.price)

riverterrace_2_9F = House('state','2 River Terrace, 9F',300,'Battery Park City',10282,3,4,True,True,True,30,False,1,4,'Apartment',False,'C',20)
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
