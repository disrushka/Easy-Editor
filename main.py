#создай тут фоторедактор Easy Editor!
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import QApplication,QListWidget, QWidget, QLabel, QRadioButton, QPushButton, QMessageBox,QVBoxLayout,QHBoxLayout,QGroupBox, QFileDialog
import os
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL.ImageFilter import (SHARPEN)
app = QApplication([])
window = QWidget()
window.resize(700, 400)

window.setWindowTitle('Приложение Easy Editor')
list_file = QListWidget()
qwerty = QLabel('Картинка')

folder = QPushButton('Папка')

left = QPushButton('Лево')
right = QPushButton('Право')
mirror = QPushButton('Зеркало')
sharpness = QPushButton('Резкость')
bw = QPushButton('Ч/б')
blur =  QPushButton('Размытие')
gran = QPushButton('Чёрные границы')
grey = QPushButton('Серый')

line11 = QHBoxLayout() 
line12 = QHBoxLayout() 

line21 = QVBoxLayout() 
line22 = QVBoxLayout() 


line21.addWidget(folder)
line21.addWidget(list_file)

line22.addWidget(qwerty)
line12.addWidget(left)
line12.addWidget(right)
line12.addWidget(mirror)
line12.addWidget(sharpness)
line12.addWidget(bw)
line12.addWidget(blur)
line12.addWidget(gran)
line12.addWidget(grey)

line22.addLayout(line12)

line11.addLayout(line21, 20)
line11.addLayout(line22, 90)



workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def filter(files, extensions):
    result = list()
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result


def showFilenamesList():
    chooseWorkdir()
    mil = ['png', 'jpg', 'jpeg', 'bmp']
    files = os.listdir(workdir)
    filenames  = filter(files, mil)
    list_file.clear()
    for i in filenames:
        list_file.addItem(i)
folder.clicked.connect(showFilenamesList)


class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.papka = 'PAPKA/'

    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)


    def showImage(self, path):
        qwerty.hide()
        pixmapimage = QPixmap(path)
        w, h = qwerty.width(), qwerty.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        qwerty.setPixmap(pixmapimage)
        qwerty.show()

    def saveImage(self):
            path = os.path.join(workdir, self.papka)
            if not(os.path.exists(path) or os.path.isdir(path)):
                os.mkdir(path)
            image_path = os.path.join(path, self.filename)
            self.image.save(image_path)


    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.papka, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.papka, self.filename)
        self.showImage(image_path)
        
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.papka, self.filename)
        self.showImage(image_path)
        
    def do_sharpness(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.papka, self.filename)
        self.showImage(image_path)

    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.papka, self.filename)
        self.showImage(image_path)

    def do_blur(self):
        self.image = self.image.filter(ImageFilter.GaussianBlur(20))
        self.saveImage()
        image_path = os.path.join(workdir, self.papka, self.filename)
        self.showImage(image_path)

    def do_gran(self):
        self.image = self.image.filter(ImageFilter.FIND_EDGES)
        self.saveImage()
        image_path = os.path.join(workdir, self.papka, self.filename)
        self.showImage(image_path)

    def do_grey(self):
        self.image = self.image.filter(ImageFilter.EMBOSS)
        self.saveImage()
        image_path = os.path.join(workdir, self.papka, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if list_file.currentRow() >= 0:
        filename = list_file.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)

list_file.currentRowChanged.connect(showChosenImage)
bw.clicked.connect(workimage.do_bw)
left.clicked.connect(workimage.do_left)
right.clicked.connect(workimage.do_right)
sharpness.clicked.connect(workimage.do_sharpness)
mirror.clicked.connect(workimage.do_mirror)
blur.clicked.connect(workimage.do_blur)
gran.clicked.connect(workimage.do_gran)
grey.clicked.connect(workimage.do_grey)


window.setLayout(line11)
window.show()
app.exec()