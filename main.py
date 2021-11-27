import sys
import os
from datetime import datetime
import json

def get_data():
    with open("record.json","r") as f:
        d = f.read()

    dj = json.loads(d)
    return dj

def com():
    if len(sys.argv) == 2:
        if sys.argv[1] == "rec":
            return 1
        elif sys.argv[1] == "run":
            return 2
    return 0

def record():
    data = get_data()
    root = data["root"]
    data = ""
    rec = {}
    for r,d,f in os.walk(root,topdown=True):
        rec[r] = {"dir":d,"file":f}
    
    data = {
        "root": root,
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "map": rec
    }

    with open("record.json","w") as f:
        f.write(json.dumps(data))

def run():
    res = {
        "new_dir": [],
        "new_file": [],
        "del_dir": [],
        "del_file": []
    }
    data = get_data()
    for r,_,f in os.walk(data["root"],topdown=True):
        if r in data["map"]:
            x = data["map"][r]
        else:
            print("NEW DIR : "+r)
            res["new_dir"].append(r)
            continue

        for i in x["file"]:
            if i not in f:
                print("DEL FILE: "+r+"/"+i)
                res["del_file"].append(r+"/"+i)

        for i in f:
            if i not in x["file"]:
                print("NEW FILE: "+r+"/"+i)
                res["new_file"].append(r+"/"+i)

        del data["map"][r]

    for i in data["map"].keys():
        print("DEL DIR : "+i)
        res["del_dir"].append(i)
        print("\tFILE INSIDE "+i)
        for j in data["map"][i]["file"]:
            print("\t - "+j)
            res["del_file"].append(i+"/"+j)

    with open("log.json","r") as f:
        a = json.loads(f.read())

    with open("log.json","w") as f:
        pl = {
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "root": data["root"],
            "alert": res
        }
        a.append(pl)
        f.write(json.dumps(a))

def main():
    try:
        c = com()
        if c == 1:
            record()
        elif c == 2:
            run()
        else:
            print("[-] Invalid argument")
    except:
        print("[-] Unknown error")

main()