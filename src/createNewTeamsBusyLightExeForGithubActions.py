import os
import shutil
import subprocess
import sys
import tempfile

def check_python_version():
    if sys.version_info < (3, 6):
        raise Exception("This script requires Python 3.6 or higher. Please update your Python version.")

def join_path(*args):
    return os.path.join(*args)

def remove_old_dist_folder(output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
        print("-- Removed old dist folder --")

def update_check_pip_manager(venv_path, pip_requirements):
    try:
        activate_script = join_path(venv_path, 'Scripts', 'activate') if os.name == 'nt' else join_path(venv_path, 'bin', 'activate')
        if os.name == 'nt':
            subprocess.run(f"{activate_script} && python -m pip install --upgrade pip && pip install -r {pip_requirements}", shell=True, check=True)
        else:
            subprocess.run(f"source {activate_script} && python -m pip install --upgrade pip && pip install -r {pip_requirements}", shell=True, check=True)
        print("-- Updated/Checked PIP Manager --")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while handling Update/Check PIP Manager: {e}")
        sys.exit(1)

def create_version_file(create_versionfile_script):
    try:
        subprocess.run(f"python {create_versionfile_script}", shell=True, check=True)
        print("-- Created Version File --")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while creating version file: {e}")
        sys.exit(1)

def start_pyinstaller(pyinstaller_path, teams_py, icon_file, version_file, output_folder):
    try:
        subprocess.run(f"{pyinstaller_path} {teams_py} --onefile --icon={icon_file} --version-file={version_file} --distpath {output_folder} --clean --windowed", shell=True, check=True)
        print("-- Started PyInstaller --")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while starting PyInstaller: {e}")
        sys.exit(1)

def copy_necessary_files(necessary_files, output_folder):
    for file in necessary_files:
        shutil.copy(file, output_folder)
    print("-- Copied necessary files for execution --")

def create_static_zip_file(output_folder, zip_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_zip_path = join_path(temp_dir, "MS_Teams_Busy_Light")
        shutil.make_archive(temp_zip_path, 'zip', output_folder)
        shutil.move(f"{temp_zip_path}.zip", zip_path)
    print("Finished creating new MS_Teams_Busy_Light.zip file")

def main():
    check_python_version()

    current_dir = os.getcwd()
    output_folder = join_path(current_dir, "dist")
    venv_path = join_path(current_dir, ".venv")
    pyinstaller_path = join_path(venv_path, 'Scripts', 'pyinstaller.exe') if os.name == 'nt' else join_path(venv_path, 'bin', 'pyinstaller')
    teams_py = join_path(current_dir, "src", "MS_Teams_Busy_Light.py")
    create_versionfile_script = join_path(current_dir, "src", "create_versionfile.py")
    pip_requirements = join_path(current_dir, "requirements.txt")
    icon_file = join_path(current_dir, "images", "traffic_light.ico")
    version_file = join_path(current_dir, "TeamsVersionFile.txt")
    necessary_files = ['README.md', 'LICENSE', 'MS_Teams_Settings.ini']
    zip_path = join_path(current_dir, "dist", "MS_Teams_Busy_Light.zip")

    print("-- Starting to create MS Teams Busy Light executable --")
    remove_old_dist_folder(output_folder)
    update_check_pip_manager(venv_path, pip_requirements)
    create_version_file(create_versionfile_script)
    start_pyinstaller(pyinstaller_path, teams_py, icon_file, version_file, output_folder)
    copy_necessary_files(necessary_files, output_folder)
    create_static_zip_file(output_folder,zip_path)

if __name__ == "__main__":
    main()