#!/usr/bin/python
import time
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileSyncHandler(FileSystemEventHandler):
    def __init__(self, fileName, serverName, password):
        self.fileName = fileName
        self.serverName = serverName
        self.password = password
        print "File to sync with server: ", fileName

    def on_modified(self, event):
        print "Change detected with type ", event.event_type, " and path ", event.src_path
        if event.src_path == self.fileName:
            print "Sync file to server"
            os.system('sshpass -p ' + self.password + ' scp ' + self.fileName + ' ' + self.serverName)


if __name__ == "__main__":
    with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json') as config_file:    
        config = json.load(config_file)
    event_handler = FileSyncHandler(config['file'], config['server'], config['password'])
    dirPath = os.path.dirname(config['file'])
    observer = Observer()
    observer.schedule(event_handler, path=dirPath, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
