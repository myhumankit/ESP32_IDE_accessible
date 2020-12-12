# First Steps

- [First Steps](#first-steps)
  - [You should know](#you-should-know)
  - [Tutorial](#tutorial)
    - [Install a new firmware or update yours](#install-a-new-firmware-or-update-yours)
      - [On ESP32](#on-esp32)
      - [A rediger selon le site officiel(ESP2866)](#a-rediger-selon-le-site-officielesp2866)
    - [Connect your ESP with the IDE](#connect-your-esp-with-the-ide)
    - [Upload a file](#upload-a-file)
    - [File operations on the device](#file-operations-on-the-device)
    - [Run a program](#run-a-program)
    - [Choose a theme](#choose-a-theme)
  - [Custom a theme](#custom-a-theme)

## You should know

* MicroPython is a version of Python softawre adapted for microcontrollers like ESP32 and Pyboard


## Tutorial

### Install a new firmware or update yours

* All the firmwares are availables here[https://micropython.org/download](https://micropython.org/download)

#### On ESP32

* Go to the menu **Tools==>BurnFirmware** or press **F7**
* Select the port of the device to update
* Select adresses: **0x1000**
* Choose the binary previously downloaded on the website dedicated
* Click on **Install firmware**
* Wait a sonor signal *device connected* and close the dialog
* You can now connect you device !

#### A rediger selon le site officiel(ESP2866)

* Go to the menu **Tools==>BurnFirmware** or press **F7**
* Select the port of the device to update
* Select adresses: **0x10**
* Choose the binary previously downloaded on the website dedicated
* Click on **Install firmware**
* Wait a sonor signal *device connected* and close the dialog
* You can now connect you device !

### Connect your ESP with the IDE

1. Go to the menu **Tools==>Connection** Settings or press **F2**
2. Select the port where your device is connected
3. Don't touch the defaults options, they're optimized
4. Click on the **Connect** button
5. If the device has been connected succesfully, you can access on the tree view section "Device". To do that press F9.

### Upload a file

1. Create a new tab in the editor with Ctrl+n or open a file of your computer with Ctrl+O
2. Edit it
3. To Upload press F4 or go to the menu **Tools==>Upload**

### File operations on the device

1. Go to the section Device of the TreeView
2. Right click on the item of your choice
3. You will see a clipboard menu with several options

### Run a program

With the TreeView:
    1. Go to the section Device of the TreeView
    2. Right click on the item of your choice
    3. Select **run**
    4. The output on the program run is on the shell panel
With the current file edited and **SAVED**:
    1. Press **F5** or go to **Tools==>UploadAndRun**
    2. The output on the program run is on the shell panel

### Choose a theme

1. Go to **Tools==>Themes** then select:
   * Dark theme ==> by default white on black with syntax highlight
   * Light theme ==> by default black on white with syntax highlight
   * Syntax Higlight On/Off

## Custom a theme

1.Open the file customize.json in the app folder
2. Change the key value of your choice with hexadecimal color picked on this site: [https://www.colorhexa.com/](https://www.colorhexa.com/) EX:
    `Text Background: "#ff0000",`
3. Save the file
4. Reload App