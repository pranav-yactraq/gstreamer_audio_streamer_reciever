import socket
import threading
import wave
from concurrent.futures import ThreadPoolExecutor

def handle_client(client_socket, client_address, wav_file, channels, sample_rate, sample_width):
    """
    Handles a single client's audio stream and saves it as a WAV file.
    """
    print(f"Connection from {client_address}")
    with client_socket, wave.open(wav_file, "wb") as wav:
        # Configure WAV file
        wav.setnchannels(channels)
        wav.setsampwidth(sample_width)  # 16-bit audio is 2 bytes
        wav.setframerate(sample_rate)

        # Receive and write the stream
        while True:
            data = client_socket.recv(4096)  # Receive audio chunks
            if not data:
                break
            wav.writeframes(data)  # Write the audio data to the WAV file

    print(f"Stream from {client_address} saved to {wav_file}")
    client_socket.close()

def start_server(port, file_prefix, channels, sample_rate, sample_width):
    """
    Starts a server on the given port and handles incoming connections.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)  # Allow up to 5 queued connections
    print(f"Server listening on port {port}...")

    with ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            client_socket, client_address = server_socket.accept()  # Accept a client connection
            wav_file = f"{file_prefix}_{client_address[1]}.wav"  # Unique file based on client address
            # Use the thread pool to handle the client
            executor.submit(handle_client, client_socket, client_address, wav_file, channels, sample_rate, sample_width)

# Stream configurations
stream_1_config = {
    "port": 8080,
    "file_prefix": "stream1_audio",  # Prefix for output files
    "channels": 3,
    "sample_rate": 48000,
    "sample_width": 2,  # 16-bit audio is 2 bits and 32-bit audio is 4 bits
}

stream_2_config = {
    "port": 8081,
    "file_prefix": "stream2_audio",
    "channels": 3,
    "sample_rate": 48000,
    "sample_width": 2,
}

# Start servers for each stream in separate threads
threading.Thread(
    target=start_server,
    args=(stream_1_config["port"], stream_1_config["file_prefix"], stream_1_config["channels"], stream_1_config["sample_rate"], stream_1_config["sample_width"]),
    daemon=True
).start()

threading.Thread(
    target=start_server,
    args=(stream_2_config["port"], stream_2_config["file_prefix"], stream_2_config["channels"], stream_2_config["sample_rate"], stream_2_config["sample_width"]),
    daemon=True
).start()

print("Servers are running. Press Ctrl+C to stop.")
while True:
    pass 