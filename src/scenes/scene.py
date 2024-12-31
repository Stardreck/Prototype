from pygame import Surface

from managers.view_manager import ViewManager
from views.view import View


class Scene(View):
    def __init__(self, screen: Surface, view_manager: ViewManager):
        super().__init__(screen, view_manager)