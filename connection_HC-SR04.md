HC-SR04 VCC  -----------------> Pi 5V
HC-SR04 GND  -----------------> Pi GND

HC-SR04 TRIG -----------------> Pi GPIO23

HC-SR04 ECHO --[1 kΩ]--o------> Pi GPIO24
                        |
                      [2 kΩ]
                        |
                        +------> Pi GND
