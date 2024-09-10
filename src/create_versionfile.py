import pyinstaller_versionfile
import datetime
import os
import sys
import configparser


versionNumber = "1.3.0" # Version scheme: major.minor.patch


def createVersionFile():
    try: 
        versionConfig = configparser.ConfigParser()
        versionConfig.read(os.path.dirname(__file__) + os.path.sep + ".." + os.path.sep + "version.conf")

        pyinstaller_versionfile.create_versionfile(
            output_file= versionConfig["Output"]["VersionFile"],
            version=versionConfig["Version"]["Number"],
            company_name= versionConfig["Data"]["CompanyName"],
            file_description=versionConfig["Data"]["Description"],
            internal_name=versionConfig["Data"]["InternalName"],
            legal_copyright="Copyright © "  
                            + str(datetime.date.today().year) + ", "
                            + "gpl-3.0",
            original_filename=versionConfig["Data"]["OriginalFilename"],
            product_name=versionConfig["Data"]["ProductName"]
        )
    except Exception as e:
        print("An exception happend: " + str(e))
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(createVersionFile())
