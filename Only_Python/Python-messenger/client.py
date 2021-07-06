import asyncio
from asyncio import transports

from PySide2.QtWidgets import QMainWindow, QApplication
from asyncqt import QEventLoop
from interface import Ui_MainWindow

class ClientProtocol(asyncio.Protocol):
    transport: transports.Transport
    window: 'MainWindow'

    def __init__(self, chat: 'MainWindow'):
        self.window = chat

    def data_received(self, data: bytes):
        decoded = data.decode()
        self.window.append_text(decoded)

    def send_data(self, message: str):
        encoded = message.encode()
        self.transport.write(encoded)

    def connection_made(self, transport: transports.Transport):
        self.window.append_text("Подключено")
        self.transport = transport

    def connection_lost(self, exception):
        self.window.append_text("Отключено")

class MainWindow(QMainWindow, Ui_MainWindow):
    protocol: ClientProtocol
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.message_button.clicked.connect(self.button)

    def button(self): # перекидываем текст из маленького поля в большое
        message_text = self.message_input.description()
        self.message_input.clear() # очищаем поле
        self.protocol.send_data(message_text)

    def append_text(self, connect: str):
        self.message_box.appendPlainText(connect)

    def build_protocol(self):
        self.protocol = ClientProtocol(self)
        return self.protocol

    async def start(self):
        self.show() # показываем окно
        event_loop = asyncio.get_running_loop()

        coroutine = event_loop.create_connection(
            self.build_protocol,
            "127.0.0.1",
            8888
        )

        await asyncio.wait_for(coroutine, 1000)

app = QApplication() # создаём приложение
loop = QEventLoop(app)
asyncio.set_event_loop(loop)

window = MainWindow() # создаём окно

loop.create_task(window.start()) # подключаемся к серверу
loop.run_forever() # запускаем бесконечный цикл (или же loop.exec_())
