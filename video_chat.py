import tkinter as tk
from tkinter import messagebox
from threading import Thread
import socket
import cv2
import numpy as np
from Crypto.Cipher import AES
import hashlib
import pickle
import zlib
import struct
from bb84_module import Party, BB84  # Assuming bb84_module.py contains the classes from your bb84.py file
from crypto_utils import encrypt, decrypt


class VideoChatApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0
        self.video_capture = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_start_server = tk.Button(window, text="Start Server", width=10, command=self.start_server)
        self.btn_start_server.pack(padx=20, pady=5, side=tk.LEFT)

        self.btn_start_client = tk.Button(window, text="Start Client", width=10, command=self.start_client)
        self.btn_start_client.pack(padx=20, pady=5, side=tk.LEFT)

        self.alice = Party()
        self.bob = Party()
        self.shared_key = None

        self.window.mainloop()

    def establish_shared_key(self):
        protocol = BB84(self.alice, self.bob, bits=256)
        intrusion, _, _ = protocol.run()

        if intrusion:
            messagebox.showerror("Intrusion Detected", "Eavesdropping was detected during key exchange.")
            return

        self.shared_key = self.alice.keys[self.bob]

    def start_server(self):
        self.server = VideoServer(self.shared_key)
        self.server_thread = Thread(target=self.server.start)
        self.server_thread.start()

        self.update_canvas()

    def start_client(self):
        self.client = VideoClient(self.shared_key)
        self.client_thread = Thread(target=self.client.start)
        self.client_thread.start()

        self.update_canvas()

    def update_canvas(self):
        if hasattr(self, 'server'):
            ret, frame = self.video_capture.read()
            if ret:
                self.server.send_frame(frame)
                self.canvas.create_image(0, 0, image=tk.PhotoImage(image=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), anchor=tk.NW)

        if hasattr(self, 'client'):
            frame = self.client.receive_frame()
            if frame is not None:
                self.canvas.create_image(0, 0, image=tk.PhotoImage(image=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), anchor=tk.NW)

        self.window.after(10, self.update_canvas)


class VideoServer:
    def __init__(self, shared_key):
        self.shared_key = shared_key
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 8484))
        self.server_socket.listen(1)
        self.client_socket, _ = self.server_socket.accept()

    def start(self):
        pass  # Placeholder, as the server is started immediately in __init__

    def send_frame(self, frame):
        # Compress the frame
        compressed_frame = zlib.compress(pickle.dumps(frame))
        
        # If a shared key is available, encrypt the frame
        if self.shared_key:
            compressed_frame = encrypt(compressed_frame, self.shared_key)

        # Send the length of the data followed by the data itself
        length = len(compressed_frame)
        self.client_socket.sendall(struct.pack('!I', length))
        self.client_socket.sendall(compressed_frame)

    def close(self):
        self.client_socket.close()
        self.server_socket.close()


class VideoClient:
    def __init__(self, shared_key):
        self.shared_key = shared_key
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 8484))

    def start(self):
        pass  # Placeholder, as the client connects immediately in __init__

    def receive_frame(self):
        # First, receive the length of the incoming data
        data_length = struct.unpack('!I', self.client_socket.recv(4))[0]
        
        # Receive the actual data
        data = self.client_socket.recv(data_length)

        # If a shared key is available, decrypt the data
        if self.shared_key:
            data = decrypt(data, self.shared_key)

        # Decompress and deserialize the frame
        frame = pickle.loads(zlib.decompress(data))
        return frame

    def close(self):
        self.client_socket.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoChatApp(root, "Quantum Video Chat")
