#           Baz's Macro/SolsRNGBot
#   A discord bot for macroing Sol's RNG on Roblox
#   Version: 1.1.9 PREVIEW
#   https://github.com/bazthedev/SolsRNGBot
#

import os
import discord
from discord.ext import commands, tasks
import pyautogui as pag
from datetime import datetime
import json
from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key
import asyncio
from PIL import ImageGrab
import requests
import logging
import screeninfo as si
import re
import glob
import shutil
import tempfile
import psutil
import random
try:
    import mousekey as mk
except ModuleNotFoundError:
    print("You need to install mousekey, by running pip install mousekey. After pressing any key, this should automatically happen, however if it does not, please run pip install mousekey.")
    os.system("pause")
    os.system("py -m pip install mousekey")
    exit("Mousekey should be installed, try running the macro again now.")

from aiohttp import ClientSession
import subprocess
import typing
from websockets import connect

mkey = mk.MouseKey()
MACROPATH = os.path.expandvars(r"%localappdata%\Baz's Macro") # Windows Roaming Path
LOCALVERSION = "1.1.9"
PRERELEASE = True
if PRERELEASE:
    print(f"Warning! This is a prerelease version of SolsRNGBot, meaning you can expect bugs and some errors to occur!\nYou can find logs relating to events that occur during the prerelease in this folder: {MACROPATH}\n\nYou are currently running prerelease for version {LOCALVERSION}, are you sure you wish to continue?")
    input("Press ENTER to continue using the macro: ")
DEFAULTSETTINGS = {"TOKEN": "", "__version__" :  LOCALVERSION, "log_channel_id": 0, "use_rblx_player" : True, "global_wait_time" : 0.1, "skip_dl": False, "mention" : True, "mention_id" : 0, "minimum_roll" : "99998", "minimum_ping" : "349999", "reset_aura" : "", "merchant_detection" : False, "send_mari" : True, "ping_mari" : False, "send_jester" : True, "ping_jester" : True, "auto_purchase_items" : {"Void Coin/Lucky Penny" : True}, "glitch_detector" : True, "ping_on_glitch" : True, "pop_in_glitch" : False, "auto_use_items_in_glitch": {"Heavenly Potion II" : {"use" : True, "amount" : 200}, "Fortune Potion III" : {"use" : True, "amount" : 1}, "Lucky Potion" : {"use" : True, "amount" : 10}, "Pumpkin" : {"use" : True, "amount" : 10}, "Haste Potion III" : {"use" : False, "amount" : 1}, "Warp Potion" : {"use" : True, "amount" : 1}, "Transcended Potion" : {"use" : False, "amount" : 1}, "Mixed Potion" : {"use" : True, "amount" : 10}, "Stella's Candle" : {"use" : True, "amount" : 1}, "Santa Claus Potion" : {"use" : True, "amount" : 5}, "Hwachae" : {"use" : True, "amount" : 1}}, "dreamspace_detector" : True, "ping_on_dreamspace" : True, "pop_in_dreamspace" : False, "auto_use_items_in_dreamspace" : {"Heavenly Potion II" : {"use" : False, "amount" : 1}, "Fortune Potion III" : {"use" : True, "amount" : 1}, "Lucky Potion" : {"use" : True, "amount" : 10}, "Pumpkin" : {"use" : True, "amount" : 10}, "Haste Potion III" : {"use" : False, "amount" : 1}, "Warp Potion" : {"use" : True, "amount" : 1}, "Transcended Potion" : {"use" : False, "amount" : 1}, "Mixed Potion" : {"use" : True, "amount" : 10}, "Stella's Candle" : {"use" : True, "amount" : 1}, "Santa Claus Potion" : {"use" : True, "amount" : 5}, "Hwachae" : {"use" : True, "amount" : 1}}, "auto_craft_mode" : False, "skip_auto_mode_warning" : False, "auto_craft_item" : {"Heavenly Potion I" : False, "Heavenly Potion II" : True, "Warp Potion" : False}, "auto_biome_randomizer" : False, "auto_strange_controller" : False, "edit_settings_mode" : True, "failsafe_key" : "ctrl+e", "merchant_detec_wait" : 0, "ps_server_link" : "", "legacy_aura_detection" : False, "take_screenshot_on_detection" : False, "ROBLOSECURITY_KEY" : "", "DISCORD_TOKEN" : "", "collect_items" : {"1" : False, "2" : False, "3" : False, "4" : False}, "sniper_enabled" : False, "sniper_toggles" : {"Glitched" : True, "Dreamspace" : False}, "sniper_channel_id" : 0, "sniper_logs" : True, "change_cutscene_on_pop" : True, "disable_autokick_prevention" : False}
VALIDSETTINGSKEYS = ["TOKEN", "__version__", "log_channel_id", "use_rblx_player", "global_wait_time", "skip_dl", "mention", "mention_id", "minimum_roll", "minimum_ping", "reset_aura", "merchant_detection", "send_mari", "ping_mari", "send_jester", "ping_jester", "auto_purchase_items", "glitch_detector", "ping_on_glitch", "pop_in_glitch", "auto_use_items_in_glitch", "dreamspace_detector", "ping_on_dreamspace", "pop_in_dreamspace", "auto_use_items_in_dreamspace", "auto_craft_mode", "skip_auto_mode_warning", "auto_craft_item", "auto_biome_randomizer", "auto_strange_controller", "edit_settings_mode", "failsafe_key", "merchant_detec_wait", "ps_server_link", "legacy_aura_detection", "take_screenshot_on_detection", "ROBLOSECURITY_KEY", "DISCORD_TOKEN", "sniper_enabled", "sniper_toggles", "collect_items", "sniper_channel_id", "sniper_logs", "change_cutscene_on_pop", "disable_autokick_prevention"]
PLACE_ID = 15532962292
BASE_ROBLOX_URL = f"https://www.roblox.com/games/{PLACE_ID}/Sols-RNG-Eon1-1"
DISCORD_WS_BASE = "wss://gateway.discord.gg/?v=10&encoding-json"
SHARELINKS_API = "https://apis.roblox.com/sharelinks/v1/resolve-link"
STARTUP_MSGS = ["Let's go gambling!", "Nah, I'd Roll", "I give my life...", "Take a break", "Waste of time", "I can't stop playing this", "Touch the grass", "Eternal time...", "Break the Reality", "Finished work for today", "When is payday???", "One who stands before God", "Flaws in the world", "We do a little bit of rolling", "Exotic Destiny", "Always bet on yourself", "Is that a Mari I hear?", "(Lime shivers quietly in the cold)", "There's no way to stop it!"]

detected_snipe = False

# THE FOLLOWING CODE IS A SLIGHTLY MODIFIED VERSION OF YAY JOINS SNIPER 1.2.10, WHICH IS OWNED BY Root1527. YOU CAN DOWNLOAD THE REGULAR VERSION OF YAY JOINS HERE: https://github.com/Root1527/yay-joins

class Sniper:
    def __init__(self):
        self.config = self._load_config()
        self.roblox_session: typing.Optional[ClientSession] = None
        self._refresh_task = None
        self.output_list = []
        self.is_running = True

        self.words = ["Glitched", "Dreamspace"]

        self.link_pattern = re.compile(
            f"https://www.roblox.com/games/{PLACE_ID}/Sols-RNG-Eon1-1\\?privateServerLinkCode="
        )
        self.link_pattern_2 = re.compile(r"https://.*&type=Server")

        self.blacklists = [
            re.compile(pattern)
            for pattern in [
                "need|want|lf|look|stop|how|bait|ste|snip|fak|real|pl|hunt|sho|sea|wait|tho|gone|think|ago|prob|try|dev|adm|or|see|cap|tot|is|us|spa|giv|get|hav|and|str|sc|br|rai|wi|san|star|null|pm|gra|pump|moon|scr|mac|do|did|jk|no|rep|dm|farm|sum|who|if|imag|pro|bot|next|post|was|bae|fae",
                "need|want|lf|look|stop|how|bait|ste|snip|fak|real|pl|hunt|sho|sea|wait|tho|gone|think|ago|prob|try|dev|adm|or|see|cap|tot|is|us|giv|get|hav|and|str|br|rai|wi|san|star|null|pm|gra|pump|moon|scr|mac|do|did|jk|no|rep|dm|farm|sum|who|if|imag|pro|bot|next|post|was|bae|fae",
            ]
        ]
        self.word_patterns = [
            re.compile(pattern)
            for pattern in [r"g[liotc]+h", r"d[rea]+ms"]
        ]

    def _load_config(self):
        with open(f"{MACROPATH}/settings.json", "r") as f:
            config = json.load(f)
        return config

    async def setup(self):
        self.roblox_session = ClientSession()
        self.roblox_session.cookie_jar.update_cookies(
            {".ROBLOSECURITY": self.config["ROBLOSECURITY_KEY"]}
        )

    async def _identify(self, ws):
        try:
            identify_payload = {
                "op": 2,
                "d": {
                    "token": self.config["DISCORD_TOKEN"],
                    "properties": {"$os": "windows", "$browser": "chrome", "$device": "pc"}
                }
            }
            await ws.send(json.dumps(identify_payload))
        except Exception as e:
            if self.config["sniper_logs"]:
                print(f"[SNIPER] Error: {e}")
        
    async def _subscribe(self, ws):
        subscription_payload = {
            "op": 14,
            "d": {
                    "guild_id": "1186570213077041233",
                    "channels_ranges": {},
                    "typing": True,
                    "threads": False,
                    "activities": False,
                    "members": [],
                    "thread_member_lists": []
                }
            }
        await ws.send(json.dumps(subscription_payload))

    async def heartbeat(self, ws, interval):
        while True:
            try:
                heartbeat_json= {
                    'op':1,
                    'd': 'null'
                }
                await ws.send(json.dumps(heartbeat_json))
                await asyncio.sleep(interval)
            except Exception as e:
                if self.config["sniper_logs"]:
                    print(f"[SNIPER] Error: {e}")

    async def _on_message(self, ws):
        while True:
            event = json.loads(await ws.recv())
            try:
                if event["t"] == "MESSAGE_CREATE":
                    channel_id = event["d"]["channel_id"]
                    content = event["d"]["content"]
                    for choice_id in self.cycle_index:
                        if int(channel_id) == [1282542323590496277, 1282542323590496277][choice_id]:
                            await self.process_message(content, choice_id)
            except Exception as e:
                if self.config["sniper_logs"]:
                    print(f"[SNIPER] Error: {e}")

    def _should_process_message(self, message: str, choice_id: int) -> bool:          
        if not self.word_patterns[choice_id].search(message.lower()):
            return False

        if self.blacklists[choice_id].search(message.lower()):
            if self.config["sniper_logs"]:
                print(f"[SNIPER] Filtered message! content: {message}")
            return False

        return True

    async def _extract_server_code(self, message: str) -> typing.Optional[str]:
        if link_match := self.link_pattern.search(message):
            return link_match.group(0).split("LinkCode=")[-1]

        if link_match_2 := self.link_pattern_2.search(message):
            share_code = link_match_2.group(0).split("code=")[-1].split("&")[0]
            return await self._convert_link(share_code)
        print("nothing")
        return None

    async def _convert_link(self, link_id: str) -> typing.Optional[str]:
        payload = {"linkId": link_id, "linkType": "Server"}

        async with self.roblox_session.post(SHARELINKS_API, json=payload) as response:
            if response.status == 403 and "X-CSRF-TOKEN" in response.headers:
                self.roblox_session.headers["X-CSRF-TOKEN"] = response.headers[
                    "X-CSRF-TOKEN"
                ]
                async with self.roblox_session.post(
                    SHARELINKS_API, json=payload
                ) as retry_response:
                    data = await retry_response.json()
            else:
                data = await response.json()

        if data["privateServerInviteData"]["placeId"] != PLACE_ID:
            if self.config["sniper_logs"]:
                print("[SNIPER] Filtered non-sols link!")
            return None

        return data["privateServerInviteData"]["linkCode"]

    async def _handle_server_join(self, choice_id: int, server_code: str):
        global detected_snipe
        os.system("taskkill /f /im RobloxPlayerBeta.exe /t")
        aura_detection.cancel()
        merchant_detection.cancel()
        biome_randomizer.cancel()
        strange_controller.cancel()
        keep_alive.cancel()
        obby_blessing.cancel()
        legacy_aura_detection.cancel()
        detected_snipe = True
        await self._join_windows(server_code)
        print(f"[SNIPER] {self.words[choice_id]} link found\nyay joins (modified for bazthedev/SolsRNGBot v{LOCALVERSION})")
        if settings["pop_in_glitch"] and self.words[choice_id] == "Glitched":
            await auto_pop("glitched")


    async def _join_windows(self, server_code: str):
        final_link = f"roblox://placeID={PLACE_ID}^&linkCode={server_code}"
        subprocess.Popen(["start", final_link], shell=True)

    async def _send_notification(self, choice_id: int, server_code: str):
        sniper_channel = client.get_channel(settings["sniper_channel_id"])
        if not sniper_channel:
            return

        colors = [11206400, 16744703]

        embed_link = f"{BASE_ROBLOX_URL}?privateServerLinkCode={server_code}"
        embed = discord.Embed(
            title = f'[{datetime.now().strftime("%H:%M:%S")}] {self.words[choice_id]} Link Sniped!',
            colour = colors[choice_id],
        )
        embed.add_field(name =  f"{self.words[choice_id]} Link:", value = embed_link, inline=True)
        embed.set_footer(text=f"yay joins (modified for bazthedev/SolsRNGBot v{LOCALVERSION})")

        await sniper_channel.send(f"<@{self.config['mention_id']}>", embed=embed)

    async def process_message(self, content: str, choice_id: int) -> None:
        try:
            if not self._should_process_message(content, choice_id):
                return

            server_code = await self._extract_server_code(content)
            if not server_code:
                return

            print(f"[SNIPER] Found message! content: {content}")

            await self._handle_server_join(choice_id, server_code)
            await self._send_notification(choice_id, server_code)

        except Exception as e:
            if self.config["sniper_logs"]:
                print(f"[SNIPER] Error processing message: {str(e)}")

    async def run(self):
        global ps_link_code
        await self.setup()

        glitch = self.config["sniper_toggles"]["Glitched"]
        dream = self.config["sniper_toggles"]["Dreamspace"]
        snipe_list = [glitch, dream]

        self.cycle_index = [i for i, x in enumerate(snipe_list) if x]

        if not (glitch or dream):
            print("[SNIPER] At least one option has to be True. Sniper has not been started.")
            return
            
        print("Started yay joins")
        ps_link_code = await self._extract_server_code(settings["ps_server_link"])
        sniper_channel = client.get_channel(settings["sniper_channel_id"])
        emb = discord.Embed(
            title="Started Sniper!",
            description = f"Snipe Glitched: {str(glitch)}\nSnipe Dreamspace: {str(dream)}"
        )
        emb.set_footer(text=f"yay joins (modified for bazthedev/SolsRNGBot v{LOCALVERSION})")
        await sniper_channel.send(embed=emb)
        while True:
            try:
                async with connect(DISCORD_WS_BASE, max_size=None, ping_interval=None) as ws:
                    await self._identify(ws)
                    await self._subscribe(ws)
                                        
                    event = json.loads(await ws.recv())
                    interval = event["d"]["heartbeat_interval"] / 1000
                    async with asyncio.TaskGroup() as tg:
                        tg.create_task(self.heartbeat(ws, interval))
                        tg.create_task(self._on_message(ws))
            except Exception as e:
                if self.config["sniper_logs"]:
                    print(f"[SNIPER] Error: {e}")


