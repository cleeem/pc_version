from genericpath import exists
import os
import requests


import customtkinter

import data_parse_all_versions

weapon_type_list = [
    "Blaster",
    "Brush",
    "Charger",
    "Maneuver",
    "Roller",
    "Saber",
    "Shelter",
    "Shooter",
    "Slosher",
    "Spinner",
    "Stringer"
]

# try:
#     for weapon_type in weapon_type_list:
#         for file in os.listdir(f"assets/{weapon_type}"):
#             os.remove(f"assets/{weapon_type}/" + file)
# except:
#     print("oui")


def dl_image(file_name, url):
    if not exists(f"assets/{file_name}.png"):
        with open(f"assets/{file_name}.png", 'wb') as file:
            file.write(requests.get(url=url).content)   

def update_weapons():
    weapon_dict = data_parse_all_versions.all_weapons

    global i
    i = 0
    lenght = len(weapon_dict)

    for name, weapon in weapon_dict.items():
        complete_name = f"{weapon.base_type}/{name}"
        dl_image(file_name=complete_name, url=weapon.image_url)
        print(f"download weapons : {i}/{lenght}", end="\r")
        i += 1

    print("weapons updated successfuly")

def update_subs_specials():
    weapon_dict = data_parse_all_versions.all_sub_specials_weapons

    global i
    i = 0
    lenght = len(weapon_dict)

    for name, url in weapon_dict.items():
        complete_name = f"subs_specials/{name}"
        dl_image(file_name=complete_name, url=url)
        print(f"download subs and spacials : {i}/{lenght}", end="\r")
        i += 1
    print("sub and specials updated successfuly")


update_weapons()
update_subs_specials()