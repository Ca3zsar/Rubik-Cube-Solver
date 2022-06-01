import serial
import time

serial_comm = serial.Serial('COM3', 9600)
serial_comm.timeout = 0.1
time.sleep(1)

while True:
    command = input("Enter command: ").strip()
    if command == 'q':
        break

    serial_comm.write((command + '\n').encode())
    # time.sleep(1)
    print(serial_comm.readall().decode())

serial_comm.close()