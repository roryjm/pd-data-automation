import os
from datetime import date


def list_all_dir(path):
    """
    Creates list of all directories in a given path.
    Files will not be returned.

    Parameters
    ----------
    path: (str) File path to directory to be searched.

    Returns
    -------
    folder_list: (list[str]) List of subfolder names within given directory.

    """
    folder_list = []
    arr = os.listdir(path)
    for i in arr:
        path_i = f"{path}/{i}"
        if os.path.isdir(path_i) == True:
            folder_list.append(i)
        else:
            continue
    
    return folder_list


    def next_folder_num(name, folder_list):
    """
    Searches list of folder names for those containing a specific string.
    If no folder names are found to contain the string and end in an integer, 
    the function returns the integer 0.
    If any folder names are found to contain the string and end in an integer, 
    the function returns the next highest integer.
    
    Parameters
    ----------
    name: (str) The sequence to look for within each folder name.
    folder_list: (list[str]) List of folder names.

    Returns
    -------
    new_folder_num: (int) An integer.

    """
    folder_nums = []
    
    for folder_name in folder_list:
        if name in folder_name:
            end_num = folder_name.rsplit('_', 1)[-1]
            if end_num.isnumeric() == True:
                folder_nums.append(int(end_num))
            else:
                continue
        else:
            continue
    
    # If folder_nums list is empty, return an empty list
    if not folder_nums:
        new_folder_num = 0
    else:
        new_folder_num = max(folder_nums) + 1
    
    return new_folder_num


def create_subfolders(parent_path, subfolder_list):
    """
    Function to create new directory within a given directory path.
    
    Parameters
    ----------
    parent_path: (str) File path of parent directory.
    subfolder_list: (list[str]) List of file names to create within parent directory.
    
    """
    for subfolder in subfolder_list:
        try:
            os.makedirs(os.path.join(parent_path, subfolder), exist_ok = True)
            print("Subdirectory '%s' created successfully" % subfolder)
        except OSError as error:
            print("Subdirectory '%s' can not be created" % subfolder)


def create_pd_dir(experiment_type, yyyymmdd=None):
    """
    Function for creating new directories for PurpleDrop experimental run data.
    
    Parameters
    ----------
    experiment_type: (str) Name of experiment.
    yyyymmdd: (str, optional) Date (in YYYYMMDD format) that the experiment was run.
    
    """
    
    mode = 0o777

    experiment_type = str(experiment_type).replace(" ","_")
    
    # Parent Directories 
    parent_dir = f"/Users/Rory/OneDrive - UW/Nivala_Lab/Data/PurpleDrop_Runs/{experiment_type}"
    if os.path.isdir(parent_dir) == False:
        print("Attempting to create directory with path '%s'" % parent_dir)
        try:
            os.makedirs(parent_dir, exist_ok = True)
            print("Directory '%s' created successfully" % experiment_type)
        except OSError as error:
            print("Directory '%s' can not be created" % experiment_type)
    else:
        pass
        
    # Scan all existing leaf
    dir_list = list_all_dir(path=parent_dir)
    
    # Find todays date
    if yyyymmdd is None:
        today = date.today()
        today = str(today).replace('-', '')
        experiment_run = experiment_type + '_' + today
    else:
        experiment_run = experiment_type + '_' + str(date)
    
    # Generate new run name based on most recent run directory found
    new_folder_num = next_folder_num(name=experiment_run, folder_list=dir_list)
    experiment_run = experiment_run + '_' + str(new_folder_num)
    
    # Create the directory
    create_subfolders(parent_path=parent_dir, subfolder_list=[experiment_run])
    
    # Create subdirectories
    new_dir = f"{parent_dir}/{experiment_run}"
    create_subfolders(parent_path=new_dir, subfolder_list=['log_files', 'visualizations', 'surface_qc'])
    
    # Create visualizations subdirectories
    vis_sub_dir = f"{parent_dir}/{experiment_run}/visualizations"
    create_subfolders(parent_path=vis_sub_dir, subfolder_list=['move_time'])