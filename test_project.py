from project import get_OS, get_adb_folder, run_command
import os


def test_get_OS():
    assert get_OS() in ["windows", "linux", "darwin"]


def test_get_adb_folder():
    assert get_adb_folder() == os.path.join(
        os.getcwd(), f"adb/{get_OS()}/platform-tools"
    ).replace("\\", "/")


def test_run_command():
    system_os = get_OS()
    folder_path = get_adb_folder()

    if system_os == "windows:":
        command = "dir"  # for windows
        output = run_command(folder_path, command)
        print(output)
        assert "adb.exe".replace("\n", "") in output
        assert "AdbWinApi.dll" in output

        invalid_command = "ls"  # It doesn't work in windows' terminal.

        output = run_command(folder_path, invalid_command)

        assert "Error message" in output

    elif system_os == "linux":
        folder_path = os.path.join(folder_path, "lib64")
        command = "ls"
        output = run_command(folder_path, command)

        assert "libc++.so" in output

    elif system_os == "darwin":
        folder_path = os.path.join(folder_path, "lib64")
        command = "ls"
        output = run_command(folder_path, command)

        assert "libc++.dylib" in output
