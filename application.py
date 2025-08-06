import subprocess
import sys
import os

def check_and_install_npyscreen():
    try:
        import npyscreen
    except ImportError:
        print("Dependency 'npyscreen' is not installed.")
        choice = input("Do you want to install it now? (y/n): ").strip().lower()
        if choice == 'y':
            print("Installing npyscreen via pip...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "npyscreen"])
            except subprocess.CalledProcessError:
                print("Failed to install npyscreen automatically. Please run manually:")
                print(f"  {sys.executable} -m pip install npyscreen")
                sys.exit(1)
            print("Installation complete. Please rerun the script.")
            sys.exit(0)
        else:
            print("Cannot continue without npyscreen. Exiting.")
            sys.exit(1)

check_and_install_npyscreen()

import npyscreen

MOD_MANAGER = "mod_manager.py"

def find_server_properties():
    search_paths = [
        "./server.properties",
        "../server.properties",
        "../../server.properties"
    ]
    for path in search_paths:
        if os.path.isfile(path):
            return os.path.abspath(path)
    return None

SERVER_PROPERTIES_PATH = find_server_properties()
if not SERVER_PROPERTIES_PATH:
    print("Error: Could not find 'server.properties' in current directory or up to two levels up.")
    sys.exit(1)

def load_properties():
    props = {}
    raw_lines = []
    with open(SERVER_PROPERTIES_PATH, "r") as f:
        for line in f:
            raw_lines.append(line.rstrip('\n'))
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                props[key.strip()] = value.strip()
    return props, raw_lines

def save_properties(props, raw_lines):
    with open(SERVER_PROPERTIES_PATH, "w") as f:
        for line in raw_lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                f.write(line + "\n")
                continue
            key = stripped.split("=", 1)[0].strip()
            if key in props:
                f.write(f"{key}={props[key]}\n")
            else:
                f.write(line + "\n")

class PropertiesForm(npyscreen.FormMultiPageAction):
    def create(self):
        self.add(npyscreen.FixedText, value="Minecraft Bedrock Server Properties Manager", editable=False, color="STANDOUT")
        self.properties, self.raw_lines = load_properties()
        self.widgets = {}
        row = 2
        for key, value in self.properties.items():
            self.widgets[key] = self.add(npyscreen.TitleText, name=key, value=value, rely=row, relx=2, begin_entry_at=20, use_two_lines=False)
            row += 1
        
        self.add(npyscreen.ButtonPress, name="Launch Mod Manager", rely=row+1, relx=2, when_pressed_function=self.launch_mod_manager)
        self.add(npyscreen.ButtonPress, name="Save and Exit", rely=row+3, relx=2, when_pressed_function=self.on_ok)

    def on_ok(self):
        for key, widget in self.widgets.items():
            self.properties[key] = widget.value
        save_properties(self.properties, self.raw_lines)
        self.parentApp.setNextForm(None)
        self.editing = False

    def on_cancel(self):
        self.parentApp.setNextForm(None)
        self.editing = False

    def launch_mod_manager(self):
        npyscreen.notify_wait("Launching mod_manager.py... Close it to return.", title="Info")
        self.parentApp.switchForm(None)
        subprocess.run([sys.executable, MOD_MANAGER])
        self.parentApp.setNextForm("MAIN")

class PropertiesApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", PropertiesForm)

if __name__ == "__main__":
    app = PropertiesApp()
    app.run()