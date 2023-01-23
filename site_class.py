import csv
import hashlib
import shelve

class House:
  def __init__(self, owner, address, area, neighborhood, zipcode, beds, baths, washer_dryer, air_conditioning, outdoor_space, parking, acreage, num_floors, type, furnished, energy_efficiency,storage_space, price = 0, listed = False, likes=0):
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
    self.likes = likes

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



class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = str(hashlib.sha256(password.encode()).hexdigest())
        self.houses = {}


class Site:

    def __init__(self):
        self.accounts = {}
        self.houses = {}

    def addAccount(self, username, password):
        accs = shelve.open('accs', writeback = True)
        newaccount = Account(username, password)
        self.accounts[username] = newaccount
        accs[username]= [password]
        accs[username].append(newaccount)
        accs[username].append({})
        accs.close()


    def login(self,username,password):
        accs = shelve.open('accs', writeback = True)
        if username in accs and accs[username][0] == str(hashlib.sha256(password.encode()).hexdigest()): #checks if account exists and password is correct
          return True
          accs.close()
        else:
          return False
          accs.close()


    def list_house(self, username, address, area, neighborhood, zipcode, beds, baths, washer_dryer, air_conditioning, outdoor_space, parking, acreage, num_floors, type, furnished, energy_efficiency,storage_space, price = 0, listed = False, likes=0):
        accs = shelve.open('accs',writeback = True)
        self.houses[address] = House(username, address, area, neighborhood, zipcode, beds, baths, washer_dryer, air_conditioning, outdoor_space, parking, acreage, num_floors, type, furnished, energy_efficiency,storage_space, price = 0, listed = False, likes=0)
        accs[username][2][address] = self.houses[address]
        print(f"list house: {accs[username][2]}")
        accs.close()

        #self.accounts[username].houses[address] = self.houses[address]


    def countlikes(self,username,address):
        accs = shelve.open('accs', writeback = True)
        count = 0
        # for item in self.houses[address].likes:
        #     count+=1
        # return count
        for item in accs[username][2].get(address).likes:
            count+=1
        return count
        accs.close()

site = Site()

def menu():


    current = None
    while True:
        choice = input('select: (1) create an account (2) login (3) list house (4) edit house (5) search houses' )

        if choice == '1':
            username = input('create a username -> ')
            password = input('create a password -> ')
            encrypted_password = str(hashlib.sha256(password.encode()).hexdigest())
            site.addAccount(username, encrypted_password)


        if choice == '2':
            username = input('enter your username -> ')
            password = input('enter your password -> ')
            if site.login(username, password):
                current = username
                print('logged in')
            else:
                print("invalid user or password")

        if choice == '3':
            if current:
                accs = shelve.open('accs', writeback = True)
                info = input('enter this house information, separated by commas: address, area, neighborhood, zipcode, beds, baths, washer/dryer (T/F), air/conditioning (T/F), outdoor_space (in sqft), parking (T/F), acreage, number of floors, type, furnished (T/F), energy efficiency rating, storage space (sqft), price. If you do not know the price, leave that area blank. -> ')
                info = info.split(', ')
                print(f"menu 1 {accs[current][2]}")
                if info[0] not in accs[current][2].keys():
                    site.list_house(current, *info)
                else:
                    print('sorry, that address has already been listed by someone.')
                print('house', info[0], 'added')
                print(f"menu 2 {accs[current][2]}")
                accs.sync()
                west = input('would you like Willow to calculate a Westimate (TM) for this house in place of the current price? (yes/no) -> ')
                if west == 'yes':
                    print(f"west {accs[current][2]}")
                    house = accs[current][2][info[0]]
                    house.westimate()
                    print('the Westimate (TM) is', house.price)
                    accs.close()
                else:
                    print('ok, we will not calculate a Westimate (TM)')
                    accs.close()

        if choice =='5':
            if current:
                whichhouse = input('enter the address of the house you want to look at -> ')
                if whichhouse in site.houses:
                    print(f"the current listed price on this house is ${site.houses[whichhouse].price}")
                    print(f"this house has {site.houses[whichhouse].likes} likes")
                    seemore = input('would you liek to see more about the house?')
                    if seemore == 'yes':
                        print(f"the house's address is {site.houses[whichhouse].address}, in {site.houses[whichhouse].neighborhood}. It has an area of {site.houses[whichhouse].area} sq ft, with {site.houses[whichhouse].storage_space} sq ft of storage space and {site.houses[whichhouse].outdoor_space} sq ft of outdoor space.")

                    else:
                        print('ok')
                    like = input('would you like to place a like on this house? (yes/no) -> ')
                    if like == "yes":
                        site.houses[whichhouse].likes +=1
                        print(f"this house now has {site.houses[whichhouse].likes} likes")
                    else:
                        print('ok')


                    placebid = input('would you like to purchase this house?')
                    if placebid == 'yes':
                        print('hi')
                        #idk what to do here tbh....
                else:
                    print ('no')

#2r, 100, Battery Park City, 10282, 2, 2, True, True, 100, True, 1, 1, Apartment, True, A, 10, 10
menu()
