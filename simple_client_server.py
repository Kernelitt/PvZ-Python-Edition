import socket
import threading
import os
import struct
import json
import base64
import sys
from io import StringIO
from cryptography.fernet import Fernet

try:
    import psutil
except ImportError:
    psutil = None

try:
    import tkinter as tk
except ImportError:
    tk = None

class SimpleServer:
    def __init__(self, host='0.0.0.0', port=12345, key=None, config_file=None):
        self.config_file = config_file or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server_config.json')
        self.config = self.load_config()
        self.host = self.config.get('host', host)
        self.port = self.config.get('port', port)
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = False
        self.key = key
        self.cipher = Fernet(key) if key else None
        self.users_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.json')
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
        self.message_handlers = {}
        self.client_nicknames = {}
        self.client_ips = {}

    def start(self):
        self.running = True
        print(f"Server started on {self.host}:{self.port}")
        threading.Thread(target=self.accept_clients, daemon=True).start()
        threading.Thread(target=self.command_loop, daemon=True).start()

    def accept_clients(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                ip = addr[0]
                if self.is_ip_allowed(ip):
                    print(f"Client connected from {addr}")
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True)
                    client_thread.start()
                    self.clients.append(client_socket)
                    self.client_ips[client_socket] = ip
                else:
                    print(f"Client from {addr} is not allowed, closing connection")
                    client_socket.close()
            except Exception as e:
                print(f"Error accepting clients: {e}")

    def is_ip_allowed(self, ip):
        if self.config.get('use_ip_whitelist', False):
            return ip in self.config.get('ip_whitelist', [])
        else:
            return ip not in self.config.get('ip_blacklist', [])

    def is_nickname_allowed(self, nickname):
        if self.config.get('use_nickname_whitelist', False):
            return nickname in self.config.get('nickname_whitelist', [])
        else:
            return nickname not in self.config.get('nickname_blacklist', [])

    def handle_client(self, client_socket):
        try:
            while True:
                header = self.recvall(client_socket, 4)
                if not header:
                    break
                msg_length = struct.unpack('>I', header)[0]
                data = self.recvall(client_socket, msg_length)
                if self.cipher:
                    data = self.cipher.decrypt(data)
                message = json.loads(data.decode())
                self.process_message(client_socket, message)
        except Exception as e:
            print(f"Client connection error: {e}")
        finally:
            client_socket.close()
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            if client_socket in self.client_nicknames:
                del self.client_nicknames[client_socket]
            if client_socket in self.client_ips:
                del self.client_ips[client_socket]
            print("Client disconnected")

    def process_message(self, client_socket, message):
        msg_type = message.get('type')
        if msg_type in self.message_handlers:
            self.message_handlers[msg_type](client_socket, message)
        elif msg_type == 'text':
            text = message.get('data')
            print(f"Received text: {text}")
            # Echo back to all clients
            self.broadcast(message)
        elif msg_type == 'file':
            filename = message.get('filename')
            filedata = base64.b64decode(message.get('data'))
            folder = 'received_files'
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                folder_path = os.path.join(script_dir, folder)
                os.makedirs(folder_path, exist_ok=True)
                filepath = os.path.join(folder_path, filename)
                with open(filepath, 'wb') as f:
                    f.write(filedata)
                print(f"Received file saved to {filepath}")
            except (PermissionError, OSError) as e:
                print(f"Error saving file: {e}")
            self.broadcast(message)
        elif msg_type == 'login':
            nickname = message.get('nickname')
            print(f"User login request: {nickname}")
            # Check if banned by nickname or IP
            ip = self.client_ips.get(client_socket)
            if nickname in self.config.get('nickname_blacklist', []):
                response = {'type': 'login_response', 'data': {'error': 'You are banned by nickname.'}}
                self.send_to_client(client_socket, response)
                client_socket.close()
                return
            if ip in self.config.get('ip_blacklist', []):
                response = {'type': 'login_response', 'data': {'error': 'Your IP is banned.'}}
                self.send_to_client(client_socket, response)
                client_socket.close()
                return
            user_info = self.users.get(nickname, {})
            self.client_nicknames[client_socket] = nickname
            response = {'type': 'login_response', 'data': user_info}
            self.send_to_client(client_socket, response)
        else:
            print("Unknown message type")

    def add_message_handler(self, msg_type, handler):
        self.message_handlers[msg_type] = handler

    def broadcast(self, message):
        data = json.dumps(message).encode()
        if self.cipher:
            data = self.cipher.encrypt(data)
        msg_length = struct.pack('>I', len(data))
        for client in self.clients:
            try:
                client.sendall(msg_length + data)
            except Exception as e:
                print(f"Error sending to client: {e}")

    def send_to_client(self, client_socket, message):
        data = json.dumps(message).encode()
        if self.cipher:
            data = self.cipher.encrypt(data)
        msg_length = struct.pack('>I', len(data))
        try:
            client_socket.sendall(msg_length + data)
        except Exception as e:
            print(f"Error sending to client: {e}")

    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)

    def command_loop(self):
        while self.running:
            try:
                command = input("")
                self.process_command(command)
            except EOFError:
                break

    def process_command(self, command):
        parts = command.split()
        if not parts:
            return
        cmd = parts[0]
        if cmd == 'list_clients':
            print("Connected clients:")
            for i, client in enumerate(self.clients):
                try:
                    addr = client.getpeername()
                    print(f"{i}: {addr}")
                except:
                    print(f"{i}: disconnected")
        elif cmd == 'send':
            if len(parts) < 3:
                print("Usage: send <client_index> <message>")
                return
            try:
                index = int(parts[1])
                message = ' '.join(parts[2:])
                if 0 <= index < len(self.clients):
                    msg = {'type': 'text', 'data': message}
                    self.send_to_client(self.clients[index], msg)
                    print(f"Sent to client {index}")
                else:
                    print("Invalid client index")
            except ValueError:
                print("Invalid index")
        elif cmd == 'update_user':
            if len(parts) < 4:
                print("Usage: update_user <nickname> <key> <value>")
                return
            nickname = parts[1]
            key = parts[2]
            value = ' '.join(parts[3:])
            if nickname in self.users:
                self.users[nickname][key] = value
                self.save_users()
                print(f"Updated {nickname}'s {key} to {value}")
            else:
                print("User not found")
        elif cmd == 'list_users':
            print("Users:")
            for nick, data in self.users.items():
                print(f"{nick}: {data}")
        elif cmd == 'kick':
            if len(parts) < 2:
                print("Usage: kick <nickname>")
                return
            nickname = parts[1]
            for client, nick in list(self.client_nicknames.items()):
                if nick == nickname:
                    try:
                        client.shutdown(socket.SHUT_RDWR)
                    except:
                        pass
                    client.close()
                    if client in self.clients:
                        self.clients.remove(client)
                    del self.client_nicknames[client]
                    del self.client_ips[client]
                    print(f"Kicked {nickname}")
                    break
            else:
                print("Nickname not found")
        elif cmd == 'ban':
            if len(parts) < 2:
                print("Usage: ban <nickname>")
                return
            nickname = parts[1]
            if nickname not in self.config['nickname_blacklist']:
                self.config['nickname_blacklist'].append(nickname)
                self.save_config()
                print(f"Banned nickname {nickname}")
                # Kick if online
                for client, nick in list(self.client_nicknames.items()):
                    if nick == nickname:
                        try:
                            client.shutdown(socket.SHUT_RDWR)
                        except:
                            pass
                        client.close()
                        if client in self.clients:
                            self.clients.remove(client)
                        del self.client_nicknames[client]
                        del self.client_ips[client]
                        print(f"Kicked banned user {nickname}")
        elif cmd == 'banip':
            if len(parts) < 2:
                print("Usage: banip <ip>")
                return
            ip = parts[1]
            if ip not in self.config['ip_blacklist']:
                self.config['ip_blacklist'].append(ip)
                self.save_config()
                print(f"Banned IP {ip}")
                # Kick if online
                for client, client_ip in list(self.client_ips.items()):
                    if client_ip == ip:
                        try:
                            client.shutdown(socket.SHUT_RDWR)
                        except:
                            pass
                        client.close()
                        if client in self.clients:
                            self.clients.remove(client)
                        if client in self.client_nicknames:
                            del self.client_nicknames[client]
                        del self.client_ips[client]
                        print(f"Kicked banned IP {ip}")
        elif cmd == 'stop':
            self.stop()
        else:
            print("Unknown command. Available: list_clients, send, update_user, list_users, kick, ban, banip, stop")

    def recvall(self, sock, n):
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            default_config = {
                'host': '0.0.0.0',
                'port': 12345,
                'use_ip_whitelist': False,
                'ip_whitelist': [],
                'ip_blacklist': [],
                'use_nickname_whitelist': False,
                'nickname_whitelist': [],
                'nickname_blacklist': []
            }
            self.save_config(default_config)
            return default_config

    def save_config(self, config=None):
        if config is None:
            config = self.config
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def stop(self):
        self.running = False
        self.server_socket.close()
        for client in self.clients:
            client.close()
        self.clients.clear()
        self.client_nicknames.clear()
        self.client_ips.clear()
        print("Server stopped")


