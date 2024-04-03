from typing import Tuple

from gi.repository import Gtk, Gio, Adw, GLib
from loguru import logger

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
        self.create_action('category-activate', self.on_category_activate_action, args=GLib.VariantType.new('s'))

    def create_action(self, name, callback, shortcuts=None, args: GLib.VariantType = None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            args: an optional GLib.VariantType
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, args)
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
        logger.info('app.preferences action activated')

    def on_toggle_completed_action(self, _widget, values: Tuple[str, bool]):
        todo_id = values[0]
        completed = values[1]
        if not todo_id or completed is None:
            logger.warning(f'Invalid toggle_completed action values: {values}')
            return

        logger.debug("toggle_completed action: todo_id={todo_id}, completed={completed}",
                     todo_id=todo_id,
                     completed=completed)
        self.todo_service.toggle_completed(todo_id, completed)

    def on_category_activate_action(self, widget, category_name: GLib.Variant):
        logger.debug('on_category_activated {}', category_name)
        self.todo_service.set_current_category(category_name.get_string())
