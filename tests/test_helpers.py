import pytest
from hotel_merge.helpers import remove_duplicates


class TestRemoveDuplicates:
    @pytest.mark.parametrize("items, case_sensitive, expected", [
        (["apple", "banana", "Apple", "orange"], True, ["apple", "banana", "Apple", "orange"]),
        (["apple", "banana", "Apple", "orange"], False, ["apple", "banana", "orange"]),
        ([], False, []),
        (["apple"], False, ["apple"]),
        (["apple", "apple", "apple"], False, ["apple"]),
    ], ids=[
        "case_sensitive",
        "case_insensitive",
        "empty_list",
        "single_element",
        "all_duplicates"
    ])
    def test_remove_duplicates(self, items, case_sensitive, expected):
        assert remove_duplicates(items, case_sensitive=case_sensitive) == expected