class SimpleClient:
    def __init__(self, host='127.0.0.1', port=12345, key=None):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.key = key
        self.cipher = Fernet(key) if key else None
        self.running = False
        self.receive_thread = None
        self.message_handler = None

    def connect(self):
        self.socket.connect((self.host, self.port))
        self.running = True
        self.receive_thread = threading.Thread(target=self.receive_loop, daemon=True)
        self.receive_thread.start()

    def send_text(self, text):
        message = {'type': 'text', 'data': text}
        self.send_message(message)

    def send_file(self, filepath):
        if not os.path.isfile(filepath):
            print(f"File {filepath} does not exist")
            return
        with open(filepath, 'rb') as f:
            filedata = base64.b64encode(f.read()).decode('utf-8')
        filename = os.path.basename(filepath)
        message = {'type': 'file', 'filename': filename, 'data': filedata}
        self.send_message(message)

    def send_login(self, nickname):
        message = {'type': 'login', 'nickname': nickname}
        self.send_message(message)

    def send_message(self, message):
        data = json.dumps(message).encode()
        if self.cipher:
            data = self.cipher.encrypt(data)
        msg_length = struct.pack('>I', len(data))
        try:
            self.socket.sendall(msg_length + data)
        except Exception as e:
            print(f"Error sending message: {e}")
            sys.exit()

    def receive_loop(self):
        try:
            while self.running:
                header = self.recvall(4)
                if not header:
                    break
                msg_length = struct.unpack('>I', header)[0]
                data = self.recvall(msg_length)
                if self.cipher:
                    data = self.cipher.decrypt(data)
                message = json.loads(data.decode())
                if self.message_handler:
                    self.message_handler(message)
        except Exception as e:
            print(f"Receive error: {e}")
        finally:
            self.socket.close()

    def recvall(self, n):
        data = b''
        while len(data) < n:
            packet = self.socket.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def set_message_handler(self, handler):
        self.message_handler = handler

    def disconnect(self):
        self.running = False
        self.socket.close()


