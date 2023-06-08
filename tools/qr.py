import qrcode

data = 'https://www.linkedin.com/in/paul-yatskevich/'

qr = qrcode.QRcode(version = 1, box_size = 10, boeder = 5)

qr add_data(data)

qr.make(fit=True)
img = qr.make_image(fill_color = 'black', back_color = 'white')

img.save('path')



# from pyzbar.pyzbar import decode
# from PIL import Image

# img = Image.open('path')

# result = decode(img)

# print(result)