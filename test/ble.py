import bluetooth
from micropython import const
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)
_IRQ_GATTS_INDICATE_DONE = const(20)
_IRQ_MTU_EXCHANGED = const(21)
_IRQ_L2CAP_ACCEPT = const(22)
_IRQ_L2CAP_CONNECT = const(23)
_IRQ_L2CAP_DISCONNECT = const(24)
_IRQ_L2CAP_RECV = const(25)
_IRQ_L2CAP_SEND_READY = const(26)
_IRQ_CONNECTION_UPDATE = const(27)
_IRQ_ENCRYPTION_UPDATE = const(28)
_IRQ_GET_SECRET = const(29)
_IRQ_SET_SECRET = const(30)
_GATTS_NO_ERROR = const(0x00)
_GATTS_ERROR_READ_NOT_PERMITTED = const(0x02)
_GATTS_ERROR_WRITE_NOT_PERMITTED = const(0x03)
_GATTS_ERROR_INSUFFICIENT_AUTHENTICATION = const(0x05)
_GATTS_ERROR_INSUFFICIENT_AUTHORIZATION = const(0x08)
_GATTS_ERROR_INSUFFICIENT_ENCRYPTION = const(0x0f)
_PASSKEY_ACTION_NONE = const(0)
_PASSKEY_ACTION_INPUT = const(2)
_PASSKEY_ACTION_DISPLAY = const(3)
_PASSKEY_ACTION_NUMERIC_COMPARISON = const(4)

class Xiaomi:
    def __init__(self):
        self.status = 0
        self.connected = False
        self.handler = 64
        self.scan_list = {}
        self.scan_done = False
        self.characteristics_list = []
        self.characteristics_done = False
        self.read_list = []
        self.read_done = False

        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self.callback)
        self.ble.gap_advertise(625)

    def callback(self, event, data):
        print('callback {}, {}'.format(event, data))
#         if event == _IRQ_CENTRAL_CONNECT:
#             print('A central has connected to this peripheral.')
#             conn_handle, addr_type, addr = data
#             
#         elif event == _IRQ_CENTRAL_DISCONNECT:
#             print('A central has disconnected from this peripheral.')
#             conn_handle, addr_type, addr = data
#             
#         elif event == _IRQ_GATTS_WRITE:
#             print('A client has written to this characteristic or descriptor.')
#             conn_handle, attr_handle = data
#             
#         elif event == _IRQ_GATTS_READ_REQUEST:
#             print('A client has issued a read. Note: this is only supported on STM32.')
#             # Return a non-zero integer to deny the read (see below), or zero (or None)
#             # to accept the read.
#             conn_handle, attr_handle = data
#             
        if event == _IRQ_SCAN_RESULT:
            print('A single scan result.')
            (addr_type, addr, adv_type, rssi, adv_data) = data
            self.scan_list[ bytes(addr) ] = (addr_type, adv_type, rssi, bytes(adv_data))

        elif event == _IRQ_SCAN_DONE:
            print('Scan duration finished or manually stopped.')
            self.scan_done = True

        elif event == _IRQ_PERIPHERAL_CONNECT:
            print('A successful gap_connect().')
            (conn_handle, addr_type, addr) = data
            self.handler = conn_handle
            self.connected = True

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            print('Connected peripheral has disconnected.')
            conn_handle, addr_type, addr = data
            if self.handler == conn_handle:
                self.connected = False
# 
#         elif event == _IRQ_GATTC_SERVICE_RESULT:
#             print('Called for each service found by gattc_discover_services().')
#             conn_handle, start_handle, end_handle, uuid = data
#             
#         elif event == _IRQ_GATTC_SERVICE_DONE:
#             print('Called once service discovery is complete.')
#             # Note: Status will be zero on success, implementation-specific value otherwise.
#             conn_handle, status = data
#             
        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            print('Called for each characteristic found by gattc_discover_services().')
            conn_handle, end_handle, value_handle, properties, uuid = data
            self.characteristics_list.append( (value_handle, properties) )
    
        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            print('Called once service discovery is complete.')
            # Note: Status will be zero on success, implementation-specific value otherwise.
            conn_handle, status = data
            if self.handler == conn_handle:
                self.characteristics_done = True
                self.status = status
#             
#         elif event == _IRQ_GATTC_DESCRIPTOR_RESULT:
#             print('Called for each descriptor found by gattc_discover_descriptors().')
#             conn_handle, dsc_handle, uuid = data
#             
#         elif event == _IRQ_GATTC_DESCRIPTOR_DONE:
#             print('Called once service discovery is complete.')
#             # Note: Status will be zero on success, implementation-specific value otherwise.
#             conn_handle, status = data
#             
        elif event == _IRQ_GATTC_READ_RESULT:
            print('A gattc_read() result.')
            conn_handle, value_handle, char_data = data
            self.read_list.append( (conn_handle, value_handle, bytes(char_data)) )
            print(conn_handle, value_handle, bytes(char_data))
            
        elif event == _IRQ_GATTC_READ_DONE:
            print('A gattc_read() has completed.')
            # Note: Status will be zero on success, implementation-specific value otherwise.
            conn_handle, value_handle, status = data
            if self.handler == conn_handle:
                self.read_done = True
                self.status = status

