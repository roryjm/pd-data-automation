import click
import os
import subprocess
import shutil
import sys
from datetime import date
from time import sleep

subprocess.call("surface_test_misl_v4.1.py", shell=True)


def query_yes_no(question, default="yes"):
    """
    Ask a yes/no question via input() and return their answer.

    Parameters
    ----------
    question: (str) A string that is presented to the user.
    default: (str) The presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    Returns
    -------
        A boolean value, with True for "yes" or False for "no".
    """

    valid = {"yes": True, "ye": True, "y": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def run_qc(save_dir, run_num):
	# Prompt user to prepare PurpleDrop
	print("Prepare PurpleDrop for quality control run")
	# Wait two seconds
	sleep(2)
	for i in range(3):
		today = date.today()
        today = str(today).replace('-', '')
        image_name = 'sweep_' + today + '_' + str(run_num) + '-' + str(i+1)
		run_qc(save_dir, image_name)
		# Ask if user is ready
		start_question = query_yes_no(f"Ready to start surface quality control run {str(i+1)} of 3?")
		if start_question == True:
			# Define path to python script
			file_path = '~/Desktop/PythonScripts/quality_control/surface_test_misl_v4.1.py'
			# Notify user that script will be executed
	    	print("Starting quality control run")
	    	# Execute script
	    	subprocess.call(f"python3 {file_path} sweep.log", shell=False)
	    	# Ask user if heatmap should be generated
	    	heatmap_question = query_yes_no('Ready to generate heatmap?')
	    	if heatmap_question == True:
	    		print("Generating heatmap from log file")
	    		subprocess.call(f"python3 {file_path} --plot sweep.log", shell=False)
	    		# Move and rename heatmap png
	    		image_path = os.path.join(file_path, 'sweep.png')
	    		save_dir = f"{save_dir}/{image_name}"
	    		shutil.move(image_path, save_dir)
	    	else:
	    		print("Terminating without generating heatmap")
	    		break

		else:
	    	print('Terminating')
	    	break

@click.command()
@click.argument('save_dir', required=False)
@click.argument('run_num', required=False)
def main(save_dir=None, run_num=None):
    
    if save_dir is None:
    	print("You must provide a save directory path")
    	sys.exit(1)

    if run_num is None:
        print("You must provide a run number")
        sys.exit(1)

    run_qc(save_dir, run_num)


if __name__ == '__main__':
    main()
