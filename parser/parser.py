import os
import csv
import re
import json
import argparse
import ast

from pathlib import Path
from os import path

def __init__(self) -> None:
    pass

def readCommands(file: Path) -> list:
    with open(file) as f:
        data = json.load(f)
        tmpList = list() 
        for name in data:
            tmpList.append(name['Name'])
        return tmpList 

def parseAll(commands: list, folderpath: Path, commandlist: dict) -> dict:

    for filename in os.listdir(folderpath):
        if filename.endswith(".ps1"):
            scriptName = str(filename)
            filepath = os.path.join(folderpath, filename)
            with open(filepath, encoding="utf8") as f:
                read_data = f.read()
                commandlist[scriptName] = {}                
                for command in commands:
                    commandlist[scriptName][command] = 1 
                    for scriptWord in read_data.split():
                        if scriptWord == command:
                            commandlist[scriptName][scriptWord] += 1
    
    return commandlist
                

def parseSingle(commands: list, folderpath: Path, filename: Path, commandlist: dict) -> dict:

    filepath = os.path.join(folderpath, filename)

    with open(filepath, encoding="utf8") as f:
        read_data = f.read()

        scriptName = str(filename)
        commandlist[scriptName] = {}
        
        for command in commands:
            commandlist[scriptName][command] = 1
            for scriptWord in read_data.split():
                if scriptWord == command:
                    try:
                        commandlist[scriptName][scriptWord] += 1
                    except:
                        commandlist[scriptName][scriptWord] = 1

    return commandlist

def findCommands(commands: list, folderpath: Path, filename: Path) -> list:
    commandlist = dict()

    if filename:
        commandlist = parseSingle(commands, folderpath, filename, commandlist) 
    else:
        commandlist = parseAll(commands, folderpath, commandlist)
    
    return commandlist

def convertToCSV(commandlist: dict, commands: list) -> None:
    commands.insert(0, 'FileName')

    with open('output.csv', 'w', newline='') as csvfile:
        w = csv.DictWriter(csvfile, commands)
        w.writeheader()
        for k in commandlist:
            w.writerow({command: commandlist[k].get(command) or k for command in commands})

def main():
    parser = argparse.ArgumentParser(description="Parses PowerShell script from the selected folder")
    parser.add_argument("folderpath", type=Path, help="Select the folder path that contains the script(s)")
    parser.add_argument("-s", "--single", type=Path, help="Process single file only, specifiy the PowerShell script") 
    parser.add_argument("-c", "--csv", action="store_true", help="Outputs to CSV instead of JSON")

    args = parser.parse_args()

    pathf = "commands.json"
    file = Path(pathf)

    if not(path.exists("commands.json")):
        print("Missing commands.json file!")
        exit()

    commands = readCommands(file) 

    commandlist = findCommands(commands, args.folderpath, args.single)

    with open("output.json", 'w') as outfile:
        json.dump(commandlist, outfile)

    convertToCSV(commandlist, commands)

if __name__ == "__main__":
    main()