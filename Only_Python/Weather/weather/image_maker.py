import os

import cv2


class ImageMaker:
    """ Рисуем открытки с прогнозом"""
    def __init__(self, data):
        """
        :param data: список словарей
        :return: итоговое изображение
        """
        self.data = data
        self.template_file = 'python_snippets/external_data/probe.jpg'
        self.icon_sun = 'python_snippets/external_data/weather_img/sun.jpg'
        self.icon_snow = 'python_snippets/external_data/weather_img/snow.jpg'
        self.icon_rain = 'python_snippets/external_data/weather_img/rain.jpg'
        self.icon_cloud = 'python_snippets/external_data/weather_img/cloud.jpg'

    def view_image(self):
        x, y = 128, 20
        for i in self.data:

            text_date = str(i[4])
            text_title = 'На улице сегодня' + i[1]
            text_temp_max = 'Максимум днем' + i[2]
            text_temp_min = 'Минимум днем ' + i[3]
            edit_image = self.edit_image(weather=i)

            new_image = cv2.putText(edit_image, text_date, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0))
            new_image = cv2.putText(edit_image, text_title, (x, y+20), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0))
            new_image = cv2.putText(edit_image, text_temp_max, (x, y+40), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0))
            new_image = cv2.putText(edit_image, text_temp_min, (x, y+60), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0))
            if not os.path.isdir('images'):
                os.mkdir('images')
            cv2.imwrite(f'images/{text_date}.jpg', new_image)

    def edit_image(self, weather):
        image = cv2.imread(self.template_file)
        width = int(image.shape[1])

        if weather[1].find('солн') != -1:
            icon = cv2.imread(self.icon_sun)
            self.gradient_and_insert(image=image, icon=icon, width=width, finish_color=[0, 255, 255])

        elif weather[1].find('сне') != -1:
            icon = cv2.imread(self.icon_snow)
            self.gradient_and_insert(image=image, icon=icon, width=width, finish_color=[255, 150, 50])

        elif weather[1].find('дожд') != -1:
            icon = cv2.imread(self.icon_rain)
            self.gradient_and_insert(image=image, icon=icon, width=width, finish_color=[255, 0, 0])

        elif weather[1].find('облачн') != -1:
            icon = cv2.imread(self.icon_cloud)
            self.gradient_and_insert(image=image, icon=icon, width=width, finish_color=[133, 133, 133])

        return image

    def gradient_and_insert(self, image, icon, width, finish_color):
        start_value_b, start_value_g, start_value_r = 255, 255, 255
        step_b = (start_value_b - finish_color[0]) / width
        step_g = (start_value_g - finish_color[1]) / width
        step_r = (start_value_r - finish_color[2]) / width
        for column in range(0, width):
            image[:, column:column + 1] = (start_value_b, start_value_g, start_value_r)
            start_value_b -= step_b
            start_value_g -= step_g
            start_value_r -= step_r
        image[:icon.shape[0], :icon.shape[1]] = icon
        return image


# postcard = ImageMaker(data=[{
#     'title': 'солнечно',
#     'temp_min': '+15',
#     'temp_max': '+25',
#     'date': '2021-06-28',
# }])
# postcard.view_image()