sniper = Sniper()

# THE ABOVE CODE IS A SLIGHTLY MODIFIED VERSION OF YAY JOINS SNIPER 1.2.10, WHICH IS OWNED BY Root1527. YOU CAN DOWNLOAD THE REGULAR VERSION OF YAY JOINS HERE: https://github.com/Root1527/yay-joins

if not os.path.exists(f"{MACROPATH}"):
    os.mkdir(MACROPATH)

if not os.path.isfile(f"{MACROPATH}/settings.json"):
    with open(f"{MACROPATH}/settings.json", "w") as f:
        json.dump(DEFAULTSETTINGS, f, indent=4)

def get_auras():
    print("Downloading Legacy Aura List")
    dl = requests.get("https://raw.githubusercontent.com/bazthedev/SolsRNGBot/main/auras.json")
    f = open(f"{MACROPATH}/auras.json", "wb")
    f.write(dl.content)
    f.close()
    print("Downloaded Legacy Aura List")
    print("Downloading Aura List")
    dl = requests.get("https://raw.githubusercontent.com/bazthedev/SolsRNGBot/main/auras_new.json")
    f = open(f"{MACROPATH}/auras_new.json", "wb")
    f.write(dl.content)
    f.close()
    print("Downloaded Aura List")

def update_settings(settings):
    with open(f"{MACROPATH}/settings.json", "w") as f:
        json.dump(settings, f, indent=4)

def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def hex2rgb(_hex):
    _hex = _hex.lstrip("#")
    return tuple(int(_hex[i:i+2], 16) for i in (0, 2, 4))

def reload_settings():
    global settings
    with open(f"{MACROPATH}/settings.json", "r") as f:
        settings = json.load(f)

def validate_settings():
    found_keys = []
    todel = []
    for k in settings.keys():
        if k not in VALIDSETTINGSKEYS:
            todel.append(k)
            print(f"Invalid setting ({k}) detected")
            logging.info(f"Invalid setting ({k}) detected")
        else:
            found_keys.append(k)
    for _ in todel:
        del settings[_]
        print(f"Invalid setting ({_}) deleted")
        logging.info(f"Invalid setting ({_}) deleted")
    for _ in VALIDSETTINGSKEYS:
        if _ not in found_keys:
            settings[_] = DEFAULTSETTINGS[_]
            print(f"Missing setting ({_}) added")
            logging.info(f"Missing setting ({_}) added")
    update_settings(settings)
    reload_settings()

def validate_pslink(ps_server_link : str):
    if "https://www.roblox.com/share?code=" not in ps_server_link:
        return False
    if "&type=Server" not in ps_server_link:
        return False
    return True

def format_roblosecurity():
    if "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_" in settings["ROBLOSECURITY_KEY"]:
        new_roblosec = settings["ROBLOSECURITY_KEY"].replace("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_", "")
        settings["ROBLOSECURITY_KEY"] = new_roblosec
        update_settings(settings)
        reload_settings()


def migrate_settings():
    if os.path.exists("./settings.json") and not os.path.exists(f"{MACROPATH}/settings.json"):
        with open("./settings.json", "r") as f:
            _ = json.load(f)
        with open(f"{MACROPATH}/settings.json", "w+") as f:
            json.dump(_, f, indent=4)
    reload_settings()

