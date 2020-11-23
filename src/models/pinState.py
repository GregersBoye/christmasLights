import json
class PinState:
    def __init__(self, pinNo, state, name):
        self.pinNo = pinNo
        self.state = state
        self.name = name

    def serialize(self):
        return {"pinNo": self.pinNo, "HIGH":str(not self.state), "name":self.name}
