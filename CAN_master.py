from os import system, name
import can
import time
import csv

#from tkinter import *

mode = 0 #0 = manual V, 1 = manual A, 2 = manual P, 3 = program
setpoint = 0
menuWait = 3

#voltage, current, power
valArray = [0, 0, 0]

#Dictionary from CSV file with program
#type(0=V,1=A,2=Power) , setpoint , next(condition) type (0,1,2) , next(condition) value
program = 0 #contains program instructions

# Clear screen (OS-independent)
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

# Setup can
def can_setup():
    #Set CAN0 speed to 1M bps
    os.system('sudo ifconfig can0 down')
    os.system('sudo ip link set can0 type can bitrate 1000000')
    os.system("sudo ifconfig can0 txqueuelen 100000")
    os.system('sudo ifconfig can0 up')

    can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')

# Sends a command to the charger
def can_send():
    pass

# Test message
def can_send_test(data):
    sff_frame = can.Message(arbitration_id=0x123, data=[0,1,2,3,4,5,6,7])
    can0.send(sff_frame)

# Safely turns off charger
def can_shutdown():
    pass

# Waits on a message from CAN bus
# updates relevant fields and prints information
def can_listen():
    print_data()
    time.sleep(3)

#prints data retrieved from CAN bus
#call only when new data is available
def print_data():
    clear()
    print("Controlling - ", end='')
    match mode:
        case 0: print("voltage", end='')
        case 1: print("current", end='')
        case 2: print("power", end='')
    print(", setpoint: "+str(setpoint)+", voltage: "+str(valArray[0])+", current: "+str(valArray[1])+", power: "+str(valArray[2]))

#root menu
def menu():
    quit = False
    clear()
    selection = input("--- Select function ---\n1: Set manual mode (V/A) \n2: Set manual setpoint \n3: Start program \n4: Shutdown charger\n5: Quit selection\n")
    match selection:
        case "1":
            menuMode()
        case "2":
            menuSetpoint()
        case "3":
            menuProgram()
        case "4":
            can_shutdown()
        case "5":
            quit = True
        case _:
            menuChoiceIncorrect()
            menu()
    if not quit: menu()

# Menu to choose mode
def menuMode():
    global mode
    clear()
    selection = input("Regulate in voltage (V), current (A) or power (P) (B - back): ").upper()
    match selection:
        case "V":
            mode = 0
        case "A":
            mode = 1
        case "P":
            mode = 2
        case "B":
            pass
        case _:
            menuChoiceIncorrect()
            menuMode()

# Menu to choose setpoint
def menuSetpoint():
    global setpoint
    clear()
    print("Input numerical value for setpoint in ", end='')
    match mode:
        case 0: print("voltage", end='')
        case 1: print("current", end='')
        case 2: print("power", end='')
    selection = input(" (B - back): ")
    try:
        sel = int(selection) #if a number
        if sel < 0:
            clear()
            print("Setpoint must be greater than 0")
            time.sleep(menuWait)
            menuSetpoint()
        else:
            setpoint = sel
    except:
        if(selection.upper() == "B"): pass #back option
        else:
            menuChoiceIncorrect() #other invalid option
            menuSetpoint()

#reads a program from a CSV file ( https://www.geeksforgeeks.org/load-csv-data-into-list-and-dictionary-using-python/ )
def menuProgram():
    global program
    selection = input("Please input path (relative or full) to CSV file of program (B - back):")
    match selection:
        case "B":
            pass
        case _:
            try:
                if(selection.split(".")[1].lower() == "csv"): #expects a string with exactly "*.csv" format
                    #correct format
                    pass
                else:
                    #wrong format
                    raise Exception()
            except: #any errors in formatting
                print("Wrong selection or nu such file")
                time.sleep(menuWait)
                menuProgram()

# Prints message when wrong selection is made in a menu
def menuChoiceIncorrect():
    print("No such selection, please choose a correct menu item")
    time.sleep(menuWait)

# Handles updating running programs
# automically updates mode and setpoint according to set values
# conditions: 0 = V, 1 = A, 2 = P, 3 = time
def updateProgram():
    pass

def main():
    try:
        can_setup()
    except:
        print("Error setting up CAN device, reconnect CAN device")
        time.sleep(menuWait)
    while(True):
        try:
            can_listen()
            if (mode == 3):
                updateProgram()
        except KeyboardInterrupt:
            menu()  

main()



""" def update():
    root.after(100, update)

def exampleView():
    rows = []
    count = 0
    for i in range(5):

        cols = []

        for j in range(4):

            e = Entry(relief=GROOVE)

            e.grid(row=i, column=j, sticky=NSEW)

            e.insert(END, '%d.%d' % (i, j+count))

            cols.append(e)

        rows.append(cols)
    mainloop() """