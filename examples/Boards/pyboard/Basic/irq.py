#hardware platform: pyboard V1.1from pyb import Pinfrom pyb import LED#from pyb import ExtIntimport pybimport timebutton=Pin('X1',Pin.IN)             #set Pin('X1') is inputled=LED(1)led.off()def mycallback(line):               #while press button,led turn on,otherwise led turn off  if(button.value()==0):    led.off()  else:    led.on()        #every time a rising  edge is seen on the X1 pin, the callback will be called.#produce a rising edge while button is pressedextint=pyb.ExtInt('X1',pyb.ExtInt.IRQ_RISING,pyb.Pin.PULL_UP,mycallback)while True:  time.sleep(0.1)