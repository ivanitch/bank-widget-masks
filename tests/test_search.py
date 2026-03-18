from src.search import process_bank_operations, process_bank_search

TRANSACTIONS = [
    {"id": 1, "description": "Перевод организации", "state": "EXECUTED"},
    {"id": 2, "description": "Перевод с карты на карту", "state": "EXECUTED"},
    {"id": 3, "description": "Открытие вклада", "state": "EXECUTED"},
    {"id": 4, "description": "Перевод организации", "state": "CANCELED"},
    {"id": 5, "description": "Перевод со счета на счет", "state": "EXECUTED"},
]


# ──────────────────────────────────────────────
# process_bank_search
# ──────────────────────────────────────────────


class TestProcessBankSearch:
    def test_returns_matching_transactions(self):
        result = process_bank_search(TRANSACTIONS, "Перевод организации")
        assert len(result) == 2
        assert all(t["description"] == "Перевод организации" for t in result)

    def test_case_insensitive(self):
        result = process_bank_search(TRANSACTIONS, "перевод")
        assert len(result) == 4  # все "Перевод ..."

    def test_partial_match(self):
        result = process_bank_search(TRANSACTIONS, "карт")
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_no_match_returns_empty_list(self):
        result = process_bank_search(TRANSACTIONS, "несуществующее")
        assert result == []

    def test_empty_transactions_list(self):
        result = process_bank_search([], "Перевод")
        assert result == []

    def test_empty_search_string_returns_all(self):
        result = process_bank_search(TRANSACTIONS, "")
        assert len(result) == len(TRANSACTIONS)

    def test_transaction_without_description_key(self):
        data = [{"id": 10}, {"id": 11, "description": "Перевод организации"}]
        result = process_bank_search(data, "Перевод")
        assert len(result) == 1
        assert result[0]["id"] == 11

    def test_regex_pattern(self):
        result = process_bank_search(TRANSACTIONS, r"^Открытие")
        assert len(result) == 1
        assert result[0]["id"] == 3

    def test_returns_list_of_dicts(self):
        result = process_bank_search(TRANSACTIONS, "вклада")
        assert isinstance(result, list)
        assert all(isinstance(t, dict) for t in result)

    def test_original_list_not_modified(self):
        original_len = len(TRANSACTIONS)
        process_bank_search(TRANSACTIONS, "Перевод")
        assert len(TRANSACTIONS) == original_len


# ──────────────────────────────────────────────
# process_bank_operations
# ──────────────────────────────────────────────


class TestProcessBankOperations:
    def test_counts_categories_correctly(self):
        categories = ["Перевод организации", "Открытие вклада"]
        result = process_bank_operations(TRANSACTIONS, categories)
        assert result["Перевод организации"] == 2
        assert result["Открытие вклада"] == 1

    def test_category_not_in_data_returns_zero(self):
        result = process_bank_operations(TRANSACTIONS, ["Несуществующая категория"])
        assert result["Несуществующая категория"] == 0

    def test_empty_categories_returns_empty_dict(self):
        result = process_bank_operations(TRANSACTIONS, [])
        assert result == {}

    def test_empty_transactions_all_zeros(self):
        result = process_bank_operations([], ["Перевод организации", "Открытие вклада"])
        assert result == {"Перевод организации": 0, "Открытие вклада": 0}

    def test_returns_dict(self):
        result = process_bank_operations(TRANSACTIONS, ["Открытие вклада"])
        assert isinstance(result, dict)

    def test_keys_match_categories(self):
        categories = ["Перевод организации", "Открытие вклада", "Перевод со счета на счет"]
        result = process_bank_operations(TRANSACTIONS, categories)
        assert set(result.keys()) == set(categories)

    def test_transaction_without_description_not_counted(self):
        data = [{"id": 10}, {"id": 11, "description": "Перевод организации"}]
        result = process_bank_operations(data, ["Перевод организации"])
        assert result["Перевод организации"] == 1

    def test_full_count(self):
        categories = [
            "Перевод организации",
            "Перевод с карты на карту",
            "Открытие вклада",
            "Перевод со счета на счет",
        ]
        result = process_bank_operations(TRANSACTIONS, categories)
        assert sum(result.values()) == len(TRANSACTIONS)
