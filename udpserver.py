import socket
import soco
import logging
import json
import time
from datetime import datetime

# pulpeye_secrets to hold private information
from pulpeye_secrets import HOME

vnum = 0.60
vmsg = "re-write...  including local and remote Sonos"

hostname = socket.gethostname()


def update_Local_Sonos(delay):
	time.sleep(delay)
	track = sonos.get_current_track_info()
	SonosLocal['name'] = sonos.player_name
	SonosLocal['volume'] = sonos.volume
	SonosLocal['state'] = sonos.get_current_transport_info()['current_transport_state']
	SonosLocal['uri'] = track['uri']
	SonosLocal['title'] = track['title']
	SonosLocal['artist'] = track['artist']
	SonosLocal['album'] = track['album']
	
	
def print_Local_Sonos():
	print ()
	print ("Local Sonos: {:<13s} ".format(SonosLocal.get('name', 'no-name')))
	print ("      {} at {:3d}% level ".format( SonosLocal.get('state',''), SonosLocal.get('volume','0')))
	print ("      Title:  {} ".format(SonosLocal.get('title', 'no-title')))	
	print ("      URI:    {} ".format(SonosLocal.get('uri', 'no-uri')))		
	print ("      Artist: {} ".format(SonosLocal.get('artist', '')))
	print ("      Album:  {} ".format(SonosLocal.get('album', '')))
	print ()
	
	

sonos = soco.SoCo('192.168.2.135')

SonosLocal = dict()
update_Local_Sonos(1)
print_Local_Sonos()

local_sonos = dict()
local_sonos['name'] = sonos.player_name
local_sonos['na'] = sonos.player_name

UDP_IP = ""
UDP_PORT = 7777

HIT_COUNT = 0

home_msg = "udpserver calling home"
meta = {}
meta['records'] = 1
meta['command'] = 0
meta['show_meta'] = 1
meta['show_raw'] = 0
meta['log'] = "empty"
meta['host'] = hostname
out = {}
out['log'] = "Version {} calling home... ".format(vnum)
meta['extra_lines'] = 15
meta['show_meta'] = 0
meta['uri'] = 'lkj'
meta['records'] = 0
out['meta'] = meta
out['samples'] = 0
new_json = json.dumps(out, indent=2).encode(encoding='utf-8')


def call_home():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Send data
        sent = sock.sendto(new_json, HOME)
    finally:
        sock.close()

# Create and configure logger
LOG_FORMAT = '%(asctime)s:%(levelname)s:  %(message)s'
logging.basicConfig(filename= "PacketLogger.log",
                    level = logging.DEBUG,
                    format = LOG_FORMAT)
logger = logging.getLogger()
# logger.info('Packet Receiver rev0.0 started on: {}'.format(hostname))

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
print("UDP server listening on port: ",UDP_PORT)
print("version: ", vnum)
print("version message: ", vmsg)
print ()
call_home()
print ()
while True:
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

	# type(data)
	
	print("Hit...")

	jdata = json.loads(data.decode("utf-8"))
	samples = jdata.get('samples','')
	meta = jdata.get('meta','')
	Sonos = jdata.get('Sonos','')
	log = jdata.get('log','')
	logger.info(log)
	dt = datetime.now()
	
	HIT_COUNT += 1
	
	if meta['extra_lines'] > 0:
		for i in range(meta['extra_lines']):
			print ()
			
	print ("Packet Received: ", dt.strftime('%Y-%m-%d %H:%M:%S'), " from ", meta.get('host','none'))		
	print ("Track: {}".format(meta.get('track','none')))
	
	if meta['command'] == 3 and (Sonos['uri'].startswith("x-sonos") or Sonos['uri'].startswith("hls-radio") or Sonos['uri'].startswith("x-rincon")):
		try:
			sonos.play_uri(title="anytext",uri=Sonos.get('uri', 'empty'))
			#sonos.set
			meta['show_meta'] = 1
		finally:
			print ("Attempting to play uri: {}".format(meta.get('uri', 'empty')))
			print ()
			print ("Remote Sonos: {:<13s} ".format(Sonos.get('name', 'no-name')))
			print ("      {} at {:3d}% level ".format( Sonos.get('state',''), Sonos.get('volume','0')))
			print ("      Title:  {} ".format(Sonos.get('title', 'no-title')))
			print ("      URI:    {} ".format(Sonos.get('uri', 'no-title')))
			
			print ("      Artist: {} ".format(Sonos.get('artist', '')))
			print ("      Album:  {} ".format(Sonos.get('album', '')))
			
			print ()
			print ("Hit Count: {}".format(HIT_COUNT))
			print ()
			update_Local_Sonos(5)
			print_Local_Sonos()

	if (meta['show_raw'] == 1):
		print ("received: ", data)
		print ()
		print ("Packet Received: ", dt.strftime('%Y-%m-%d %H:%M:%S'), " from ", meta.get('host','none'))

	if meta['show_meta'] == 1:
		print ("Meta:   ", meta)
		print ("Sonos:   ", Sonos)

	if meta['records'] > 0:
		print ("Sample: ", samples)
		print ("Log:    ", log)

	for i in range(1):
		print ()

	

