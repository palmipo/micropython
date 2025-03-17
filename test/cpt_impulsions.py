import time

if __name__=='__main__':
    try:
        from master.pia.piaisrpico import PiaIsrPico
        rc = PiaIsrPico(14, machine.Pin.PULL_UP, machine.Pin.IRQ_FALLING)
        fin = False
        while fin == False:
            if rc.isActivated() is True:
                print('validation')
            time.sleep(10)
    except KeyboardInterrupt:
        sys.exit()
