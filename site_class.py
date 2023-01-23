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
        self.offers = {}


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

def search_menu(current, house):
    print(f"this house's address is {house.address}, and the current listed price on this house is ${house.price}")
    print(f"this house has {house.likes} likes")
    seemore = input('would you liek to see more about the house?')
    if seemore == 'yes':
        print(f"the house's address is {house.address}, in {house.neighborhood}. It has an area of {house.area} sq ft, with {house.storage_space} sq ft of storage space and {house.outdoor_space} sq ft of outdoor space.")

    else:
        print('ok')
    like = input('would you like to place a like on this house? (yes/no) -> ')
    if like == "yes":
        house.likes +=1
        print(f"this house now has {house.likes} likes")
    else:
        print('ok')

    placebid = input('would you like to purchase this house?')
    if placebid == 'yes':
        bid = input('enter your offer amount -> ')
        email = input('enter your preferred email address to be contacted for the house -> ')
        owner = house.owner
        owner.offers[current] = [bid]
        owner.offers[current].append(email)
        print('the owner has been alerted to your bid.')

site = Site()

def menu():


    current = None
    while True:
        choice = input('select: (1) create an account (2) login (3) list house (4) edit house (5) search houses (6) logout -> ' )

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
                searchtype = input('select: (1) search for a specific address (2) search by attribute -> ')
                if searchtype == '1':
                    whichhouse = input('enter the address of the house you want to look at -> ')
                    if whichhouse in site.houses:
                        house = site.houses[whichhouse]
                        search_menu(current, house)
                    else:
                        print ('no')
                else:
                    attribute = input('select which attribute you would like to search with: (1) all houses (2) price range (3) neighborhood (4) area range -> ')
                    if attribute == '1':
                        for house in site.houses:
                            print(f"address: {site.houses[house].address}, price: ${site.houses[house].price}, area: {site.houses[house].area} sqft")
                            more = input('would you like more info? (yes/no) -> ')
                            if more == 'yes':
                                search_menu(current, site.houses[house])
                            else:
                                pass

                    elif attribute == '2':
                        low = int(input('input lowest price ($) -> '))
                        high = int(input('input highest price ($) -> '))
                        for house in site.houses:
                            if low < site.houses[house].price < high:
                                print(f"address: {site.houses[house].address}, price: ${site.houses[house].price}, area: {site.houses[house].area} sqft")
                                more = input('would you like more info? (yes/no) -> ')
                                if more == 'yes':
                                    search_menu(current, site.houses[house])
                                else:
                                    pass
                    elif attribute == '2':
                        neighborhood = input('enter the name of the desired neighborhood -> ')
                        for house in site.houses:
                            if lower(site.houses[house].neighborhood) == lower(neighborhood):
                                print(f"address: {site.houses[house].address}, price: ${site.houses[house].price}, area: {site.houses[house].area} sqft")
                                more = input('would you like more info? (yes/no) -> ')
                                if more == 'yes':
                                    search_menu(current, site.houses[house])
                                else:
                                    pass
                    else:
                        low = int(input('input lowest area (sqft) -> '))
                        high = int(input('input highest area (sqft) -> '))
                        for house in site.houses:
                            if low < site.houses[house].area < high:
                                print(f"address: {site.houses[house].address}, price: ${site.houses[house].price}, area: {site.houses[house].area} sqft")
                                more = input('would you like more info? (yes/no) -> ')
                                if more == 'yes':
                                    search_menu(current, site.houses[house])
                                else:
                                    pass

        if choice == '6':
            break


<<<<<<< HEAD
=======
                    placebid = input('would you like to purchase this house?')
                    if placebid == 'yes':
                        print('hi')
                        #idk what to do here tbh....
                else:
                    print ('no')

>>>>>>> 273d52c38941a73174d24817b1b11eaab99f606d
#2r, 100, Battery Park City, 10282, 2, 2, True, True, 100, True, 1, 1, Apartment, True, A, 10, 10
menu()
