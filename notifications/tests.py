import os
import unittest
from unittest.mock import patch, Mock

import telebot

from notifications.bot import send_telegram_message


class TestSendTelegramMessage(unittest.TestCase):

    def setUp(self):
        os.environ["TELEGRAM_CHAT_ID"] = "123456789"
        os.environ["TELEGRAM_BOT_TOKEN"] = "test-token"

        self.bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

    def tearDown(self):
        os.environ.pop("TELEGRAM_CHAT_ID", None)
        os.environ.pop("TELEGRAM_BOT_TOKEN", None)

    @patch("telebot.TeleBot")
    def test_send_telegram_message_to_correct_chat_id(self, mock_bot):
        mock_bot_instance = mock_bot.return_value
        mock_bot_instance.send_message.return_value = Mock()

        send_telegram_message("Test message")

        mock_bot_instance.send_message.assert_called_once_with(
            "123456789",
            "Test message"
        )

    @patch("telebot.TeleBot")
    def test_send_telegram_message_with_correct_text(self, mock_bot):
        mock_bot_instance = mock_bot.return_value
        mock_bot_instance.send_message.return_value = Mock()

        send_telegram_message("Test message")

        mock_bot_instance.send_message.assert_called_once_with(
            "123456789",
            "Test message"
        )

    def test_send_telegram_message_with_missing_chat_id(self) -> None:
        os.environ.pop("TELEGRAM_CHAT_ID", None)

        with self.assertRaises(Exception):
            send_telegram_message("Test message")

    def test_send_telegram_message_with_missing_bot_token(self) -> None:
        os.environ.pop("TELEGRAM_BOT_TOKEN", None)

        with self.assertRaises(Exception):
            send_telegram_message("Test message")
