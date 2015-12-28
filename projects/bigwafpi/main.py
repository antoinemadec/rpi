#!/usr/bin/python



#====================================
# imports
#====================================
import copy
import subprocess as proc
from multiprocessing import Process, Queue
from time import *
import Adafruit_CharLCD as LCD



#====================================
# parameters
#====================================
MAX_PARAM_VALUE = 512-1
PARAM_NAME_SIZE = 5
CFG_FILENAME    = "config.txt"



#====================================
# functions
#====================================
def parse_cfg(file_name):
    cfg_file        = open (file_name)
    cfg             = cfg_file.read().splitlines()
    l_file_name     = []
    l_effect_name   = []
    l_default_val   = []
    for line in cfg:
        l_default_val_for_line = []
        if line[0] == '#':
            continue
        else:
            tab = line.split(";")
            for tab_idx in range(0, len(tab)):
                elt = tab[tab_idx].strip()
                if tab_idx == 0:
                    l_file_name.append(elt)
                elif tab_idx == 1:
                    l_effect_name.append(elt)
                else:
                    param = elt.split("=")[0]
                    value = int(elt.split("=")[1])
                    l_default_val_for_line.append([param, value])
            l_default_val.append(l_default_val_for_line)
    return (l_file_name, l_effect_name, l_default_val)


def update_cfg(file_name, effect_name, curr_param_val):
    param_str = ""
    print curr_param_val
    for i in range(0,len(curr_param_val)):
        name    = curr_param_val[i][0]
        value   = str(curr_param_val[i][1])
        param_str += "; "+name+"="+value+" "
    proc.call(["/bin/bash", "./update_params_in_cfg.bash"]+[file_name,effect_name,param_str])


def clip(lo, x, hi):
    return max(lo, min(hi, x))


def get_next_state(state, sel, left, right, down, up):
    global effect_nb
    mode        = state[0]
    eff_idx     = state[1]
    param_idx   = state[2]
    param_val   = copy.deepcopy(state[3])
    save        = state[4]
    if sel:
        mode = (mode+1)%2
        if mode==1:
            param_idx=0
    elif mode==0:
        # effect mode
        if right:
            eff_idx = clip(0, eff_idx+1, effect_nb-1)
        elif left:
            eff_idx = clip(0, eff_idx-1, effect_nb-1)
        elif down:
            save = 1
        else:
            save = 0
    else:
        # parameters mode
        param_nb    = len(param_val[eff_idx])
        if right:
            param_idx = clip(0, eff_idx+1, param_nb-1)
        elif left:
            param_idx = clip(0, eff_idx-1, param_nb-1)
        elif up:
            param_val[eff_idx][param_idx][1] = clip(0, param_val[eff_idx][param_idx][1]+1, MAX_PARAM_VALUE)
        elif down:
            param_val[eff_idx][param_idx][1] = clip(0, param_val[eff_idx][param_idx][1]-1, MAX_PARAM_VALUE)
    return [mode, eff_idx, param_idx, param_val, save]


def print_effect(effect_name):
    print "DBG: effect_name=%s" % effect_name
    lcd.clear()
    lcd.blink(False)
    lcd.message(effect_name)
    lcd.set_cursor(0,1)
    lcd.message("save +")   # TODO


def print_param(curr_param_val, param_idx, clear):
    pos=[[0,0], [8,0], [1,0], [1,8]]
    if clear:
        lcd.clear()
        lcd.blink(True)
        for p in range(0,len(curr_param_val)):
            name = curr_param_val[p][0][0:PARAM_NAME_SIZE].ljust(PARAM_NAME_SIZE)
            val  = curr_param_val[p][1]
            lcd.set_cursor(pos[p][0],pos[p][1])
            lcd.message(name+str(val))
    else:
        val  = curr_param_val[param_idx][1]
        lcd.set_cursor(pos[param_idx][0]+PARAM_NAME_SIZE,pos[param_idx][1])
        lcd.message(str(val))
    lcd.set_cursor(pos[param_idx][0],pos[param_idx][1])


def print_lcd(q_print):
    while True:
        args = q_print.get()
        # only consider last value
        while q_print.empty() == False:
            args = q_print.get()
        if args[0] == 0:
            print_effect(args[1])
        else:
            print_param(args[1],args[2],args[3])


def send_param_pd(curr_param_val):
    p_idx=[1,2,0,3]
    string=""
    for i in range(0,len(curr_param_val)):
        string += str(p_idx[i]) + " " + str(curr_param_val[i][1]*2) + ";\n" # *2 because 512 to code 1024
    proc.check_output("echo -n "+'"'+string+'" | pdsend 5001 localhost udp', shell=True)


#====================================
# exectution
#====================================
# open effect name and functions
(file_name, effect_name, param_val) = parse_cfg(CFG_FILENAME)
effect_nb = len(effect_name)

# init LCD
lcd = LCD.Adafruit_CharLCDPlate()
lcd.clear()
lcd.set_color(1,1,1)
lcd.message("** Big Waf PI **\n");
lcd.message("      by antoine");

# spawn pd
proc.call("pd -nomidi -nogui server.pd &", shell=True)
sleep(5)

# spawn LCD printing
q_print = Queue()
p = Process(target=print_lcd, args=(q_print,))
p.start()

# listen to GPIO ; communicate with pd
state   = [0,0,0,param_val,0]
boot    = 1
idle    = 1
while True:
    next_state = get_next_state(
            state,
            lcd.is_pressed(LCD.SELECT),
            lcd.is_pressed(LCD.LEFT), lcd.is_pressed(LCD.RIGHT),
            lcd.is_pressed(LCD.DOWN), lcd.is_pressed(LCD.UP))
    # avoid rebond with push buttons
    if idle == 1:
        sleep(.2)
        idle = 0
    if next_state != state or boot:
        mode_old        = state[0]
        eff_idx_old     = state[1]
        state           = next_state
        mode            = state[0]      # 0: choose effect ; 1: change params
        eff_idx         = state[1]
        param_idx       = state[2]
        param_val       = state[3]
        save            = state[4]
        current_param   = param_val[eff_idx]
        if mode==0:
            q_print.put((mode, effect_name[eff_idx]))
            if eff_idx_old != eff_idx or boot:
                boot = 0
                # close old effect, open and display new
                proc.check_output("echo '1 "+ file_name[eff_idx_old] +";' | pdsend 5000 localhost", shell=True)
                proc.check_output("echo '0 "+ file_name[eff_idx] +";' | pdsend 5000 localhost", shell=True)
            if save:
                update_cfg(CFG_FILENAME,effect_name[eff_idx],current_param)
        else:
            q_print.put((mode, current_param, param_idx, mode_old != mode))
        send_param_pd(current_param)
    else:
        sleep(.2)
        idle = 1
