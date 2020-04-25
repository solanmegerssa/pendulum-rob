import serial
import time

def hil_sim(env, arduino_port="/dev/ttyACM0", baud=115200):
    arduino_connection = serial.Serial(arduino_port, baud, timeout=0.1)
    observation = env.reset()
    while True:
        env.render(mode="human")
        msg_str = write_serial_message(observation)
        print(msg_str)
        arduino_connection.write(msg_str.encode())
        observation, _, _, _ = env.step(0.1)
        time.sleep(.01) # Delay for one tenth of a second

def write_serial_message(observation):
    msg_str = "<"
    for data in observation:
        msg_str += '%.3f'%(data)
        msg_str += ", "
    msg_str += ">"

    return msg_str
