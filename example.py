from PIL import Image
import pillow_avif

bonus = "a"



img = Image.open(f"bonus/{bonus}.png")

img.show()
print(img.size)
a = img.resize((64,64), Image.ANTIALIAS)

a.save(f"bonus/{bonus}.png")

img2 = Image.open(f"bonus/{bonus}.png")
img2.show()
