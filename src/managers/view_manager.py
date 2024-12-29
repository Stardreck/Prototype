from pygame import Surface
from managers.manager import Manager

class ViewManager(Manager):
    def __init__(self, screen: Surface):
        super().__init__()
        self.screen: Surface = screen
        self.current_view = None
        self.view_registry = {}

    def register_view(self, view_name: str, view_class):
        """
        Registers a view class with a unique name.
        :param view_name: Unique name of the view
        :param view_class: Class of the view
        """
        self.view_registry[view_name] = view_class

    def set_view(self, view_name: str, *args, **kwargs):
        """
        Switches to the view registered with the specified name.
        :param view_name: The name of the view
        """
        if view_name not in self.view_registry:
            raise ValueError(f"View '{view_name}' is not registered.")
        view_class = self.view_registry[view_name]
        self.current_view = view_class(self.screen, self, *args, **kwargs)

    def render(self):
        """
        Runs the current view until it is no longer visible.
        """
        while self.current_view and self.current_view.is_visible:
            self.current_view.render()
