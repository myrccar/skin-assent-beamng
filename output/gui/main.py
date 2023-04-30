import os
import shutil
import win32com

class Backend():
    def __init__(self):
        #get beamng mod directory
        self.beamng_path = fr"{os.environ.get('LOCALAPPDATA')}\beamNG.drive\latest.lnk"
        self.beamng_path = self.open_shortcut(self.beamng_path)
        self.beamng_path = f"{self.beamng_path}\mods/unpacked/"
        #get current work dir
        self.cwd = os.path.abspath(os.getcwd())

    def open_shortcut(self,path):
        shell = win32com.client.Dispatch("WScript.Shell")
        print(os.path.exists(path[0:]))
        shortcut = shell.CreateShortCut(f"{path}")
        return shortcut.Targetpath
    
    def replace_in_file(self, filename, search_string, replace_string):
        with open(filename, 'r') as file:
            content = file.read()

        new_content = content.replace(search_string, replace_string)

        with open(filename, 'w') as file:
            file.write(new_content)

    def generate_files(self,name,author,vehicle,beamng_path):
        self.name = name
        self.mod_name = self.name.replace(" ","_")
        self.author = author
        self.vehicle = vehicle
        self.beamng_path = beamng_path
        if not os.path.exists(self.beamng_path):
            print("error invalid beamng path. placing in documents")
            self.beamng_path = os.path.expanduser('~/Documents')
        #make main folders
        self.mod_path = f"{self.beamng_path}/{self.mod_name}/vehicles/{self.vehicle}/{self.mod_name}"
        os.makedirs(self.mod_path)
        #copy template files
        shutil.copyfile(f"{os.getcwd()}/vehicles/{self.vehicle}/{self.vehicle}_skin_SKINNAME.dds",f"{self.mod_path}/{vehicle}_skin_{self.mod_name}.dds")
        shutil.copyfile(f"{os.getcwd()}/vehicles/{self.vehicle}/{self.vehicle}.jbeam",f"{self.mod_path}/{vehicle}.jbeam")
        #check maters file name
        if os.path.exists(f"{os.getcwd()}/vehicles/{self.vehicle}/materials.json"):
            shutil.copyfile(f"{os.getcwd()}/vehicles/{self.vehicle}/materials.json",f"{self.mod_path}/materials.json")
            self.replace_in_file(f"{self.mod_path}/materials.json","SKINNAME",self.mod_name)
        else:
            shutil.copyfile(f"{os.getcwd()}/vehicles/{self.vehicle}/skin.materials.json",f"{self.mod_path}/skin.materials.json")
            self.replace_in_file(f"{self.mod_path}/skin.materials.json","SKINNAME",self.mod_name)
        #replace in jbeam
        self.replace_in_file(f"{self.mod_path}/{vehicle}.jbeam","SKINNAME",self.mod_name)
        self.replace_in_file(f"{self.mod_path}/{vehicle}.jbeam","YOUR SKIN NAME",self.name)
        self.replace_in_file(f"{self.mod_path}/{vehicle}.jbeam","SKIN NAME",self.name)
        self.replace_in_file(f"{self.mod_path}/{vehicle}.jbeam","YOU",self.author)
