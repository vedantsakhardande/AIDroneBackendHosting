import qrcode
import random

def genqrcode():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    number=random.randint(0,100)
    number=number*random.randint(0,100)
    number=number*random.randint(0,100)
    number=number*random.randint(0,100)
    number=number*random.randint(0,100)
    qr.add_data(number)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img = img.save("code.jpg")

if __name__ == "__main__":
    genqrcode()