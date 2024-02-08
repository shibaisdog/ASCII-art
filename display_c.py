import threading,pygame,time,cv2
import subprocess
from PIL import Image
import moviepy.editor as mp
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
success = True
path = "./source/video.mp4"
sound = "./source/video.mp3"
vidObj = cv2.VideoCapture(path)
clip = mp.VideoFileClip(path)
clip.audio.write_audiofile(sound)
ASCII_CHARS = [' ','`','-','_',':','"',"'",'=','~','+','*','a','\\','/','|','1','2','(',')','[',']','<','>','?','7','0','#','$','&']
ASCII_CHARS.reverse()
ASCII_CHARS = ASCII_CHARS[::-1]
def resize(image,new_width):
    (old_width,old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int((aspect_ratio * new_width)/2)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image
def grayscalify(image):
    return image.convert('L')
def modify(image,buckets):
    initial_pixels = list(image.getdata())
    new_pixels = [ASCII_CHARS[pixel_value//buckets] for pixel_value in initial_pixels]
    return ''.join(new_pixels)
def do(image,new_width):
    image = grayscalify(image)
    pixels = modify(image,9)
    len_pixels = len(pixels)
    new_image = [pixels[index:index+int(new_width)] for index in range(0, len_pixels, int(new_width))]
    return (new_image)
def print_image_with_ansi(image):
    pixels = list(image.getdata())
    ansi_code = []
    for pixel_value in pixels:
        ansi_code.append("\033[38;2;{};{};{}m".format(pixel_value[0],pixel_value[1],pixel_value[2]))
    return (ansi_code)
def work():
    success,image = vidObj.read()
    resize_p = 200
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    image = Image.fromarray(image)
    image = resize(image,resize_p)
    a = print_image_with_ansi(image)
    b = do(image,resize_p)
    e = len(b)-1
    l = int(len(a)/len(b))
    t = 0
    i = 0
    j = 0
    li = "\r"
    text = ""
    while True:
        if j >= e:
            break
        if i >= l:
            li += text+"\n"
            text = ""
            i = 0
            j += 1
        text += (a[t]+b[j][i])+"\033[0m"
        t += 1
        i += 1
    print(li, end='', flush=True)
so = pygame.mixer.Sound(sound)
so.set_volume(0.5)
so.play()
while True:
    clock.tick(10)
    vidObj.read()
    vidObj.read()
    threading.Thread(target=work).start()