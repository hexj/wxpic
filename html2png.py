import os
import time
import threading

pairs = ['EUR_USD', 'USD_JPY', 'GBP_USD', 'AUD_USD', 'NZD_USD', 'USD_CHF', 'USD_CAD']
freqs = ['D', 'H1', 'M1']
pair_freqs = [(p, f) for p in pairs for f in freqs]
fxdfs = {k: None for k in pair_freqs}


def html2png(filename):
    html_url = 'file:///home/yiju/vboxshare/output/{}.html'.format(filename)
    pic_path = '/home/yiju/vboxshare/output/{}.png'.format(filename)

    os.system('CutyCapt --url={} --out={} --min-width=900 --zoom-factor=3.0'.format(html_url, pic_path))


while 1:
    for pair, freq in fxdfs.keys():
        filename = '{}_{}'.format(pair.replace('_', ''), freq)
        t_pic = threading.Thread(
            target=html2png,
            args=(filename,))
        t_pic.daemon = True
        t_pic.start()

    time.sleep(10)
