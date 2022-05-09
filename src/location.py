import geocoder

class Location:
  def __init__(self, lat=None, lon=None, address=None):
    self.lat = lat
    self.lon = lon
    self.address = address

  def coord_to_addr(self):
    self.address = geocoder.osm([self.lat, self.lon], method='reverse').json['address']


  def addr_to_coord(self):
    g = geocoder.osm(self.address).json
    self.lat = g['lat']
    self.lon = g['lng']

  def __str__(self):
    return "lat: {}\tlong: {}\taddress: {}".format(self.lat, self.lon, self.address)