async def use_item(item_name : str, amount : int, close_menu : bool):
    mkey.left_click_xy_natural(inv_button_pos[0], inv_button_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(items_pos[0], items_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(search_pos[0], search_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.type(item_name)
    await asyncio.sleep(settings["global_wait_time"]) 
    mkey.left_click_xy_natural(query_pos[0], query_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(item_amt_pos[0], item_amt_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.press(Key.ctrl)
    _keyboard.press("a")
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.release("a")
    _keyboard.release(Key.ctrl)
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.type(str(amount))
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(use_pos[0], use_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    if close_menu:
        mkey.left_click_xy_natural(close_pos[0], close_pos[1])
        await asyncio.sleep(settings["global_wait_time"])

async def align_camera():
    print("Aligning Camera....")
    _keyboard.press(Key.esc)
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.release(Key.esc)
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.press("r")
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.release("r")
    await asyncio.sleep(settings["global_wait_time"])    
    _keyboard.press(Key.enter)
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.release(Key.enter)
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(collection_open_pos[0], collection_open_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(exit_collection_pos[0], exit_collection_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.press(Key.shift)
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.release(Key.shift)
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.press(Key.shift)
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.release(Key.shift)
    await asyncio.sleep(settings["global_wait_time"])
    for i in range(80):
        _mouse.scroll(0, 30)
    await asyncio.sleep(2)
    for i in range(3):
        _mouse.scroll(0, -5)
        await asyncio.sleep(settings["global_wait_time"])
    await asyncio.sleep(settings["global_wait_time"])

async def do_obby_blessing():
    _keyboard.press(Key.shift)
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.release(Key.shift)
    await asyncio.sleep(0.1)
    mkey.move_relative(int(500 * scale_w), 0) # 0.36 sens
    await asyncio.sleep(0.1)
    _keyboard.press(Key.shift)
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.release(Key.shift)
    await asyncio.sleep(0.1)
    _keyboard.press("w")
    await asyncio.sleep(4.5) # vip +
    _keyboard.release("w")
    await asyncio.sleep(0.1)
    _keyboard.press(Key.shift)
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.release(Key.shift)
    await asyncio.sleep(0.1)
    mkey.move_relative(int(-500 * scale_w), 0) # 0.36 sens
    await asyncio.sleep(0.1)
    _keyboard.press("w")
    await asyncio.sleep(1.5) # vip +
    _keyboard.release("w")
    await asyncio.sleep(0.1)    
    mkey.move_relative(int(500 * scale_w), 0) # 0.36 sens
    await asyncio.sleep(0.1)
    _keyboard.press("w")
    await asyncio.sleep(2) # vip +
    _keyboard.release("w")
    await asyncio.sleep(0.1)
    _keyboard.press("d")
    await asyncio.sleep(2) # vip +
    _keyboard.release("d")
    await asyncio.sleep(0.1)
    _keyboard.press("a")
    await asyncio.sleep(0.1) # vip +
    _keyboard.release("a")
    await asyncio.sleep(0.1)
    _keyboard.press("s")
    await asyncio.sleep(0.1) # vip +
    _keyboard.release("s")
    await asyncio.sleep(0.1)
    _keyboard.press(Key.space)
    _keyboard.press("w")
    await asyncio.sleep(0.2) # vip +
    _keyboard.release("w")
    _keyboard.release(Key.space)
    await asyncio.sleep(0.1)
    _keyboard.press("w")
    await asyncio.sleep(4) # vip +
    _keyboard.release("w")
    await asyncio.sleep(1)
    _keyboard.press("w")
    await asyncio.sleep(0.1)
    _keyboard.press(Key.space)
    await asyncio.sleep(0.3)
    _keyboard.release(Key.space)
    await asyncio.sleep(0.6) # vip +
    _keyboard.release("w")
    await asyncio.sleep(0.1)    
    mkey.move_relative(int(250 * scale_w), 0) # 0.36 sens
    await asyncio.sleep(0.1)
    _keyboard.press("w")
    await asyncio.sleep(0.3) # vip +
    _keyboard.release("w")
    await asyncio.sleep(1)
    _keyboard.press("s")
    await asyncio.sleep(0.1) # vip +
    _keyboard.release("s")
    await asyncio.sleep(0.1)
    _keyboard.press("w")
    _keyboard.press(Key.space)
    await asyncio.sleep(0.1)
    _keyboard.release(Key.space)
    await asyncio.sleep(0.1) # vip +
    _keyboard.release("w")
    await asyncio.sleep(0.3) 
    _keyboard.press("w")
    await asyncio.sleep(0.1)
    _keyboard.press(Key.space)
    await asyncio.sleep(0.3)
    _keyboard.release(Key.space)
    await asyncio.sleep(0.6) # vip +
    _keyboard.release("w")
    await asyncio.sleep(0.1)
    _keyboard.press("w")
    await asyncio.sleep(5) # vip +
    _keyboard.release("w")
    await asyncio.sleep(1)
    _keyboard.press("s")
    await asyncio.sleep(0.1) # vip +
    _keyboard.release("s")
    await asyncio.sleep(0.1)
    _keyboard.press(Key.space)
    _keyboard.press("w")
    await asyncio.sleep(0.2) # vip +
    _keyboard.release("w")
    _keyboard.release(Key.space)
    await asyncio.sleep(0.1)
    _keyboard.press(Key.space)
    _keyboard.press("w")
    await asyncio.sleep(0.2) # vip +
    _keyboard.release("w")
    _keyboard.release(Key.space)
    await asyncio.sleep(0.1)
    mkey.move_relative(int(-250 * scale_w), 0) # 0.36 sens
    await asyncio.sleep(0.1)
    _keyboard.press("w")
    await asyncio.sleep(1.3) # vip +
    _keyboard.release("w")
    await asyncio.sleep(1)
    mkey.move_relative(int(-500 * scale_w), 0) # 0.36 sens
    await asyncio.sleep(0.1)
    _keyboard.press("s")
    await asyncio.sleep(0.1) # vip +
    _keyboard.release("s")
    await asyncio.sleep(0.1)
    _keyboard.press(Key.space)
    _keyboard.press("w")
    await asyncio.sleep(0.2) # vip +
    _keyboard.release("w")
    _keyboard.release(Key.space)
    await asyncio.sleep(0.1)

async def collect_item(item_collection_index : int):
    await align_camera()
    if item_collection_index == 1:
        if not settings["collect_items"]["1"]:
            item_collection_index += 1
        else:
            _keyboard.press(Key.shift)
            await asyncio.sleep(settings["global_wait_time"])
            _keyboard.release(Key.shift)
            await asyncio.sleep(0.1)
            mkey.move_relative(int(500 * scale_w), 0) # 0.36 sens
            await asyncio.sleep(0.1)
            _keyboard.press(Key.shift)
            await asyncio.sleep(settings["global_wait_time"])
            _keyboard.release(Key.shift)
            await asyncio.sleep(0.1)
            _keyboard.press("w")
            await asyncio.sleep(4.5) # vip +
            _keyboard.release("w")
            await asyncio.sleep(0.1)
            _keyboard.press(Key.shift)
            await asyncio.sleep(settings["global_wait_time"])
            _keyboard.release(Key.shift)
            await asyncio.sleep(0.1)
            mkey.move_relative(int(-500 * scale_w), 0) # 0.36 sens
            await asyncio.sleep(0.1)
            _keyboard.press("w")
            await asyncio.sleep(2) # vip +
            _keyboard.release("w")
            await asyncio.sleep(0.1)
    if item_collection_index == 2:
        if not settings["collect_items"]["2"]:
            item_collection_index += 1
        else:
            pass
    if item_collection_index == 3:
        if not settings["collect_items"]["3"]:
            item_collection_index += 1
        else:
            pass
    if item_collection_index == 4:
        if not settings["collect_items"]["4"]:
            item_collection_index += 1
        else:
            pass
    if item_collection_index == 4:
        item_collection_index = 1
    else:
        item_collection_index += 1

async def leave_main_menu():
    if get_latest_equipped_aura(rblx_log_dir) == "In Main Menu":
        mkey.left_click_xy_natural(start_btn_pos[0], start_btn_pos[1])
        await asyncio.sleep(2)
        await leave_main_menu()

async def leave_main_menu_ms():
    if get_latest_equipped_aura(ms_rblx_log_dir) == "In Main Menu":
        mkey.left_click_xy_natural(start_btn_pos[0], start_btn_pos[1])
        await asyncio.sleep(2)
        await leave_main_menu_ms()


def get_latest_hovertext(logs_dir):
    log_files = glob.glob(os.path.join(logs_dir, "*.log"))
    if not log_files:
        return None

    latest_log_file = max(log_files, key=os.path.getctime)
    try:
        temp_file = os.path.join(tempfile.gettempdir(), "solsrngbot_biome_detection.log")
        shutil.copy2(latest_log_file, temp_file)
    except PermissionError:
        return None

    json_pattern = re.compile(r'\{.*\}')
    last_hover_text = None

    try:
        with open(temp_file, "r", encoding="utf-8") as file:
            for line in reversed(file.readlines()):
                match = json_pattern.search(line)
                if match:
                    try:
                        json_data = json.loads(match.group())
                        hover_text = json_data.get("data", {}).get("largeImage", {}).get("hoverText")
                        if hover_text:
                            return hover_text
                    except json.JSONDecodeError:
                        continue
    except Exception:
        return None
    
    return last_hover_text

def get_latest_equipped_aura(logs_dir):
    log_files = glob.glob(os.path.join(logs_dir, "*.log"))
    if not log_files:
        return None

    latest_log_file = max(log_files, key=os.path.getctime)
    try:
        temp_file = os.path.join(tempfile.gettempdir(), "solsrngbot_aura_detection.log")
        shutil.copy2(latest_log_file, temp_file)
    except PermissionError:
        return None

    json_pattern = re.compile(r'\{.*\}')
    
    try:
        with open(temp_file, "r", encoding="utf-8") as file:
            for line in reversed(file.readlines()):
                match = json_pattern.search(line)
                if match:
                    try:
                        json_data = json.loads(match.group())
                        if json_data.get("data", {}).get("state", "") == "In Main Menu":
                            return "In Main Menu"
                        aura = json_data.get("data", {}).get("state", "").replace("Equipped \"", "").replace("\"", "")
                        if aura:
                            aura = aura.replace("_", ": ")
                            return aura
                    except json.JSONDecodeError:
                        continue
    except Exception:
        return None
    
    return None

def exists_procs_by_name(name):
    for p in psutil.process_iter(['name']):
        if p.info['name'].lower() == name.lower():
            return True
    return False

def get_process_by_name(name):
    for p in psutil.process_iter(['name']):
        if p.info['name'].lower() == name.lower():
            return p
    return False

def match_rblxms_hwnd_to_pid(pid):
    for w in mkey.get_all_windows():
        if w.pid == pid and w.title == "MSCTFIME UI":
            return w
    return False

async def auto_pop(biome : str):
    global ps_link_code
    _ended = False
    while not exists_procs_by_name("Windows10Universal.exe"):
        pass # Wait for roblox to start
    ps_rblxms = get_process_by_name("Windows10Universal.exe")
    rblxms_window = match_rblxms_hwnd_to_pid(ps_rblxms.pid)
    mkey.activate_window(rblxms_window.hwnd)
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(ms_rblx_spawn_pos[0], ms_rblx_spawn_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(ms_rblx_spawn_pos[0], ms_rblx_spawn_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.press(Key.f11)
    await asyncio.sleep(0.1)
    _keyboard.release(Key.f11)
    await leave_main_menu_ms()
    if settings["change_cutscene_on_pop"]:
        mkey.left_click_xy_natural(menu_btn_pos[0], menu_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(settings_btn_pos[0], settings_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(rolling_conf_pos[0], rolling_conf_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(cutscene_conf_pos[0], cutscene_conf_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        _keyboard.press(Key.ctrl)
        _keyboard.press("a")
        await asyncio.sleep(settings["global_wait_time"])
        _keyboard.release("a")
        _keyboard.release(Key.ctrl)
        await asyncio.sleep(settings["global_wait_time"])
        _keyboard.type("9999999999")
        await asyncio.sleep(settings["global_wait_time"])
        _keyboard.press(Key.enter)
        await asyncio.sleep(settings["global_wait_time"])
        _keyboard.release(Key.enter)
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(menu_btn_pos[0], menu_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(menu_btn_pos[0], menu_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
    if biome.lower() == "glitched" and settings["pop_in_glitch"]:
        original_hp2_amt = settings["auto_use_items_in_glitch"]["Heavenly Potion II"]["amount"]
        for item in reversed(settings["auto_use_items_in_glitch"].keys()):
            if biome.lower() != get_latest_hovertext(ms_rblx_log_dir).lower():
                _ended = True
            if _ended:
                break
            if not settings["auto_use_items_in_glitch"][item]["use"]:
                continue
            if item == "Heavenly Potion II" or item == "Oblivion Potion":
                while True:
                    if get_latest_hovertext(ms_rblx_log_dir).lower() != biome:
                        print("Biome has ended")
                        _ended = True
                        break
                    else:
                        if original_hp2_amt > 10:
                            await use_item(item, 10, True)
                            original_hp2_amt -= 10
                        elif original_hp2_amt > 1:
                            await use_item(item, 1, True)
                            original_hp2_amt -= 1
                        else:
                            break
                    await asyncio.sleep(2)
            else:
                await use_item(item, settings["auto_use_items_in_glitch"][item]["amount"], True)
    
    os.system("taskkill /f /im Windows10Universal.exe /t")

    if not legacy_aura_detection.is_running() and settings["legacy_aura_detection"]:
        legacy_aura_detection.start()
    elif not aura_detection.is_running():
        aura_detection.start()    
    if valid_ps:
        print("Attempting to rejoin private server")
        await asyncio.sleep(5)
        await sniper._join_windows(ps_link_code)
        await asyncio.sleep(10)
        ps_rblxms = get_process_by_name("Windows10Universal.exe")
        rblxms_window = match_rblxms_hwnd_to_pid(ps_rblxms.pid)
        mkey.activate_window(rblxms_window.hwnd)
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(ms_rblx_spawn_pos[0], ms_rblx_spawn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(ms_rblx_spawn_pos[0], ms_rblx_spawn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        _keyboard.press(Key.f11)
        await asyncio.sleep(0.1)
        _keyboard.release(Key.f11)
        await leave_main_menu_ms()
        print("Success!")
    else:
        exit("No server to rejoin in settings")
    if not keep_alive.is_running():
        keep_alive.start()
    if not merchant_detection.is_running() and settings["merchant_detection"]:
        merchant_detection.start()
    if not biome_randomizer.is_running() and settings["auto_biome_randomizer"]:
        biome_randomizer.start()
    if not strange_controller.is_running() and settings["auto_strange_controller"]:
        strange_controller.start()

migrate_settings()

if not os.path.exists(f"{MACROPATH}/scr/"):
    os.mkdir(f"{MACROPATH}/scr/")

if not os.path.exists(f"{MACROPATH}/plugins/"):
    os.mkdir(f"{MACROPATH}/plugins/")
    os.mkdir(f"{MACROPATH}/plugins/config/")

if not os.path.exists(f"{MACROPATH}/logs/"):
    os.mkdir(f"{MACROPATH}/logs/")

now = datetime.now()
client = commands.Bot(commands.when_mentioned, case_insensitive=True, intents=None)
_mouse = mouse.Controller()
_keyboard = keyboard.Controller()
screens = si.get_monitors()
monitor = None
for mon in screens:
    if mon.is_primary:
        monitor = mon
scale_w = monitor.width / 2560
scale_h = monitor.height / 1440
aura_button_pos = ((53 * scale_w), (538 * scale_h))
inv_button_pos = ((67 * scale_w), (732 * scale_h))
default_pos = ((1280 * scale_w), (720 * scale_h))
close_pos = ((1887 * scale_w), (399 * scale_h))
search_pos = ((1164 * scale_w), (486 * scale_h))
secondary_pos = ((564 * scale_w), (401 * scale_h))
query_pos = ((1086 * scale_w), (572 * scale_h))
equip_pos = ((812 * scale_w), (844 * scale_h))
use_pos = ((910 * scale_w), (772 * scale_h))
item_amt_pos = ((756 * scale_w), (772 * scale_h))
items_pos = ((1692 * scale_w), (440 * scale_h)) 
purchase_btn_pos = ((990 * scale_w), (860 * scale_h))
quantity_btn_pos = ((910 * scale_w), (796 * scale_h))
open_merch_pos = ((876 * scale_w), (1256 * scale_h))
merch_item_pos_1 = (int(656 * scale_w), int(922 * scale_h))
merch_item_pos_1_end = (int(890 * scale_w), int(994 * scale_h))
merch_item_pos_1_purchase = ((766 * scale_w), (988 * scale_h))
merch_item_pos_2 = (int(908 * scale_w), int(922 * scale_h))
merch_item_pos_2_end = (int(1142 * scale_w), int(994 * scale_h))
merch_item_pos_2_purchase = ((1024 * scale_w), (986 * scale_h))
merch_item_pos_3 = (int(1160 * scale_w), int(922 * scale_h))
merch_item_pos_3_end = (int(1396 * scale_w), int(994 * scale_h))
merch_item_pos_3_purchase = ((1278 * scale_w), (988 * scale_h))
merch_item_pos_4 = (int(1416 * scale_w), int(922 * scale_h))
merch_item_pos_4_end = (int(1650 * scale_w), int(994 * scale_h))
merch_item_pos_4_purchase = ((1512 * scale_w), (988 * scale_h))
merch_item_pos_5 = (int(1666 * scale_w), int(922 * scale_h))
merch_item_pos_5_end = (int(1898 * scale_w), int(994 * scale_h))
merch_item_pos_5_purchase = ((1762 * scale_w), (986 * scale_h))
menu_btn_pos = ((42 * scale_w), (898 * scale_h))
settings_btn_pos = ((1278 * scale_w), (738 * scale_h))
rolling_conf_pos = ((888 * scale_w), (498 * scale_h))
cutscene_conf_pos = ((1518 * scale_w), (812 * scale_h))
craft_btn_pos = ((764 * scale_w), (764 * scale_h))
hp1_pos_potions = ((1064 * scale_w), (840 * scale_h))
hp1_pos_celestial = ((1064 * scale_w), (1024 * scale_h))
hp2_pos_potions = ((1064 * scale_w), (910 * scale_h))
auto_btn_pos = ((940 * scale_w), (762 * scale_h))
auto_mode_swap = 0
auto_craft_index = 3
hp1_recipe_pos = ((1516 * scale_w), (684 * scale_h))
hp2_recipe_pos = ((1516 * scale_w), (836 * scale_h))
warp_recipe_pos = ((1516 * scale_w), (980 * scale_h))
merchant_face_pos_1 = (int(841 * scale_w), int(1056 * scale_h))
merchant_face_pos_2 = (int(855 * scale_w), int(1063 * scale_h))
collection_open_pos = ((54 * scale_w), (624 * scale_h))
exit_collection_pos = ((510 * scale_w), (146 * scale_h))
start_btn_pos = ((1252 * scale_w), (1206 * scale_h))
mari_cols = ["#767474", "#767476", "#757474", "#7c7c7c", "#7c7a7c", "#7a7878", "#787678", "#787878"]
jester_cols = ["#e2e2e2", "#e1e1e1", "#e0e0e0"]
previous_biome = None
previous_aura = None
popping = False
valid_ps = False
item_collection_index = 1
use_ms_rblx = False
rblx_player_log_dir = os.path.expandvars(r"%localappdata%\Roblox\logs") # This is for the Roblox Player
ms_rblx_log_dir = os.path.expandvars(r"%LOCALAPPDATA%\Packages\ROBLOXCorporation.ROBLOX_55nm5eh3cm0pr\LocalState\logs") # This is for the Microsoft Store version of Roblox
ms_rblx_spawn_pos = ((820 * scale_w), (548 * scale_h))
ps_link_code = 0
WINDY_MULTIPLIER = 3
SNOWY_MULTIPLIER = 3
RAINY_MULTIPLER = 4
SANDSTORM_MULTIPLIER = 4
HELL_MULTIPLIER = 6
STARFALL_MULTIPLIER = 10
CORRUPTION_MULTIPLIER = 5
NULL_MULTIPLIER = 1000
GLITCHED_MULTIPLIER = 1
DREAMSPACE_MULTIPLIER = 1
_plugins = []
auto_purchase = {"Void Coin/Lucky Penny": ["#ff92fe", "#ff9e4e"]}
logger = logging.Logger("SolsRNGBot logging")
logging.basicConfig(filename=f"{MACROPATH}/logs/solsrngbot_{now.strftime('%d.%m.%Y_%H;%M;%S')}.log", level=logging.INFO)
print(f"Starting SolsRNGBot v{LOCALVERSION}")
logging.info(f"Starting SolsRNGBot v{LOCALVERSION}")

if not os.path.exists(f"{MACROPATH}/settings.json"):
    x = open(f"{MACROPATH}/settings.json", "w")
    x.write('{}')
    x.close()
    with open(f"{MACROPATH}/settings.json", "w") as f:
        json.dump(DEFAULTSETTINGS, f, indent=4)
    os.system(f"notepad {MACROPATH}/settings.json")
    exit("Opened Macro Settings")


reload_settings()


if settings["__version__"] < LOCALVERSION:
    settings["__version__"] = LOCALVERSION
    update_settings(settings)
    reload_settings()

if settings["__version__"] > LOCALVERSION:
    print("You are running newer settings with an older version of this program. This may delete some of your settings. Are you sure you want to continue (y)? ")
    confirm = input("")
    if confirm[0].lower() != "y":
        exit("You are running newer settings with an older version of this program.")

        
# Settings integrity check
validate_settings()

if settings["use_rblx_player"]:
    rblx_log_dir = rblx_player_log_dir
else:
    print("Defaulting to Microsoft store roblox")
    rblx_log_dir = ms_rblx_log_dir

mkey.enable_failsafekill(settings["failsafe_key"])

if settings["edit_settings_mode"] or settings["TOKEN"] == "":
    settings["edit_settings_mode"] = False
    print("Edit settings mode is enabled!")
    if settings["TOKEN"] == "":
        print("You need to add your bot token between the \"\" and then save the file.")
    update_settings(settings)
    reload_settings()
    os.system(f"notepad {MACROPATH}/settings.json")
    print("Edit settings has been disabled, starting macro as normal...")
    reload_settings()
    print("Success!")
    print("Validating settings")
    validate_settings()

    
if settings["sniper_enabled"] and (settings["ROBLOSECURITY_KEY"] == "" or settings["DISCORD_TOKEN"] == ""):
    print("You must provide both your ROBLOSECURITY cookie and your Discord Token for the sniper to work.")
    settings["edit_settings_mode"] = True
    update_settings(settings)
    reload_settings()
    exit()

if settings["ROBLOSECURITY_KEY"] != "":
    format_roblosecurity()

if not settings["skip_dl"]:
    get_auras()

if not os.path.exists(f"{MACROPATH}/auras.json") or not os.path.exists(f"{MACROPATH}/auras_new.json"):
    get_auras()

if settings["legacy_aura_detection"]:
    with open(f"{MACROPATH}/auras.json", "r") as f:
        auras = json.load(f)
else:
    with open(f"{MACROPATH}/auras_new.json", "r") as f:
        auras = json.load(f)

if settings["ps_server_link"] != "":
    if not validate_pslink(settings["ps_server_link"]):
        print("Invalid Private Server Link")
        valid_ps = False
    else:
        valid_ps = True

__version__ = settings["__version__"]

@client.event
async def on_ready():
    print(random.choice(STARTUP_MSGS))
    print(f"Started at {now.strftime('%d/%m/%Y %H:%M:%S')} running v{__version__} using local version {LOCALVERSION}")
    logging.info(f"Started at {now.strftime('%d/%m/%Y %H:%M:%S')} running v{__version__} using local version {LOCALVERSION}")
    await client.change_presence(activity=discord.Game(name=f"bazthedev/SolsRNGBot v{LOCALVERSION}"))
    await asyncio.sleep(settings["global_wait_time"])
    await leave_main_menu()
    await asyncio.sleep(settings["global_wait_time"])
    if settings["auto_craft_mode"] and not settings["merchant_detection"]:
        crafts = ""
        for item in settings["auto_craft_item"].keys():
            if settings["auto_craft_item"][item]:
                crafts += f"{item}\n"
        print("[WARNING] Auto Craft Mode is on. You will not be able to use certain features whilst this settings is on.")
        print(f"The item(s) you are automatically crafting are:\n{crafts}")
        if not settings["skip_auto_mode_warning"]:
            print("Please ensure that you are ostanding next to the cauldron so that you can see the \"f\" prompt. When you have done this, please press enter.")
            input("")
        else:
            print("Please ensure that you are ostanding next to the cauldron so that you can see the \"f\" prompt.")
        if settings["reset_aura"] != "":
            settings["reset_aura"] = ""
            update_settings(settings)
            reload_settings()
        print("Starting auto craft mode. Please click back onto Roblox and wait 5 seconds")
        await asyncio.sleep(5)
        auto_craft.start()
    else:
        if settings["log_channel_id"] != 0:
            if not settings["disable_autokick_prevention"]:
                keep_alive.start()
                print("Started Autokick Prevention")
                logging.info("Started Autokick Prevention")
                await asyncio.sleep(((settings["global_wait_time"] * 7) + 0.7))
        if settings["sniper_enabled"] and settings["sniper_channel_id"] != "":
            yay_joins_sniper.start()
        """for _ in settings["collect_items"]:
            if _:
                collect_items.start()
                break"""
    if settings["log_channel_id"] != 0:
        if settings["auto_craft_mode"] and not settings["merchant_detection"]:
            log_channel = client.get_channel(settings["log_channel_id"])
            emb = discord.Embed(
                title="Bot has started",
                description=f"Mode: Auto Craft\nAuto Craft item(s):\n{crafts}\nStarted at {now.strftime('%d/%m/%Y %H:%M:%S')}"
            )
            emb.set_footer(text=f"bazthedev/SolsRNGBot v{LOCALVERSION}")
            await log_channel.send(embed=emb)
        else:
            log_channel = client.get_channel(settings["log_channel_id"])
            emb = discord.Embed(
                title="Bot has started",
                description=f"Mode: Normal\nStarted at {now.strftime('%d/%m/%Y %H:%M:%S')}"
            )
            emb.set_footer(text=f"bazthedev/SolsRNGBot v{LOCALVERSION}")
            await log_channel.send(embed=emb)
        if settings["legacy_aura_detection"]:
            legacy_aura_detection.start()
            print("Started Legacy Aura Detection")
            logging.info("Started Legacy Aura Detection")
        else:
            aura_detection.start()
            print("Started Aura Detection")
            logging.info("Started Aura Detection")
        if settings["glitch_detector"]:
            glitch_detector.start()
            print("Started Glitch Biome Detection")
            logging.info("Started Glitch Biome Detection")
        if settings["dreamspace_detector"]:
            dreamspace_detector.start()
            print("Started Dreamspace Biome Detection")
            logging.info("Started Dreamspace Biome Detection")
    else:
        print("You must select a channel ID, you can do this by running the set_log_channel command.")
    if settings["auto_biome_randomizer"]:
        biome_randomizer.start()
        print("Started Biome Randomizer")
        logging.info("Started Biome Randomizer")
    if settings["auto_strange_controller"]:
        await asyncio.sleep((settings["global_wait_time"] * 60))
        strange_controller.start()
        print("Started Strange Controller")
        logging.info("Started Strange Controller")
    if settings["merchant_detection"] and settings["log_channel_id"] != 0:
        if settings["auto_biome_randomizer"] or settings["auto_strange_controller"]:
            await asyncio.sleep((settings["global_wait_time"] * 60))
        merchant_detection.start()
        print("Started Merchant Detection")
        logging.info("Started Merchant Detection")
    print(f"Started SolsRNGBot v{LOCALVERSION}")
    
@tasks.loop(seconds=0)
async def glitch_detector():
    rnow = datetime.now()
    global previous_biome, popping
    latest_hovertext = get_latest_hovertext(rblx_log_dir)
    log_channel = client.get_channel(settings["log_channel_id"])
    if latest_hovertext == "GLITCHED" and previous_biome != "GLITCHED":
        merchant_detection.stop()
        yay_joins_sniper.cancel()
        previous_biome = latest_hovertext
        popping = True
        storimg = pag.screenshot(f"{MACROPATH}/scr/screenshot_glitch.png")
        up = discord.File(f"{MACROPATH}/scr/screenshot_glitch.png", filename="glitch.png")
        print("Glitch Biome started")    
        emb = discord.Embed(
                title="GLITCH BIOME DETECTED",
                description=f"A GLITCH biome was detected at {rnow.strftime('%d/%m/%Y %H:%M:%S')}",
                colour=discord.Colour.from_rgb(101, 255, 101)
        )
        emb.set_image(url="attachment://glitch.png")
        if valid_ps:
            emb.add_field(name="Private Server Link:", value=f"{settings["ps_server_link"]}", inline=True)
        if settings["ping_on_glitch"]:
            await log_channel.send("@everyone", embed=emb, file=up)
        else:
            await log_channel.send(embed=emb, file=up)
        if settings["pop_in_glitch"] and popping:
            if settings["auto_craft_mode"] and not settings["merchant_detection"]:
                auto_craft.stop()
            popping = False
            await auto_pop("glitched")
        else:
            popping = False
    elif previous_biome == "GLITCHED" and latest_hovertext != "GLITCHED":
        previous_biome = None
        if settings["auto_craft_mode"] and not settings["merchant_detection"]:
            auto_craft.start()
        elif settings["merchant_detection"]:
            merchant_detection.start()
        if settings["sniper_enabled"]:
            yay_joins_sniper.start()
        print("Glitch biome ended")
        emb = discord.Embed(
                title="Glitch Biome Ended",
                description=f"A GLITCH biome ended at {rnow.strftime('%d/%m/%Y %H:%M:%S')}",
                colour=discord.Colour.from_rgb(101, 255, 101)
        )
        await log_channel.send(embed=emb)
        

@tasks.loop(seconds=0)
async def dreamspace_detector():
    rnow = datetime.now()
    global previous_biome, popping
    latest_hovertext = get_latest_hovertext(rblx_log_dir)
    log_channel = client.get_channel(settings["log_channel_id"])
    if latest_hovertext == "DREAMSPACE" and previous_biome != "DREAMSPACE":
        merchant_detection.stop()
        previous_biome = latest_hovertext
        popping = True
        storimg = pag.screenshot(f"{MACROPATH}/scr/screenshot_dreamspace.png")
        up = discord.File(f"{MACROPATH}/scr/screenshot_dreamspace.png", filename="dreamspace.png")
        print("Dreamspace Biome started")    
        emb = discord.Embed(
                title="DREAMSPACE BIOME DETECTED",
                description=f"A DREAMSPACE biome was detected at {rnow.strftime('%d/%m/%Y %H:%M:%S')}",
                colour=discord.Colour.from_rgb(255, 105, 180)
        )
        emb.set_image(url="attachment://dreamspace.png")
        if valid_ps:
            emb.add_field(name="Private Server Link:", value=f"{settings["ps_server_link"]}", inline=True)
        if settings["ping_on_dreamspace"]:
            await log_channel.send("<@everyone>",embed=emb, file=up)
        else:
            await log_channel.send(embed=emb, file=up)
        if settings["pop_in_dreamspace"] and popping:
            if settings["auto_craft_mode"] and not settings["merchant_detection"]:
                auto_craft.stop()
            popping = False
            await auto_pop("dreamspace")      
        else:
            popping = False
    elif previous_biome == "DREAMSPACE" and latest_hovertext != "DREAMSPACE":
        previous_biome = None
        if settings["auto_craft_mode"] and not settings["merchant_detection"]:
            auto_craft.start()
        elif settings["merchant_detection"]:
            merchant_detection.start()
        if settings["sniper_enabled"]:
            yay_joins_sniper.start()
        print("Dreamspace Biome ended")
        emb = discord.Embed(
                title="Dreamspace Biome Ended",
                description=f"A DREAMSPACE biome ended at {rnow.strftime('%d/%m/%Y %H:%M:%S')}",
                colour=discord.Colour.from_rgb(255, 105, 180)
        )
        await log_channel.send(embed=emb)

@tasks.loop(count=None)
async def yay_joins_sniper():
    await sniper.run()

@client.event
async def on_command_error(ctx, error):
    print(str(error))
    logging.error(str(error))

@tasks.loop(seconds=2100)
async def biome_randomizer():
    await use_item("Biome Random", 1, True)

@tasks.loop(seconds=1200)
async def strange_controller():
    await use_item("Strange Control", 1, True)

@client.command()
async def get_biome(ctx):
    latest_hovertext = get_latest_hovertext(rblx_log_dir)
    await ctx.send(f"The current biome is: {latest_hovertext}")

@client.command()
async def get_aura(ctx):
    current_aura = get_latest_equipped_aura(rblx_log_dir)
    if current_aura == "In Main Menu":
        await ctx.send("Currently in the main menu.")
    elif current_aura == "_None_":
        await ctx.send("There is no equipped aura.")
    else:
        await ctx.send(f"The currently equipped aura is: {current_aura}")

@client.command()
@commands.is_owner()
async def set_log_channel(ctx):
    await ctx.send("Updating log channel...")
    new_log_channel_id = ctx.message.channel.id
    settings["log_channel_id"] = new_log_channel_id
    update_settings(settings)
    reload_settings()
    await ctx.send(f"Log Channel set to {ctx.message.channel.mention}")
    logging.info(f"Log Channel set to {ctx.message.channel.mention}")

@client.command()
@commands.is_owner()
async def set_sniper_channel(ctx):
    await ctx.send("Updating sniper logs channel...")
    new_sniper_channel_id = ctx.message.channel.id
    settings["sniper_channel_id"] = new_sniper_channel_id
    update_settings(settings)
    reload_settings()
    await ctx.send(f"Sniper Channel set to {ctx.message.channel.mention}! This will change will take place next time the macro is run.")
    logging.info(f"Sniper Channel set to {ctx.message.channel.mention}")

@client.command()
@commands.is_owner()
async def set_mention(ctx):
    await ctx.send("Updating user to mention...")
    settings["mention_id"] = ctx.author.id
    update_settings(settings)
    reload_settings()
    await ctx.send(f"User to mention is now {ctx.author.mention}")
    logging.info(f"User to mention is now {ctx.author.id}")

@client.command()
@commands.is_owner()
async def set_min_roll(ctx, minimum : str):
    try:
        int(minimum)
    except TypeError:
        await ctx.send("The value provided is not a number")
        return
    await ctx.send("Changing minimum roll alert...")
    settings["minimum_roll"] = minimum
    update_settings(settings)
    reload_settings()
    await ctx.send(f"Minimum roll alert is now {minimum}")
    logging.info(f"Minimum roll alert is now {minimum}")

@client.command()
@commands.is_owner()
async def set_min_ping(ctx, minimum : str):
    try:
        int(minimum)
    except TypeError:
        await ctx.send("The value provided is not a number")
        return
    await ctx.send("Changing minimum ping alert...")
    settings["minimum_ping"] = minimum
    update_settings(settings)
    reload_settings()
    await ctx.send(f"Minimum ping alert is now {minimum}")
    logging.info(f"Minimum ping alert is now {minimum}")

@client.command()
async def mode(ctx):
    if settings["auto_craft_mode"] and not settings["merchant_detection"]:
        crafts = ""
        for item in settings["auto_craft_item"].keys():
            if settings["auto_craft_item"][item]:
                crafts += f"{item}\n"
        await ctx.send(f"The bot is currently running in Auto Craft mode, and the item(s) being crafted are:\n{crafts}")
    else:
        await ctx.send("The bot is running in Normal mode.")

@client.command()
@commands.is_owner()
async def stop(ctx):
    await ctx.send("Manual stop initiated")
    logging.warning("Manual stop initiated")
    if settings["legacy_aura_detection"]:
        legacy_aura_detection.stop()
    keep_alive.stop()
    await client.close()
    print("Aw dang it")

@client.command()
@commands.is_owner()
async def edit_settings(ctx):
    settings["edit_settings_mode"] = True
    update_settings(settings)
    reload_settings()
    await ctx.send("The next time you run the macro, the settings will be opened.")

@client.command()
@commands.is_owner()
async def storage_scr(ctx):
    await ctx.send("Taking screenshot of Aura Storage, please wait, this will take a few seconds.")
    logging.info("Taking screenshot of Aura Storage")
    mkey.left_click_xy_natural(aura_button_pos[0], aura_button_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(search_pos[0], search_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    storimg = pag.screenshot(f"{MACROPATH}/scr/screenshot_storage.png")
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(close_pos[0], close_pos[1])
    await ctx.send(file=discord.File(f"{MACROPATH}/scr/screenshot_storage.png"))

@client.command()
@commands.is_owner()
async def inv_scr(ctx):
    await ctx.send("Taking screenshot of inventory, please wait, this will take a few seconds.")
    logging.info("Taking screenshot of inventory")
    mkey.left_click_xy_natural(inv_button_pos[0], inv_button_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(search_pos[0], search_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    storimg = pag.screenshot(f"{MACROPATH}/scr/screenshot_inventory.png")
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(close_pos[0], close_pos[1])
    await ctx.send(file=discord.File(f"{MACROPATH}/scr/screenshot_inventory.png"))

@client.command()
@commands.is_owner()
async def get_settings(ctx):
    settings_str = """"""
    for _ in settings:
        if _ == "TOKEN" or _ == "auto_use_items_in_glitch" or _ == "auto_use_items_in_dreamspace" or _ == "ROBLOSECURITY_KEY" or _ == "DISCORD_TOKEN":
            continue
        settings_str += f"Setting: {_}; Value: {settings[_]}\n"
    await ctx.send(f"```\n{settings_str}\n```")

@client.command()
@commands.is_owner()
async def enable(ctx, setting):
    if setting not in VALIDSETTINGSKEYS:
        await ctx.send("That setting does not exist.")
        return
    if "bool" not in str(type(settings[setting])):
        await ctx.send("That setting cannot be toggled.")
        return
    if settings[setting] == True:
        await ctx.send("This setting is already on.")
        return
    settings[setting] = True
    update_settings(settings)
    reload_settings()
    await ctx.send(f"{setting} has been enabled.")

@client.command()
@commands.is_owner()
async def disable(ctx, setting):
    if setting not in VALIDSETTINGSKEYS:
        await ctx.send("That setting does not exist.")
        return
    if "bool" not in str(type(settings[setting])):
        await ctx.send("That setting cannot be toggled.")
        return
    if settings[setting] == False:
        await ctx.send("This setting is already off.")
        return
    settings[setting] = False
    update_settings(settings)
    reload_settings()
    await ctx.send(f"{setting} has been disabled.")

@client.command()
@commands.is_owner()
async def purchase_item(ctx, item : int, amount = 25):
    if not settings["merchant_detection"]:
        await ctx.send("Merchant Detection is disabled. Please enable it to use this feature.")
        return
    if settings["auto_craft_mode"]:
        await ctx.send("Auto Craft mode is enabled. Please disable it to use this feature.")
        return
    if item > 5 or item < 1:
        await ctx.send("A merchant only sells 5 items at a time")
        return
    try:
        int(amount)
    except Exception:
        await ctx.send("You need to provide a number for items to buy.")
        return
    if item == 1:
        mkey.left_click_xy_natural(merch_item_pos_1_purchase[0], merch_item_pos_1_purchase[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(quantity_btn_pos[0], quantity_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        _keyboard.type(str(amount))
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(purchase_btn_pos[0], purchase_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        log_channel = client.get_channel(settings["log_channel_id"])
        if settings["ping_merchant"] and settings["mention_id"] != 0:
            await log_channel.send(f"<@{settings["mention_id"]}>\nPurchased item in box 1 from merchant")
        else:
            await log_channel.send(f"Purchased item in box 1 from merchant")
        logging.info(f"Purchased item in box 1 from merchant")
        await asyncio.sleep(2)
    elif item == 2:
        mkey.left_click_xy_natural(merch_item_pos_2_purchase[0], merch_item_pos_2_purchase[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(quantity_btn_pos[0], quantity_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        _keyboard.type(str(amount))
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(purchase_btn_pos[0], purchase_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        log_channel = client.get_channel(settings["log_channel_id"])
        if settings["ping_merchant"] and settings["mention_id"] != 0:
            await log_channel.send(f"<@{settings["mention_id"]}>\nPurchased item in box 2 from merchant")
        else:
            await log_channel.send(f"Purchased item in box 2 from merchant")
        logging.info(f"Purchased item in box 2 from merchant")
        await asyncio.sleep(2)
    elif item == 3:
        mkey.left_click_xy_natural(merch_item_pos_3_purchase[0], merch_item_pos_3_purchase[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(quantity_btn_pos[0], quantity_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        _keyboard.type(str(amount))
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(purchase_btn_pos[0], purchase_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        log_channel = client.get_channel(settings["log_channel_id"])
        if settings["ping_merchant"] and settings["mention_id"] != 0:
            await log_channel.send(f"<@{settings["mention_id"]}>\nPurchased item in box 3 from merchant")
        else:
            await log_channel.send(f"Purchased item in box 3 from merchant")
        logging.info(f"Purchased item in box 3 from merchant")
        await asyncio.sleep(2)
    elif item == 4:
        mkey.left_click_xy_natural(merch_item_pos_4_purchase[0], merch_item_pos_4_purchase[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(quantity_btn_pos[0], quantity_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        _keyboard.type(str(amount))
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(purchase_btn_pos[0], purchase_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        log_channel = client.get_channel(settings["log_channel_id"])
        if settings["ping_merchant"] and settings["mention_id"] != 0:
            await log_channel.send(f"<@{settings["mention_id"]}>\nPurchased item in box 4 from merchant")
        else:
            await log_channel.send(f"Purchased item in box 4 from merchant")
        logging.info(f"Purchased item in box 4 from merchant")
        await asyncio.sleep(2)
    elif item == 5:
        mkey.left_click_xy_natural(merch_item_pos_5_purchase[0], merch_item_pos_5_purchase[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(quantity_btn_pos[0], quantity_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        _keyboard.type(str(amount))
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(purchase_btn_pos[0], purchase_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        log_channel = client.get_channel(settings["log_channel_id"])
        if settings["ping_merchant"] and settings["mention_id"] != 0:
            await log_channel.send(f"<@{settings["mention_id"]}>\nPurchased item in box 5 from merchant")
        else:
            await log_channel.send(f"Purchased item in box 5 from merchant")
        logging.info(f"Purchased item in box 5 from merchant")
        await asyncio.sleep(2)

@tasks.loop(seconds=577)
async def keep_alive():
    mkey.left_click_xy_natural(close_pos[0], close_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(close_pos[0], close_pos[1])
    await asyncio.sleep(settings["global_wait_time"])

@tasks.loop(seconds=720)
async def obby_blessing():
    await align_camera()
    await asyncio.sleep(settings["global_wait_time"])
    await do_obby_blessing()
    await asyncio.sleep(settings["global_wait_time"])

@tasks.loop(seconds=1200)
async def collect_items():
    pass

@tasks.loop(seconds=60)
async def auto_craft():
    global auto_mode_swap, auto_craft_index
    items_to_craft = []
    for itm in settings["auto_craft_item"].keys():
        if settings["auto_craft_item"][itm]:
            items_to_craft.append(itm)
    if len(items_to_craft) == 1:
        return
    _keyboard.press("f")
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.release("f")
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(hp1_recipe_pos[0], hp1_recipe_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    _mouse.scroll(0, -30)
    await asyncio.sleep(settings["global_wait_time"])
    _mouse.scroll(0, -30)
    await asyncio.sleep(settings["global_wait_time"])
    _mouse.scroll(0, -30)
    await asyncio.sleep(settings["global_wait_time"])
    _mouse.scroll(0, -30)
    await asyncio.sleep(settings["global_wait_time"])
    _mouse.scroll(0, -30)
    await asyncio.sleep(settings["global_wait_time"])
    if auto_mode_swap == 9:
        auto_mode_swap = 0
        if auto_craft_index == 1:
            if settings["auto_craft_item"]["Heavenly Potion II"]:
                auto_craft_index = 2
                mkey.left_click_xy_natural(hp2_recipe_pos[0], hp2_recipe_pos[1])
                await asyncio.sleep(settings["global_wait_time"])
                mkey.left_click_xy_natural(auto_btn_pos[0], auto_btn_pos[1])
                await asyncio.sleep(settings["global_wait_time"])
            elif settings["auto_craft_item"]["Warp Potion"]:
                auto_craft_index = 3
                mkey.left_click_xy_natural(warp_recipe_pos[0], warp_recipe_pos[1])
                await asyncio.sleep(settings["global_wait_time"])
                mkey.left_click_xy_natural(auto_btn_pos[0], auto_btn_pos[1])
                await asyncio.sleep(settings["global_wait_time"])
        elif auto_craft_index == 2:
            if settings["auto_craft_item"]["Warp Potion"]:
                auto_craft_index = 3
                mkey.left_click_xy_natural(warp_recipe_pos[0], warp_recipe_pos[1])
                await asyncio.sleep(settings["global_wait_time"])
                mkey.left_click_xy_natural(auto_btn_pos[0], auto_btn_pos[1])
                await asyncio.sleep(settings["global_wait_time"])
            elif settings["auto_craft_item"]["Heavenly Potion I"]:
                auto_craft_index = 1    
                mkey.left_click_xy_natural(hp1_recipe_pos[0], hp1_recipe_pos[1])
                await asyncio.sleep(settings["global_wait_time"])
                mkey.left_click_xy_natural(auto_btn_pos[0], auto_btn_pos[1])
                await asyncio.sleep(settings["global_wait_time"])
        elif auto_craft_index == 3:
            if settings["auto_craft_item"]["Heavenly Potion I"]:
                auto_craft_index = 1
                mkey.left_click_xy_natural(hp1_recipe_pos[0], hp1_recipe_pos[1])
                await asyncio.sleep(settings["global_wait_time"])
                mkey.left_click_xy_natural(auto_btn_pos[0], auto_btn_pos[1])
                await asyncio.sleep(settings["global_wait_time"])
            elif settings["auto_craft_item"]["Heavenly Potion II"]:
                auto_craft_index = 2
                mkey.left_click_xy_natural(hp2_recipe_pos[0], hp2_recipe_pos[1])
                await asyncio.sleep(settings["global_wait_time"])
                mkey.left_click_xy_natural(auto_btn_pos[0], auto_btn_pos[1])
                await asyncio.sleep(settings["global_wait_time"])
    if "Heavenly Potion I" in items_to_craft:
        mkey.left_click_xy_natural(hp1_recipe_pos[0], hp1_recipe_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(craft_btn_pos[0], craft_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(hp1_pos_potions[0] - (110 * scale_w), hp1_pos_potions[1])
        await asyncio.sleep(0.1)
        mkey.left_click_xy_natural(hp1_pos_potions[0] - (110 * scale_w), hp1_pos_potions[1])
        await asyncio.sleep(settings["global_wait_time"])
        _keyboard.type("100")
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(hp1_pos_potions[0], hp1_pos_potions[1])
        await asyncio.sleep(settings["global_wait_time"])
        _mouse.scroll(0, -10)
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(hp1_pos_celestial[0], hp1_pos_celestial[1])
        await asyncio.sleep(settings["global_wait_time"])
        _mouse.scroll(0, 10)
        await asyncio.sleep(settings["global_wait_time"])
    if "Heavenly Potion II" in items_to_craft:
        mkey.left_click_xy_natural(hp2_recipe_pos[0], hp2_recipe_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(craft_btn_pos[0], craft_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(hp1_pos_potions[0], hp1_pos_potions[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(hp1_pos_potions[0], hp1_pos_potions[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(hp2_pos_potions[0], hp2_pos_potions[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(hp2_pos_potions[0] - (110 * scale_w), hp2_pos_potions[1])
        await asyncio.sleep(0.1)
        mkey.left_click_xy_natural(hp2_pos_potions[0] - (110 * scale_w), hp2_pos_potions[1])
        await asyncio.sleep(settings["global_wait_time"])
        _keyboard.type("125")
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(hp2_pos_potions[0], hp2_pos_potions[1])
        await asyncio.sleep(settings["global_wait_time"])
        _mouse.scroll(0, 10)
        await asyncio.sleep(settings["global_wait_time"])
        _mouse.scroll(0, -10)
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(hp1_pos_celestial[0], hp1_pos_celestial[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(craft_btn_pos[0], craft_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(hp1_pos_celestial[0], hp1_pos_celestial[1])
        await asyncio.sleep(settings["global_wait_time"])
        _mouse.scroll(0, 10)
    if "Warp Potion" in items_to_craft:
        mkey.left_click_xy_natural(warp_recipe_pos[0], warp_recipe_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(craft_btn_pos[0], craft_btn_pos[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(hp1_pos_potions[0], hp1_pos_potions[1])
        await asyncio.sleep(settings["global_wait_time"])
        _mouse.scroll(0, -30)
        await asyncio.sleep(settings["global_wait_time"])
        _mouse.scroll(0, -30)
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(hp1_pos_celestial[0] - (110 * scale_w), hp1_pos_celestial[1])
        await asyncio.sleep(0.1)
        mkey.left_click_xy_natural(hp1_pos_celestial[0] - (110 * scale_w), hp1_pos_celestial[1])
        await asyncio.sleep(settings["global_wait_time"])
        _keyboard.type("1000")
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(hp1_pos_potions[0], hp1_pos_potions[1])
        await asyncio.sleep(settings["global_wait_time"])
        mkey.left_click_xy_natural(hp1_pos_celestial[0], hp1_pos_celestial[1])
        await asyncio.sleep(settings["global_wait_time"])
        _mouse.scroll(0, 30)
        await asyncio.sleep(settings["global_wait_time"])
        _mouse.scroll(0, 30)
        await asyncio.sleep(settings["global_wait_time"])
    auto_mode_swap += 1

@tasks.loop(seconds=0)
async def reset_aura():
    reset_aura.stop()

@reset_aura.after_loop
async def on_reset_aura_cancel():
    current_aura = get_latest_equipped_aura(rblx_log_dir)
    if current_aura == settings["reset_aura"]:
        return    
    mkey.left_click_xy_natural(aura_button_pos[0], aura_button_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(search_pos[0], search_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.type(settings["reset_aura"])
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(query_pos[0], query_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(equip_pos[0], equip_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(equip_pos[0], equip_pos[1])
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.press(Key.cmd)
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.release(Key.cmd)
    await asyncio.sleep(settings["global_wait_time"])
    _mouse.position = close_pos
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.press(Key.cmd)
    await asyncio.sleep(settings["global_wait_time"])
    _keyboard.release(Key.cmd)
    await asyncio.sleep(settings["global_wait_time"])
    mkey.left_click_xy_natural(close_pos[0], close_pos[1])
    
@tasks.loop(seconds=150)
async def merchant_detection():
    if settings["log_channel_id"] == 0:
        print("You must select a channel ID, you can do this by running the set_log_channel command.")
        return    
    if legacy_aura_detection.is_being_cancelled():
        return
    await use_item("Merchant Teleport", 1, False)
    await asyncio.sleep(settings["merchant_detec_wait"])
    px = ImageGrab.grab().load()
    colour = px[default_pos[0], default_pos[1]]
    hex_col = rgb2hex(colour[0], colour[1], colour[2])
    colour2 = px[secondary_pos[0], secondary_pos[1]]
    hex_col2 = rgb2hex(colour2[0], colour2[1], colour2[2])
    if (hex_col == "#000000" and hex_col2 == "#000000"):
        rnow = datetime.now()
        mkey.left_click_xy_natural(close_pos[0], close_pos[1])
        await asyncio.sleep(1)
        _keyboard.press("e")
        await asyncio.sleep(2)
        _keyboard.release("e")
        await asyncio.sleep(3)
        px = ImageGrab.grab().load()
        await asyncio.sleep(2)
        mkey.left_click_xy_natural(open_merch_pos[0], open_merch_pos[1])
        await asyncio.sleep(0.5)
        merchimg = pag.screenshot(f"{MACROPATH}/scr/screenshot_merchant.png")
        await asyncio.sleep(0.2)
        up = discord.File(f"{MACROPATH}/scr/screenshot_merchant.png", filename="merchant.png")
        _break = False
        cols = []
        try:
            for y in range(merchant_face_pos_1[1], merchant_face_pos_2[1]):
                for x in range(merchant_face_pos_1[0], merchant_face_pos_2[0]):
                    if _break:
                        break
                    colour = px[x, y]
                    hex_col = rgb2hex(colour[0], colour[1], colour[2])
                    cols.append(hex_col)
                    if hex_col in mari_cols:
                        emb = discord.Embed(
                                        title = f"Mari Spawned",
                                        description = f"A Mari selling the following items in the screenshot has been detected at time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}",
                                        colour = discord.Color.from_rgb(255, 255, 255)
                        )
                        emb.set_image(url="attachment://merchant.png")
                        log_channel = client.get_channel(settings["log_channel_id"])
                        if settings["send_mari"]:
                            if settings["ping_jester"] and settings["mention_id"] != 0:
                                await log_channel.send(f"<@{settings["mention_id"]}>", embed=emb, file=up)
                            else:
                                await log_channel.send(embed=emb, file=up)
                        logging.info("A Mari has been detected")
                        _break = True
                    elif hex_col in jester_cols:
                        emb = discord.Embed(
                                    title = f"Jester Spawned",
                                    description = f"A Jester selling the following items in the screenshot has been detected at time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}",
                                    colour = discord.Color.from_rgb(176, 49, 255)
                        )
                        emb.set_image(url="attachment://merchant.png")
                        log_channel = client.get_channel(settings["log_channel_id"])
                        if settings["send_jester"]:
                            if settings["ping_jester"] and settings["mention_id"] != 0:
                                await log_channel.send(f"<@{settings["mention_id"]}>", embed=emb, file=up)
                            else:
                                await log_channel.send(embed=emb, file=up)
                        logging.info("A Jester has been detected")
                        _break = True
                if _break:
                    break
            with open("test.json", "w") as f:
                json.dump(cols, f, indent=4)
        except Exception as e:
            print(e)
    else:
        mkey.left_click_xy_natural(close_pos[0], close_pos[1])

@tasks.loop(seconds=0)
async def aura_detection():
    global previous_aura
    current_aura = get_latest_equipped_aura(rblx_log_dir)
    if previous_aura == None:
        previous_aura = current_aura
        return
    if current_aura == "In Main Menu":
        return
    if current_aura == settings["reset_aura"] and settings["reset_aura"] != "":
        return
    if current_aura == previous_aura:
        return
    if settings["log_channel_id"] == 0:
        print("You must select a channel ID, you can do this by running the set_log_channel command.")
        return
    try:
        if current_aura.lower() in auras.keys():
            previous_aura = current_aura
            rnow = datetime.now()
            current_biome = get_latest_hovertext(rblx_log_dir)
            if current_biome.lower() == auras[current_aura.lower()]["native_biome"].lower():
                if current_biome.lower() == "snowy":
                    aura_rarity = int(auras[current_aura.lower()]["rarity"]) / SNOWY_MULTIPLIER
                elif current_biome.lower() == "windy":
                    aura_rarity = int(auras[current_aura.lower()]["rarity"]) / WINDY_MULTIPLIER
                elif current_biome.lower() == "rainy":
                    aura_rarity = int(auras[current_aura.lower()]["rarity"]) / RAINY_MULTIPLER
                elif current_biome.lower() == "sandstorm":
                    aura_rarity = int(auras[current_aura.lower()]["rarity"]) / SANDSTORM_MULTIPLIER                
                elif current_biome.lower() == "hell":
                    aura_rarity = int(auras[current_aura.lower()]["rarity"]) / HELL_MULTIPLIER
                elif current_biome.lower() == "starfall":
                    aura_rarity = int(auras[current_aura.lower()]["rarity"]) / STARFALL_MULTIPLIER
                elif current_biome.lower() == "corruption":
                    aura_rarity = int(auras[current_aura.lower()]["rarity"]) / CORRUPTION_MULTIPLIER
                elif current_biome.lower() == "null":
                    aura_rarity = int(auras[current_aura.lower()]["rarity"]) / NULL_MULTIPLIER
                elif current_biome.lower() == "glitched":
                    aura_rarity = int(auras[current_aura.lower()]["rarity"]) / GLITCHED_MULTIPLIER
                elif current_biome.lower() == "dreamspace":
                    aura_rarity = int(auras[current_aura.lower()]["rarity"]) / DREAMSPACE_MULTIPLIER
                log_channel = client.get_channel(settings["log_channel_id"])
                emb = discord.Embed(
                    title=f"Aura Rolled: {current_aura}",
                    description=f"Rolled Aura: {current_aura}\nWith chances of 1/{str(aura_rarity)} (from {auras[current_aura.lower()]["native_biome"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}",
                    colour=discord.Colour.from_rgb(hex2rgb(auras[current_aura.lower()]["emb_colour"])[0],hex2rgb(auras[current_aura.lower()]["emb_colour"])[1],hex2rgb(auras[current_aura.lower()]["emb_colour"])[2])
                )
                emb.set_thumbnail(url=auras[current_aura.lower()]["img_url"])
            else:
                log_channel = client.get_channel(settings["log_channel_id"])
                emb = discord.Embed(
                    title=f"Aura Rolled: {current_aura}",
                    description=f"Rolled Aura: {current_aura}\nWith chances of 1/{auras[current_aura.lower()]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}",
                    colour=discord.Colour.from_rgb(hex2rgb(auras[current_aura.lower()]["emb_colour"])[0],hex2rgb(auras[current_aura.lower()]["emb_colour"])[1],hex2rgb(auras[current_aura.lower()]["emb_colour"])[2])
                )
                emb.set_thumbnail(url=auras[current_aura.lower()]["img_url"])
            if settings["take_screenshot_on_detection"]:                    
                auraimg = pag.screenshot(f"{MACROPATH}/scr/screenshot_aura.png")
                up = discord.File(f"{MACROPATH}/scr/screenshot_aura.png", filename="aura.png")
                emb.set_image(url="attachment://aura.png")
                if settings["mention"] and settings["mention_id"] != 0 and (int(auras[current_aura.lower()]["rarity"]) > int(settings["minimum_ping"])):
                    await log_channel.send(f"<@{settings["mention_id"]}>", embed=emb, file=up)
                else:
                    await log_channel.send(embed=emb, file=up)
            else:
                if settings["mention"] and settings["mention_id"] != 0 and (int(auras[current_aura.lower()]["rarity"]) > int(settings["minimum_ping"])):
                    await log_channel.send(f"<@{settings["mention_id"]}>", embed=emb)
                else:
                    await log_channel.send(embed=emb)
            print(f"Rolled Aura: {current_aura}\nWith chances of 1/{auras[current_aura.lower()]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}")
            logging.info(f"Rolled Aura: {current_aura}\nWith chances of 1/{auras[current_aura.lower()]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}")
            if settings["reset_aura"] != "":
                reset_aura.start()
    except KeyError:
        pass
    except Exception as e:
        print(e)

@tasks.loop(seconds=0)
async def legacy_aura_detection():
    global hex_col, hex_col2, colour, colour2
    if settings["log_channel_id"] == 0:
        print("You must select a channel ID, you can do this by running the set_log_channel command.")
        return    
    px = ImageGrab.grab().load()
    colour = px[default_pos[0], default_pos[1]]
    hex_col = rgb2hex(colour[0], colour[1], colour[2])
    colour2 = px[secondary_pos[0], secondary_pos[1]]
    hex_col2 = rgb2hex(colour2[0], colour2[1], colour2[2])
    try:
        check = auras[f"{hex_col},{hex_col2}"]
        legacy_aura_detection.stop()
    except KeyError:
        for k in auras.keys():
            _ = list(k.split(","))
            if _[0] == hex_col and _[1] == "#******":
                hex_col2 = "#******"
                legacy_aura_detection.stop()
    except Exception as e:
        print(e)

@legacy_aura_detection.after_loop
async def on_legacy_aura_detection_cancel():
    global hex_col, hex_col2, colour, colour2
    try:
        rnow = datetime.now()
        if int(auras[f"{hex_col},{hex_col2}"]["rarity"]) > int(settings["minimum_roll"]):
            if hex_col == "#5bffb0": # overdrive detector
                await asyncio.sleep(5)
                px = ImageGrab.grab().load()
                colour = px[default_pos[0], default_pos[1]]
                hex_col = rgb2hex(colour[0], colour[1], colour[2])
                if hex_col == "#d31e21":
                    hex_col2 = "#******"
                    auraimg = pag.screenshot(f"{MACROPATH}/scr/screenshot_aura.png")
                    await asyncio.sleep(1)
                    up = discord.File(f"{MACROPATH}/scr/screenshot_aura.png", filename="aura.png")
                    emb = discord.Embed(
                        title = f"Aura Rolled: {auras[f"{hex_col},{hex_col2}"]["name"]}",
                        description = f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]}\nWith chances of 1/{auras[f"{hex_col},{hex_col2}"]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}\nDetected Colours: {hex_col}, {hex_col2}",
                        colour = discord.Color.from_rgb(colour[0], colour[1], colour[2])
                    )
                    emb.set_image(url="attachment://aura.png")
                    log_channel = client.get_channel(settings["log_channel_id"])
                    if settings["mention"] and settings["mention_id"] != 0 and (int(auras[f"{hex_col},{hex_col2}"]["rarity"]) > int(settings["minimum_ping"])):
                        await log_channel.send(f"<@{settings["mention_id"]}>", embed=emb, file=up)
                    else:
                        await log_channel.send(embed=emb, file=up)
                    print(f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]}\nWith chances of 1/{auras[f"{hex_col},{hex_col2}"]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}\nDetected Colours: {hex_col}, {hex_col2}")
                    logging.info(f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]} at time: {rnow.strftime('%d/%m/%Y %H:%M:%S')} using detected colours: {hex_col}, {hex_col2}")
                else:
                    hex_col == "#5bffb0"
                    hex_col2 = "#050e09"
                    auraimg = pag.screenshot(f"{MACROPATH}/scr/screenshot_aura.png")
                    await asyncio.sleep(1)
                    up = discord.File(f"{MACROPATH}/scr/screenshot_aura.png", filename="aura.png")
                    emb = discord.Embed(
                            title = f"Aura Rolled: {auras[f"{hex_col},{hex_col2}"]["name"]}",
                            description = f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]}\nWith chances of 1/{auras[f"{hex_col},{hex_col2}"]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}\nDetected Colour: {hex_col}",
                            colour = discord.Color.from_rgb(colour[0], colour[1], colour[2])
                    )
                    emb.set_image(url="attachment://aura.png")
                    log_channel = client.get_channel(settings["log_channel_id"])
                    if settings["mention"] and settings["mention_id"] != 0 and (int(auras[f"{hex_col},{hex_col2}"]["rarity"]) > int(settings["minimum_ping"])):
                        await log_channel.send(f"<@{settings["mention_id"]}>", embed=emb, file=up)
                    else:
                        await log_channel.send(embed=emb, file=up)
                    print(f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]}\nWith chances of 1/{auras[f"{hex_col},{hex_col2}"]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}\nDetected Colour: {hex_col}")
                    logging.info(f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]} at time: {rnow.strftime('%d/%m/%Y %H:%M:%S')} using detected colour: {hex_col}")
            elif hex_col == "#3c66ff": # history detector
                await asyncio.sleep(1)
                auraimg = pag.screenshot(f"{MACROPATH}/scr/screenshot_aura.png")
                await asyncio.sleep(8)
                px = ImageGrab.grab().load()
                colour = px[default_pos[0], default_pos[1]]
                hex_col = rgb2hex(colour[0], colour[1], colour[2])
                if hex_col == "#59ff96":
                    hex_col2 = "#******"
                    auraimg = pag.screenshot(f"{MACROPATH}/scr/screenshot_aura.png")
                    await asyncio.sleep(1)
                    up = discord.File(f"{MACROPATH}/scr/screenshot_aura.png", filename="aura.png")
                    emb = discord.Embed(
                            title = f"Aura Rolled: {auras[f"{hex_col},{hex_col2}"]["name"]}",
                            description = f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]}\nWith chances of 1/{auras[f"{hex_col},{hex_col2}"]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}\nDetected Colour: {hex_col}",
                            colour = discord.Color.from_rgb(colour[0], colour[1], colour[2])
                    )
                    emb.set_image(url="attachment://aura.png")
                    log_channel = client.get_channel(settings["log_channel_id"])
                    if settings["mention"] and settings["mention_id"] != 0 and (int(auras[f"{hex_col},{hex_col2}"]["rarity"]) > int(settings["minimum_ping"])):
                        await log_channel.send(f"<@{settings["mention_id"]}>", embed=emb, file=up)
                    else:
                        await log_channel.send(embed=emb, file=up)
                    print(f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]}\nWith chances of 1/{auras[f"{hex_col},{hex_col2}"]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}\nDetected Colour: {hex_col}")
                    logging.info(f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]} at time: {rnow.strftime('%d/%m/%Y %H:%M:%S')} using detected colour: {hex_col}")
                else:
                    hex_col = "#3c66ff"
                    hex_col2 = "#******"
                    up = discord.File(f"{MACROPATH}/scr/screenshot_aura.png", filename="aura.png")
                    emb = discord.Embed(
                            title = f"Aura Rolled: {auras[f"{hex_col},{hex_col2}"]["name"]}",
                            description = f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]}\nWith chances of 1/{auras[f"{hex_col},{hex_col2}"]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}\nDetected Colour: {hex_col}",
                            colour = discord.Color.from_rgb(colour[0], colour[1], colour[2])
                    )
                    emb.set_image(url="attachment://aura.png")
                    log_channel = client.get_channel(settings["log_channel_id"])
                    if settings["mention"] and settings["mention_id"] != 0 and (int(auras[f"{hex_col},{hex_col2}"]["rarity"]) > int(settings["minimum_ping"])):
                        await log_channel.send(f"<@{settings["mention_id"]}>", embed=emb, file=up)
                    else:
                        await log_channel.send(embed=emb, file=up)
                    print(f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]}\nWith chances of 1/{auras[f"{hex_col},{hex_col2}"]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}\nDetected Colour: {hex_col}")
                    logging.info(f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]} at time: {rnow.strftime('%d/%m/%Y %H:%M:%S')} using detected colour: {hex_col}")     
            elif hex_col2 == "#******":
                auraimg = pag.screenshot(f"{MACROPATH}/scr/screenshot_aura.png")
                await asyncio.sleep(1)
                up = discord.File(f"{MACROPATH}/scr/screenshot_aura.png", filename="aura.png")
                emb = discord.Embed(
                        title = f"Aura Rolled: {auras[f"{hex_col},{hex_col2}"]["name"]}",
                        description = f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]}\nWith chances of 1/{auras[f"{hex_col},{hex_col2}"]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}\nDetected Colour: {hex_col}",
                        colour = discord.Color.from_rgb(colour[0], colour[1], colour[2])
                )
                emb.set_image(url="attachment://aura.png")
                log_channel = client.get_channel(settings["log_channel_id"])
                if settings["mention"] and settings["mention_id"] != 0 and (int(auras[f"{hex_col},{hex_col2}"]["rarity"]) > int(settings["minimum_ping"])):
                    await log_channel.send(f"<@{settings["mention_id"]}>", embed=emb, file=up)
                else:
                    await log_channel.send(embed=emb, file=up)
                print(f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]}\nWith chances of 1/{auras[f"{hex_col},{hex_col2}"]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}\nDetected Colour: {hex_col}")
                logging.info(f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]} at time: {rnow.strftime('%d/%m/%Y %H:%M:%S')} using detected colour: {hex_col}")
            else:
                auraimg = pag.screenshot(f"{MACROPATH}/scr/screenshot_aura.png")
                await asyncio.sleep(1)
                up = discord.File(f"{MACROPATH}/scr/screenshot_aura.png", filename="aura.png")
                emb = discord.Embed(
                    title = f"Aura Rolled: {auras[f"{hex_col},{hex_col2}"]["name"]}",
                    description = f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]}\nWith chances of 1/{auras[f"{hex_col},{hex_col2}"]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}\nDetected Colours: {hex_col}, {hex_col2}",
                    colour = discord.Color.from_rgb(colour[0], colour[1], colour[2])
                )
                emb.set_image(url="attachment://aura.png")
                log_channel = client.get_channel(settings["log_channel_id"])
                if settings["mention"] and settings["mention_id"] != 0 and (int(auras[f"{hex_col},{hex_col2}"]["rarity"]) > int(settings["minimum_ping"])):
                    await log_channel.send(f"<@{settings["mention_id"]}>", embed=emb, file=up)
                else:
                    await log_channel.send(embed=emb, file=up)
                print(f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]}\nWith chances of 1/{auras[f"{hex_col},{hex_col2}"]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}\nDetected Colours: {hex_col}, {hex_col2}")
                logging.info(f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]} at time: {rnow.strftime('%d/%m/%Y %H:%M:%S')} using detected colours: {hex_col}, {hex_col2}")
        else:
            print(f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]}\nWith chances of 1/{auras[f"{hex_col},{hex_col2}"]["rarity"]}\nAt time: {rnow.strftime('%d/%m/%Y %H:%M:%S')}\nDetected Colours: {hex_col}, {hex_col2}")
            logging.info(f"Rolled Aura: {auras[f"{hex_col},{hex_col2}"]["name"]} at time: {rnow.strftime('%d/%m/%Y %H:%M:%S')} using detected colours: {hex_col}, {hex_col2}")
        if int(auras[f"{hex_col},{hex_col2}"]["rarity"]) >= 1000000 and int(auras[f"{hex_col},{hex_col2}"]["rarity"]) <= 99999998:
            await asyncio.sleep(8)
        elif int(auras[f"{hex_col},{hex_col2}"]["rarity"]) >= 99999 and int(auras[f"{hex_col},{hex_col2}"]["rarity"]) <= 999999:
            await asyncio.sleep(10)
        elif int(auras[f"{hex_col},{hex_col2}"]["rarity"]) >= 9999999:
            await asyncio.sleep(10)
        if settings["reset_aura"] != "":
            reset_aura.start()
    except Exception as e:
        print(e)
    finally:
        legacy_aura_detection.restart()

@client.command()
async def plugins(ctx):
    await ctx.send("Installed Plugins:")
    for plu in _plugins:
        await ctx.send(plu)

for filename in os.listdir(f"{MACROPATH}/plugins"):
    if filename.endswith(".py"):
        client.load_extension(f"plugins.{filename[:-3]}")
        print(f"Loaded plugin: {filename[:-3]}")
        logging.info(f"Loaded plugin: {filename[:-3]}")
        _plugins.append(filename[:-3])

client.run(settings["TOKEN"])
