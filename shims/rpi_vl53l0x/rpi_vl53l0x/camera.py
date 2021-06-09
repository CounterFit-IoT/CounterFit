'''
The picamera package consists of several modules which provide a pure Python
interface to the Raspberry Pi's camera module.
'''
# pylint: disable=import-error
from counterfit_connection import CounterFitConnection
from PIL import Image

class PiCamera():
    '''
    Provides a pure Python interface to a virtual Raspberry Pi camera module.
    '''
    # pylint: disable=unused-argument
    def __init__(self, resolution = None, **kwargs):
        if resolution is not None:
            self.__width: int = resolution[0]
            self.__height: int = resolution[1]
        else:
            self.__width = -1
            self.__height = -1

        self.__rotation = 0

    @property
    def resolution(self):
        '''
        Retrieves or sets the resolution at which image captures, video
        recordings, and previews will be captured.
        '''
        return (self.__width, self.__height)

    @resolution.setter
    def resolution(self, val):
        '''
        Retrieves or sets the resolution at which image captures, video
        recordings, and previews will be captured.
        '''
        self.__width = int(val[0])
        self.__height = int(val[1])

    @property
    def rotation(self):
        '''
        Retrieves or sets the current rotation of the camera's image.
        '''
        return self.__rotation

    @rotation.setter
    def rotation(self, val: int):
        '''
        Retrieves or sets the current rotation of the camera's image.
        '''
        self.__rotation = val

    def __resize_and_crop(self, image: Image) -> Image:
        width_adjust =  self.__width / image.size[0]
        height_adjust = self.__height / image.size[1]

        max_adjust = max([width_adjust, height_adjust])

        new_width = int(image.size[0] * max_adjust)
        new_height = int(image.size[1] * max_adjust)

        image = image.resize((new_width, new_height))

        left = 0
        bottom = 0

        if image.size[0] > self.__width:
            left = int((image.size[0] - self.__width) / 2)
        if image.size[1] > self.__height:
            bottom = int((image.size[1] - self.__height) / 2)

        image = image.crop((left, bottom, self.__width + left, self.__height + bottom))

        return image

    def capture(self, output, image_format=None):
        '''
        Capture an image from the camera, storing it in *output*.
        '''
        # read the image from Counterfit
        raw_image = CounterFitConnection.read_binary_sensor('Picamera')
        raw_image.seek(0)

        image = Image.open(raw_image)

        if self.__rotation > 0:
            image = image.rotate(self.__rotation, expand=True)

        if self.__width > 0 and self.__height > 0:
            image = self.__resize_and_crop(image)

        image.save(output, format=image_format)
