import device.artnet.ArtNet

class ArtDmx(ArtNet):
	super().__init__(0x5000, 0, 0)