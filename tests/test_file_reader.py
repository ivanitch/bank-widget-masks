from unittest.mock import patch

import pandas as pd

from src.file_reader import get_transactions_from_csv, get_transactions_from_excel

SAMPLE_CSV_CONTENT = (
    "id;state;date;amount;currency_name;currency_code;from;to;description\n"
    "650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;USD;Счет 1;Счет 2;Перевод\n"
    "3598919;EXECUTED;2020-12-06T23:00:58Z;29740;Peso;RUB;Карта 1;Карта 2;Оплата\n"
    "593027;CANCELED;2023-07-22T05:02:01Z;30368;Shilling;USD;Счет 3;Счет 4;Возврат\n"
)

SAMPLE_ROWS = [
    {
        "id": "650703",
        "state": "EXECUTED",
        "date": "2023-09-05T11:30:32Z",
        "amount": "16210",
        "currency_name": "Sol",
        "currency_code": "USD",
        "from": "Счет 1",
        "to": "Счет 2",
        "description": "Перевод",
    },
    {
        "id": "3598919",
        "state": "EXECUTED",
        "date": "2020-12-06T23:00:58Z",
        "amount": "29740",
        "currency_name": "Peso",
        "currency_code": "RUB",
        "from": "Карта 1",
        "to": "Карта 2",
        "description": "Оплата",
    },
    {
        "id": "593027",
        "state": "CANCELED",
        "date": "2023-07-22T05:02:01Z",
        "amount": "30368",
        "currency_name": "Shilling",
        "currency_code": "USD",
        "from": "Счет 3",
        "to": "Счет 4",
        "description": "Возврат",
    },
]


# ──────────────────────────────────────────────
# get_transactions_from_csv
# ──────────────────────────────────────────────


class TestGetTransactionsFromCsv:
    def test_returns_list_of_dicts(self):
        sample_df = pd.DataFrame(SAMPLE_ROWS)
        with patch("src.file_reader.pd.read_csv", return_value=sample_df):
            result = get_transactions_from_csv("data/transactions.csv")

        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_correct_number_of_rows(self):
        sample_df = pd.DataFrame(SAMPLE_ROWS)
        with patch("src.file_reader.pd.read_csv", return_value=sample_df):
            result = get_transactions_from_csv("data/transactions.csv")

        assert len(result) == 3

    def test_correct_field_values(self):
        sample_df = pd.DataFrame(SAMPLE_ROWS)
        with patch("src.file_reader.pd.read_csv", return_value=sample_df):
            result = get_transactions_from_csv("data/transactions.csv")

        assert result[0]["id"] == "650703"
        assert result[0]["state"] == "EXECUTED"
        assert result[0]["currency_code"] == "USD"

    def test_file_not_found_returns_empty_list(self):
        with patch("src.file_reader.pd.read_csv", side_effect=FileNotFoundError):
            result = get_transactions_from_csv("data/missing.csv")

        assert result == []

    def test_generic_read_error_returns_empty_list(self):
        with patch("src.file_reader.pd.read_csv", side_effect=Exception("bad file")):
            result = get_transactions_from_csv("data/broken.csv")

        assert result == []

    def test_empty_dataframe_returns_empty_list(self):
        empty_df = pd.DataFrame(
            columns=["id", "state", "date", "amount", "currency_name", "currency_code", "from", "to", "description"]
        )
        with patch("src.file_reader.pd.read_csv", return_value=empty_df):
            result = get_transactions_from_csv("data/empty.csv")

        assert result == []

    def test_nan_values_converted_to_none(self):
        row = SAMPLE_ROWS[0].copy()
        row["from"] = None
        df = pd.DataFrame([row])
        with patch("src.file_reader.pd.read_csv", return_value=df):
            result = get_transactions_from_csv("data/transactions.csv")

        assert result[0]["from"] is None

    def test_read_csv_called_with_correct_separator(self):
        sample_df = pd.DataFrame(SAMPLE_ROWS)
        with patch("src.file_reader.pd.read_csv", return_value=sample_df) as mock_read:
            get_transactions_from_csv("data/transactions.csv")

        mock_read.assert_called_once_with("data/transactions.csv", sep=";", dtype=str, encoding="utf-8")

    def test_canceled_transactions_included(self):
        sample_df = pd.DataFrame(SAMPLE_ROWS)
        with patch("src.file_reader.pd.read_csv", return_value=sample_df):
            result = get_transactions_from_csv("data/transactions.csv")

        states = [r["state"] for r in result]
        assert "CANCELED" in states

    def test_single_row(self):
        df = pd.DataFrame([SAMPLE_ROWS[0]])
        with patch("src.file_reader.pd.read_csv", return_value=df):
            result = get_transactions_from_csv("data/transactions.csv")

        assert len(result) == 1
        assert result[0]["id"] == "650703"


