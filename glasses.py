from PIL import Image
import math
from PIL import ImageDraw


leftgl_x = 194
leftgl_y = 133
rightgl_x = 547
rightgl_y = 133
eyes_dist_gl = math.sqrt((rightgl_x-leftgl_x)**2 + (rightgl_y-leftgl_y)**2)


def put_glasses(img, lefteye_x, lefteye_y, righteye_x, righteye_y):
    eyes_dist = math.sqrt((righteye_x - lefteye_x) ** 2 + (righteye_y - lefteye_y) ** 2)
    koef = eyes_dist / eyes_dist_gl
    glasses = Image.open('resources/glasses.png')
    glasses = glasses.resize([int(i*koef) for i in glasses.size])
    h_ang = math.degrees(math.atan(abs(righteye_y-lefteye_y)/abs(righteye_x-lefteye_x))) * (1 if righteye_y > lefteye_y else -1)
    glasses = glasses.rotate(h_ang, expand=True)
    pos_x = lefteye_x + (righteye_x - lefteye_x)//2 - glasses.size[0]//2
    pos_y = lefteye_y + (righteye_y - lefteye_y)//2 - glasses.size[1]//2
    img.paste(glasses, (pos_x, pos_y), glasses)
    return img


def emphasize_eyes(img, lefteye_x, lefteye_y, righteye_x, righteye_y):
    draw = ImageDraw.Draw(img)
    draw.ellipse((lefteye_x-2, lefteye_y-2, lefteye_x+2, lefteye_y+2), fill='red')
    draw.ellipse((righteye_x-2, righteye_y-2, righteye_x+2, righteye_y+2), fill='red')
    return img
