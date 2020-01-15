#!python
import os
import json
import sys
import subprocess
def parse():
    scriptPath = os.path.dirname(__file__)+"\\.bycmd.json"
    if os.path.exists(scriptPath):
        jsonCon=json.loads(''.join(open(scriptPath,'r').readlines()))
        javaPath=jsonCon['java']
        apktoolPath=jsonCon['apktool']
        apksignerPath=jsonCon['apksigner']
        jadxPath=jsonCon['jadx']
        if len(sys.argv)<3:
            print("bycmd unpack/pack <IN> <OUT> -s deviceSerial -p PC_port")
        else:
            todo=sys.argv[1]
            IN=sys.argv[2]
            OUT=sys.argv[3]
            server=[]
            port='5005'
            if '-s' in sys.argv:
                server=['-s',sys.argv[sys.argv.index("-s")+1]]
            if '-p' in sys.argv:
                post=sys.argv[sys.argv.index('-p')+1]
            if todo=="unpack":
                apktool_cmd=["{}".format(javaPath)]+["-Xmx256m"]+["-jar"]+["{}".format(apktoolPath)]+["d"]+["-f"]+["-o"]+["{}".format(OUT)]+["{}".format(IN)]
                jadx_cmd=["{}".format(jadxPath)]+["-r"]+["-d"]+["{}".format(OUT)]+["{}".format(IN)]
                print("apktool disasm:")
                subprocess.Popen(apktool_cmd,shell=True).wait()
                print("jadx decompile:")
                subprocess.Popen(jadx_cmd,shell=True).wait()
            elif todo=="pack":
                keyPath=jsonCon['key']
                adbPath=jsonCon['adb']
                mainfestPath=os.path.abspath(IN)+"\\AndroidManifest.xml"
                package=None
                if os.path.exists(mainfestPath):
                    import xml.etree.ElementTree as ET
                    tree = ET.parse(mainfestPath)
                    package=tree.getroot().get("package")
                apktool_cmd=["{}".format(javaPath)]+["-Xmx256m"]+["-jar"]+["{}".format(apktoolPath)]+["b"]+["-o"]+["{}".format(OUT)]+["{}".format(IN)]
                apksigner_cmd=["{}".format(javaPath)]+["-jar"]+["{}".format(apksignerPath)]+["sign"]+["--ks"]+["{}".format(keyPath)]+["{}".format(OUT)]
                print("apktool rebuild:")
                subprocess.Popen(apktool_cmd,shell=True).wait()
                print("apksigner sign:")
                subprocess.Popen(apksigner_cmd,shell=True).wait()
                if package is not None:                    
                    print("adb try to uninstall package:")
                    adb_cmd=["{}".format(adbPath)]+server+["uninstall"]+["{}".format(package)]
                    subprocess.Popen(adb_cmd,shell=True).wait()
                    print("adb install package:")
                    adb_cmd=["{}".format(adbPath)]+server+["install"]+["{}".format(OUT)]
                    subprocess.Popen(adb_cmd,shell=True).wait()
                    print("adb start package with debug mode:")
                    adb_cmd=["{}".format(adbPath)]+server+["shell"]+["am"]+["start"]+["-D"]+["-n"]+["{}/.MainActivity".format(package)]
                    subprocess.Popen(adb_cmd,shell=True).wait()
                    adb_cmd=["{}".format(adbPath)]+server+["shell"]+["pidof"]+["{}".format(package)]
                    pid=subprocess.check_output(adb_cmd).strip("\r\n").strip("\n")
                    print("adb transport:")
                    adb_cmd=["{}".format(adbPath)]+server+["forward"]+["tcp:{}".format(port)]+["jdwp:{}".format(pid)]
                    subprocess.Popen(adb_cmd,shell=True).wait()
            else:
                print("bycmd unpack/pack <IN> <OUT> -s deviceSerial -p PC_port")
parse()
