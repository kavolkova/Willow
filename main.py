import pandas as pd
df = pd.read_csv('/Users/lizuckerman/Desktop/ppsfs.csv')

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
    i = df.loc(self.neighborhood)
    print(i)
    # ppsf = df[i][1]
    # print(ppsf)
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

vanderbilt_414 = House('state', '414 Vanderbilt Ave', 500, 'Fort Greene', 11238, 4, 4, True, True, True, 50, False, 1, 4, 'House', False, 'D', 20)
vanderbilt_414.westimate()
print(vanderbilt_414.price)
