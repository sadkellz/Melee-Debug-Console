import threading
import time

import pymem
from pymem.exception import ProcessNotFound

EMU_SIZE = 0x2000000
EMU_DIST = 0x10000

GALE01 = None
pm = None
proc = None
pm_lock = threading.Lock()


# Finds the specific page with the size of EMU_SIZE.
def pattern_scan_all(handle, pattern, *, return_multiple=False):
    next_region = 0
    found = []

    try:
        while next_region < 0x7FFFFFFF0000:
            next_region, page_found = pymem.pattern.scan_pattern_page(
                handle,
                next_region,
                pattern,
                return_multiple=return_multiple
            )

            if not return_multiple and page_found:
                if (next_region - page_found) == int(EMU_SIZE):
                    return page_found

            if page_found:
                if (next_region - page_found) == int(EMU_SIZE):
                    found += page_found

        if not return_multiple:
            return None
        return found
    except:
        return None


resources_initialized = threading.Event()


def get_proc():
    global pm
    global GALE01
    pids = ["Slippi Dolphin.exe", "Dolphin.exe"]
    byte_pattern = bytes.fromhex("47 41 4C 45 30 31 00 02")
    while True:
        for pid in pids:
            try:
                pm = pymem.Pymem(pid)
                # Access a process attribute to check if the process exists
                pm.process_handle
                if pm is not None:
                    GALE01 = pattern_scan_all(pm.process_handle, byte_pattern)
                else:
                    GALE01 = None
                break  # Break the loop if the process is found
            except ProcessNotFound:
                continue
        else:
            # If no process is found, set pm to None
            pm = None
        resources_initialized.set()
        time.sleep(1)


def get_melee():
    global GALE01
    handle = pm.process_handle
    byte_pattern = bytes.fromhex("47 41 4C 45 30 31 00 02")
    if pm is None:
        return
    while True:
        try:
            GALE01 = pattern_scan_all(handle, byte_pattern)
            print("getting")
            # break  # Break the loop if the process is found
        except:
            GALE01 = None
            continue
        print(GALE01)
        time.sleep(1)
