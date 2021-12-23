import xlrd, itertools
from datetime import datetime
#	Declare Constants	—	—-—	
MAXLOAD = 50
CAPACITIES = [1.8, 10, 18, MAXLOAD]
TIME_WINDOW = 8
SPEED = 50
PICKUPS_TOTAL = 12
ALPHA = 0.2
LOADTIME = 0.5
FILENAME = "INPUT.xlsx"
#	Declare global variables	
LOCATIONS = [] # List of location names
DISTANCES = {} # Nested dictionary of distances. ['A']['B'] = distance A-B 
DEPOT_DIST = {} # Dictionary of depot distances. Sorted by distance, descending REQUESTS = [] # List of Request objects
PICKUPS = []	# List of all pickup locations in REQUESTS
#	Define Classes			
class Request:
# A request has: Pickup, Destination, Load, Distance 
    def	__init__(self, pickup, dest, load):
        self.pickup = pickup
        self.dest = dest
        self.load = load
        self.distance = DISTANCES[pickup][dest]
        self.loadtime = LOADTIME

    def set_pickup(self, pickup):
        if pickup != self.pickup: 
            self.pickup = pickup 
        self.distance = DISTANCES[pickup][self.dest]

    def	_repr_(self):
        return "[%s, %s, %d T, %d km]" % (self.pickup, self.dest, self.load, self.distance)

    def	_str__(self): 
        return self.repr_0

class Truck:
#	A truck has: Speed, Capacity
    speed = SPEED
    def	_init_(self, capacity): 
        self.capacity = capacity
class Trip:
#	A trip has: list of requests from the same pickup, total load, total distance
    def	_init_(self, request):
        self.pickup = request.pickup 
        self.dests = [request, dest] 
        self, load = request, load
        self.distance = request.distance
        self.loadtime = request.loadtime
        
    def add_request(self, request):
        self, self.dests.append(request.dest)
        self.load += request.load
        self.distance += request.distance
        self.loadtime += request.loadtime

    def swap_requests(self, x, y):
        self.dests[x], self.dests[y] = self, dests[y], self.dests[x]
        self.recalculate_distance()

    def recalculate_distance(self):
        self, distance = 0
        for i in range(len(self.dests)):
            self.distance += DISTANCES[self.pickup if i==0 else self.dests[i-l]][self.dests[i]]

    def	_repr_(self):
        string = '"\tPickup from: %s. Load: %.2f. Load time: %.2f hrs. Total time: %.2f hrs. \t\tDeliver to: %s."' % (self.pickup, self.load, self.loadtime, (self.distance/SPEED + self.loadtime)," -- ".join(self.dests))
        return string

    def __str__(self):
        return self.__repr__()
    
class Route:
#	A route has: A truck, a list of trips, total distance

    newid = itertools.count()
    
    def	_init_(self, trip, truck):
        self.id = next(self.newid)
        self.truck = truck
        self.trips = [trip]
        self.distance = trip.distance + DEPOT_DIST[trip.pickup]
        self.loadtime = trip.loadtime
        
    def add_trip(self, trip):
        self.distance += trip.distance + DISTANCES[trip.pickup][self.trips[-l].dests[-l]]
        self.trips.append(trip)
        self.loadtime += trip.loadtime
        
    def __repr__(self):
        string = "Route %d. Truck capacity: %dT. Trips total: %d. Total time: %.2f hrs. Total distance:  %.2f km."   %   (self.id  +  1, self.truck.capacity, len(self.trips),(self.distance/SPEED + self.loadtime), self.distance)        
        return string
    
    def	_str__(self):
        return self.__repr__0
    
class Schedule:
#	A schedule has: a date, list of routes, total distance
    def	_init_(self):
        self.date = datetime.date(datetime.now())
        self.routes = []
        self, distance = 0
        
    def add_route(self, route):
        self.routes.append(route)
        self.distance += route.distance
        
    def	__repr__(self):
        string = "Schedule for %s. Total routes: %s. Total distance: %.2f km." % (self.date.strftime("%m/%d/%Y"), len(self.routes), self.distance)
        return string
    
    def	_str__(self):
        return self.__repr__0
    
#				 read input function-		—		
    def read_input():
        global LOCATIONS, DISTANCES, DEPOT_DIST, REQUESTS, PICKUPS
        book = xlrd.open_workbook(FILENAME, encoding_override='cpl252')
        sheet = book.sheet_by_index(0)
        nrows = sheet.nrows
        ncols = sheet.ncols
        
        LOCATIONS = [sheet.cell_value(r, 3) for r in range(2, nrows)]
        DISTANCES = {LOCATIONS[i] : {LOCATIONS[j] : sheet.cell_value(2 + i, 4 + j)
            for j in range(len(LOCATIONS))}
            for i in range(len(LOCATIONS))}
        DEPOT_DIST = {LOCATIONS[i] : sheet.cell_value(2 + i, 0) for i in range(PICKUPS_TOTAL)}	
        DEPOTDIST = {k : v for k, v in sorted(DEPOT_DIST.items(), key=lambda item:item[1], reverse=True)}
        
        sheet2 = book.sheet_by_index(1)
        nrows2 = sheet2.nrows
        ncols2 = sheet2.ncols
        REQUESTS = [Request(*sheet2.row_values(i)) for i in range(1, nrows2)]
        PICKUPS = list(dict.fromkeys([r.pickup for r in REQUESTS]))
        
    read_input()
    
    
import random, bisect, copy
from datetime import datetime 
# from config import *

#	-greedy function					
def greedy():
    pickups = copy.deepcopy(PICKUPS) 
    trips = []

# $ ************************** Make trips *************************** 

    while pickups != []:
# 1. Get a pickup location pickups
        pickup = pickups.pop()
