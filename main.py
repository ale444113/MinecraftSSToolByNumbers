import psutil
import subprocess
import json
import colorama
import pathlib
import os
import sys
import time
import zipfile
from strings import javawStrings, dpsStrings
with open('config.json') as f:
    config = json.load(f)


class screan_share_tool_by_numbers(object):
    def __init__(self):
        self.recordingSoftwares = config["recordingSoftwares"]
        self.max_modification_time = config["modification"]
        self.path_with_username = '/'.join(os.getcwd().split('\\', 3)[:3])
        self.drive_letter = os.getcwd().split('\\', 1)[0]+'/'
        #Colors
        self.color_blue = colorama.Fore.BLUE
        self.color_red = colorama.Fore.RED
        self.color_green = colorama.Fore.GREEN
        self.color_magneta = colorama.Fore.LIGHTMAGENTA_EX
        self.color_yellow = colorama.Fore.YELLOW
        self.color_clear = colorama.Style.RESET_ALL
        self.welcome_message = colorama.Fore.BLUE+"-"*4 + "Bienvenido a esta SS tool creada por alenumbers nwn" + "-"*5+colorama.Style.RESET_ALL
        self.end_message = colorama.Fore.BLUE+"-"*28 + "Fin" + "-"*29+colorama.Style.RESET_ALL
        self.separator = colorama.Fore.LIGHTCYAN_EX+"-"*60 +self.color_clear
        #Clear command and minecraft path
        if sys.platform == "cygwin" or sys.platform == "win32":
            self.minecraft_path = self.path_with_username + "/AppData/Roaming/.minecraft"
            self.clear_command = os.system('cls')
        else:
            self.minecraft_path = "~/Library/Application Support/minecraft"
            self.clear_command = os.system('clear')

    def get_service_pid(self,name,is_csrss):
        if is_csrss:
            return [proc.pid for proc in psutil.process_iter() if proc.name() == "csrss.exe"]
        response = str(subprocess.check_output(f'tasklist /svc /FI "Services eq {name}"')).split('\\r\\n')
        for process in response:
            if name in process:
                pid = process.split()[1]
                return pid

    def minecraft_abierto(self):
        for p in psutil.process_iter(attrs=['pid', 'name']):
            if 'javaw' in p.info['name']:  
                pid = p.info['pid']
                process = p.cmdline()
                mcprocess_info = {}
                for argument in process:
                    if "--" in argument:
                        mcprocess_info[argument.split("--")[1]] = process[process.index(argument) + 1]
                if "username" in mcprocess_info:
                    print(self.color_magneta+"Minecraft encontrado buscando información..."+self.color_clear)

                    self.javawPid = pid
                    print(f'    Username: {mcprocess_info["username"]}')
                    print(f'    Version: {mcprocess_info["version"]}')
                    print(f'    Path: {mcprocess_info["gameDir"]}')
                    return True
        print(self.color_red+"Minecraft no encontrado O.o"+self.color_clear)
        return False
    
    def common_hacks(self):
        if "huzuni" in os.listdir(self.minecraft_path): print(self.color_red+'Huzuni encontrado en la .minecraft'+self.color_clear)
        elif "wurst" in os.listdir(self.minecraft_path): print(self.color_red+'Wurst encontrado en la .minecraft'+self.color_clear)
        elif "gc" in os.listdir(self.minecraft_path): print(self.color_red+'Un ghost client fue encontrado en la .minecraft'+self.color_clear)
        else: print(self.color_green+'Ningun hack común encontrado en la .minecraft'+self.color_clear)
        
    def check_jnativehook(self):
        if sys.platform == "win32" or sys.platform == "cygwin": path = self.path_with_username + "/AppData/Local/Temp"
        elif sys.platform == "linux": path = "~/tmp"
        else:
            print(self.color_red+"Esta herramienta no esta disponible en este sistema operativo"+self.color_clear)
            return False
        for e in os.listdir(path):
            if e == "Jnativehook.dll":
                print(self.color_red+"Encontré un jnativehook autoclicker"+self.color_clear)
                return True
        print(self.color_green+"No hay jnativehook autoclicker"+self.color_clear)

    def software_grabar(self):
        tasks = str(subprocess.check_output('tasklist')).lower()
        found = [x for x in self.recordingSoftwares if x in tasks]

        if found:
            print(self.color_red+'Software(s) de grabación encontrado(s)'+self.color_clear)
            for software in found:
                print(f'    {self.color_yellow}{self.recordingSoftwares[software]}{self.color_clear} encontrado')
        else:
            print(self.color_green+'No se ha encontrado ningun software de grabación'+self.color_clear)

    def modification_time(self):
        print(self.color_magneta+'Fecha de modificación de las carpetas principales'+self.color_clear)
        #RecybleBin
        recycle_bin_path = self.drive_letter+"/$Recycle.Bin/"
        modTime = os.path.getmtime(recycle_bin_path)
        modTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTime)).split(' ')
        print(f'    Recycle Bin: {modTime[1]} {modTime[0]}')
        
        #Mods
        mods_path = self.minecraft_path + "/mods"
        modTime = os.path.getmtime(mods_path)
        modTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTime)).split(' ')
        print(f'    Mods: {modTime[1]} {modTime[0]}')

        #Versions
        mods_path = self.minecraft_path + "/versions"
        modTime = os.path.getmtime(mods_path)
        modTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTime)).split(' ')
        print(f'    Versions: {modTime[1]} {modTime[0]}')

        #Texturepacks
        mods_path = self.minecraft_path + "/resourcepacks"
        modTime = os.path.getmtime(mods_path)
        modTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTime)).split(' ')
        print(f'    Resourcepacks: {modTime[1]} {modTime[0]}')

    def show_jar_classes(self,jar_file):
        zf = zipfile.ZipFile(jar_file, 'r')
        all_classes = []
        try:
            lst = zf.infolist()
            for zi in lst:
                fn = zi.filename
                if fn.endswith('.class'):
                    all_classes.append(fn.split('/')[len(fn.split('/'))-1])
        finally:
            zf.close()
        return all_classes

    def is_raven(self,zip_to_check):
        #Here I do a try/except because the mcmod.info couldn't existe if it is a normal zip or it couldnt existe the url in the mcmod.info if the mod isnt raven
        try:
            zf = zipfile.ZipFile(zip_to_check, 'r')
            mcmodinfo = dict(json.load(zf.open('mcmod.info'))[0])
            if mcmodinfo['authorList'] == ['OFP', 'Fyu', 'spiderfrog', 'Yario & Extazz'] and mcmodinfo['url'] == 'https://www.youtube.com/ofpmedia': return True
        except: 
            pass
        return False

    def mods(self):
        print(self.color_magneta+'Aquí tienes una lista de todos los mods'+self.color_clear)
        path = self.minecraft_path + "/mods"
        for x in os.listdir(path): 
            if x.endswith('.jar'):
                if "$ . class" in self.show_jar_classes(self.minecraft_path + "/mods/"+x): print(self.color_red + x + " (Injected)"+ self.color_clear)
                elif "  ‏ $ ‏‏ .class" in self.show_jar_classes(self.minecraft_path + "/mods/"+x):print(self.color_red + x + " (Injected)"+ self.color_clear) 
                else: print(self.color_green + x + self.color_clear)
            elif x.endswith('zip'):
                if self.is_raven(self.minecraft_path + "/mods/"+x): print(self.color_red + x + " es un raven ghost client"+ self.color_clear)
                else: print(self.color_yellow + x + self.color_clear)

    def get_strings(self,PID):
        cmd = f'strings.exe -pid {PID} -raw -nh'
        strings = str(subprocess.check_output(cmd)).replace("\\\\","/")
        strings = list(set(strings.split("\\r\\n")))
        return strings

    def check_strings(self):
        print(self.color_magneta+'Comprobando strings... (esto puede tardar un rato)'+self.color_clear)
        #Check javaw
        javaw_strings = self.get_strings(self.javawPid)
        found = [f'{javawStrings[x]} ({x})' for x in javaw_strings if x in javawStrings]

        if found:
            for hack in found:
                print(self.color_red+f'    {hack} fue encontrado'+self.color_clear)
        else:
            print(self.color_green+f'    No encontre nada en los strings de javaw'+self.color_clear)
        #Check dps
        dpsPid = self.get_service_pid('DPS', False)
        dps_strings = self.get_strings(dpsPid)
        dps_strings = ['.exe!'+x.split('!')[3] for x in dps_strings if '.exe!' in x and x.startswith('!!')]

        found = [x for x in dps_strings if x in dpsStrings]
        if found:
            for string in found: print(self.color_red+f'    {dpsStrings[string]} ({string}) fue encontrado'+self.color_clear)
        else:
            print(self.color_green+f'    No encontré hacks en el dps'+self.color_clear)
        #Check csrss
        csrssPid = self.get_service_pid('csrss', True)[1]
        csrss_strings = self.get_strings(csrssPid)
        csrss_strings = ['.exe!'+x.split('!')[3] for x in csrss_strings if '.exe!' in x and x.startswith('!!')]
        if csrss_strings:
            for string in csrss_strings: print(self.color_red+f'    {string} fue encontrado en csrss'+self.color_clear)
        else:
            print(self.color_green+f'    No encontré hacks en el csrss'+self.color_clear)
    def recents(self):
        if sys.platform == "win32" or sys.platform == "cygwin":
            print(self.color_magneta+"He encontrado los siguientes archivos recientes"+self.color_clear)
            path = self.path_with_username + "/AppData/Roaming/Microsoft/Windows/Recent/"
            for e in os.listdir(path):
                e = e.replace('.lnk','')
                if e.endswith('.zip'): print(e.replace('.zip', '') + self.color_blue + ".zip"+ self.color_clear)
                elif e.endswith('.dll'): print(e.replace('.dll', '') + self.color_red + ".dll"+ self.color_clear)
                elif e.endswith('exe'): print(e.replace('.exe', '') + self.color_yellow + ".exe"+ self.color_clear)
        else:
            print(self.color_red+"Esta herramienta no esta disponible en este sistema operativo"+self.color_clear)

    def downloads(self):
        if sys.platform == "win32" or sys.platform == "cygwin": path = self.path_with_username + "/Downloads/"
        else: path = "~/Downloads/" 
        print(self.color_magneta+"He encontrado los siguientes archivos en descargas"+self.color_clear)
        for e in os.listdir(path):
            e = e.replace('.lnk','')
            if e.endswith('.zip'): print(e.replace('.zip', '') + self.color_blue + ".zip"+ self.color_clear)
            elif e.endswith('.dll'): print(e.replace('.dll', '') + self.color_red + ".dll"+ self.color_clear)
            elif e.endswith('.exe'): print(e.replace('.exe', '') + self.color_yellow + ".exe"+ self.color_clear)
            

ss = screan_share_tool_by_numbers()

ss.clear_command
print(ss.welcome_message)
if ss.minecraft_abierto() == True:
    print("")
    ss.common_hacks()
    ss.check_jnativehook()
    print(ss.separator)
    ss.software_grabar()
    print(ss.separator)
    ss.mods()
    print(ss.separator)
    ss.modification_time()
    print(ss.separator)
    ss.check_strings()
    print(ss.separator)
    ss.recents()
    print(ss.separator)
    ss.downloads()
print(ss.end_message)
input("Pulsa enter para continuar... ")
ss.clear_command