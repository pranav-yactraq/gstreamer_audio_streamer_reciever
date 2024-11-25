import subprocess
import re
import datetime
import json
# Run the bash command

def is_json_key_present(json, key):
    try:
        buf = json[key]
    except KeyError:
        return False

    return True

command = "gst-device-monitor-1.0 Audio"  # Can also try Audio/Source
devices_json_info = [] # array which will have the json result.
data = {
    "devices" : [],
    "wasapisrc_devices" : []
}

def sort_wasapi_src_devices(data):
    selected = []
    for obj in data:
        if obj['device.api'] == 'wasapi' and obj['class'] == "Audio/Source":
            print(obj)
            print(obj['caps'])
            s = obj['caps'].split(',')
            obj['caps'] = s[0]
            s.pop(0)
            for data in s:
                new_key_value = data.split('=')
                obj[new_key_value[0].strip()] = new_key_value[1].strip()
            selected.append(obj)
    print(len(selected),'No of devices available as wasapi src')
    return selected


try:
   result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
   device_blocks = re.split(r'\n\s*\n', result.stdout)
   i = 0 
   for block in device_blocks:
       device = {}
       i=i+1
       if block == 'Probing devices...' or block == 'Device found:' or block == '':
            continue 
       raw_block_info = block.strip().split('\n')
       print('\n\ndevice object',i,raw_block_info,'\nsplit lines =',len(raw_block_info))
       for info in raw_block_info:
            print('\n\nnon stripped line',info)
            temp = info.strip().split(':')
            print(temp,len(temp))
            if temp[0] == 'properties':
               continue 
            if len(temp) == 2:
               device[temp[0].strip()] = temp[1].strip()
               print(device)
            if len(temp) == 1:
               temp_two = temp[0].strip().split('=')
               if(len(temp_two)>1):
                  device[temp_two[0].strip()] = temp_two[1].strip()
       print('\n\n final device object becomes:',device)
       devices_json_info.append(device)
   print(devices_json_info)
   data['devices'] = devices_json_info
   data['wasapisrc_devices'] = sort_wasapi_src_devices(devices_json_info) 
   with open('devices.json', 'w') as json_file:
      json.dump(data, json_file, indent=4)
   print("JSON file 'devices.json' created successfully.")
except subprocess.CalledProcessError as e:
   print(f"Error: {e}")
