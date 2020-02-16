# @see https://www.embarcados.com.br/raspberry-pi-gpio-modo-input-python/
import RPi.GPIO as gpio
import os
import time
import requests
import config

gpio.setmode(gpio.BCM)

gpio.setup(23, gpio.IN, pull_up_down = gpio.PUD_DOWN)
gpio.setup(24, gpio.IN, pull_up_down = gpio.PUD_DOWN)
gpio.setup(27, gpio.OUT)




def doorbell(which, holding=False, previous_alert=0):
    labels = {'front': 'sala', 'back': 'cozinha'}

    if(holding == True or time.time() - previous_alert < 15):
        return previous_alert

    # alerta
    return alert(labels[which])


def alert(label):
    print 'Alerting ' + label
    payload = {'value1': label}
    r = requests.post("https://maker.ifttt.com/trigger/doorbell/with/key/" + config.IFTTT_TOKEN, params=payload)
    return time.time()


def alert_init():
    requests.post("https://maker.ifttt.com/trigger/doorbell_init/with/key/" + config.IFTTT_TOKEN)




holding = {'front': False, 'back': False}
previous_alert = {'front': 0, 'back': 0}
ios = {23: 'back', 24: 'front'}


alert_init()

while True:
    pressing = False
    pressed = {'front': gpio.input(24), 'back': gpio.input(23)}

    # Cozinha
    slug = 'back'
    if(pressed[slug] == 1):
        previous_alert[slug] = doorbell(slug, holding[slug], previous_alert[slug])
        holding[slug] = True
        pressing = True
    else:
        holding[slug] = False


    # Sala
    slug = 'front'
    if(pressed[slug] == 1):
        previous_alert[slug] = doorbell(slug, holding[slug], previous_alert[slug])
        holding[slug] = True
        pressing = True
    else:
        holding[slug] = False

    time.sleep(0.2)

gpio.cleanup()
exit()