import pandas as pd
from ConvertIsoCountry import *
import random as rm
from System import *
import typing

"""
in this script my goal to automet the generation of the opject in this project so I could have in theory
all the world Airports, Airplans models and so on 

"""
# data wrangling 
airports_df = pd.read_csv("Data/airports.csv")
airports_df = airports_df[airports_df["country"].notna()]
airports_df["country"] = airports_df["country"].apply(convert_country_alpha2_to_country)
def gen_dates():
    """
    generate random days, hours, and minutes from the current date to a month in the futare
    """
    start = datetime.now()
    
    random_days = rm.randint(0, 30)
    random_hours = rm.randint(0, 23)
    random_minutes = rm.randint(0, 59)
    
    #get the random Date
    random_date = start + timedelta(days=random_days, hours=random_hours, minutes=random_minutes)
    return random_date
    

# init 10 airports 
def get_airport_info(iata_code:str):
    df = airports_df[airports_df["iata"] == iata_code]
    return df.name, df.country, df.city, df.lon, df.lat
list_iata = ["CAI", "DXB", "LHR", "LAX", "CDG", "FRA", "LAS", "ATL", "STN", "MAN"]
for iata in list_iata:
    name, country, city, lon, lat = get_airport_info(iata)
    # get the instance of the ten airports
    Airport(name, country, city, lon, lat)
    
# init 2 planes
planes_list = []
boeing_737 = Aeroplane("Boeing_737", 162, 917)
planes_list.append(boeing_737)
airbus_380 = Aeroplane("Airbus_380", 525, 902)
planes_list.append(airbus_380)

# generate  100 flight
def generate_flights(num_flights: int = 100) -> List[Flight]:
    """
    Generate a specified number of random flights.

    Args:
        num_flights (int): The number of flights to generate. Default is 100.

    Returns:
        List[Flight]: A list of generated Flight objects.
    """
    flights = []
    airports = Airport.get_all_instances()
    planes = Aeroplane.get_all_instances()
    
    # Create airline instances
    egyptair = EgyptAir("EgyptAir", 0.1, 2,50) 
    singapore_airlines = SingaporeAirlines("Singapore Airlines", 0.12, 4)  
    airlines = [egyptair, singapore_airlines]

    for _ in range(num_flights):
        # Randomly select departure and arrival airports
        leave, arrival = rm.sample(airports, 2)
        
        # Randomly select an airline and a plane
        airline = rm.choice(airlines)
        plane = rm.choice(planes)
        
        # Generate a random departure time
        leave_time = gen_dates()
        
        # Randomly select a flight class
        f_class = rm.choice([None, "Economy", "Business", "First Class"])
        
        # Create the flight
        flight = Flight(airline, plane, arrival, leave, leave_time, f_class)
        flights.append(flight)
    
    return flights

# Generate 100 flights
generated_flights = generate_flights(100)

# Print some information about the generated flights
for i, flight in enumerate(generated_flights[:5], 1):  # Print details of first 5 flights
    print(f"Flight {i}:")
    print(f"  From: {flight.leave.name} ({flight.leave.city}, {flight.leave.country})")
    print(f"  To: {flight.arrival.name} ({flight.arrival.city}, {flight.arrival.country})")
    print(f"  Airline: {flight.airline.name}")
    print(f"  Departure: {flight.leave_time}")
    print(f"  Arrival: {flight.arrival_time}")
    print(f"  Aircraft: {flight.aeroplane.model}")
    print(f"  Flight Cost: ${flight.flight_cost:.2f}")
    print(f"  Class: {flight.f_class or 'Not specified'}")
    print()

print(f"Total flights generated: {len(generated_flights)}")
