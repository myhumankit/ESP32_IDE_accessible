# Complete project details at https://RandomNerdTutorials.com


import sys


def web_page():

    # bmp180 = bmp180.bmp180(i2c=busi2c)

    # bmp180 = BMP180(busi2c)

    html = """<!DOCTYPE html>

  <html>

  <head>

  <meta name="viewport" content="width=device-width, initial-scale=1">

  <link rel="icon" href="data:,"><style>body { text-align: center; font-family: "Trebuchet MS", Arial;}

  table { border-collapse: collapse; width:35%; margin-left:auto; margin-right:auto; }

  th { padding: 14px; background-color: #0043af; color: white; }

  tr { border: 2px solid #ddd; padding: 12px; }

  tr:hover { background-color: #bcbcbc; }

  td { border: none; padding: 16px; }

  </style>

  </head>

  <body>

  <h1>ESP with BMp180</h1>

  <table><tr><th>MEASUREMENT</th><th>VALUE</th></tr>

  <tr><td>Temp. Celsius</td><td><span class="sensor">""" + str(bmp180.temperature) + """</span></td></tr>

  <tr><td>Temp. Fahrenheit</td><td><span class="sensor">""" + str(round((bmp180.read_temperature()/100.0) * (9/5) + 32, 2)) + """F</span></td></tr>

  <tr><td>Pressure</td><td><span class="sensor">""" + str(bmp180.pressure) + """</span></td></tr>

  <tr><td>Humidity</td><td><span class="sensor">""" + str(999) + """</span></td></tr>

  </body>

  </html>"""

    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr_1 = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

print("Address 1 : ", addr_1)

s.bind(('', 80))

s.listen(1)


while True:

    try:

        if gc.mem_free() < 102000:

            gc.collect()

        #

        s.settimeout(2)

        try:

            conn, addr = s.accept()

            except Exception as er:

                # conn.close()

                pass

                # s.close()

                print(er.args[0] in (110, 'timed out'))

                print("Connexion closed.").

                # pass

                # 110 is ETIMEDOUT

            else:

                print('Client connecté de ', addr)

                conn.settimeout(4.0)

                print('Got a connection from %s' % str(addr))

                request = conn.recv(1024)

                conn.settimeout(None)

                request = str(request)

                print('Content = %s' % request)

                response = web_page()

                conn.send('HTTP/1.1 200 OK\n')

                conn.send('Content-Type: text/html\n')

                conn.send('Connection: close\n\n')

                conn.sendall(response)

                conn.close()

            finally:

                print("execution finally")
