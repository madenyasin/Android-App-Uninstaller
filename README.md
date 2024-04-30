# Android App Uninstaller using ADB (no-root)

This project provides a user-friendly form application developed using the Python programming language and the Tkinter library. The application's primary purpose is to facilitate the removal of system applications on Android devices using the Android Debug Bridge (ADB). It allows users to uninstall applications like Google's pre-installed apps (e.g., YouTube) and manufacturer-specific apps that are typically not removable through normal means on the device.

## Getting Started

- By using this application, you accept the risk of potential malfunctions or issues occurring on your Android device.
  
Follow these steps to get the project up and running on your local machine.

### Prerequisites

- Python (3 or higher)
- Debian-based distributions: Install the required package and library by running the following commands:

```bash
sudo apt-get update
sudo apt install python3-pip
sudo apt-get install python3-tk
```

- Enable **USB debugging** from your phone's settings.
- **Grant permission** for USB debugging when prompted.

### Installation

1. Clone the repository to your local machine using the following command:

```bash
  git clone https://github.com/madenyasin/Android-App-Uninstaller.git
```

2. Navigate to the project folder:

```bash
  cd Android-App-Uninstaller
```

3. Install the required libraries listed in the `requirements.txt` file using the following command:\
   
**Windows:**
```bash
  pip install -r requirements.txt
```
**Linux, MacOS:**
```bash
  pip3 install -r requirements.txt
```

## Usage

1. Connect your Android phone to the computer. (USB debugging must be enabled, and permission for USB debugging should be granted.)

2. Run the application by executing the following command:\
   
**Windows:**
```bash
  python project.py
```
**Linux, MacOS:**
```bash
  python3 project.py
```
3. Select your phone from the list first.

4. The package names of the installed apps on your phone will be listed in the left-hand side list. 

5. Select the package name of the app you want to remove from the list, then press the 'Uninstall Selected App' button.

6. The application will use ADB commands to uninstall the selected apps from your Android device.

## Log
When an application is uninstalled, information about the uninstalled app is recorded in a '`log.json`' file. (Simultaneously, the information is also stored in a database named '`log_database.db`'.)
  
## Notes

- Be cautious while uninstalling system applications, as removing certain apps can affect the functionality of your device. Only uninstall apps that you are sure about.
 
- If removing any application results in your phone's functionality being impaired, either reinstall that application or perform a factory reset on your phone. (A hard reset may also resolve your issue.)

## License

This project is licensed under the [MIT License](LICENSE).
