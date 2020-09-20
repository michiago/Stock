from unittest.mock import patch
from src.application import menu


def test_menu_1():

    with patch("builtins.input", side_effect=["1", "q"]):
        with patch("src.functions.getHistoricalQuotes") as mock:
            menu()
            mock.assert_called()


def test_menu_2():

    with patch("builtins.input", side_effect=["2", "q"]):
        with patch("src.functions.getLatestQuote") as mock:
            menu()
            mock.assert_called()


def test_menu_3():

    with patch("builtins.input", side_effect=["3", "q"]):
        with patch("src.functions.getGraphHistoricalExchangeRate") as mock:
            menu()
            mock.assert_called()


def test_menu_4():

    with patch("builtins.input", side_effect=["4", "q"]):
        with patch("src.functions.getGraphHistoricalQuotes") as mock:
            menu()
            mock.assert_called()


def test_menu_5():

    with patch("builtins.input", side_effect=["5", "q"]):
        with patch("src.functions.getGraphHistoricalIntervalQuotes") as mock:
            menu()
            mock.assert_called()