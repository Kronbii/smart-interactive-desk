from . import config
from . import ds4
from . import web
from . import manual
from . import auto
from .utils import log
import multiprocessing
import time

#TODO: add a priority system to the threads

def run_web():
    web.main()

def run_manual():
    manual.main()
    
def run_auto():
    auto.main()
    
def run_ds4():
    ds4.main()

def main():
    if config.ds4_control:
        ds4_thread = multiprocessing.Process(target=run_ds4)
        ds4_thread.start()
    if config.web_control:
        web_thread = multiprocessing.Process(target=run_web)
        web_thread.start()
    if config.manual_control:
        manual_thread = multiprocessing.Process(target=run_manual)
        manual_thread.start()
    if config.auto_control:
        auto_thread = multiprocessing.Process(target=run_auto)
        auto_thread.start()
        
    ds4_thread.join()
    web_thread.join()
    manual_thread.join()
    auto_thread.join()
    print("All tasks completed")


if __name__ == "__main__":
    main()
