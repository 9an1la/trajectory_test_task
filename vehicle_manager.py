from math import sin, cos, sqrt, radians, atan2
import requests


class Vehicle:
    def __init__(self, id, name, model, year, color, price, latitude, longitude):
        self.vehicle_id = id
        self.name = name
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"<Vehicle: {self.name} {self.model} {self.year} {self.color} {self.price}>"

    def __repr__(self):
        return f"<Vehicle: {self.name} {self.model} {self.year} {self.color} {self.price}>"


class VehicleManager:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_vehicles(self):
        response = requests.get(f'{self.base_url}/vehicles')
        vehicles_data = response.json()
        return [self.create_vehicle_from_data(vehicle_data) for vehicle_data in vehicles_data]

    def filter_vehicles(self, params):
        all_vehicles = self.get_vehicles()
        res = []

        for vehicle in all_vehicles:
            for key, value in params.items():
                if getattr(vehicle, key) == value:
                    res.append(vehicle)
        return res

    def get_vehicle(self, vehicle_id):
        response = requests.get(f'{self.base_url}/vehicles/{vehicle_id}')
        vehicle_data = response.json()
        return self.create_vehicle_from_data(vehicle_data)

    def add_vehicle(self, vehicle):
        vehicle_data = self.get_vehicle_data(vehicle)
        response = requests.post(f'{self.base_url}/vehicles', json=vehicle_data)
        return vehicle

    def update_vehicle(self, vehicle):
        vehicle_data = self.get_vehicle_data(vehicle)
        response = requests.put(f'{self.base_url}/vehicles/{vehicle.vehicle_id}', json=vehicle_data)
        return vehicle

    def delete_vehicle(self, id):
        response = requests.delete(f'{self.base_url}/vehicles/{id}')
        return response.status_code == 204


    def create_vehicle_from_data(self, vehicle_data):
        return Vehicle(vehicle_data['id'], vehicle_data['name'],
                       vehicle_data['model'], vehicle_data['year'],
                       vehicle_data['color'], vehicle_data['price'],
                       vehicle_data['latitude'], vehicle_data['longitude'])

    def get_vehicle_data(self, vehicle):
        return {
            'id': vehicle.vehicle_id,
            'name': vehicle.name,
            'model': vehicle.model,
            'year': vehicle.year,
            'color': vehicle.color,
            'price': vehicle.price,
            'latitude': vehicle.latitude,
            'longitude': vehicle.longitude
        }

    def get_distance(self, id1, id2):
        vehicle1 = self.get_vehicle(id1)
        vehicle2 = self.get_vehicle(id2)

        radius = float(6371)

        lat1 = radians(vehicle1.latitude)
        lon1 = radians(vehicle1.longitude)
        lat2 = radians(vehicle2.latitude)
        lon2 = radians(vehicle2.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = (c * radius)
        return distance

    def get_nearest_vehicle(self, id):
        vehicle1 = self.get_vehicle(id)
        nearest_vehicle = None
        min_distance = float('inf')
        all_vehicles = self.get_vehicles()

        for vehicle2 in all_vehicles:
            if vehicle1.vehicle_id != vehicle2.vehicle_id:
                distance = self.get_distance(id1=vehicle1.vehicle_id, id2=vehicle2.vehicle_id)
                if min_distance > distance:
                    min_distance = distance
                    nearest_vehicle = vehicle2
        return nearest_vehicle
