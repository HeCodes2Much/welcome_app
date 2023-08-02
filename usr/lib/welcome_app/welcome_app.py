import gi
import json
import warnings
import os
from xdg import BaseDirectory

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango

class WelcomeApp(Gtk.Window):
    def __init__(self, app_data, padding):
        super(WelcomeApp, self).__init__(title=app_data["app_name"])
        # Set the window type to DIALOG for a floatable window
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)

        self.set_default_size(800, 500)
        self.set_resizable(False)  # Disable window resizing

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_start(padding)
        vbox.set_margin_end(padding)
        vbox.set_margin_top(padding)
        vbox.set_margin_bottom(padding)
        self.add(vbox)

        scrolled_window_1 = Gtk.ScrolledWindow()
        scrolled_window_1.set_hexpand(True)
        scrolled_window_1.set_vexpand(True)
        vbox.pack_start(scrolled_window_1, True, True, 0)

        text_view_1 = Gtk.TextView()
        text_buffer_1 = text_view_1.get_buffer()
        text_buffer_1.set_text(app_data["welcome_message"]["text"])

        # Center align the text
        text_view_1.set_wrap_mode(Gtk.WrapMode.WORD)
        text_view_1.set_justification(Gtk.Justification.CENTER)
        text_view_1.set_editable(False)
        text_view_1.set_cursor_visible(False)

        # Apply custom font size for welcome_message
        self.apply_custom_font(text_view_1, app_data["welcome_message"]["font_size"])

        scrolled_window_1.add(text_view_1)

        scrolled_window_2 = Gtk.ScrolledWindow()
        scrolled_window_2.set_hexpand(True)
        scrolled_window_2.set_vexpand(True)
        vbox.pack_start(scrolled_window_2, True, True, 0)

        text_view_2 = Gtk.TextView()
        text_buffer_2 = text_view_2.get_buffer()
        text_buffer_2.set_text(app_data["welcome_description"]["text"])

        # Prevent text editing
        text_view_2.set_editable(False)
        text_view_2.set_cursor_visible(False)

        # Apply custom font size for welcome_description
        self.apply_custom_font(text_view_2, app_data["welcome_description"]["font_size"])

        scrolled_window_2.add(text_view_2)

        for layer_data in app_data["layers"]:
            button_box = Gtk.Box(spacing=10)
            for button_data in layer_data["buttons"]:
                button = Gtk.Button(label=button_data["label"])
                button.connect("clicked", self.on_button_clicked, button_data["command"])
                button_box.pack_start(button, True, True, 0)
            vbox.pack_start(button_box, True, True, 0)

        # Create the separator at the bottom
        separator_bottom = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(separator_bottom, False, False, 0)

        # Create the footer box
        footer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        vbox.pack_start(footer_box, False, False, 0)

        # Add the toggle switch to the footer box (right-aligned)
        self.toggle_switch = Gtk.ToggleButton()
        self.toggle_switch.connect("toggled", self.on_toggle_button_toggled)
        footer_box.pack_end(self.toggle_switch, False, False, 0)

        # Add a label next to the toggle switch (right-aligned)
        toggle_label = Gtk.Label(label="Toggle Label")
        footer_box.pack_end(toggle_label, False, False, 0)

        # Create a revealer to move the footer_box side to side
        self.revealer = Gtk.Revealer()
        self.revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_RIGHT)
        self.revealer.set_transition_duration(500)  # 0.5 second transition
        vbox.pack_start(self.revealer, False, False, 0)

        # Check if autostart entry exists and set the toggle button state
        self.check_autostart()

        self.connect("delete-event", Gtk.main_quit)
        self.connect("key-press-event", self.on_key_press)
        self.show_all()

    def apply_custom_font(self, text_view, font_size):
        font_desc = Pango.FontDescription("Sans " + str(font_size))
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            text_view.override_font(font_desc)

    def on_button_clicked(self, button, command):
        print(command)

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()

    def on_toggle_button_toggled(self, button):
        if button.get_active():
            # Change the background color to green when toggled ON
            self.set_toggle_color("green")
            # Move the footer_box to the right when toggled ON
            self.move_footer_box(True)
            # Add autostart entry when toggled ON
            self.add_autostart()
            print("Toggle button is ON")
        else:
            # Change the background color to red when toggled OFF
            self.set_toggle_color("red")
            # Move the footer_box to the left when toggled OFF
            self.move_footer_box(False)
            # Remove autostart entry when toggled OFF
            self.remove_autostart()
            print("Toggle button is OFF")

    def set_toggle_color(self, color_name):
        # Set the background color of the toggle switch
        style_context = self.toggle_switch.get_style_context()
        color = Gdk.color_parse(color_name)
        rgba = Gdk.RGBA.from_color(color)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            self.toggle_switch.override_background_color(Gtk.StateFlags.NORMAL, rgba)

    def move_footer_box(self, move_right):
        # Move the footer_box using the revealer
        if move_right:
            self.revealer.set_reveal_child(True)
        else:
            self.revealer.set_reveal_child(False)

    def check_autostart(self):
        autostart_file_path = os.path.join(BaseDirectory.xdg_config_home, "autostart", "welcome_app.desktop")
        self.toggle_switch.set_active(os.path.exists(autostart_file_path))
        # Set the initial state and color of the toggle switch
        self.set_toggle_color("green" if self.toggle_switch.get_active() else "red")

    def add_autostart(self):
        # Get the autostart directory path
        autostart_dir = os.path.join(BaseDirectory.xdg_config_home, "autostart")

        # Create the autostart entry file
        autostart_file_path = os.path.join(autostart_dir, "welcome_app.desktop")

        # Modify this line with the actual path to your Python script
        app_script_path = "/usr/bin/welcome_app"

        autostart_entry = f"""[Desktop Entry]
Name=WelcomeApp
Exec={app_script_path}
Type=Application
X-GNOME-Autostart-enabled=true
"""

        # Write the autostart entry to the file
        with open(autostart_file_path, "w") as autostart_file:
            autostart_file.write(autostart_entry)

        # Set executable permissions (octal value 755) on the desktop file
        os.chmod(autostart_file_path, 0o755)

    def remove_autostart(self):
        # Get the autostart directory path
        autostart_dir = os.path.join(BaseDirectory.xdg_config_home, "autostart")

        # Remove the autostart entry file if it exists
        autostart_file_path = os.path.join(autostart_dir, "welcome_app.desktop")
        if os.path.exists(autostart_file_path):
            os.remove(autostart_file_path)

if __name__ == "__main__":
    with open("/usr/lib/welcome_app/welcome_data.json", "r") as file:
        app_data = json.load(file)

    padding = app_data["padding"]
    WelcomeApp(app_data, padding)
    Gtk.main()
