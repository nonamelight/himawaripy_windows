import threading
import sys

def open_settings_gui(current_config, on_save_callback, on_preview_callback):
    import tkinter as tk
    from tkinter import messagebox
    
    root = tk.Tk()
    root.title("HimawariPy Settings")
    root.geometry("300x380")
    
    tk.Label(root, text="Update Interval (minutes):").pack(pady=(15, 5))
    interval_var = tk.IntVar(value=current_config.get("interval", 10))
    tk.Entry(root, textvariable=interval_var).pack()
    
    tk.Label(root, text="Earth Scale (%):").pack(pady=(15, 5))
    scale_var = tk.IntVar(value=current_config.get("scale", 100))
    tk.Entry(root, textvariable=scale_var).pack()
    
    tk.Label(root, text="Time Travel (Past Hours):").pack(pady=(15, 5))
    history_var = tk.DoubleVar(value=current_config.get("history_offset", 0) / 60.0)
    
    def trigger_preview():
        preview_config = {
            "interval": interval_var.get(),
            "scale": scale_var.get(),
            "history_offset": int(history_var.get() * 60)
        }
        on_preview_callback(preview_config)

    def on_slider_release(event):
        trigger_preview()
        
    slider = tk.Scale(root, from_=0, to=24, orient=tk.HORIZONTAL, variable=history_var, resolution=0.5)
    slider.bind("<ButtonRelease-1>", on_slider_release)
    slider.pack()
    
    startup_var = tk.BooleanVar(value=current_config.get("run_at_startup", True))
    tk.Checkbutton(root, text="Run at Windows Startup", variable=startup_var).pack(pady=(10, 5))
    
    def save_and_close():
        try:
            interval = interval_var.get()
            scale = scale_var.get()
            history = int(history_var.get() * 60)
            if interval < 1 or scale < 10 or scale > 200:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid values. Please enter valid numbers.")
            return
            
        new_config = {
            "interval": interval,
            "scale": scale,
            "history_offset": history,
            "run_at_startup": startup_var.get()
        }
        on_save_callback(new_config)
        root.destroy()
        
    tk.Button(root, text="Save & Apply", command=save_and_close).pack(pady=15)
    
    import webbrowser
    link_frame = tk.Frame(root)
    link_frame.pack(side=tk.BOTTOM, pady=(0, 15))
    
    tk.Label(link_frame, text="Developed by gandalp", font=("Arial", 8)).pack(side=tk.TOP)
    tk.Label(link_frame, text="nonamelight1@naver.com", font=("Arial", 8)).pack(side=tk.TOP)
    
    url_label = tk.Label(link_frame, text="GitHub Repository", font=("Arial", 8, "underline"), fg="blue", cursor="hand2")
    url_label.pack(side=tk.TOP)
    url_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/nonamelight/himawaripy_windows"))
    
    root.eval('tk::PlaceWindow . center')
    
    # Bring window to front
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    root.mainloop()

def create_tray_icon(on_update, on_settings, on_quit):
    try:
        import pystray
        import PIL.ImageDraw
        from PIL import Image
    except ImportError:
        sys.exit("Please install 'pystray' and 'pillow' to use the tray mode.")

    # Generate a simple icon for the tray
    icon_image = Image.new("RGB", (64, 64), color=(0, 0, 0))
    d = PIL.ImageDraw.Draw(icon_image)
    d.ellipse((8, 8, 56, 56), fill=(73, 109, 137))

    menu = pystray.Menu(
        pystray.MenuItem("Update Now", on_update),
        pystray.MenuItem("Settings", on_settings),
        pystray.MenuItem("Quit", on_quit)
    )

    icon = pystray.Icon("himawaripy", icon_image, "himawaripy", menu)
    return icon
