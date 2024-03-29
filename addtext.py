import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont

def cv2ImgAddText(img, text, x, y, textColor, textSize):
    if (isinstance(img, numpy.ndarray)):  #判断是否OpenCV图片类型
        y = int(y * (img.shape[0]/650))#height
        x = int(x * (img.shape[1]/490))#width
        textSize = int(textSize*(img.shape[0]/650)* (img.shape[1]/490))
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(".font/simsun.ttc", textSize, encoding="utf-8")
    #draw.text((left, top), text, textColor, font=fontText)
    shadowcolor = (0,0,0)
    # thin border
    draw.text((x - 1, y), text, font=font, fill=shadowcolor)
    draw.text((x + 1, y), text, font=font, fill=shadowcolor)
    draw.text((x, y - 1), text, font=font, fill=shadowcolor)
    draw.text((x, y + 1), text, font=font, fill=shadowcolor)
  
    # thicker border
    draw.text((x - 1, y - 1), text, font=font, fill=shadowcolor)
    draw.text((x + 1, y - 1), text, font=font, fill=shadowcolor)
    draw.text((x - 1, y + 1), text, font=font, fill=shadowcolor)
    draw.text((x + 1, y + 1), text, font=font, fill=shadowcolor)
    # now draw the text over it
    draw.text((x, y), text, font=font, fill=textColor)
    
    return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)