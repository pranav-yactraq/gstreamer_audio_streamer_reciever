import subprocess
import json

with open('devices.json', 'r') as file:
    data = json.load(file)

devices = [] 
for device in data['wasapisrc_devices']:
    print(device)# from here we can pass the device ids to the below command dynamically.
    devices.append(device)

command = """gst-launch-1.0 wasapisrc device=""" + """\""""  + devices[0]['device.strid']+"""\"""" + """ !audioconvert ! audioresample ! "audio/x-raw,format=S16LE,rate=48000,channels=3" ! queue ! tcpclientsink host=127.0.0.1 port=8080 wasapisrc device=""" + """\"""" + devices[1]['device.strid']+ """\"""" + """ ! audioconvert ! audioresample ! "audio/x-raw,format=S16LE,rate=48000,channels=3" ! queue ! tcpclientsink host=127.0.0.1 port=8081"""

print("Streaming has started running. Press Ctrl+C to stop.")
try:
    result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
    print('Press Control C to Stop the streaming.')
    print(result.stdout)
except subprocess.CalledProcessError as e:
   print(f"Error: {e}")