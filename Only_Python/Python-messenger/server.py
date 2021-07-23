import asyncio

from asyncio import transports


class ServerProtocol(asyncio.Protocol):
    login: str = None
    server: 'Server'
    transport: transports.Transport

    def __init__(self, server: 'Server'):
        self.server = server

    def data_received(self, data: bytes):
        print(data)

        decoded = data.decode()

        if self.login is not None:
            self.send_messange(decoded)
        else:
            if decoded.startswith('login:'):
                self.login = decoded.replace('login:', '')
                for user in self.server.clients:
                    if user.login == self.login:
                        self.transport.write(f'Логин занят, попробуйте другой'.encode())
                        print(f'{self.login} уже есть')
                        self.transport.close()

                self.transport.write(f'Привет, {self.login}!\n'.encode())
            else:
                self.transport.write('Неверный логин\n'.encode())

    def connection_made(self, transport: transports.Transport):
        self.server.clients.append(self)
        self.transport = transport

        print('Новый клиент')

    def connection_lost(self, exception):
        self.server.clients.remove(self)

        print('Клиент вышел')

    def send_messange(self, content: str):
        messange = f"{self.login}: {content}"

        for user in self.server.clients:
            user.transport.write(messange.encode())


class Server:
    clients: list

    def __init__(self):
        self.clients = []

    def build_protocol(self):
        return ServerProtocol(self)

    async def start(self):
        loop = asyncio.get_running_loop()

        coroutine = await loop.create_server(
            self.build_protocol,
            '127.0.0.1',
            8888,
        )

        print('Сервер запущен...')

        await coroutine.serve_forever()


process = Server()

try:
    asyncio.run(process.start())
except KeyboardInterrupt:
    print('Сервер остановлен вручную')
