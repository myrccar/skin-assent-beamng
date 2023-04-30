from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager
import json
import os
import shutil
import subprocess
import win32com.client
import sys 
import main
import easygui

backend = main.Backend()

class SkinAssent(App):
    def __init__(self, **kwargs):
        super(SkinAssent, self).__init__(**kwargs)
    def build(self):
        return MyScreenManager()
    def get_vehicles(self):
        self.vehicle_names_json = None
        with open("vehicle_names.json") as f:
            self.vehicle_names_json = json.loads(f.read())
        vehicle_names = []
        for key,value in self.vehicle_names_json.items():
            vehicle_names.append(str(key))
        
        return vehicle_names

class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        self.name = "unknown_skin_name"
        self.author = "unknown"
        self.vehicle = "bolide"
        self.beamng_path = backend.beamng_path
        with open("vehicle_names.json","r") as f:
            self.vehicle_names_json = json.loads(f.read())
        super().__init__(**kwargs)

    def build(self):
        return MyScreenManager()

    def generate_files(self):
        self.ids.info = "generating..."
        self.name = self.ids.name.text
        self.author = self.ids.author.text
        backend.generate_files(
            self.name,
            self.author,
            self.vehicle,
            self.beamng_path
        )
    
    
    def vehicle_selected(self,text):
        self.vehicle = self.vehicle_names_json[text]

    def set_info(self,info):
        self.ids.info = info

    def next_page(self):
        current_index = self.screen_names.index(self.current)
        if current_index + 1 < len(self.screen_names):
            return self.screen_names[current_index + 1]
        return self.current

    def previous_page(self):
        current_index = self.screen_names.index(self.current)
        if current_index - 1 >= 0:
            return self.screen_names[current_index - 1]
        return self.current
    
    def change_path(self):
        self.beamng_path = easygui.diropenbox(msg="select output folder")
        self.ids.path.text = self.beamng_path

        

def main():
    SkinAssent().run()


if __name__ == '__main__':
    main()