"""
NOM : GULZAR
PRÉNOM : ZIA
SECTION : B1-INFO
MATRICULE : 000595624
"""
from pixel import Pixel
class Image:
    """
    Class representing an image formed by all the pixel objects.

    Attributes:
        self.w (int): Width of the image.
        self.h (int): Height of the image.
        self.p (list): List of pixel objects representing the image.

    Methods:
        __init__: Initializes the Image object.
        get_width: Returns the width of the image.
        get_height: Returns the height of the image.
        get_pixels: Returns the list of pixels in the image.
        __getitem__: Returns the pixel at a specific position in the image.
    """
    def __init__(self, width:int,height:int,pixels):
        """
                Initializes an Image object with the specified width, height, and a list of pixels.

                Args:
                    width (int): The width of the image.
                    height (int): The height of the image.
                    pixels (list): List of Pixel objects representing the image.

                Raises:
                    IndexError: If the length of the pixel list does not match the expected dimensions.
                    ValueError: If any element in the pixels list is not of type Pixel.
                """
        dimensions = width*height
        self.w = width
        self.h = height
        if len(pixels) != dimensions:
            raise IndexError("the length of the list does not correspond")
        else:
            for pixel in pixels:
                if type(pixel) != Pixel:
                    raise ValueError("does not correspond to the right type")
        self.p = pixels
    def get_width(self):
        """
                Returns the width of the image.

                Returns:
                    int: Width of the image.
                """
        return self.w
    def get_height(self):
        """
                Returns the height of the image.

                Returns:
                    int: Height of the image.
                """
        return self.h
    def get_pixels(self):
        """
               Returns the list of pixels representing the image.

               Returns:
                   list: List of Pixel objects representing the image.
               """
        return self.p
    def __getitem__(self, pos):
        """
                Retrieves the pixel at the specified position in the image.

                Args:
                    pos (tuple): Tuple containing the x and y coordinates of the pixel.

                Returns:
                    Pixel: Pixel object at the specified position.

                Raises:
                    IndexError: If the position is out of bounds.
                """
        dimensions = self.w*self.h
        if pos[0]< 0 or pos[1] > dimensions-1:
           raise IndexError("out of range")
        return self.p[pos[0]%self.w+(pos[1]%self.h)*self.w] #formula to get the index of the pixel
    def __setitem__(self, pos, pix):
        """
                Sets the pixel at the specified position in the image.

                Args:
                    pos (tuple): Tuple containing the x and y coordinates of the pixel.
                    pix (Pixel): Pixel object to set at the specified position.

                Raises:
                    IndexError: If the position is out of bounds.
                """
        dimensions = self.w * self.h
        if pos[0] < 0 or pos[1] > dimensions-1:
            raise IndexError("hors de la liste")
        self.p[pos[0]%self.w+(pos[1]%self.h)*self.w] = pix
    def __eq__(self, other):
        """
                Checks if two images are the same image.

                Args:
                    other (Image): The other image to compare.

                Returns:
                    bool: True if the images are the same, False otherwise.
                """
        if not isinstance(other,Image):
            return False
        return (self.w, self.h, self.p) == (other.w, other.h, other.p)




