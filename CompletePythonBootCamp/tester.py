import unittest
import to_be_tested

class TestCap(unittest.TestCase):
    def test_one_word(self):
        text = 'python'
        result = to_be_tested.cap(text)
        self.assertEqual(result, 'Python')

    def test_multiple_words(self):
        text = 'multy word'
        result = to_be_tested.cap(text)
        self.assertEqual(result, 'Multy Word')

if __name__ == '__main__':
    unittest.main()