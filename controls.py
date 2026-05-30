# https://github.com/ikbenjepapa/VRC-transapp
# https://github.com/cyberkitsune/vrc-osc-scripts

from pythonosc import osc_server, udp_client
from pythonosc.dispatcher import Dispatcher

VRCHAT_IP = "127.0.0.1"
# VRCHAT_IP = "192.168.178.23"
VRCHAT_PORT = 9000
LISTEN_PORT = 9001

osc_client = udp_client.SimpleUDPClient(VRCHAT_IP, VRCHAT_PORT)
dispatcher = Dispatcher()

def handle_move_forward(url, value):
	vertical = float(value)
	print(f"Received {url}: {vertical}")
	osc_client.send_message("/input/Vertical", vertical)

def handle_move_back(url, value):
	vertical = float(value)
	print(f"Received {url}: {vertical}")
	osc_client.send_message("/input/Vertical", -vertical)

def handle_move_left(url, value):
	horizontal = float(value)
	print(f"Received {url}: {horizontal}")
	osc_client.send_message("/input/Horizontal", -horizontal)

def handle_move_right(url, value):
	horizontal = float(value)
	print(f"Received {url}: {horizontal}")
	osc_client.send_message("/input/Horizontal", horizontal)

def handle_jump(url, value):
	jump = float(value)
	print(f"Received {url}: {jump}")
	osc_client.send_message("/input/Jump", jump)

def handle_voice(url, value):
	voice = float(value)
	print(f"Received {url}: {voice}")
	osc_client.send_message("/input/Voice", voice)


osc_client.send_message("/input/Voice", 0.0)
osc_client.send_message("/input/Voice", 1.0)

dispatcher.map("/avatar/parameters/MoveForward", handle_move_forward)
dispatcher.map("/avatar/parameters/MoveBack", handle_move_back)
dispatcher.map("/avatar/parameters/MoveLeft", handle_move_left)
dispatcher.map("/avatar/parameters/MoveRight", handle_move_right)
dispatcher.map("/avatar/parameters/Jump", handle_jump)
dispatcher.map("/avatar/parameters/Voice", handle_voice)

server = osc_server.ThreadingOSCUDPServer((VRCHAT_IP, LISTEN_PORT), dispatcher)
print(f"Movement OSC bridge listening on {server.server_address}")
server.serve_forever()