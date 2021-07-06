import asyncio

from asyncio import transports


class ServerProtocol(asyncio.Protocol): # наследуем, чтобы не писать все методы самому, они уже есть
    login: str = None
    server: 'Server'
    transport: transports.Transport

    def __init__(self, server: 'Server'):
        self.server = server

    def data_received(self, data: bytes): # получение данных по сети
        print(data)

        decoded = data.decode()

        if self.login is not None: # если есть логин, отправляем сообщение (отдельная функция)
            self.send_messange(decoded)
        else: # если нет логина, регистрируемся
            if decoded.startswith('login:'):
                self.login = decoded.replace('login:', '') # убираем логин, оставляем само имя
                for user in self.server.clients:
                    if user.login == self.login:
                        self.transport.write(f'Логин занят, попробуйте другой'.encode())
                        print(f'{self.login} уже есть')
                        self.transport.close()

                self.transport.write(f'Привет, {self.login}!\n'.encode())
            else:
                self.transport.write('Неверный логин\n'.encode())

    def connection_made(self, transport: transports.Transport): # если всё ок
        self.server.clients.append(self)
        self.transport = transport

        print('Новый клиент')

    def connection_lost(self, exception): # если разрыв соединения
        self.server.clients.remove(self)

        print('Клиент вышел')

    def send_messange(self, content: str): # отправка сообщений
        messange = f"{self.login}: {content}"

        for user in self.server.clients:
            user.transport.write(messange.encode())

class Server:
    clients: list # список клиентов

    def __init__(self):
        self.clients = []

    def build_protocol(self): # конструктор протокола
        return ServerProtocol(self) # возвращаем новый объект

    async def start(self): # функция запускает сервер, асинхронно
        loop = asyncio.get_running_loop() # получаем управление событийным циклом

        coroutine = await loop.create_server( # асинхронная функция, внутри неё сервер
            self.build_protocol, # конструктор протокола
            '127.0.0.1', # ip сервера, на котором работаем
            8888, # порт (частота, на которой находятся потоки сообщений) >1024
        )

        print('Сервер запущен...')

        await coroutine.serve_forever()

process = Server()

try:
    asyncio.run(process.start()) # запускаем сервер
except KeyboardInterrupt:
    print('Сервер остановлен вручную')






