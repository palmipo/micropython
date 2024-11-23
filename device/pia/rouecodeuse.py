from master.pia.piaisrbouncepico import PiaIsrBouncePico
import time

class RoueCodeuse:
    def __init__(self, pinA, pinB, pinSelect):
        self.pinA = PiaIsrBouncePico(pinA)
        self.pinB = PiaIsrBouncePico(pinB)
        self.pinS = PiaIsrBouncePico(pinSelect)
        
        self.oldA = self.pinA.isActivated()
        self.oldB = self.pinB.isActivated()

    def isSelected(self):
        return self.pinS.isActivated()

# A B
# 0 0
# 0 1
# 1 1
# 1 0
    def isMoved(self):
        newA = self.pinA.isActivated()
        newB = self.pinB.isActivated()
        if (self.oldA == False) and (self.oldB == False):
            self.oldA = newA
            self.oldB = newB
            if (newA == False) and (newB == True):
                return 1
            elif (newA == True) and (newB == False):
                return -1
            else return 0

        elif (self.oldA == False) and (self.oldB == True):
            self.oldA = newA
            self.oldB = newB
            if (newA == True) and (newB == True):
                return 1
            elif (newA == False) and (newB == False):
                return -1
            else return 0

        elif (self.oldA == True) and (self.oldB == True):
            self.oldA = newA
            self.oldB = newB
            if (newA == True) and (newB == False):
                return 1
            elif (newA == False) and (newB == True):
                return -1
            else return 0

        elif (self.oldA == True) and (self.oldB == False):
            self.oldA = newA
            self.oldB = newB
            if (newA == False) and (newB == False):
                return 1
            elif (newA == True) and (newB == True):
                return -1
            else return 0

rc = RoueCodeuse(1, 2, 3)
fin = False
while fin == False:
    print('validation {}'.format(rc.isSelected()))
    print('rotation {}'.format(rc.isMoved()))
    time.sleep_ms(100)