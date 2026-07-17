import threading
import os
import time
import sys
from himawaripy.config import load_config, save_config, set_startup
from himawaripy.core import thread_main
from himawaripy.view import open_settings_gui, create_tray_icon

def run_tray_mode(args):
    try:
        import schedule
    except ImportError:
        sys.exit("Please install 'schedule' to use the tray mode.")

    update_lock = threading.Lock()

    def job():
        with update_lock:
            print("Starting scheduled background update...")
            try:
                thread_main(args)
                print("Update completed.")
            except SystemExit as e:
                print("Job exited:", e)
            except Exception as e:
                print("Error during update:", e)

    def on_update(icon, item):
        threading.Thread(target=job, daemon=True).start()

    def on_quit(icon, item):
        icon.stop()
        os._exit(0)
        
    def on_settings(icon, item):
        def on_save(new_config):
            save_config(new_config)
            set_startup(new_config.get("run_at_startup", True))
            schedule.clear()
            schedule.every(new_config["interval"]).minutes.do(job)
            on_update(icon, None)
            
        def on_preview(preview_config):
            def do_preview():
                with update_lock:
                    try:
                        thread_main(args, custom_config=preview_config)
                    except SystemExit:
                        pass
                    except Exception as e:
                        print("Preview error:", e)
            threading.Thread(target=do_preview, daemon=True).start()
            
        current_config = load_config()
        threading.Thread(target=open_settings_gui, args=(current_config, on_save, on_preview), daemon=True).start()

    icon = create_tray_icon(on_update, on_settings, on_quit)

    current_config = load_config()
    set_startup(current_config.get("run_at_startup", True))
    
    schedule.every(current_config["interval"]).minutes.do(job)

    def scheduler_loop():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=scheduler_loop, daemon=True).start()
    on_update(icon, None)

    print("Running in Tray Mode. Check your system tray.")
    icon.run()
