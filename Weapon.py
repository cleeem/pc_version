
class Weapon:

    ROOT_URL_IMAGES = "https://leanny.github.io/splat3/images"


    switch_weapon_type = {
        "Blaster"   : "Blaster",
        "Brush"     : "Brush",
        "Charger"   : "Charger",
        "Maneuver"  : "Dualies",
        "Roller"    : "Roler",
        "Saber"     : "Splatana",
        "Shelter"   : "Brella",
        "Shooter"   : "Shooter",
        "Slosher"   : "Slosher",
        "Spinner"   : "Splatling",
        "Stringer"  : "Stringer",
    }



    def __init__(self, data: dict) -> None:
        self.id: int = data["Id"]
        self.name: str = data["__RowId"].removesuffix("_00") 

        self.damage_type: str = data["DefaultHitEffectorType"]
        self.range: float = data["Range"]
        self.shop_price: int = data["ShopPrice"]
        self.unlock_rank: int = data["ShopUnlockRank"]
        self.points_for_special: int = data["SpecialPoint"]
        
        self.base_type = data["__RowId"].split("_")[0]
        self.type_translate = self.switch_weapon_type.get(data["__RowId"].split("_")[0], None)

        self.image_url = f"{self.ROOT_URL_IMAGES}/weapon_flat/Path_Wst_{data['__RowId']}.png"
        # print(self.image_url)

        sp_wp: str = data["SpecialWeapon"]
        self.special_weapon_name: str = sp_wp.removeprefix("Work/Gyml/").removesuffix(".spl__WeaponInfoSpecial.gyml")
        self.special_weapon_image_url: str = f"{self.ROOT_URL_IMAGES}/subspe/Wsp_{self.special_weapon_name}00.png"

        sb_wp: str = data["SubWeapon"]
        self.sub_weapon_name: str = sb_wp.removeprefix("Work/Gyml/").removesuffix(".spl__WeaponInfoSub.gyml")
        self.sub_weapon_image_url: str = f"{self.ROOT_URL_IMAGES}/subspe/Wsb_{self.sub_weapon_name}00.png"


    def __str__(self) -> str:
        res = f"""
ID                 : {self.id} 
Name               : {self.name}
weapon type        : {self.type}
image Url          : {self.image_url}
Hitbox Type        : {self.damage_type}
Range              : {self.range}
Shop Price         : {self.shop_price}
Unlock Rank        : {self.unlock_rank}
Sub Weapon         : {self.sub_weapon_name}
Sub Weapon Url     : {self.sub_weapon_image_url}
Special Weapon     : {self.special_weapon_name}
Special Weapon Url : {self.special_weapon_image_url}

"""
        return res
    