# ──────────────────────────────────────────────
# get_transactions_from_excel
# ──────────────────────────────────────────────


class TestGetTransactionsFromExcel:
    def test_returns_list_of_dicts(self):
        sample_df = pd.DataFrame(SAMPLE_ROWS)
        with patch("src.file_reader.pd.read_excel", return_value=sample_df):
            result = get_transactions_from_excel("data/transactions.xlsx")

        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_correct_number_of_rows(self):
        sample_df = pd.DataFrame(SAMPLE_ROWS)
        with patch("src.file_reader.pd.read_excel", return_value=sample_df):
            result = get_transactions_from_excel("data/transactions.xlsx")

        assert len(result) == 3

    def test_correct_field_values(self):
        sample_df = pd.DataFrame(SAMPLE_ROWS)
        with patch("src.file_reader.pd.read_excel", return_value=sample_df):
            result = get_transactions_from_excel("data/transactions.xlsx")

        assert result[1]["id"] == "3598919"
        assert result[1]["state"] == "EXECUTED"
        assert result[1]["currency_code"] == "RUB"

    def test_file_not_found_returns_empty_list(self):
        with patch("src.file_reader.pd.read_excel", side_effect=FileNotFoundError):
            result = get_transactions_from_excel("data/missing.xlsx")

        assert result == []

    def test_generic_read_error_returns_empty_list(self):
        with patch("src.file_reader.pd.read_excel", side_effect=Exception("corrupt")):
            result = get_transactions_from_excel("data/broken.xlsx")

        assert result == []

    def test_empty_dataframe_returns_empty_list(self):
        empty_df = pd.DataFrame(
            columns=["id", "state", "date", "amount", "currency_name", "currency_code", "from", "to", "description"]
        )
        with patch("src.file_reader.pd.read_excel", return_value=empty_df):
            result = get_transactions_from_excel("data/empty.xlsx")

        assert result == []

    def test_nan_values_converted_to_none(self):
        row = SAMPLE_ROWS[0].copy()
        row["to"] = None
        df = pd.DataFrame([row])
        with patch("src.file_reader.pd.read_excel", return_value=df):
            result = get_transactions_from_excel("data/transactions.xlsx")

        assert result[0]["to"] is None

    def test_read_excel_called_with_dtype_str(self):
        sample_df = pd.DataFrame(SAMPLE_ROWS)
        with patch("src.file_reader.pd.read_excel", return_value=sample_df) as mock_read:
            get_transactions_from_excel("data/transactions.xlsx")

        mock_read.assert_called_once_with("data/transactions.xlsx", dtype=str)

    def test_all_states_preserved(self):
        sample_df = pd.DataFrame(SAMPLE_ROWS)
        with patch("src.file_reader.pd.read_excel", return_value=sample_df):
            result = get_transactions_from_excel("data/transactions.xlsx")

        states = {r["state"] for r in result}
        assert states == {"EXECUTED", "CANCELED"}

    def test_single_row(self):
        df = pd.DataFrame([SAMPLE_ROWS[2]])
        with patch("src.file_reader.pd.read_excel", return_value=df):
            result = get_transactions_from_excel("data/transactions.xlsx")

        assert len(result) == 1
        assert result[0]["id"] == "593027"
