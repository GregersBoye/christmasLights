import json
class PinState:
    def __init__(self, pinNo, state):
        self.pinNo = pinNo
        self.state = state

    def serialize(self):
        return {"pinNo": self.pinNo, "HIGH":str(not self.state)}
