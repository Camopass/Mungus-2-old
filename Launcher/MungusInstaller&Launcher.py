import pip
import os
import zipfile
import tkinter


# Installs packages required for the installer to run
def install_packages():
    try:
        import requests
    except ImportError:
        pip.main(["install", "requests"])
        pip.main(["install", "pywin32"])


# Check to see if we have the most recent version of mungus.
def check_for_updates():
    import requests
    try:
        with open("Mungus-2-master/version.txt", "r") as f:
            current_version = f.read()
    except FileNotFoundError:
        return False
    most_recent_version = requests.get("https://raw.githubusercontent.com/Camopass/Mungus-2/master/version.txt").text
    return current_version == most_recent_version


# Install the source code for mungus
def install_mungus():
    import requests
    with requests.get("https://github.com/Camopass/Mungus-2/archive/refs/heads/master.zip", stream=True) as r:
        r.raise_for_status()
        with open("Mungus2.zip", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return "Mungus2.zip"


# Unzip the source code files into a directory for mungus.
def unzip_files():
    with zipfile.ZipFile("Mungus2.zip", 'r') as zip_ref:
        zip_ref.extractall("./")


def create_shortcut():
    import win32com.client

    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    path = os.path.join(desktop, 'Mungus 2.lnk')
    target = os.path.join(os.getcwd(), "Mungus-2-master/main.py")
    icon = os.path.join(os.getcwd(), "Mungus-2-master/Mungus.ico")

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(path)
    shortcut.TargetPath = target
    shortcut.IconLocation = icon
    shortcut.WindowStyle = 7
    shortcut.save()


# Run the main installing sequence
def install():
    install_packages()
    if not check_for_updates():
        print("Updating Mungus.")
        install_mungus()
        unzip_files()
        pip.main(["install", r'-r%s\Mungus-2-master\requirements.txt' % os.getcwd()])
        create_shortcut()
        with open("%s/Mungus2 Launch Info [DO NOT DELETE RENAME OR MOVE].txt" % os.path.join(os.environ["USERPROFILE"],
                                                                                             "Desktop"), 'w') as f:
            f.write(os.path.join(os.getcwd(), 'Mungus-2-master'))
    else:
        print("No updates necessary.")


#  ---------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    install()
