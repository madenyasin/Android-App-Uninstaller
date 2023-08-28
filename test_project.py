from project import get_OS, get_adb_folder, run_command

# The tests were run on a Windows device.

def test_get_OS():
    assert get_OS() == "windows"

def test_get_adb_folder():
    assert get_adb_folder() == "C:\\Users\\ymaden\\Desktop\\app-remover-with-adb\\adb\\windows\\platform-tools"

def test_run_command():
    folder_path = get_adb_folder()
    command = "dir" # for windows
    output = run_command(folder_path, command)

    assert "adb.exe".replace("\n", "") in output
    assert "AdbWinApi.dll" in output

    invalid_command = "ls" # It doesn't work in windows' terminal.

    output = run_command(folder_path, invalid_command)
    
    assert "Error message" in output