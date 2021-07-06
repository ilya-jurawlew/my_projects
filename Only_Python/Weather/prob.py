import cv2


class ImageMaker:
    """Класс рисования открытки с прогнозом"""

    def __init__(self, data):
        self.data = data

    def view_image(self):
        x, y = 128, 20
        for i in self.data:
            edit_image = self.edit_image(weather=i)


    def edit_image(self, weather):
        image = cv2.imread('python_snippets/external_data/probe.jpg')
        width = int(image.shape[1])

        if weather['title'] == 'дождь':
            icon = cv2.imread('python_snippets/external_data/weather_img/rain.jpg')
            start_value = 255
            step = (start_value - 20) / width
            for column in range(0, width):
                image[:, column:column + 1] = (255, 150, 50)
                start_value -= step
            image[:icon.shape[0], :icon.shape[1]] = icon

        cv2.namedWindow('test', cv2.WINDOW_NORMAL)
        cv2.imshow('test', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return image


postcard = ImageMaker(data=[{
    'title': 'дождь',
    'temp_min': '+15',
    'temp_max': '+25',
    'date': '2021-06-28',
}])
postcard.view_image()
