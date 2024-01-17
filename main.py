import os
import json
import socket
import base64
import requests
import subprocess
from dotenv import load_dotenv
from datetime import datetime
import argparse

load_dotenv()

parser = argparse.ArgumentParser(description='Choose level 1 for a simple audit or level 2 for advanced security auditing.')
parser.add_argument('--level', type=int, help='Choose between level 1 or level 2', required=True)

args = parser.parse_args()

if args.level not in [1, 2]:
    raise argparse.ArgumentTypeError(f"Invalid level: {args.level}. Must be either 1 or 2.")

url = os.getenv('url', 'http://localhost:80')

user_feedback = []
result = {'score': 32, 'commands': []}
commands: list = []
current_date = datetime.now().date()

# Get Metadata
result["hostname"] = socket.gethostname()
result["ip"] = socket.gethostbyname(socket.gethostname())
result["date"] = current_date.strftime("%Y-%m-%d")
print(f"HOSTNAME: {result['hostname']}")
print(f"IP: {result['ip']}")
print(f"DATE: {result['date']}")

# Get Commands
response = requests.get(f'{url}/command/get_commands')
if response.status_code == 200:
    commands = response.json()
    print("GET request was successful!")
else:
    print(f"GET request failed with status code {response.status_code}")


for commandObject in commands:
    if commandObject['level'][1] > args.level:
        continue

    script = base64.b64decode(commandObject["script"]).decode('utf-8')
    output = None
    process = None

    if 'sudo' in script:
        while True:
            user_input = input(
                f'\n"{script}"\n\nThe command contains a sudo modifier. Would you still like to run this command? [y/n]\t').strip().lower()
            if user_input in {'y', 'yes'}:
                print(f"Executing: {script}")
                process = subprocess.Popen(["bash", "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output, error = process.communicate()
                # if process.returncode == 10 -> needs manual reviewing
                break
            elif user_input in {'n', 'no'}:
                print("Operation canceled.")
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
    else:
        # if process.returncode == 10 -> needs manual reviewing
        process = subprocess.Popen(["bash", "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()
    if process.returncode == 1:
        user_feedback.append({"Error": "The execution caused unwanted results", "Requirement": commandObject['description'], "Command": commandObject['command'], "Output": output, "Reference": f"For more information, check the CIS-benchmark at chapter {commandObject['chapter']}"})
    elif process.returncode == 10:
        user_feedback.append(
            {"Error": "This command needs to be manually reviewed", "Requirement": commandObject['description'], "Command": commandObject['command'], "Output": output, "Reference": f"For more information, check the CIS-benchmark at chapter {commandObject['chapter']}"})
    result['commands'].append({'command': commandObject, 'result': {'output': output, 'value': process.returncode}})

# ToDO - result.json needs to be sent to fastapi backend
result_post = requests.post(f'{url}/result/', json=result)
if result_post.status_code == 200:
    print("Results have been sent")
else:
    print(f"Results could not be sent: {result_post.text}")


with open('result.json', 'w') as f:
    json.dump(result, f, indent=4)

with open('user_feedback.json', 'w') as f:
    json.dump(user_feedback, f, indent=4)
