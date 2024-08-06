import qrcode

def generate_qr_code(data, filename):
    """
    Generate a QR code from the provided data and save it to a file.

    Args:
        data (str): The data to encode in the QR code.
        filename (str): The filename to save the QR code image to.
    """
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(filename)

# Example usage:
data = 'https://www.linkedin.com/in/paul-yatskevich/'
filename = 'linkedin_qr.png'
generate_qr_code(data, filename)





from pyzbar import pyzbar
from PIL import Image

def decode_qr_code(filename):
    """
    Decode a QR code from an image file.

    Args:
        filename (str): The filename of the QR code image to decode.

    Returns:
        list: A list of decoded QR code data.
    """
    img = Image.open(filename)
    decoded_data = pyzbar.decode(img)
    return decoded_data

# Example usage:
filename = 'linkedin_qr.png'
decoded_data = decode_qr_code(filename)
print(decoded_data)
