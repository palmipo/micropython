class RoueCodeuseEtat:
    def __init__(self, valeurA, valeurB):
        self.pinA = valeurA
        self.pinB = valeurB
        
    def transition(self, pinA, pinB):
        if (pinA == self.pinA):
            if (pinB == self.pinB):
                retrun 0
            else:
                retrun +1
        else:
            if (pinB == self.pinB):
                return -1
            else:
                return 0
