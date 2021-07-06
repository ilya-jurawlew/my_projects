from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch, Mock

from pony.orm import rollback, db_session
from vk_api.bot_longpoll import VkBotMessageEvent

from bot import Bot
import settings
from generate_ticket import generate_ticket


def isolate_db(test_func):
    def wrapper(*args, **kwargs):
        with db_session:
            test_func(*args, **kwargs)
            rollback()
    return wrapper


class Test1(TestCase):
    RAW_EVENT = {
        'type': 'message_new',
        'object': {
            'message': {'date': 1610816558, 'from_id': 66167825, 'id': 53, 'out': 0, 'peer_id': 66167825,
                        'text': 'привет', 'conversation_message_id': 53, 'fwd_messages': [], 'important': False,
                        'random_id': 0, 'attachments': [], 'is_hidden': False},
            'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link',
                                               'intent_subscribe', 'intent_unsubscribe'],
                            'keyboard': True, 'inline_keyboard': True, 'carousel': False, 'lang_id': 0}},
        'group_id': 201527308,
        'event_id': '3048c0331a1213b0cb5cfe5fcda5b9b727434411'}

    def test_run(self):
        count = 5
        events = [{}] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.send_image = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call({})
                assert bot.on_event.call_count == count

    INPUTS = [
        'Привет',
        'А когда?',
        'Где будет конференция?',
        'Зарегистрируй меня',
        'Илья',
        'Мой адрес емейл ili@email',
        'ili@email.com',
    ]

    EXPECTED_OUTPUTS = [
        settings.DEFAULT_ANSWER,
        settings.INTENTS[0]['answer'],
        settings.INTENTS[1]['answer'],
        settings.SCENARIOS['registration']['steps']['step1']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['failure_text'],
        settings.SCENARIOS['registration']['steps']['step3']['text'].format(name='Илья', email='ili@email.com')
    ]

    @isolate_db
    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock
        events = []

        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('bot.VkBotLongPoll', return_value=long_poller_mock):
            bot = Bot('', '')
            bot.api = api_mock
            bot.send_image = Mock()
            bot.run()
        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])
        assert real_outputs == self.EXPECTED_OUTPUTS

    def image_generation(self):
        with open('files/avatar.jpg', 'rb') as avatar_file:
            avatar_mock = Mock
            avatar_mock.content = avatar_file.read()
        with patch('requests.get', return_value=avatar_mock):
            ticket_file = generate_ticket('Ilia', 'email@email.com')
        with open('files/ticket_example.png', 'rb') as expected_file:
            expected_bytes  = expected_file.read()
        assert ticket_file.read() == expected_bytes
