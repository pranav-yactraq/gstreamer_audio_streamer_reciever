## How to Run
1. Start the server - python3 gsteramer_persitent_streamer.py 
2. In another terminal run $ python3 gstreamer_audio_devices_list_to_json.py -- Finds all devices then sorts among them the wasapisrc_devices and are stored in devices.json file.
3. To start streaming audio run python3 gstreamer_audio_streamer_vanilla.py 

## Requirements
1. Stereo Mix Enabled. In the case of device speaker, for Windows OS Platform we need Stereo Mix enabled at our client device. Stereo Mix is the device that generally capture the sound coming from the client device. Hence Enabling Stereo Mix is must for the following script to capture audio from device.
2. Gstreamer installed on Windows  

## Basic Description of Approach
 gstreamer finds us all the set of audio based devices. For windows ,platform higher than or Vista , wasapi [Windows Audio Support API] based devices are the one we are concerned with as , wasapi [Windows Audio Support API] are scoped at low level [soundcard] , hence reliable for capturing audio data from most of windows devices.

## Format 
F32LE Channel 3 48000 , wav file setter width = 2 ->  bad
F32LE Channel 3 48000 , wav file setter width = 4 -> bad
F32LE Channel 2 48000 , wav file setter width = 4 -> bad
S16LE Channel 2 48000 , wav file setter width = 2 -> bad
S16LE Channel 2 48000 , wav file setter width = 4-> hearable okayish quality fastforwarded.
#### S16LE Channel 3 48000 , wav file setter width = 2-> best conversion.
S!6LE Channel 3 48000 , wav file setter width = 4-> hearable fast forwarded.
