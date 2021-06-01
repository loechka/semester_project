"""Module contains GameObject class."""

from pygame.rect import Rect


class GameObject:
    """
    GameObject class based on pygame.Rect.

    This is a simple square object with bounds properties,
    which also has speed and can move.
    """

    def __init__(self, x: int, y: int, w: int, h: int, speed: tuple = (0, 0)):
        """
        Init GameObject with certain features.

        Keyword arguments:
        :param x: left coordinate
        :param y: top coordinate
        :param w: object width
        :param h: object height
        :params speed: object speed
        """
        self.bounds = Rect(x, y, w, h)
        self.speed = speed

    @property
    def left(self):
        """Return left bound."""
        return self.bounds.left

    @property
    def right(self):
        """Return right bound."""
        return self.bounds.right

    @property
    def top(self):
        """Return top bound."""
        return self.bounds.top

    @property
    def bottom(self):
        """Return bottom bound."""
        return self.bounds.bottom

    @property
    def width(self):
        """Return width."""
        return self.bounds.width

    @property
    def height(self):
        """Return height."""
        return self.bounds.height

    @property
    def center(self):
        """Return rectangle center."""
        return self.bounds.center

    @property
    def centerx(self):
        """Return rectangle horisontal center."""
        return self.bounds.centerx

    @property
    def centery(self):
        """Return rectangle vertical center."""
        return self.bounds.centery

    def draw(self, surface):
        """
        Draw object.
        
        Needs to be updated in child classes
        """
        pass

    def move(self, dx: int, dy:int):
        """Move object.

        Keyword arguments:
        :param dx: horisontal step
        :param dy: vertical step
        """
        self.bounds = self.bounds.move(dx, dy)

    def update(self):
        """Update object position."""
        if self.speed == [0, 0]:
            return

        self.move(*self.speed)
