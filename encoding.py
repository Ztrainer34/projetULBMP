"""
NOM : GULZAR
PRÉNOM : ZIA
SECTION : B1-INFO
MATRICULE : 000595624
"""
from image import Image
from pixel import Pixel
def conversion(nb):
    """
        Converts an integer into its byte specifically on 2 bytes representation for Encode and Decode

        Args:
            nb (int): Integer value to be converted.

        Returns:
            bytes:  2 bytes representing the integer
        """
    nb = bin(nb)
    binary_bytes = int(nb, 2).to_bytes(2, byteorder='little')
    return binary_bytes


class Encoder:
    """
    Class for encoding ULBMP images , which returns None and writes the encoded data in a file in 4 different
    versions

    Methods:
        __init__: Initializes the Encoder object.
        version4: Encodes the image using version 4 encoding.
        RLE: Performs Run-Length Encoding on the image data.
        version3_depth8: Encodes the image with 8-bit depth using version 3 encoding.
        save_to: Saves the encoded image to a file.
    """
    def __init__(self,img: Image,*args,**kwargs):
        """
                Initializes an Encoder object.

                Args:
                    img (Image): Image object to be encoded.
                    *args: Variable containing the version in which the image will be encoded.
                    **kwargs: variables containing the depth and a bool specifying the RLE

                Raises:
                    Exception: If the specified version is invalid.
                """
        self.i = img
        self.a = args[0] if args else 1 #default format 1
        if self.a > 5:
           raise Exception("Invalid version")
        self.k = kwargs

    def version4(self,i,Encodage,p_prime):
        """
                Encodes pixels using Version 4 algorithm based on the difference with the previous pixel.

                Args:
                    i (int): Index of the pixel we are on.
                    Encodage (bytes): Encoded data.
                    p_prime (Pixel): Previous pixel.

                Returns:
                    bytes: Encoded pixel data.
                """
        Dr = self.i.get_pixels()[i]._r - p_prime._r
        Dg = self.i.get_pixels()[i]._g - p_prime._g
        Db = self.i.get_pixels()[i]._b - p_prime._b
        Delta_green_red = Dg - Dr
        Delta_blue_red = Db - Dr
        Delta_red_green = Dr - Dg
        Delta_blue_green = Db - Dg
        Delta_red_blue = Dr - Db
        Delta_green_blue = Dg - Db
        list_deltargb = []
        temp = 0

        if -2 <= Dr <= 1 and -2 <= Dg <= 1 and -2 <= Db <= 1: #small_diff
            Dr += 2
            Dg += 2
            Db += 2
            list_deltargb.extend((Dr, Dg, Db))
            for i in list_deltargb:
                temp = temp << 2 | i
            concatenated_binary = bin(temp)[2:].zfill(8)
            concatenated_binary = int(concatenated_binary, 2).to_bytes(1)
            return concatenated_binary

        elif -32 <= Dg <= 31 and -8 <= Dr - Dg <= 7 and -8 <= Db - Dg <= 7:  # inter_diff
            Dg += 32
            Delta_red_green += 8
            Delta_blue_green += 8
            list_deltargb.extend((1, Dg, Delta_red_green, Delta_blue_green))
            temp = temp << 1 | list_deltargb[0]
            temp = temp << 6 | list_deltargb[1]
            for i in list_deltargb[2:]:
                temp = temp << 4 | i
            concatenated_binary = bin(temp)[2:].zfill(16)
            concatenated_binary = int(concatenated_binary, 2).to_bytes(2)
            return concatenated_binary

        elif -128 <= Dr <= 127 and -32 <= Dg - Dr <= 31 and -32 <= Db - Dr <= 31: # Big_diff_r
            Dr += 128
            Delta_green_red += 32
            Delta_blue_red += 32
            list_deltargb.extend((8, Dr, Delta_green_red, Delta_blue_red))
            temp = temp << 4 | list_deltargb[0]
            temp = temp << 8 | list_deltargb[1]
            for i in list_deltargb[2:]:
                temp = temp << 6 | i
            concatenated_binary = bin(temp)[2:].zfill(24)
            concatenated_binary = int(concatenated_binary, 2).to_bytes(3)
            return concatenated_binary

        elif -128 <= Dg <= 127 and -32 <= Dr - Dg <= 31 and -32 <= Db - Dg <= 31: # Big_diff_g
            Dg += 128
            Delta_red_green += 32
            Delta_blue_green += 32
            list_deltargb.extend((9, Dg, Delta_red_green, Delta_blue_green))
            temp = temp << 4 | list_deltargb[0]
            temp = temp << 8 | list_deltargb[1]
            for i in list_deltargb[2:]:
                temp = temp << 6 | i
            concatenated_binary = bin(temp)[2:].zfill(24)
            concatenated_binary = int(concatenated_binary, 2).to_bytes(3)
            return concatenated_binary

        elif -128 <= Db <= 127 and -32 <= Dr - Db <= 31 and -32 <= Dg - Db <= 31: #big_diff_b
            Db += 128
            Delta_red_blue += 32
            Delta_green_blue += 32
            list_deltargb.extend((10, Db, Delta_red_blue, Delta_green_blue))
            temp = temp << 4 | list_deltargb[0]
            temp = temp << 8 | list_deltargb[1]
            for i in list_deltargb[2:]:
                temp = temp << 6 | i
            concatenated_binary = bin(temp)[2:].zfill(24)
            concatenated_binary = int(concatenated_binary, 2).to_bytes(3)
            return concatenated_binary

        else: #new_pixel
            list_deltargb.extend(
                (255, self.i.get_pixels()[i]._r, self.i.get_pixels()[i]._g, self.i.get_pixels()[i]._b))
            return bytes(list_deltargb)
    def RLE(self,header,width,height,ok = True,rle = None,depth = None):
        """
               Performs Run-Length Encoding which is based on 4 bytes for a single pixel in which the first
               byte indicates the number of repetitions.

               Args:
                   header (bytes): Header data.
                   width (bytes): Width of the image.
                   height (bytes): Height of the image.
                   ok (bool): Flag indicating RLE usage.
                   rle (bytes): RLE data.
                   depth (bytes): Depth of color.

               Returns:
                   bytes: Encoded image data.
               """
        compteur = 0 #counting the number of pixels
        iter_ = 0 #number of iterations
        temp = 0
        color = []
        while compteur < (self.i.get_width() * self.i.get_height()):

            if temp > 255 - 1: # if temp surpasses 255, resets it to 0 as a single byte can only represent values up to 255
               pixel = self.i.get_pixels()[compteur]
               color.extend((iter_, pixel._r, pixel._g, pixel._b))
               iter_ = 0
               temp = 0

            if compteur == (self.i.get_width() * self.i.get_height()) - 1:
               iter_ += 1
               pixel = self.i.get_pixels()[compteur]
               color.extend((iter_, pixel._r, pixel._g, pixel._b))

            elif self.i.get_pixels()[compteur] == self.i.get_pixels()[compteur + 1]:
               iter_ += 1

            else:
               iter_ += 1
               pixel = self.i.get_pixels()[compteur]
               color.extend((iter_, pixel._r, pixel._g, pixel._b))
               iter_ = 0
            temp += 1
            compteur += 1
        if ok: #if the rle is in format 2
           Encodage = header + width + height + bytes(color)
        else: #if the rle is in format 3
           Encodage = header + width + height + depth + rle + bytes(color)
        return Encodage
    def version3_depth8(self,header,width,height,index_pixel):
        """
                Performs Run-Length Encoding with the depth at 8.

                Args:
                    header (bytes): Header data.
                    width (bytes): Width of the image.
                    height (bytes): Height of the image.
                    index_pixel (list): contains the indexes to the palette

                Returns:
                    bytes: Encoded image data.
                """
        compteur = 0
        iter_ = 0
        temp = 0
        color = []
        while compteur < (self.i.get_width() * self.i.get_height()):

              for i in index_pixel:

                  if temp > 255 - 1:
                     color.extend((iter_,i))
                     iter_ = 0
                     temp = 0

                  if compteur == (self.i.get_width() * self.i.get_height()) - 1:
                     iter_ += 1
                     color.extend((iter_,i))

                  elif self.i.get_pixels()[compteur] == self.i.get_pixels()[compteur + 1]:
                      iter_ += 1

                  else:
                      iter_ += 1
                      color.extend((iter_,i))
                      iter_ = 0
                  temp += 1
                  compteur += 1

        Encodage = header +bytes(color)
        return Encodage

    def save_to(self, path: str):
        """
        Saves the encoded image into a file.
        Args:
            path (str): File path to save the image.
        Returns:
            None
        """
        width = conversion(self.i.get_width())
        height = conversion(self.i.get_height())

        if self.a == 1: #format1
          header = bytes([0x55, 0x4c, 0x42, 0x4d, 0x50, 0x01, 0x0c, 0x00])
          color = []
          for pixel in self.i.get_pixels():
              colors = (pixel._r,pixel._g,pixel._b)
              color.extend(colors)
          Encodage = header + width + height + bytes(color)
          with open(path, 'wb') as f:
              f.write(Encodage)

        if self.a == 2:  #format2
           header = bytes([0x55, 0x4c, 0x42, 0x4d, 0x50, 0x02, 0x0c, 0x00])
           Encodage = Encoder.RLE(self, header, width, height)
           with open(path, 'wb') as f:
                  f.write(Encodage)

        elif self.a == 3:  #format3
            header = bytes([0x55, 0x4c, 0x42, 0x4d, 0x50, 0x03])
            depth = self.k.get("depth") if self.k.get("depth") is not None or self.k.get("depth") > 25 else ValueError("invalid argument") #verifies if there is a missing argument or invalid argument
            rle = self.k.get("rle") if self.k.get("rle") is not None or self.k.get("rle") is not bool  else ValueError("invalid argument")
            if not rle:
               rle_byte = bytes([0])
            else:
               rle_byte = bytes([1])
            pal = [] #contains the pallette with the pixels as objects
            indexage = {} #contains the index to each pixel in the palette
            pallete = [] #palette that containts pixel as RGB (0,0,0)
            index_pixel = [] # contains the indexes used
            if depth <= 8:
               compt = 0
               for pixel in self.i.get_pixels():
                   if pixel not in pal:
                      pal.append(pixel)

               for pixel in pal:
                   indexage[pixel.r] = compt
                   pallete += [pixel._r,pixel._g,pixel._b]
                   compt += 1

               for i in range(len(self.i.get_pixels())):
                   for index in indexage:
                       index_pixel.append(indexage.get(index))
                   if len(index_pixel) == len(self.i.get_pixels()):
                      break

               Encodage = header + width + height + bytes([depth]) + rle_byte+ bytes(pallete)
               Encodage = header + conversion(len(Encodage)+2) + width + height + bytes([depth]) + rle_byte + bytes(pallete)
               temp = 0
               if not rle:
                   for ind in index_pixel:
                       temp = temp | ind
                       temp = temp << depth
                   res = temp << (8 - (len(self.i.get_pixels()) % (8 // depth)) * depth)-1  #the pixels which will be converted to hex
                   Encodage = header + conversion(len(Encodage)) + width + height + bytes([depth]) + rle_byte + bytes(pallete) + bytes([res])
                   with open(path, 'wb') as f:
                       f.write(Encodage)
               else:
                   Encodage = Encoder.version3_depth8(self,Encodage,width,height,index_pixel)
                   with open(path, 'wb') as f:
                       f.write(Encodage)
            elif depth == 24:
               if rle:
                  header = bytes([0x55, 0x4c, 0x42, 0x4d, 0x50, 0x03, 0x0e, 0x00])
                  Encodage = Encoder.RLE(self,header, width, height,False,rle_byte,bytes([depth]))
                  with open(path, 'wb') as f:
                      f.write(Encodage)
               else:
                  header = bytes([0x55, 0x4c, 0x42, 0x4d, 0x50, 0x03, 0x0c, 0x00])
                  color = []
                  for pixel in self.i.get_pixels():
                       colors = (pixel._r, pixel._g, pixel._b)
                       color.extend(colors)
                  Encodage = header + width + height + bytes([depth]) + rle_byte + bytes(color)
                  with open(path, 'wb') as f:
                      f.write(Encodage)

        elif self.a == 4:  #format4
            header = bytes([0x55, 0x4c, 0x42, 0x4d, 0x50, 0x04, 0x0c, 0x00])
            p_prime = Pixel(0, 0, 0)
            Encodage = header + width + height
            i = 0
            while i != len(self.i.get_pixels()):
                  concaneted_binary = Encoder.version4(self, i, Encodage, p_prime)
                  i += 1
                  p_prime = self.i.get_pixels()[i - 1]
                  Encodage += concaneted_binary
            with open(path, 'wb') as f:
                f.write(Encodage)


class Decoder:


   @staticmethod
   def decode_bloc(bloc,p_prime,all_pixel,index):
       """
          Decodes a block of pixels for the 4 version

        Args:
            bloc (str): Type of block.
            p_prime (Pixel): Previous pixel.
            all_pixel : List of all pixels.
            index (int): Current index in the list of pixels.

        Returns:
            Pixel: Decoded pixel.
            int: Updated index.
       """
       if bloc == "new_pixel":
          pix = Pixel(all_pixel[index+1],all_pixel[index+2],all_pixel[index+3])
          index = index + 4
       elif bloc == "small_diff":
           binary_pixel = bin(all_pixel[index])[2:].zfill(8)
           red = p_prime.r + int(binary_pixel[2:4],2)-2
           green = p_prime.v + int(binary_pixel[4:6],2)-2
           blue = p_prime.b + int(binary_pixel[6:8],2)-2
           pix = Pixel(red,green,blue)
           index = index +1
       elif bloc == "inter_diff":
           binary_pixel = bin(all_pixel[index])[2:].zfill(8)
           binary_pixel_2 = bin(all_pixel[index+1])[2:].zfill(8)
           green = p_prime.v + int(binary_pixel[2:],2) - 32
           dr = int(binary_pixel_2[:4],2) + int(binary_pixel[2:],2)
           red = p_prime.r + dr - 8 -32
           db = int(binary_pixel_2[4:],2) + int(binary_pixel[2:],2)
           blue = p_prime.b + db -8 -32
           pix = Pixel(red,green,blue)
           index = index + 2
       elif bloc == "diff_r":
           binary_pixel_1 = bin(all_pixel[index])[2:].zfill(8)
           binary_pixel_2 = bin(all_pixel[index + 1])[2:].zfill(8)
           binary_pixel_3 = bin(all_pixel[index + 2])[2:].zfill(8)
           dr = int(binary_pixel_1[4:] + binary_pixel_2[:4],2)
           red = p_prime.r + dr -128
           dg = int(binary_pixel_2[4:] + binary_pixel_3[:2],2) + dr
           green = p_prime.v + dg -32 -128
           db = int(binary_pixel_3[2:],2)+dr
           blue = p_prime.b + db - 32 -128
           pix = Pixel(red, green, blue)
           index = index + 3
       elif bloc == "diff_g":
           binary_pixel_1 = bin(all_pixel[index])[2:].zfill(8)
           binary_pixel_2 = bin(all_pixel[index + 1])[2:].zfill(8)
           binary_pixel_3 = bin(all_pixel[index + 2])[2:].zfill(8)
           dg = int(binary_pixel_1[4:] + binary_pixel_2[:4],2)
           green = p_prime.v + dg -128
           dr = int(binary_pixel_2[4:] + binary_pixel_3[:2], 2) + dg
           red = p_prime.r + dr -32 -128
           db = int(binary_pixel_3[2:],2)+dg
           blue = p_prime.b + db - 32 -128
           pix = Pixel(red, green, blue)
           index = index + 3
       else:
           binary_pixel_1 = bin(all_pixel[index])[2:].zfill(8)
           binary_pixel_2 = bin(all_pixel[index + 1])[2:].zfill(8)
           binary_pixel_3 = bin(all_pixel[index + 2])[2:].zfill(8)
           db = int(binary_pixel_1[4:] + binary_pixel_2[:4], 2)
           blue = p_prime.b + db -128
           dr = int(binary_pixel_2[4:] + binary_pixel_3[:2], 2) + db
           red = p_prime.r + dr - 32 - 128
           dg = int(binary_pixel_3[2:], 2) + db
           green = p_prime.v + dg - 32 - 128
           pix = Pixel(red, green, blue)
           index = index + 3
       return pix,index
   @staticmethod
   def identify_bloc(byte):
       """
       Identifies the type of block.

        Args:
            byte: Byte representing the block type.

        Returns:
            str: Type of block.
       """
       first = byte >> 6
       if  first == 0:
          return "small_diff"
       elif first == 1:
          return "inter_diff"
       elif first == 3:
          return "new_pixel"
       elif first == 2:
           second = byte >> 4
           if second == 8:
               return "diff_r"
           elif second == 9:
               return "diff_g"
           elif second == 10 :
               return "diff_b"
   @staticmethod
   def create_palette(palette):
       """
       Creates a palette of different pixels from the given data.

        Args:
            palette (list): List of pixel data.

        Returns:
            list: Palette of Pixel objects.
       """
       pal = []
       for i in range(0,len(palette),3):
           pal.append(Pixel(palette[i],palette[i+1],palette[i+2]))
       return pal

   @staticmethod
   def load_from(path: str):
       """
       Loads an image from the specified file path and then returns a image which will be used in Encoder to
       Encode the image.

        Args:
            path (str): File path to the image.

        Returns:
            Image: Loaded image object.

        Raises:
            Exception: If the format is incorrect or insufficient information is provided.
       """
       pixels = []
       with open(path, 'rb') as file:
            lines = file.read()
            ULBMP = lines[0:5]
            version = lines[5:6]
            header = lines[6:8]
            width = int.from_bytes(lines[8:10],byteorder='little')
            height = int.from_bytes(lines[10:12],byteorder='little')

            if version == b'\x01':
               for i in range(0,len(lines[12:-1]),3):
                   pixel = Pixel(lines[12+i],lines[12+i+1],lines[12+i+2])
                   pixels.append(pixel)

            elif version == b'\x02':
                 my_pixels = list(lines[12:])
                 step = 4
                 for i in range(0, len(my_pixels), step):
                    for j in range(my_pixels[i]):
                        color = my_pixels[i+1:i + 4]
                        pixels.append(Pixel(color[0],color[1],color[2]))

            elif version == b'\x03':
                bpp = int.from_bytes(lines[12:13], byteorder='little')
                rle = lines[13:14]
                if rle == b'\x00' and bpp < 8:
                   palette = list(lines[14:int.from_bytes(header, byteorder='little')])
                   palette = Decoder.create_palette(palette)
                   pix = lines[int.from_bytes(header, byteorder='little'):]

                   for byte in pix:
                       binary_string = bin(byte)[2:].zfill(8)
                       for i in range(0, len(binary_string), bpp):
                           pos = int(binary_string[i:i + bpp], 2)
                           if width*height > len(pixels):
                              pixels.append(palette[pos])

                elif rle == b'\x00' and bpp > 8:
                    for i in range(0, len(lines[14:-1]), 3):
                        pixel = Pixel(lines[14 + i], lines[14 + i + 1], lines[14 + i + 2])
                        pixels.append(pixel)
                else:
                    palette = list(lines[14:int.from_bytes(header, byteorder='little')])
                    pix = lines[int.from_bytes(header, byteorder='little'):]#pixels after the palette
                    step = 2 if bpp == 8 else 4# jump to take depending on the bpp
                    for i in range(0,len(pix),step):
                        color = palette[pix[i+1]*3:(pix[i+1]*3)+3]
                        for j in range(pix[i]):
                              if bpp == 24:
                                 color = pix[i+1:i + 4]
                              pixels.append(Pixel(*color))

            elif version == b'\x04':
                 all_pixel = lines[12:]
                 p_prime = Pixel(0,0,0) #previous pixel
                 index = 0
                 while index != len(all_pixel):
                       bloc = Decoder.identify_bloc(all_pixel[index])
                       pixel , index = Decoder.decode_bloc(bloc,p_prime,all_pixel,index)
                       p_prime = pixel
                       pixels.append(pixel)

       if ULBMP != b'ULBMP':
          raise Exception("wrong format")
       elif len(lines) < 15:
           raise Exception("not enough information")
       return Image(width,height,pixels)




