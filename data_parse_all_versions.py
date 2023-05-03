import requests
import json

from Weapon import Weapon

response_versions = requests.get(
    url="https://leanny.github.io/splat3/versions.json"
)

all_verions_list: list = json.loads(response_versions.text)

last_version: str = all_verions_list[-1]


def set_version_url(version = last_version):
    global latest_version_response
    latest_version_response= requests.get(
        url = f"https://leanny.github.io/splat3/data/mush/{version}/WeaponInfoMain.json"
    )

    # print(version)

    global last_data
    last_data= json.loads(latest_version_response.text)

set_version_url()

ban_word_list = [
    "Coop",
    "Msn",
    "Rival",
    "AMB",
    "Free",
    "Mission",
]


all_sub_specials_weapons = {}


def is_ok(name):
    for word in ban_word_list:
        if word in name:
            return False

    return True


def add_sub_special(weapon: Weapon):
    if not weapon.sub_weapon_name in all_sub_specials_weapons.keys():
        all_sub_specials_weapons[weapon.sub_weapon_name] = weapon.sub_weapon_image_url

    if not weapon.special_weapon_name in all_sub_specials_weapons.keys():
        all_sub_specials_weapons[weapon.special_weapon_name] = weapon.special_weapon_image_url

def get_all_weapon_info():
    weapons_dict = {}

    for dictonary in last_data:
        current_weapon = Weapon(dictonary)
        if is_ok(current_weapon.name):
            weapons_dict[current_weapon.name] = current_weapon
            # print(current_weapon)

            add_sub_special(current_weapon)

    return weapons_dict

all_weapons = get_all_weapon_info()

