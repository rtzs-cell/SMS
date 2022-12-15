from captcha.image import ImageCaptcha
import random, string


def captcha_check():
    chr_all = string.ascii_letters + string.digits
    chr_4 = ''.join(random.sample(chr_all, 4))
    image = ImageCaptcha().generate_image(chr_4)
    #image.save('./%s.jpg' % chr_4)
    return image, chr_4
