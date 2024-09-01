from abc import ABC, abstractmethod
from math import sin, cos, sqrt, atan2, radians
from datetime import datetime, timedelta
from typing import List


all_instances = {}

class BaseClass(ABC):
    """    
    abstract class to ensure that every object has to_dict 
    and from_dict methodes
    
    """
    def __init__(self):
        cls = self.__class__
        if cls not in all_instances:
            all_instances[cls] = []
        all_instances[cls].append(self)
    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> 'BaseClass':
        pass
    @classmethod
    def get_all_instances(cls):
        return all_instances.get(cls, [])
    
class Airline(BaseClass):
    def __init__(self, name:str, base_cost:float):
        super().__init__()
        self.name:str = name
        self.base_cost:float = base_cost
    @abstractmethod
    def get_services(self):
        pass
    def to_dict(self) -> dict:
       return {
           'name': self.name,
           'base_cost': self.base_cost
               }

    @classmethod
    def from_dict(cls, data: dict) -> 'Airline':
        return cls(data['name'])
    
class Airport(BaseClass):
    def __init__(self, name:str, country:str, city:str, longitude:float, latitude:float):
        super().__init__()
        self.name:str = name
        self.country:str = country
        self.city = city
        self.longitude:float = longitude
        self.latitude:float = latitude
    @staticmethod    
    def get_distance(l_airport, ar_airport):
        # Approximate radius of earth in km
        R = 6373.0

        lat1 = radians(l_airport.latitude.iloc[0])
        lon1 = radians(l_airport.longitude.iloc[0])
        lat2 = radians(ar_airport.latitude.iloc[0])
        lon2 = radians(ar_airport.longitude.iloc[0])


        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        print("Result: ", "{:.2f}".format(distance) + "km")
        return distance
        
    def to_dict(self) -> dict:
       return {
           'name': self.name,
           'country': self.country,
           'city': self.city,
           'logitude': self.longitude,
           'latitude': self.latitude
           }

    @classmethod
    def from_dict(cls, data: dict) -> 'Airport':
        return cls(data['location'])   
    def __str__(self):
        return str(self.name)
class Aeroplane(BaseClass):
    __uni_plan = 0
    def __init__(self, model:str, n_seats:int, speed:float):
        super().__init__()
        self.model:str = model
        self.speed:float = speed
        self.n_seats:int = n_seats
        self.available_seats:int = n_seats
        self.plane_code = "P" + "0"*(5 - len(str(Aeroplane.__uni_plan))) + str(Aeroplane.__uni_plan)+ "X"
        Aeroplane.__uni_plan += 1
    def book_plane(self):
        self.available_seats -= 1
    
    def to_dict(self) -> dict:
       return {
           'model': self.model,
           'number_of_seats': self.n_seats,
           'speed': self.speed,
           'available_seats': self.available_seats
           }

    @classmethod
    def from_dict(cls, data: dict) -> 'Airline':
        return cls(data['model'], data["number of seats"])
    
class Flight(BaseClass):
    __uni_code = 0
    def __init__(self, airline:Airline, aeroplane:Aeroplane, arrival:Airport,
                 leave:Airport, leave_time:datetime, f_class:str = None):
        super().__init__()
        self.flight_code =  str(Flight.__uni_code) + (5 - len(str(Flight.__uni_code)))*"0" + "x"
        self.aeroplane:Aeroplane = aeroplane
        self.airline:Airline = airline
        self.arrival:Airport = arrival
        self.leave:Airport = leave
        self.leave_time:datetime = leave_time
        self.arrival_time:datetime = self.__arrivaltimecalc()
        self.flight_cost = self.__costcalc() 
        self.f_class:str = f_class
    
        Flight.__uni_code =+ 1
    def __costcalc(self):
        """
        calculate the cost of the flieght
        """
        icost = Airport.get_distance(self.leave, self.arrival)*self.airline.base_cost
        
        return icost
    def __arrivaltimecalc(self):
        distance = Airport.get_distance(self.leave, self.arrival)
        time_hours = distance / self.aeroplane.speed
        hours = int(time_hours)
        minutes = int((time_hours - hours) * 60)
        return self.leave_time + timedelta(hours=hours, minutes=minutes)

    
    
    def to_dict(self) -> dict:
        return {
            'flight_code': self.flight_code,
            'aeroplane': self.aeroplane.to_dict(),
            'airline': self.airline.to_dict(),
            'departure': self.leave.to_dict(),
            'arrival': self.arrival.to_dict(),
            'departure_time': self.leave_time.isoformat(),
            'arrival_time': self.arrival_time.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Flight':
        return cls(
            Airline.from_dict(data['airline']),
            Aeroplane.from_dict(data['aeroplane']),
            Airport.from_dict(data['arrival']),
            datetime.fromisoformat(data['arrival_time']),
            Airport.from_dict(data['departure']),
            datetime.fromisoformat(data['departure_time']),
        )
    
    
    
    
    
    def __str__(self):
        txt = f"""
        you booked a flight form {self.leave} airport to {self.arrival} airport
        the flight will take off on {self.leave_time} and arrive on {self.arrival_time}
        the code of the flight is {self.flight_code}
        """
        return txt
         
         
class passenger:
    
    def __init__(self, name:str, palance_acount:float, phone_number:str = None):
        self.name = name
        self.palance_acount = palance_acount
        self.phone_number:str = phone_number
        
    def pay(self, service_price):
        self.palance_acount -= service_price
class EgyptAir(Airline):        
    def __init__(self, name:str, base_cost:float ,baggage_kg_fees:float, cancellation_fees:int):  
        super().__init__(name, base_cost)
        self.baggage_kg_fees:float = baggage_kg_fees
        self.cancellation_fees = cancellation_fees
        
    def baggage_fees(self, kgs):
        return self.baggage_kg_fees * kgs
    
    def get_services():
        print("EgyptAir will provide you with this services")
        print("""
              1.Priority Boarding
              2.Extra Legroom
              3.Premium Snacks
              """)
        
class SingaporeAirlines(Airline):        
    def __init__(self, name:str, base_cost:float, baggage_kg_fees:float):  
        super().__init__(name, base_cost)
        self.baggage_kg_fees:float = baggage_kg_fees
    def baggage_fees(self, kgs):
        return self.baggage_kg_fees * kgs        
    def get_services():
        print("Singapore Airlines will provide you with this services")
        print("""
              1.wifi
              2.In-flight Entertainment
              3.Lounge Access
              """)          
    
class BookingSystem:
    """
     Ask the passenger which country they want to travel to
     Display the available flights to the chosen destination (e.g., 100 flights)
     Show all relevant information for each flight, such as dates and costs
     Book the flight 
    """
    def __init__(self):
        pass
    
  
         
        