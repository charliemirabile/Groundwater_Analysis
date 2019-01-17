import serial

io=serial.Serial('/dev/ttyACM0',9600)

print(io.name)

while True:
    test=io.readline()
    print(str(test))
