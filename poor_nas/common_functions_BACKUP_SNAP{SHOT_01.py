###
### changed the mergerfs mount to mount the disk AND the top level folder
### eg from 
###    /srv/usb3disk1
### to
###    /srv/usb3disk1/mediaroot
###
### So we must change all this code to suit that
### 

import os
import sys
import subprocess
from pathlib import Path
import glob
import re
import logging
import pprint

# Configuration
DEBUG_IS_ON = False  # Set to True to enable debug printing
objPrettyPrint = None
#

def init_PrettyPrinter(TERMINAL_WIDTH):
    # Set up prettyprint for formatting
    global objPrettyPrint
    objPrettyPrint = pprint.PrettyPrinter(width=TERMINAL_WIDTH, compact=False, sort_dicts=False)  # facilitates formatting
    return

def init_logging(log_filename):
    # Set up logging
    logging.basicConfig(filename=log_filename,
                        level=logging.DEBUG if DEBUG_IS_ON else logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s')

def debug_pause():
    if DEBUG_IS_ON:
        message = f"DEBUG: Press Enter to continue..."
        logging.debug(message)
        print(message, flush=True)
        input()

def debug_log_and_print(message, data=None):
    """
    Logs and prints a message with optional data, if DEBUG is on.
    """
    if DEBUG_IS_ON:
        logging.debug(message)
        print(f"DEBUG: {message}", flush=True)
        if data is not None:
            logging.debug(objPrettyPrint.pformat(data))
            print(objPrettyPrint.pformat(data), flush=True)

def error_log_and_print(message, data=None):
    """
    Logs and prints a message with optional data, if DEBUG is on.
    """
    logging.error(message)
    print(f"ERROR: {message}", flush=True)
    if data is not None:
        logging.error(objPrettyPrint.pformat(data))
        print(objPrettyPrint.pformat(data), flush=True)

def log_and_print(message, data=None):
    """
    Logs and prints a message with optional data.
    """
    logging.info(message)
    print(f"{message}", flush=True)
    if data is not None:
        logging.info(objPrettyPrint.pformat(data))
        print(objPrettyPrint.pformat(data), flush=True)

def find_mount_point_from_path(path):
    """
    Returns the status, error number, error string, and the mount point from a path.
    """
    status = True
    error_number = 0
    error_string = ""
    resolved_mount_point_str = ""
    try:
        resolved_path = Path(path).resolve(strict=True)
        while not resolved_path.is_mount():
            resolved_path = resolved_path.parent
        resolved_mount_point_str = str(resolved_path)
    except OSError as e:
        error_number = e.errno
        error_string = e.strerror
        status = False
    except Exception as e:
        error_number = getattr(e, 'errno', None)
        error_string = str(e)
        status = False
    return status, error_number, error_string, resolved_mount_point_str

def get_top_level_folder_from_path(path):
    """
    Returns the status, error number, error string, and the topmost folder underneath the mount point from a path.
    """
    status = True
    error_number = 0
    error_string = ""
    resolved_top_level_folder_str = ""
    try:
        resolved_path = Path(path).resolve(strict=True)
    except OSError as e:
        error_number = e.errno
        error_string = e.strerror
        status = False
        return status, error_number, error_string, resolved_top_level_folder_str
    except Exception as e:
        error_number = getattr(e, 'errno', None)
        error_string = str(e)
        status = False
        return status, error_number, error_string, resolved_top_level_folder_str
    status, error_number, error_string, resolved_mount_point = find_mount_point_from_path(resolved_path)
    if not status or not resolved_mount_point:
        return status, error_number, error_string, resolved_top_level_folder_str
    try:
        resolved_path_under_mount = resolved_path.relative_to(resolved_mount_point)
        resolved_top_level_folder_str = resolved_path_under_mount.parts[0] if resolved_path_under_mount.parts else ""
    except OSError as e:
        error_number = e.errno
        error_string = e.strerror
        status = False
    except Exception as e:
        error_number = getattr(e, 'errno', None)
        error_string = str(e)
        status = False
    return status, error_number, error_string, resolved_top_level_folder_str

def extract_five_path_components(path):
    """
    Returns a status, error number, error string, and 5 path components:
    - status: boolean indicating if the whole process succeeded
    - error_number: the error number if an exception occurred, otherwise 0
    - error_string: the error string if an exception occurred, otherwise an empty string
    - the resolved path
    - the resolved mount point
    - the resolved path underneath the mount point
    - the resolved topmost folder underneath the mount point
    - the resolved remaining path underneath the topmost folder
    from a given path.
    Called:
        status, error_number, error_string, resolved_path, resolved_mount_point, resolved_path_under_mount, resolved_top_level_folder, resolved_path_under_top_level_folder = extract_five_path_components(path)
    """
    status = True
    error_number = 0
    error_string = ""
    resolved_path_str = ""
    resolved_mount_point_str = ""
    resolved_path_under_mount_str = ""
    resolved_top_level_folder_str = ""
    resolved_path_under_top_level_folder_str = ""

    if status:
        try:
            resolved_path = Path(path).resolve(strict=True)
            resolved_path_str = str(resolved_path)
        except OSError as e:
            error_number = e.errno
            error_string = e.strerror
            status = False
        except Exception as e:
            error_number = getattr(e, 'errno', None)
            error_string = str(e)
            status = False
    if status:
        try:
            resolved_mount_point = resolved_path
            while not resolved_mount_point.is_mount():
                resolved_mount_point = resolved_mount_point.parent
            resolved_mount_point_str = str(resolved_mount_point)
        except OSError as e:
            error_number = e.errno
            error_string = e.strerror
            status = False
        except Exception as e:
            error_number = getattr(e, 'errno', None)
            error_string = str(e)
            status = False
    if status:
        try:
            resolved_path_under_mount = resolved_path.relative_to(resolved_mount_point)
            resolved_path_under_mount_str = str(resolved_path_under_mount) if str(resolved_path_under_mount) != "." else ""
        except OSError as e:
            error_number = e.errno
            error_string = e.strerror
            status = False
        except Exception as e:
            error_number = getattr(e, 'errno', None)
            error_string = str(e)
            status = False
    if status:
        try:
            resolved_top_level_folder = resolved_path_under_mount.parts[0] if resolved_path_under_mount.parts else ""
            resolved_top_level_folder_str = str(resolved_top_level_folder)
        except OSError as e:
            error_number = e.errno
            error_string = e.strerror
            status = False
        except Exception as e:
            error_number = getattr(e, 'errno', None)
            error_string = str(e)
            status = False
    if status:
        try:
            resolved_path_under_top_level_folder = Path(*resolved_path_under_mount.parts[1:]) if len(resolved_path_under_mount.parts) > 1 else Path()
            resolved_path_under_top_level_folder_str = str(resolved_path_under_top_level_folder)
        except OSError as e:
            error_number = e.errno
            error_string = e.strerror
            status = False
        except Exception as e:
            error_number = getattr(e, 'errno', None)
            error_string = str(e)
            status = False
    return status, error_number, error_string, resolved_path_str, resolved_mount_point_str, resolved_path_under_mount_str, resolved_top_level_folder_str, resolved_path_under_top_level_folder_str

def get_free_disk_space(path):
    """
    Get the free disk space for the given path.
    Returns a tuple:
    - status: boolean indicating if the whole process succeeded
    - error_number: the error number if an exception occurred, otherwise 0
    - error_string: the error string if an exception occurred, otherwise an empty string
    - free_space: the free space in bytes, or 0 if an error occurred
    """
    status = True
    error_number = 0
    error_string = ""
    free_space = 0

    try:
        st = os.statvfs(path)
        free_space = st.f_bavail * st.f_frsize
    except OSError as e:
        error_number = e.errno
        error_string = e.strerror
        status = False
    except Exception as e:
        error_number = getattr(e, 'errno', None)
        error_string = str(e)
        status = False
    return status, error_number, error_string, free_space

def get_mergerfs_disks_in_LtoR_order_from_fstab():
    """
    Reads the /etc/fstab file to find the disks used in the mergerfs mount line.
    Handles globbing patterns to expand disk entries.
    
    Returns:
        list of dict: A list of dictionaries, each representing a detected mergerfs underlying disk in LtoR order from fstab.
        Each dictionary contains:
            - 'disk_mount_point' (str): The mount point path of the disk (e.g., '/srv/usb3disk1').
            - 'free_disk_space' (int): The free disk space available on the disk in bytes.
    Example:
        [
            {'disk_mount_point': '/srv/usb3disk1', 'free_disk_space': 1234567890},
            {'disk_mount_point': '/srv/usb3disk2', 'free_disk_space': 987654321},
        ]

    Notes: this does not guarantee a detected underlying disk contains a root folder or any 'top level media folders' under it.
           Handle disks referenced but not mounted in /etc/fstab.
           Does not depend on the mergerfs disk mount referencing a top-level root folder or not.
           If a top-level root folder specified in the mergerfs mount does not exist, the disk is skipped for this run.
           Skips unmounted disks for this run.
    """
    the_mergerfs_disks_in_LtoR_order_from_fstab = []
    try:
        with open('/etc/fstab', 'r') as fstab_file:
            fstab_lines = fstab_file.readlines()
        # Loop through all lines in fstab looking for 'mergerfs' mounts.
        # Keep the valid mergerfs underlying disks in LtoR order
        # so we can use it later to determine the 'ffd', aka 'first found disk', for each 'top media folder' by parsing this list
        fstab_mergerfs_line = ''
        number_of_mergerfs_lines = 0
        for line in fstab_lines:
            # Example line (without the #) we are looking for
            # ... when delete, only delete the first found, backup copies of a file are unaffected
            #         /srv/usb3disk*/mediaroot /srv/media mergerfs defaults,category.action=ff,category.create=ff,category.search=all,moveonenospc=true,dropcacheonclose=true,cache.readdir=true,cache.files=partial,lazy-umount-mountpoint=true 0 0
            debug_log_and_print(f"A line was read from /etc/fstab:", data=line)
            if line.startswith('#') or not line.strip():
                continue
            fields = line.split()
            if any('mergerfs' in field.lower() for field in fields):  # Identify mergerfs entries
                number_of_mergerfs_lines += 1
                fstab_mergerfs_line = line.strip()
                debug_log_and_print(f"MergerFS line found: {line.strip()}")
                # fields[0] should contain one or more and/or globbed, underlying file system mount points used by mergerfs
                mount_points = fields[0]
                # Split apart a possible list of underlying file system mount points separated by ':'
                split_disks = mount_points.split(':')
                # Process each underlying file system mount point separately, catering for globbing entries
                for disk in split_disks:
                    if '*' in disk:
                        # Handle wildcard globbing pattern (eg /mnt/hdd*)
                        expanded_paths = sorted(glob.glob(disk))
                        debug_log_and_print(f"MergerFS line Handling wildcard globbing pattern ... expanded_paths:", data=expanded_paths)
                        # Iterate over each path in the expanded paths
                        for ep in expanded_paths:
                            # if it is detected as valid (i.e. it is mounted and the rest of it is valid and exists) then find the free disk space and add it to the_mergerfs_disks_in_LtoR_order_from_fstab 
                            efpc_status, efpc_error_number, efpc_error_string, efpc_resolved_path, efpc_resolved_mount_point, efpc_resolved_path_under_mount, efpc_resolved_top_level_folder, efpc_resolved_path_under_top_level_folder = extract_five_path_components(ep)
                            if efpc_resolved_mount_point == "" or not efpc_status:
                                continue # disk perhaps not mounted etc, skip to the end of this FOR iteration
                            # Get the free disk space
                            fds_status, fds_error_number, fds_error_string, fds_free_disk_space = get_free_disk_space(efpc_resolved_mount_point)
                            the_mergerfs_disks_in_LtoR_order_from_fstab.append({'disk_mount_point': efpc_resolved_mount_point, 'free_disk_space': fds_free_disk_space})
                    elif '{' in disk and '}' in disk:
                        # Handle curly brace globbing pattern (eg /mnt/{hdd1,hdd2})
                        pattern = re.sub(r'\{(.*?)\}', r'(\1)', disk)
                        expanded_paths = sorted(glob.glob(pattern))
                        # Iterate over each path in the expanded paths
                        for ep in expanded_paths:
                            # if it is detected as valid (i.e. it is mounted and the rest of it is valid and exists) then find the free disk space and add it to the_mergerfs_disks_in_LtoR_order_from_fstab 
                            efpc_status, efpc_error_number, efpc_error_string, efpc_resolved_path, efpc_resolved_mount_point, efpc_resolved_path_under_mount, efpc_resolved_top_level_folder, efpc_resolved_path_under_top_level_folder = extract_five_path_components(ep)
                            if efpc_resolved_mount_point == "" or not efpc_status:
                                continue # disk perhaps not mounted etc, skip to the end of this FOR iteration
                            # Get the free disk space
                            fds_status, fds_error_number, fds_error_string, fds_free_disk_space = get_free_disk_space(efpc_resolved_mount_point)
                            the_mergerfs_disks_in_LtoR_order_from_fstab.append({'disk_mount_point': efpc_resolved_mount_point, 'free_disk_space': fds_free_disk_space})
                    else:
                        # Handle plain (eg /mnt/hdd1 underlying file system mount point
						# Do not care if there is an error from get_free_disk_space ... the free disk space will be returned as zero which is OK
                        efpc_status, efpc_error_number, efpc_error_string, efpc_resolved_path, efpc_resolved_mount_point, efpc_resolved_path_under_mount, efpc_resolved_top_level_folder, efpc_resolved_path_under_top_level_folder = extract_five_path_components(disk)
                        if efpc_resolved_mount_point == "" or not efpc_status:
                            continue # disk perhaps not mounted etc, skip to the end of this FOR iteration
                        fds_status, fds_error_number, fds_error_string, fds_free_disk_space = get_free_disk_space(efpc_resolved_mount_point)
                        the_mergerfs_disks_in_LtoR_order_from_fstab.append({'disk_mount_point': efpc_resolved_mount_point, 'free_disk_space': fds_free_disk_space})
    except Exception as e:
        error_log_and_print(f"Error reading /etc/fstab: {e}")
        sys.exit(1)  # Exit with a status code indicating an error

    # If more than 1 mergerfs line is found, it's a conflict
    if number_of_mergerfs_lines > 1:
        error_log_and_print(f"Multiple mergerfs lines found in 'fstab'. Aborting.")
        sys.exit(1)  # Exit with a status code indicating an error

    if (number_of_mergerfs_lines < 1) or (len(the_mergerfs_disks_in_LtoR_order_from_fstab) < 1) :
        error_log_and_print(f"ZERO detections of 'mergerfs' underlying disks in LtoR order from 'fstab':", data=the_mergerfs_disks_in_LtoR_order_from_fstab)
        sys.exit(1)  # Exit with a status code indicating an error

    debug_log_and_print(f"Detected 'mergerfs' underlying disks in LtoR order from fstab '{fstab_mergerfs_line}'", data=the_mergerfs_disks_in_LtoR_order_from_fstab)
    return the_mergerfs_disks_in_LtoR_order_from_fstab

def detect_mergerfs_disks_having_a_root_folder_having_files(mergerfs_disks_in_LtoR_order_from_fstab):
    """
    Checks each underlying mergerfs disk_mount_point for the presence of a single root folder like 'mediaroot'.
    If multiple root folders are found on a single disk_mount_point, it raises an error with details.
    
    Args:
        mergerfs_disks_in_LtoR_order_from_fstab (list of dict): A list of dictionaries representing detected mergerfs underlying disks.
            Each dictionary contains:
                - 'disk_mount_point' (str): The mount point path of the disk (e.g., '/srv/usb3disk1').
                - 'free_disk_space' (int): The free disk space available on the disk in bytes.
    
    Returns:
        dict: A dictionary containing information about disks with root folders and their top-level media folders.
        Key: 'disk_mount_point' (str): The mount point path of the disk (e.g., '/srv/usb3disk1').
        Value: dict with the following keys:
            - 'root_folder_path' (Path): The path to the root folder (e.g., Path('/srv/usb3disk1/mediaroot')).
            - 'top_level_media_folders' (list of dict): A list of dictionaries, each representing a top-level media folder.
                Each dictionary contains:
                    - 'top_level_media_folder_name' (str): The name of the media folder (e.g., 'Movies').
                    - 'top_level_media_folder_path' (Path): The path to the media folder (e.g., Path('/srv/usb3disk1/mediaroot/Movies')).
                    - 'ffd' (str): Initially an empty string, will be populated later with the first found disk (FFD).
                    - 'number_of_files' (int): The number of files in the media folder.
                    - 'disk_space_used' (int): The disk space used by the media folder in bytes.
    Example:
        {
            '/srv/usb3disk1': {
                'root_folder_path': Path('/srv/usb3disk1/mediaroot'),
                'top_level_media_folders': [
                    {
                        'top_level_media_folder_name': 'Movies',
                        'top_level_media_folder_path': Path('/srv/usb3disk1/mediaroot/Movies'),
                        'ffd': '',
                        'number_of_files': 1500,
                        'disk_space_used': 12000000000
                    },
                    ...
                ]
            },
            ...
        }
    """
    those_mergerfs_disks_having_a_root_folder_having_files = {}
    for disk_info in mergerfs_disks_in_LtoR_order_from_fstab:
        disk_mount_point = disk_info['disk_mount_point']
        try:
            disk_mount_point_path = Path(disk_mount_point)
            if disk_mount_point_path.is_dir():
                # find candidate media root folder with name 'mediaroot'
                #candidate_root_folders = [d.name for d in sorted(disk_mount_point_path.iterdir()) if d.is_dir() and re.match(r'^mediaroot[1-8]$', d.name)]
                candidate_root_folders = [d.name for d in sorted(disk_mount_point_path.iterdir()) if d.is_dir() and re.match(r'^mediaroot$', d.name)]
                # Check for multiple root folders on the same disk
                if len(candidate_root_folders) > 1:
                    error_log_and_print(f"Each disk_mount_point should only have only one root folder like 'mediaroot'.")
                    error_log_and_print(f"Error: disk_mount_point {disk_mount_point} has multiple root folders:", data=candidate_root_folders)
                    sys.exit(1)  # Exit with a status code indicating an error
                elif len(candidate_root_folders) == 1:
                    found_root_folder = candidate_root_folders[0]
                    found_root_folder_path = disk_mount_point_path / found_root_folder
                    found_top_level_media_folders_list = []
                    for top_level_media_folder in sorted(found_root_folder_path.iterdir()):
                        if top_level_media_folder.is_dir():
                            number_of_files = sum([len(files) for r, d, files in os.walk(top_level_media_folder)])
                            disk_space_used = sum([os.path.getsize(os.path.join(r, file)) for r, d, files in os.walk(top_level_media_folder) for file in files])
                            if number_of_files > 0:
                                found_top_level_media_folders_list.append({
                                    'top_level_media_folder_name': top_level_media_folder.name,
                                    'top_level_media_folder_path': top_level_media_folder,
                                    'ffd': '',
                                    'number_of_files': number_of_files,
                                    'disk_space_used': disk_space_used
                                })
                    # if a disk_mount_point with a known root folder has top level media folders having files, then save them
                    if found_top_level_media_folders_list:
                        those_mergerfs_disks_having_a_root_folder_having_files[disk_mount_point] = {
                            'root_folder_path': found_root_folder_path,
                            'top_level_media_folders': found_top_level_media_folders_list
                        }
                        debug_log_and_print(f"disk_mount_point '{disk_mount_point}' has root folder '{found_root_folder}' with top level media folders having files:", data=found_top_level_media_folders_list)
                else:
                    pass
        except Exception as e:
            error_log_and_print(f"Error accessing {disk_mount_point}: {e}")
            sys.exit(1)  # Exit with a status code indicating an error

    if len(those_mergerfs_disks_having_a_root_folder_having_files) < 1:
        error_log_and_print(f"ZERO Detected 'mergerfs' underlying disks having a root folder AND top_level_media_folders having files:", data=mergerfs_disks_in_LtoR_order_from_fstab)
        sys.exit(1)  # Exit with a status code indicating an error

    debug_log_and_print(f"Detected 'mergerfs' underlying disks having a root folder AND top level media folders having files:", data=those_mergerfs_disks_having_a_root_folder_having_files)
    return those_mergerfs_disks_having_a_root_folder_having_files

def get_unique_top_level_media_folders(mergerfs_disks_in_LtoR_order_from_fstab, mergerfs_disks_having_a_root_folder_having_files):
    """
    Consolidates and derives unique top-level media folder names from the detected disks.
    Also determines the first found disk (FFD) for each unique media folder and additional information.
    
    Args:
        mergerfs_disks_having_a_root_folder_having_files (dict): A dictionary containing information about disks with root folders and their top-level media folders.
            Key: 'disk_mount_point' (str): The mount point path of the disk (e.g., '/srv/usb3disk1').
            Value: dict with the following keys:
                - 'root_folder_path' (Path): The path to the root folder.
                - 'top_level_media_folders' (list of dict): A list of dictionaries, each representing a top-level media folder.
                    - 'top_level_media_folder_name' (str): The name of the media folder.
                    - 'top_level_media_folder_path' (Path): The path to the media folder.
                    - 'ffd' (str): Initially an empty string, will be populated later with the FFD.
                    - 'number_of_files' (int): The number of files in the media folder.
                    - 'disk_space_used' (int): The disk space used by the media folder in bytes.
        mergerfs_disks_in_LtoR_order_from_fstab (list of dict): A list of dictionaries representing detected mergerfs underlying disks.
            Each dictionary contains:
                - 'disk_mount_point' (str): The mount point path of the disk (e.g., '/srv/usb3disk1').
                - 'free_disk_space' (int): The free disk space available on the disk in bytes.
    
    Returns:
        dict: A dictionary containing unique top-level media folders and related derived information.
        Key: 'top_level_media_folder_name' (str): The unique name of the top-level media folder (e.g., 'Movies').
        Value: dict with the following keys:
            - 'ffd' (str): The first found disk for this media folder.
            - 'disk_info' (list of dict): A list of dictionaries with information about each disk containing this media folder.
                Each dictionary contains:
                    - 'disk_mount_point' (str): The mount point path of the disk.
                    - 'is_ffd' (bool): Whether this disk is the FFD for the media folder.
                    - 'root_folder_path' (Path): The path to the root folder.
                    - 'number_of_files' (int): The number of files in this media folder on this disk.
                    - 'disk_space_used' (int): The disk space used by this media folder on this disk.
                    - 'total_free_disk_space' (int): The total free disk space on this disk.
    Example:
        {
            'Movies': {
                'ffd': '/srv/usb3disk1',
                'disk_info': [
                    {
                        'disk_mount_point': '/srv/usb3disk1',
                        'is_ffd': True,
                        'root_folder_path': Path('/srv/usb3disk1/mediaroot'),
                        'number_of_files': 1500,
                        'disk_space_used': 12000000000,
                        'total_free_disk_space': 50000000000
                    },
                    {
                        'disk_mount_point': '/srv/usb3disk2',
                        'is_ffd': False,
                        'root_folder_path': Path('/srv/usb3disk2/mediaroot'),
                        'number_of_files': 1500,
                        'disk_space_used': 12000000000,
                        'total_free_disk_space': 60000000000
                    },
                    ...
                ]
            },
            ...
        }
    """
    unique_top_level_media_folders = {}

    # Step 1: Gather all unique top-level media folders
    for disk_info in mergerfs_disks_having_a_root_folder_having_files.values():
        for media_folder_info in disk_info['top_level_media_folders']:
            top_level_media_folder_name = media_folder_info['top_level_media_folder_name']
            if top_level_media_folder_name not in unique_top_level_media_folders:
                unique_top_level_media_folders[top_level_media_folder_name] = {
                    'top_level_media_folder_name': top_level_media_folder_name,
                    'ffd': '',
                    'disk_info': []
                }

    # Step 2: Determine the ffd (first found disk) for each top-level media folder
    for top_level_media_folder_name, folder_info in unique_top_level_media_folders.items():
        for disk_info in mergerfs_disks_in_LtoR_order_from_fstab:
            disk_mount_point = disk_info['disk_mount_point']
            if disk_mount_point in mergerfs_disks_having_a_root_folder_having_files:
                disk_root_folder_info = mergerfs_disks_having_a_root_folder_having_files[disk_mount_point]
                for media_folder_info in disk_root_folder_info['top_level_media_folders']:
                    if media_folder_info['top_level_media_folder_name'] == top_level_media_folder_name:
                        if folder_info['ffd'] == '':
                            folder_info['ffd'] = disk_mount_point
                        is_ffd = (disk_mount_point == folder_info['ffd'])
                        folder_info['disk_info'].append({
                            'disk_mount_point': disk_mount_point,
                            'is_ffd': is_ffd,
                            'root_folder_path': str(disk_root_folder_info['root_folder_path']),
                            'number_of_files': media_folder_info['number_of_files'],
                            'disk_space_used': media_folder_info['disk_space_used'],
                            'total_free_disk_space': disk_info['free_disk_space']
                        })

    # Step 3: Update ffd for each folder in mergerfs_disks_having_a_root_folder_having_files
    for disk_info in mergerfs_disks_having_a_root_folder_having_files.values():
        for media_folder_info in disk_info['top_level_media_folders']:
            media_folder_name = media_folder_info['top_level_media_folder_name']
            media_folder_info['ffd'] = unique_top_level_media_folders[media_folder_name]['ffd']

    return unique_top_level_media_folders, mergerfs_disks_having_a_root_folder_having_files
