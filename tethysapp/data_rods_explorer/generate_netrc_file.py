import os
from subprocess import Popen
from getpass import getpass
import stat

from tethysapp.data_rods_explorer.app import DataRodsExplorer as App

def generate_netrc_file(username, password):
    urs_url = "urs.earthdata.nasa.gov"

    contents = f"machine {urs_url} login {username} password {password}"

    netrc_path = os.path.expanduser("~/.netrc")

    with open(netrc_path, "w") as f:
        f.write(contents)
        f.close()

    os.chmod(netrc_path, stat.S_IRUSR | stat.S_IWUSR)

try:
    username = App.get_custom_setting("earth_data_username")
    password = App.get_custom_setting("earth_data_password")

    if username is None or password is None:
        print("Earthdata credentials not set in app settings.")
        username = input("Enter Earthdata Login Username: ")
        password = getpass("Enter Earthdata Login Password: ")

    generate_netrc_file(username, password)
    print("Successfully generated .netrc file.")

except Exception as e:
    print(f"Could not generate .netrc file: {e}")