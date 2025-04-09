from PIL import Image
img = Image.open("download.jpeg")
img.save("icon.ico", format="ICO")
