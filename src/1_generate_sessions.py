from telethon.sync import TelegramClient
import time, os, json

from telethon.sync import TelegramClient
from telethon.sync import functions
from telethon.tl.types import InputBotAppShortName

from cache_data import SimpleCache

def getUrl(client: TelegramClient, peer: str, bot: str, url: str, platform: str = "ios", start_param: str = ""):
    return client(
        functions.messages.RequestWebViewRequest(
            peer=peer,
            bot=bot,
            platform=platform,
            url=url,
            from_bot_menu=False,
            start_param=start_param
        )
    )

def getAppUrl(client: TelegramClient, bot: str, platform: str = "ios", start_param: str = "", short_name: str = "start"):
    return client(
        functions.messages.RequestAppWebViewRequest(
            peer="me",
            app=InputBotAppShortName(bot_id=client.get_input_entity(bot), short_name=short_name),
            platform=platform,
            start_param=start_param
        )
    )

def cache_url(client, cache_db):
        blum_url = getAppUrl(
            client,
            'BlumCryptoBot',
            start_param=f'ref_pOBaesfYXS',
            short_name='app'
        ).url

        cache_db.set('blum_url', blum_url)
        print(f"[INFO] BlumCryptoBot URL fetched and cached: {blum_url}")
        time.sleep(6)


def create_client(config_id, api_id, api_hash):
    session_name = input(
        "Please enter a unique name for the session (like: session_25 or you can enter phone number):  ")

    print(f"[INFO] Creating Telegram client for session: {session_name}")
    client = TelegramClient(
        f'sessions/{session_name}',
        api_id,
        api_hash,
        device_model=f"All-In-One(MA)"
    )

    print("[INFO] Starting Telegram client...")
    client.start()

    client_id = client.get_me(True).user_id
    print(f"[INFO] Client started. User ID: {client_id}")

    cache_db = SimpleCache(config_id)
    cache_url(client, cache_db)
    cache_db.set("client_id", client_id)

    print("[INFO] Disconnecting Telegram client...")

    client.disconnect()

    print(f"\n\nSession {session_name} added and saved successfully! 🎉\n\n")


config = SimpleCache("config")
print('please add tg accounts in the same order as they exist')

global_config = SimpleCache('config')
if not global_config.get("api_key"):
    print('PLEASE PROVIDE API_KEY')
    raise Exception("Provide api_key")
if not len(global_config.get("api_hash")):
    print('PLEASE PROVIDE API_KEY')
    raise Exception("Provide api_hash")

for group_id in range(config.get("from_id"), config.get("to_id") + 1):
    print(f'dealing with group {group_id}')
    for id in range(config.get("accounts_in_one_tg_profile")):
        print(f'group {group_id}. account {id}')
        config_id = str(group_id) + "_" + str(id)
        client_config = SimpleCache(config_id)
        if client_config.is_empty():
            create_client(config_id, global_config.get("api_key"), global_config.get("api_hash"))
            time.sleep(1)
        else:
            print('already exist!')
