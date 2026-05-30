import asyncio
import os
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
import obsws_python as obs
from dotenv import load_dotenv

# Load environment from .env (if present)
load_dotenv()

# --- CONFIGURATION ---
OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PASSWORD = os.getenv("OBS_PASSWORD")
MIC_SOURCE_NAME = "Microphone"  # Exact name of your mic source in OBS
# ---------------------

# OBS client will be initialized in main to avoid connecting on import
obs_client = None

def on_vrc_mute(address, *args):
    is_muted = args[0]  # Returns True if muted in VRChat, False if unmuted
    try:
        if obs_client is None:
            print("OBS client not initialized yet; ignoring mute event")
            return
        obs_client.set_input_mute(MIC_SOURCE_NAME, is_muted)
        status = "MUTED" if is_muted else "UNMUTED"
        print(f"[VRChat] Syncing mute status: OBS Mic is now {status}")
    except Exception as e:
        print(f"Failed to communicate with OBS: {e}")

# Set up OSC Listener for VRChat's mute network address
dispatcher = Dispatcher()
dispatcher.map("/avatar/parameters/MuteSelf", on_vrc_mute)

async def init_main():
    global obs_client
    # Initialize OBS WebSocket client inside main
    try:
        obs_client = obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD)
        print("Successfully connected to OBS WebSocket!")
    except Exception as e:
        print(f"Could not connect to OBS: {e}")
        # continue running the OSC listener even if OBS isn't available

    # VRChat transmits OSC out on port 9001 by default
    server = AsyncIOOSCUDPServer(("127.0.0.1", 9001), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    print("Bridge is running! Listening for VRChat Mute toggles...")
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(init_main())

