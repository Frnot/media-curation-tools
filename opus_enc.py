#!/usr/bin/python3

import subprocess
import multiprocessing
from multiprocessing import Pool, Process, Queue
import threading
from threading import Semaphore
import os
import shutil


source_dir = "/mnt/music"
dest_dir = "music"

# for file in /mnt/music
# if file is flac
# send filepath to converter job
#elif file is mp3
# send filepath to copy job


def main():
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            filepath = os.path.join(root,file)

            if filepath.lower().endswith(".flac"):
                encode(filepath, "")
            elif filepath.lower().endswith(".mp3"):
                pass





def encode(flacpath, opuspath):
    # copy flacpath from mount to local disk
    localpath = os.path.join(dest_dir,os.path.relpath(flacpath, start=source_dir))
    print(localpath)
    #os.makedirs(os.path.dirname(localpath), exist_ok=True)
    #shutil.copy(flacpath, localpath)



def execute(command, return_rc=False):
    cmdarr = command.split()
    result = subprocess.run(cmdarr, text=True, capture_output=True)

    if return_rc:
        return result.returncode, result.stderr.strip()
    else:
        return result.stdout


class Scheduler:
    def __init__(self):
        self.threads = int(multiprocessing.cpu_count())
        self.job_queue = Queue()
        #todo: run task runner in seperate thread
        #self.taskrunner()

        self.pool = Pool(processes=self.thread)
        self.workers = Semaphore(self.threads)


    def taskrunner(self):
        # Will execute if any workers are available, else will block
        while True:
            self.workers.acquire()
            job = self.job_queue.get()
            self.pool.apply_async(job, callback=self.workers.release())

    def schedule(self, job):
        #j = Job(job)
        self.job_queue.put(j)

    


main()