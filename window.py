"""
NOM : GULZAR
PRÉNOM : ZIA
SECTION : B1-INFO
MATRICULE : 000595624
"""
from PySide6.QtGui import QImage, QPixmap, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QGraphicsView, QGraphicsScene, QFileDialog, QLabel, QInputDialog, QErrorMessage
from encoding import Decoder, Encoder

class MyWindow(QMainWindow):
    """
        Main application window for ULBMP image processing.

        Attributes:
            load_button (QPushButton): Button for loading an image.
            save_to_button (QPushButton): Button for saving an image.
            color_count_label (QLabel): Label for displaying the number of colors in the image.
            scene (QGraphicsScene): Graphics scene for displaying the image.
            view (QGraphicsView): Graphics view for displaying the scene.
            decoded_image (Image): Decoded image object.
            colors (int): Number of colors in the image.
        """
    def __init__(self):
        """
                Initializes the main window.
                """
        super().__init__()

        self.setWindowTitle("ULBMP")


        layout = QVBoxLayout()


        self.load_button = QPushButton("Load image")
        self.load_button.clicked.connect(self.load_file)
        layout.addWidget(self.load_button)


        self.save_to_button = QPushButton("Save image")
        self.save_to_button.clicked.connect(self.show_save_options)
        layout.addWidget(self.save_to_button)


        self.color_count_label = QLabel("colors: 0")
        layout.addWidget(self.color_count_label)


        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


        self.decoded_image = None
        self.colors = None

    def load_file(self):
        """
                Loads an image file.
                """
        file_name, _ = QFileDialog.getOpenFileName(self, "Load File", "", "All files (*)")
        if file_name:
            if file_name.endswith('.ulbmp'):
                self.decoded_image = Decoder.load_from(file_name)  # Stocker l'image décodée
                image = QImage(self.decoded_image.get_width(), self.decoded_image.get_height(), QImage.Format_RGB32)
                colors = set()
                for i in range(self.decoded_image.get_width()):
                    for j in range(self.decoded_image.get_height()):
                        pixel = self.decoded_image.__getitem__((i, j))
                        colors.add((pixel.r, pixel.v, pixel.b))
                        image.setPixelColor(i, j, QColor(pixel.r, pixel.v, pixel.b))
                self.draw_image(image)
                self.view.setFixedSize(image.width()+10, image.height()+10)
                self.initUILayout(image.width(), image.height())
                self.color_count_label.setText(f"colors: {len(colors)}")
                self.colors = len(colors)
            else:
                self.show_error_message("Erreur de lecture", "Problème lors de la lecture de l'image : 'wrong format: missing ULBMP in the header'.")

    def show_save_options(self):
        """
                Displays save options for the image.
                """
        if not self.scene.items() or not self.decoded_image:
            return

        options = ["FORMAT 1","FORMAT 2", "FORMAT 3","FORMAT 3 (RLE)","FORMAT 4"]
        option, ok = QInputDialog.getItem(self, "Options", "Sélectionnez une option:", options, editable=False)
        if ok:
            if option == "FORMAT 1":
                file_name, _ = QFileDialog.getOpenFileName(self, "Load File", "", "All files (*)")
                Encoder(self.decoded_image, 1).save_to(file_name)
            elif option == "FORMAT 2":
                file_name, _ = QFileDialog.getOpenFileName(self, "Load File", "", "All files (*)")
                Encoder(self.decoded_image, 2).save_to(file_name)
            elif option == "FORMAT 3 (RLE)":
                file_name, _ = QFileDialog.getOpenFileName(self, "Load File", "", "All files (*)")
                if 16 <= self.colors <= 256:
                   Encoder(self.decoded_image, 3,depth = 8 , rle = True ).save_to(file_name)
                elif self.colors > 256:
                   Encoder(self.decoded_image, 3, depth= 24, rle=True).save_to(file_name)
                else:
                    self.show_error_message("Erreur d'ecriture","pas assez de couleur")

            elif option == "FORMAT 3":
                file_name, _ = QFileDialog.getOpenFileName(self, "Load File", "", "All files (*)")
                if self.colors <= 2:
                    Encoder(self.decoded_image, 3, depth= 1, rle=False).save_to(file_name)
                elif self.colors <= 4:
                    Encoder(self.decoded_image, 3, depth= 2, rle=False).save_to(file_name)
                elif self.colors <= 16:
                    Encoder(self.decoded_image, 3, depth= 4, rle=False).save_to(file_name)
                elif self.colors <= 256:
                     Encoder(self.decoded_image, 3,depth = 8 , rle = False ).save_to(file_name)
                else:
                    Encoder(self.decoded_image, 3, depth= 24, rle= False).save_to(file_name)
            elif option == "FORMAT 4":
                file_name, _ = QFileDialog.getOpenFileName(self, "Load File", "", "All files (*)")
                Encoder(self.decoded_image,4).save_to(file_name)


    def draw_image(self, image):
        """
                Draws the image on the scene.

                Args:
                    image (QImage): Image to draw.
                """
        self.scene.clear()
        pixmap = QPixmap.fromImage(image)
        self.scene.addPixmap(pixmap)
    def initUILayout(self, image_width, image_height):
        """
                Initializes the UI layout based on the dimensions of the loaded image.

                Args:
                    image_width (int): Width of the loaded image.
                    image_height (int): Height of the loaded image.
                """

        self.view.setMinimumSize(image_width+10+10, image_height+10+10)
        self.view.setMaximumSize(image_width+10+10, image_height+10+10)


        self.setMinimumSize(image_width+30+10, image_height +120+10)
        self.setMaximumSize(image_width+30+10 , image_height +120+10)

    def show_error_message(self, title, message):
        """
                Displays an error message dialog.

                Args:
                    title (str): Title of the error message dialog.
                    message (str): Content of the error message.
                """
        error_dialog = QErrorMessage()
        error_dialog.setWindowTitle(title)
        error_dialog.showMessage(message)
        error_dialog.exec_()

