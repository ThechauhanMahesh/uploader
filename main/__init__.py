#ChauhanMahesh/DroneBots/COL

from telethon import TelegramClient
from decouple import config
import logging
import time

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# variables
API_ID = 4796990
API_HASH = "32b6f41a4bf740efed2d4ce911f145c7"
BOT_TOKEN = "5089347286:AAEnZX3zLwmuDxaE253n3zaO04NsBxWft0Q"
BOT_UN = "TheUploaderProBot"
FORCESUB = int("-1001711957758")
FORCESUB_UN = "DroneBots"
ACCESS_CHANNEL = int("-1001879806908")
MONGODB_URI = "mongodb+srv://Vasusen:darkmaahi@cluster0.o7uqb.mongodb.net/cluster0?retryWrites=true&w=majority"
AUTH_USERS = 5351121397

#Connection
Drone = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 
