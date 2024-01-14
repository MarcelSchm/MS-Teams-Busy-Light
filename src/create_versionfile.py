import pyinstaller_versionfile, datetime, os, sys
#from src.utils import VERSION_CONFIG_FILE, ConfigurationVersionFileSections, ConfigurationVersionFileVersionOptions, ConfigurationVersionFileDataOptions, ConfigurationVersionFileOutputOptions
versionNumber = "1.1.0" # Version scheme: major.minor.patch


def createVersionFile():
    try: 
        
        pyinstaller_versionfile.create_versionfile(
            output_file= "TeamsVersionFile.txt",
            version=versionNumber,
            company_name= "https://github.com/MarcelSchm",
            file_description="Reads MS Teams Log File for Presence Status and sends cmds via COM Port to busy light.",
            internal_name="MS-Teams-Busy-Light.exe",
            legal_copyright="Copyright © "  
                            + str(datetime.date.today().year) + ", "
                            + "gpl-3.0",
            original_filename="MS-Teams-Busy-Light.exe",
            product_name="MS Teams Presence Status Busy Light"
        )
    except Exception as e:
        print("An exception happend: " + str(e))
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(createVersionFile())
