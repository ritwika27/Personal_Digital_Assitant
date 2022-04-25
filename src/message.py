from msg_enum import Msg_type

class Message():
    def __init__(self, **kwargs):
        self.msg = None
        self.msg_type = None
        self.sender = None
        self.receiver = None

        if len(kwargs) == 1:
            # Copying constroctor
            assert isinstance(args, Message)
            if isinstance(args, Message):
                self.msg = kwargs['msg'].get_msg()
                self.msg_type = kwargs['msg'].get_msg_type()
                self.sender = kwargs['msg'].get_sender()
                self.receiver = kwargs['msg'].get_receiver()
        elif len(kwargs) == 4 or len(kwargs) == 3:
            # Message(msg, type, sender, receiver)
            self.msg = kwargs['msg']
            self.msg_type = kwargs['msg_type']
            self.sender = kwargs['sender'] if 'sender' in kwargs else -1
            self.receiver = kwargs['receiver'] if 'receiver' in kwargs else -1
        else:
            raise "argument error"

    
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

    def reply(self, msg, msg_type):
        return Message(msg = msg, msg_type=msg_type, sender = self.receiver, receiver = self.sender)
