import qrcode
data = "Chichu"

img = qrcode.make(data)
img.save("E:/VS Code/Python/qrcode1.jpg")