if tk:
    class ServerGUI:
        def __init__(self, server):
            self.server = server
            self.root = tk.Tk()
            self.root.title("Server Control")
            self.root.geometry("1000x600")

            # Main frame
            main_frame = tk.Frame(self.root)
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Users list on the left
            self.users_list = tk.Listbox(main_frame, width=30)
            self.users_list.pack(side=tk.LEFT, fill=tk.Y)

            # Console text area
            self.console = tk.Text(main_frame, wrap=tk.WORD)
            self.console.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            # Bottom frame
            bottom_frame = tk.Frame(self.root)
            bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

            self.memory_label = tk.Label(bottom_frame,text="Memory ??")
            self.memory_label.pack(side=tk.LEFT)
            # Command entry on the right
            self.command_entry = tk.Entry(bottom_frame)
            self.command_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            self.command_entry.bind("<Return>", self.on_command)

            # Redirect stdout
            self.stdout_buffer = StringIO()
            self.old_stdout = sys.stdout
            sys.stdout = self

            # Start server
            threading.Thread(target=self.server.start, daemon=True).start()

            # Start updates
            self.update_gui()

            self.root.mainloop()

        def write(self, text):
            self.console.insert(tk.END, text)
            self.console.see(tk.END)

        def flush(self):
            pass

        def on_command(self, event):
            command = self.command_entry.get()
            self.command_entry.delete(0, tk.END)
            self.server.process_command(command)

        def update_gui(self):
            # Update memory
            if psutil:
                mem = psutil.virtual_memory()
                self.memory_label.config(text=f"Memory: {mem.percent}%")
            else:
                self.memory_label.config(text="Memory: N/A")

            # Update users list
            self.users_list.delete(0, tk.END)
            for i, client in enumerate(self.server.clients):
                try:
                    addr = client.getpeername()
                    self.users_list.insert(tk.END, f"{i}: {addr}")
                except:
                    self.users_list.insert(tk.END, f"{i}: disconnected")

            self.root.after(1000, self.update_gui)

        def __del__(self):
            sys.stdout = self.old_stdout
else:
    class ServerGUI:
        def __init__(self, server):
            print("Tkinter not available. Running server in console mode.")
            self.server = server
            self.server.start()
