import hashlib
import os
import sys
import time
import requests
import json
import re
import socket
import uuid
import subprocess
import shutil
import base64
import traceback

from config.files.mc_replace_text import mc_replace_text_mccolors, mc_replace_text_json
from config.files.questions import skip_0on, specific_name, specific_version
from config.files.checks_mcptool import check_node, check_server, check_encoding, check_java, check_file, check_folder, check_nmap, check_port, check_qubo, check_ngrok, check_updates, check_nmap_error, motd_1, motd_2, motd_3
from mcstatus import MinecraftServer
from datetime import datetime
from colorama import Fore, init
from json import JSONDecodeError
def usage():
    print ("Command: " + sys.argv[0] + " <ip> <port> <packet>")

def get_server(ip, skip, logs_file):
    """ Server info """
    global number_of_servers

    try:
        players = None
        srv = MinecraftServer.lookup(ip)

        response = srv.status()
        motd = mc_replace_text_mccolors(response.description)
        motd_ = response.description.replace('§1', '').replace('§2', '').replace('§3', '').replace('§4', '').replace('§5', '').replace('§6', '').replace('§7', '').replace('§8', '').replace('§9', '').replace('§0', '').replace('§a', '').replace('§b', '').replace('§c', '').replace('§d', '').replace('§e', '').replace('§f', '').replace('§k', '').replace('§l', '').replace('§m', '').replace('§n', '').replace('§o', '').replace('§r', '').replace('\n', '')
        motd_ = re.sub(" +", " ", motd_)
        version = mc_replace_text_mccolors(response.version.name)
        version_ = response.version.name.replace('§1', '').replace('§2', '').replace('§3', '').replace('§4', '').replace('§5', '').replace('§6', '').replace('§7', '').replace('§8', '').replace('§9', '').replace('§0', '').replace('§a', '').replace('§b', '').replace('§c', '').replace('§d', '').replace('§e', '').replace('§f', '').replace('§k', '').replace('§l', '').replace('§m', '').replace('§n', '').replace('§o', '').replace('§r', '').replace('\n', '')
        version_ = re.sub(" +", " ", version_)

        if response.players.sample is not None:
            players = str([f"{player.name} ({player.id})" for player in response.players.sample])
            players = players.replace("[", "").replace("]", "").replace("'", "")

        if skip:
            if not str(response.players.online) == "0":
                pass

            else:
                return

        print(f"\n     {lblack}[{lred}I{white}P{lblack}] {white}{ip}")
        print(f"     {lblack}[{lred}MO{white}TD{lblack}] {white}{motd}")
        print(f"     {lblack}[{lred}Ver{white}sion{lblack}] {white}{version}")
        print(f"     {lblack}[{lred}Proto{white}col{lblack}] {white}{response.version.protocol}")
        print(f"     {lblack}[{lred}Play{white}ers{lblack}] {white}{response.players.online}{lblack}/{white}{response.players.max}")

        if bot_connect:
            host = ip.split(":")
            connect("check", host[0], host[1], None, None)

        with open(logs_file, "a", encoding="utf8") as f:
            f.write(f"\n\n[IP] {ip}")
            f.write(f"\n[MOTD] {motd_}")
            f.write(f"\n[Version] {version_}")
            f.write(f"\n[Protocol] {response.version.protocol}")
            f.write(f"\n[Players] {response.players.online}/{response.players.max}")

        if response.players.sample is not None:
            if players != "":
                try:
                    re.findall(r"[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]", players)
                    if "00000000-0000-0000-0000-000000000000" not in players:
                        print(f"     {lblack}[{lred}Nam{white}es{lblack}] {white}{players}")
                        with open(logs_file, "a") as f:
                            f.write(f"\n[Names] {players}")

                except:
                    pass

        number_of_servers += 1

    except:
        pass

