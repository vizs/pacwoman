# Get package's info in json using the AUR's RPC interface
# Accompanies pacwoman.py

import json
import urllib.request

# import files
import configuration

# set search's heading to an empty str if colored output is set to False
if not configuration.colored_output:
    configuration.color_search_heading = ""

def pretty_print_json(json_data):
    heading = lambda text: configuration.color_search_heading + text + ":" + \
        configuration.color_normal + " "

    nth_iteration = 0
    num_results = len(json_data["results"])

    print(heading("Results")  + str(num_results) + "\n")

    data_points = ["Name", "Version", "Maintainer", "Description"]

    for package in json_data["results"]:
        nth_iteration += 1
        output = ""

        for data_point in data_points:
            output += heading(data_point) + str(package.get(data_point)) + "\n"

        if nth_iteration < num_results:
            output += "\n"

        print(output)

def search(package_name, search_type):
    base_url = "https://aur.archlinux.org/rpc/?v=5&type=search&arg=" + \
        package_name

    if search_type != "none" or search_type != None:
        rpc_url = base_url + "&by=" + search_type

    search_data = urllib.request.urlopen(rpc_url).read()
    search_data = json.loads(search_data)
    return search_data

def package_deatil(package_name, json_data):
    heading = lambda text: configuration.color_search_heading + text + ":" + \
        configuration.color_normal + " "

    data_points = ["Name", "Version", "Maintainer", "Description"]
    details = ""

    for package in json_data["results"]:
        if package["Name"] == package_name:
            for data_point in data_points:
                details += heading(data_point) + str(package.get(data_point)) + "\n"

    print(details)

def get_depends(package_name):
    data = urllib.request.urlopen("https://aur.archlinux.org/rpc/?v=5&" +\
        "type=multiinfo&arg=" + package_name).read()

    data = json.loads(data)

    results = data.get("results")
 
    for result in results:
        if result.get("Name") == package_name:
            depends = result.get("Depends")

            for depend in depends:
                print(depend)
