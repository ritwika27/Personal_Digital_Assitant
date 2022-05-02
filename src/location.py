import geocoder

class Location:
    def __init__(self, lat=None, lon=None, address=None):
        self.lat = lat
        self.lon = lon
        self.address = address

        if (address and not lat and not lon):
            g = geocoder.osm(address)
            self.lat = g.json['lat']
            self.lon = g.json['lng']

    def __str__(self):
        return "lat: {}\tlong: {}\taddress: {}".format(self.lat, self.lon, self.address)
