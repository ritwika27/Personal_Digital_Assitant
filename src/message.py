from msg_enum import Msg_type

class Message():
    def __init__(self, *args):
        self.msg = None
        self.msg_type = None
        self.sender = None
        self.receiver = None
        self.message_direction = None

        if len(args) == 1:
            if isinstance(args, Message):
                self.msg = args.get_msg()
                self.msg_type = args.get_msg_type()
                self.sender = args.get_sender()
                self.receiver = args.get_receiver()
                self.message_direction = args.get_message_direction()
        elif len(args) == 
    
    def get_msg(self):
        return self.msg

    def get_msg_type(self):
        return self.msg_type

    def get_sender(self):
        return self.sender

    def get_receiver(self):
        return self.receiver

    def get_message_direction(self):
        return self.message_direction
