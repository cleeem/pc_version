from PIL import Image
import os

for file in os.listdir("assets_badges"):
    img = Image.open(f"assets_badges/{file}")

    # img.show()
    print(img.size)
    a = img.resize((64,64), Image.ANTIALIAS)

    a.save(f"assets/{file}")

    img2 = Image.open(f"assets/{file}")
    # img2.show()

Image._Color()