#         elif event == _IRQ_GATTC_WRITE_DONE:
#             print('A gattc_write() has completed.')
#             # Note: Status will be zero on success, implementation-specific value otherwise.
#             conn_handle, value_handle, status = data
#             
#         elif event == _IRQ_GATTC_NOTIFY:
#             print('A server has sent a notify request.')
#             conn_handle, value_handle, notify_data = data
#             
#         elif event == _IRQ_GATTC_INDICATE:
#             print('A server has sent an indicate request.')
#             conn_handle, value_handle, notify_data = data
#             
#         elif event == _IRQ_GATTS_INDICATE_DONE:
#             print('A client has acknowledged the indication.')
#             # Note: Status will be zero on successful acknowledgment, implementation-specific value otherwise.
#             conn_handle, value_handle, status = data
#             
#         elif event == _IRQ_MTU_EXCHANGED:
#             print('ATT MTU exchange complete (either initiated by us or the remote device).')
#             conn_handle, mtu = data
#             
#         elif event == _IRQ_L2CAP_ACCEPT:
#             print('A new channel has been accepted.')
#             # Return a non-zero integer to reject the connection, or zero (or None) to accept.
#             conn_handle, cid, psm, our_mtu, peer_mtu = data
#             
#         elif event == _IRQ_L2CAP_CONNECT:
#             print('A new channel is now connected (either as a result of connecting or accepting).')
#             conn_handle, cid, psm, our_mtu, peer_mtu = data
#             
#         elif event == _IRQ_L2CAP_DISCONNECT:
#             print('Existing channel has disconnected (status is zero), or a connection attempt failed (non-zero status).')
#             conn_handle, cid, psm, status = data
#             
#         elif event == _IRQ_L2CAP_RECV:
#             print('New data is available on the channel. Use l2cap_recvinto to read.')
#             conn_handle, cid = data
#             
#         elif event == _IRQ_L2CAP_SEND_READY:
#             print('A previous l2cap_send that returned False has now completed and the channel is ready to send again.')
#             # If status is non-zero, then the transmit buffer overflowed and the application should re-send the data.
#             conn_handle, cid, status = data
#             
#         elif event == _IRQ_CONNECTION_UPDATE:
#             print('The remote device has updated connection parameters.')
#             conn_handle, conn_interval, conn_latency, supervision_timeout, status = data
#             
#         elif event == _IRQ_ENCRYPTION_UPDATE:
#             print('The encryption state has changed (likely as a result of pairing or bonding).')
#             conn_handle, encrypted, authenticated, bonded, key_size = data
#             
#         elif event == _IRQ_GET_SECRET:
#             # Return a stored secret.
#             # If key is None, return the index'th value of this sec_type.
#             # Otherwise return the corresponding value for this sec_type and key.
#             sec_type, index, key = data
#             return value
#         
#         elif event == _IRQ_SET_SECRET:
#             # Save a secret to the store for this sec_type and key.
#             sec_type, key, value = data
#             return True
#         
#         elif event == _IRQ_PASSKEY_ACTION:
#             # Respond to a passkey request during pairing.
#             # See gap_passkey() for details.
#             # action will be an action that is compatible with the configured "io" config.
#             # passkey will be non-zero if action is "numeric comparison".
#             conn_handle, action, passkey = data

    def scan(self, timeout):
        self.scan_done = False
        self.ble.gap_scan(0)
        time.sleep(timeout)
        self.ble.gap_scan(None)
        while (self.scan_done == False):
            time.sleep(1)
        for elem in self.scan_list:
            print('{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))
        return self.scan_list


    def connect(self, addr_type, addr):
        self.ble.gap_connect(addr_type, addr)
        cpt = 0
        while(self.connected == False) and (cpt < 10):
            time.sleep(1)
            cpt += 1
        return self.connected
        
    def disconnect(self):
        self.ble.gap_disconnect(self.handler)
        cpt = 0
        while(self.connected == True) and (cpt < 10):
            time.sleep(1)
            cpt += 1
        return self.connected

    def read_characteristics(self, start_handle, end_handle, uuid=None):
        self.characteristics_done = False
        if self.connected == True:
            self.ble.gattc_discover_characteristics(self.handler, start_handle, end_handle, uuid)
            cpt = 0
            while(self.characteristics_done == False) and (cpt < 10):
                time.sleep(1)
                cpt += 1
        return self.characteristics_list

    def read(self, value_handle):
        self.read_done = False
        if self.connected == True:
            self.ble.gattc_read(self.handler, value_handle)
            cpt = 0
            while(self.read_done == False) and (cpt < 10):
                time.sleep(1)
                cpt += 1
        return self.read_list

        
import time, struct
ble = Xiaomi()
try:
    lscan = ble.scan(60)
    for elem in lscan:
        ble.connect(1, elem)
        # ble.connect(1, b'\xa4\xc1\x38\x75\x6d\xd7') # LYWSD03MML
        # if True == ble.connect(1, b'\xC6\x41\x41\xB4\x54\xC3'): # fly_pad
        print('-> read_characteristics')
        lst = ble.read_characteristics(0x0001, 0xffff, bluetooth.UUID('ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6')) # LYWSD03MML
        # lst = ble.read_characteristics(0x0001, 0xffff, bluetooth.UUID('9e35fa01-4344-44d4-a2e2-0c7f6046878b')) # fly_pad
        print('<- read_characteristics')
        if size(lst) != 0:
            print(lst)
            print('-> read')
            res = ble.read(lst[0][1])
            print(res[0][2])
            print(struct.unpack('<BBBBBB', res[0][2]))
            print('<- read')
    print(ble.connected)
finally:
    ble.disconnect()
    print('FIN.')
 