"""
NOM : GULZAR
PRÉNOM : ZIA
SECTION : B1-INFO
MATRICULE : 000595624
"""
class Pixel:
    """
        Class representing a single pixel in an image.

        Attributes:
            _r (int): Red component of the pixel.
            _g (int): Green component of the pixel.
            _b (int): Blue component of the pixel.

        Methods:
            __init__: Initializes the Pixel object.
        """
    def __init__(self, RED, GREEN, BLUE):
        """
               Initializes a Pixel object with the specified RGB values.

               Args:
                   RED (int): Value of the red component of the pixel.
                   GREEN (int): Value of the green component of the pixel.
                   BLUE (int): Value of the blue component of the pixel.

               Raises:
                   ValueError: If any of the RGB values is negative.
               """
        if RED < 0 or GREEN < 0 or BLUE < 0:
            raise ValueError("Les valeurs RGB ne peuvent pas être négatives")
        self._r = RED
        self._g = GREEN
        self._b = BLUE

    @property
    def r(self):
        """
                Returns the value of the red component of the pixel.

                Returns:
                    int: Value of the red component.
                """
        return self._r

    @property
    def v(self):
        """
                Returns the value of the green component of the pixel.

                Returns:
                    int: Value of the green component.
                """
        return self._g

    @property
    def b(self):
        """
                Returns the value of the blue component of the pixel.

                Returns:
                    int: Value of the blue component.
                """
        return self._b

    def __eq__(self, other):
        """
                Checks if two pixels are equal.

                Args:
                    other (Pixel): The other pixel to compare.

                Returns:
                    bool: True if the pixels are equal, False otherwise.
                """
        if not isinstance(other, Pixel):
            return False
        return (self._r, self._g, self._b) == (other._r, other._g, other._b)