# 2. Get all the requests from that pickup, sorted by distance, descending
    Request_group = [r for r in REQUESTS if r.pickup == pickup and (r.distance/SPEED + LOADTIME) <= TIME_WINDOW]
    request_group = sorted(request_group, key=lambda item:item.distance, reverse=True)
# 3.Assign all these requests into trips
    while request_group != []:
# 3a. Create a RCL
# "rcl" is the index of the first item in the RCL
# In other words, RCL = request_group[rcl:]
        dmin = request_group[-l].distance
        dmax = request_group[0].distance
        rcl = next(x for x, val in enumerate(request_group) if val.distance <= (dmin + ALPHA * (dmax - dmin)))
# 3b. Randomy get a request from RCL to put into a trip
        request = request_group.pop(random.randint(rcl, len(request_group)-l))
        trip = Trip(request)
        if requestgroup == []:
            trips.append(trip) 
            break
# 3c. Create a temp group of distances between last dest to other dests
# Only consider those that don't exceed MAX LOAD and TIME WINDOW
# If the temp group is empty, then move on to the next trip
# Otherwise, create a RCL and continue adding to the current trip
        while True:
            temp_group = [Request(trip.dests[-1], r.dest, r.load) for r in request_group if r.load + trip.load <= MAXLOAD and ((DISTANCES [trip .pickup][r.dest] + trip.distance)/SPEED + trip.loadtime + LOADTIME) <= TIME_WINDOW]
            if temp_group == []:
                trips, append(trip)
                break
        temp_group = sorted(temp_group, key=lambda item:item. distance, reverse = True) 
        dmin = temp_group[-l].distance
        dmax = temp_group[0].distance
        rcl = next(x for x, val in enumerate(temp_group) if val.distance <= (dmin + ALPHA * (dmax - dmin)))
        request = temp_group[random.randint(rcl, len(temp_group)-l)]
        trip.add_request(request)
        request_group.pop(next(x for x, val in enumerate(request_group) if val.dest == request.dest))
        # ******************** Merge trips into routes*********************
        # 4. Merge trips that have the shortest intermediate distance until reaching TIMEWINDOW
        schedule = Schedule()
        depot_dist_keys = list(DEPOT_DIST.keys())
        while trips != []:
            truck = None
        # 4a. Take out a trip whose pickup has the smallest depot_dist
            found = False
            while not found:
                pickup = depot_dist_keys[-l]
                for i in range(len(trips)):
                    if trips[i] .pickup == pickup:
        # 4b. Based on the load of this trip, select truck with the appropriate capacity
                        truck = Truck(CAPACITIES[bisect.bisect_left(CAPACITIES,trips[i].load)])
        # 4c. Add the trip to a route
                        route = Route(trips.pop(i), truck)
                        found = True
                        break
                    if not found:
                        depot_dist_keys.pop()
        #	4d. Keep merging until reaching TIME_WINDOW
        #	Only merge with trips that satisfy truck's capacity
            while True:
                last_dest = route.trips[-1].dests[-1]
                pickup_dist = {k : v for k, V in sorted(DISTANCES[last_dest].items(), key = lambda item : item[l], reverse = True)}
                merged = False
                while not merged and pickup_dist != {}:
                    item = pickup_dist.popitem()
                    for i in range(len(trips)):
                        if trips[i].pickup == item[0]:
                            if trips[i].load <= truck.capacity and ((item[l] + trips [i].distance + route.distance)/SPEED + route.loadtime + trips[i].loadtime) <= TIME__WINDOW:
                                route.add_trip(trips.pop(i))
                                merged = True
                                break
                if not merged:
                    break
        #	4e. Now that a route is completed, we add it to the schedule
            Schedule.add_route(route)
        #	5. Return schedule to phase 2
            return schedule
    
import random, copy, math

from phase_1 import greedy
#	Define global variables and parameters

SCHEDULE = greedy()
INITIAL_TEMP = 1000
DELTA = 0.95
MAX_ITER = 7000

def grasp():
    print_schedule(SCHEDULE)
    temperature = INITIAL_TEMP
    k=l
    # best SCHEDULE.distance
    i = 0
    iterations = [SCHEDULE]
    print('Initial distance: %.2f km.' %(SCHEDULE.distance))
    while temperature > l and k < MAX_ITER :
        sched = copy.deepcopy(iterations[-l])
        for route in sched.routes:
            sched.distance -= route.distance
            for idx, trip in enumerate(route.trips):
                if len(trip.dests) >= 2:
                    route.distance -= trip.distance
                    indexes = random.sample(range(len(trip.dests)), 2)
                    trip.swap_requests(*indexes)
                    route.distance += trip.distance
            sched.distance += route.distance
#print('Iteration %d. Temperature: %.2f. Total distance: %.2f km.' %(k, temperature, sched.distance))
#	Compare distance and Determine whether to accept this new schedule
    if sched.distance < best:
#print('\tAccept with new best.')
        best = sched.distance 
        iterations.append(sched)
        i = len(iterations) - 1
    else:
        u = random.random()
        p = math.e ** ((best-sched.distance)/temperature)
        if p > u:
#print('\tu = %.2f, p = %.2f .Accept with no new best.' %(u,p))
            Iterations.append(sched)
        else:
#print('\tu = %.2f, p = %.2f. Reject.' %(u, p))
            pass
# Increment variables
    Temperature *= DELTA
    k += 1
print('Phase 2 Complete. Current best distance: %.2f km. i = %d.' %(best, i + 1)) 
for idx, value in enumerate(iterations):
    print('%d.' %(idx + 1) + str(value))
def print_schedule(schedule): 
    print(schedule)
    for route in schedule.routes:
        print('-'*100)
        print(route)
        for trip in route.trips:
            print(trip)
    print('-'*100) 
    
grasp()
