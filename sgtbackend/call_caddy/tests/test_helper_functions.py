import unittest
from call_caddy.helpers.evaluate_major_championship import is_major

class TestHelperFunctions(unittest.TestCase):

    def test_is_major_is_a_major(self):
        assert is_major("Masters Tournament") == True
        assert is_major("PGA Championship") == True
        assert is_major("The Open Championship") == True
        assert is_major("U.S. Open") == True

    def test_is_major_not_case_sensitive(self):
        assert is_major("MASTERS TOURNAMENT") == True
            
    def test_is_major_is_not_a_major(self):
        assert is_major("Some random tourney") == False

    def test_is_major_empty_string(self):
        assert is_major("") == False

    def test_is_major_none(self):
        assert is_major(None) == False