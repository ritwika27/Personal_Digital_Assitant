class Location:
    def __init__(self, lat=None, lon=None, address=None):
        self.lat = lat
        self.lon = lon
        self.address = address

    def __str__(self):
        return "lat: {}\tlong: {}\taddress: {}".format(self.lat, self.lon, self.address)
