

class Event():
  def __init__(self, event_id, preference, event_location, user_location, start_time, end_time, title, description):
    self.event_id = event_id
    self.preference = preference
    self.event_location = event_location
    self.user_location = user_location
    self.start_time = start_time
    self.end_time = end_time
    self.title = title
    self.description = description
    self.estimate = None # type datetime.timedelta


  def __str__(self):
    return "(event_id: {}, preference: {}, event_location: {}, user_location: {}, start_time: {}, end_time: {}, title: {}, description: {})".format(self.event_id, self.preference, self.event_location.__str__(), self.user_location.__str__(), self.start_time, self.end_time, self.title, self.description)
