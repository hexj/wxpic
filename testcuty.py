import threading
import os


def get_pic(filename):
    os.system('CutyCapt --url=file:///home/yiju/Downloads/front/tech.html --out={}.png --min-width=100 --min-height=10 --zoom-factor=2.0'.format(filename))


ths = []
for i in range(8):
    t = threading.Thread(target=get_pic, args=('tech'+str(i),))
    ths.append(t)
    t.start()
    # get_pic('tech'+str(i))

for t in ths:
    t.join()
