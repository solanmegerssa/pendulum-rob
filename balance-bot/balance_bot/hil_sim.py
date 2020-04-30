import serial
import time

def hil_sim(env, arduino_port="/dev/ttyACM0", baud=9600):
    arduino_connection = serial.Serial(arduino_port, baud, timeout=0.1)
    observation = env.reset()
    while True:
        env.render(mode="human")
        write_observation_msg(observation, arduino_connection)
        time.sleep(.01) # Delay for one tenth of a second
        control_response = read_control_msg(arduino_connection)
        observation, _, _, _ = env.step(control_response)

def write_observation_msg(observation, arduino_connection):
    """ takes array of observation and writes to serial line """
    msg_str = "<"
    for data in observation:
        msg_str += '%.6f'%(data)
        msg_str += ", "
    msg_str += ">"
    # print(msg_str)
    arduino_connection.write(msg_str.encode())

def read_control_msg(arduino_connection):
    """ reads serial line, parses message, and returns control command """
    try:
        data = arduino_connection.readline()[:-2].decode() #the last bit gets rid of the new-line chars
    except UnicodeDecodeError:
        print("decode error")
        return 0.0
    
    control = 0.0
    if data and data[0:2]=="<@":
        # print("DATA: {}".format(data))
        control = data.split("@")[-1]
        # print("control after split: {}".format(control))
        control = float(control.split(">")[0])
    else:
        print("missed control loop")
    print(control)
    return control