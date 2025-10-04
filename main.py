import sys
import os
import shutil
import traceback
import atexit
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QStandardPaths
from generator import PasswordGenerator

def get_app_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def get_resource_path(relative_path):
    base_path = get_app_directory()
    return os.path.join(base_path, relative_path)

def clear_pycache():
    print("Looking for Python cache folders...")
    pycache_found = False
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                print(f"Cleared cache: {pycache_path}")
                pycache_found = True
            except Exception as e:
                print(f"Couldn't clear {pycache_path}: {e}")
    
    if not pycache_found:
        print("No cache folders found")

def clear_pyqt_cache():
    print("Cleaning up PyQt5 temporary files...")
    cache_locations = [
        Path.home() / '.cache' / 'PasswordGenerator',
        Path.home() / '.local' / 'share' / 'PasswordGenerator',
    ]
    
    try:
        cache_locations.append(Path(QStandardPaths.writableLocation(QStandardPaths.CacheLocation)))
        cache_locations.append(Path(QStandardPaths.writableLocation(QStandardPaths.DataLocation)))
    except Exception:
        pass
    
    cache_cleared = False
    for cache_dir in cache_locations:
        if cache_dir.exists():
            try:
                shutil.rmtree(cache_dir)
                print(f"Removed temporary files: {cache_dir}")
                cache_cleared = True
            except Exception as e:
                print(f"Couldn't remove {cache_dir}: {e}")
    
    if not cache_cleared:
        print("No temporary files to clean up")

def cleanup_on_exit():
    print("\n" + "="*50)
    print("Cleaning up before exit...")
    clear_pycache()
    clear_pyqt_cache()
    print("Cleanup finished!")
    print("="*50)

def set_custom_icon(app, icon_path):
    if os.path.exists(icon_path):
        icon = QIcon(icon_path)
        app.setWindowIcon(icon)
        print(f"Custom icon loaded: {icon_path}")
        return True
    else:
        print(f"Icon file not found: {icon_path}")
        return False

def main():
    try:
        print("Starting Password Generator...")
        clear_pyqt_cache()
        
        app = QApplication(sys.argv)
        
        atexit.register(cleanup_on_exit)
        
        # Set basic app information
        app.setApplicationName("Password Generator")
        app.setApplicationVersion("1.0")
        app.setOrganizationName("PasswordGenerator")
        
        # Try to find and set the app icon
        app_dir = get_app_directory()
        icon_path = os.path.join(app_dir, "private-key-generator.png")
        
        if not set_custom_icon(app, icon_path):
            # If the main icon isn't found, try the resource path
            resource_icon_path = get_resource_path("private-key-generator.png")
            if not set_custom_icon(app, resource_icon_path):
                print("Using default system icon")
        
        window = PasswordGenerator()

        if os.path.exists(icon_path):
            window.setWindowIcon(QIcon(icon_path))
        else:
            resource_icon_path = get_resource_path("private-key-generator.png")
            if os.path.exists(resource_icon_path):
                window.setWindowIcon(QIcon(resource_icon_path))
        
        window.show()
        
        print("Application ready!")
        
        # Start the application
        exit_code = app.exec_()
        
        return exit_code
        
    except Exception as e:
        print(f"Failed to start application: {e}")
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)