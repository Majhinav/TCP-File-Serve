#  Multithreaded TCP File Server

A high-performance, multithreaded TCP File Server built entirely in Python. This project allows multiple client connections concurrently to seamlessly upload, download, list, and delete files remotely inside a containerized environment.

---

##  Features
* **Asynchronous Multi-Threading:** Handles concurrent client operations smoothly using native threading protocols.
* **Granular File Controls:** Clean implementation of custom streaming protocols for remote storage execution.
* **Isolated Environments:** Separate workspaces keeping development assets cleanly detached from server storage dependencies.

---

##  System Architecture Directory Layout

```text
TCP-File-Serve/
│
├── file_server/
│   ├── client_workspace/    #  Local files ready for upload/download
│   ├── server_storage/      #  Remote server directory holding live assets
│   ├── client.py            #  Interactive socket consumer client runtime 
│   └── server.py            #  Asynchronous TCP listening hub entrypoint
└── README.md                #  System setup guide documentation
```

---

##  Setup & Local Quickstart Instructions

### 1. Initialize and Start the Listening Server
Open a dedicated terminal window panel inside your Codespace and boot up the network socket:
```bash
python3 file_server/server.py
```
*Expected console feedback:* `[*] Server listening on 0.0.0.0:9999`

### 2. Connect Your Interactive Consumer Client
Open a separate split terminal panel window alongside your active server session and type:
```bash
python3 file_server/client.py
```

---

## 🎮 Command Interface Execution Usage

Once connected via the client node workspace interface panel console system loop tracking, you can trigger these operations inside the console interface environment manually:

| Operational Command String Input | Action Result Context Routing | Example Command Run Usage |
| :--- | :--- | :--- |
| `LIST` | Pulls a complete text configuration manifest of current items hosted inside the remote storage folder directory maps. | `LIST` |
| `UPLOAD <filename>` | Sends an asset from your local `client_workspace` partition directly into the server's cloud bucket stack. | `UPLOAD sample.txt` |
| `DOWNLOAD <filename>` | Fetches a target asset securely down from the host node straight to your designated client workspace paths. | `DOWNLOAD sample.txt` |
| `DELETE <filename>` | Triggers filesystem purging handlers to erase target files directly off remote tracking drives cleanly. | `DELETE sample.txt` |
| `EXIT` | Safely disconnects the network loop tracker pipe and terminates current runtime threads cleanly. | `EXIT` |
