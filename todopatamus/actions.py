from gi.repository import Gtk, Gio, Adw, GLib

from todopatamus.services.todo_service import TodoService


class Actions:
    app: Gtk.Application = None
    todo_service: TodoService = None

    def __init__(self, app: Gtk.Application):
        self.app = app
        self.todo_service = self.app.get_property('todo_service')

        self.create_action('quit', lambda *_: self.app.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('toggle-complete', self.on_toggle_completed_action, args=GLib.VariantType.new('(sb)'))

    def create_action(self, name, callback, shortcuts=None, args: GLib.VariantType = None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.app.add_action(action)
        if shortcuts:
            self.app.set_accels_for_action(f"app.{name}", shortcuts)

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.app.props.active_window,
                                application_name='todopatamus',
                                application_icon='com.tenderowl.todopatamus',
                                developer_name='Andrey Maksimov',
                                version='0.1.0',
                                developers=['Andrey Maksimov'],
                                copyright='© 2024 Andrey Maksimov')
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def on_toggle_completed_action(self, widget, *args):
        print('toggle_completed action activated')
        print(args)
