import unittest
from number_pattern import process_number, generate_big_int

class TestNumberPattern(unittest.TestCase):

    def test_process_number_zeros_and_ones(self):
        import math
        # Three zeros, one one -> n=3 for 0 -> ((1<<3)-1)**3 = 7**3 = 343 -> log10(343)
        # n=1 for 1 -> (1<<1)**1 = 2**1 = 2 -> log10(2)
        # diff = |log10(343) - log10(2)|
        expected = abs(math.log10(343) - math.log10(2))
        self.assertAlmostEqual(process_number(1000), expected)

    def test_process_number_single_digit(self):
        # Only one type of digit, so differences should be 0 because the list `values` has length 1.
        self.assertAlmostEqual(process_number(222), 0)

    def test_process_number_simple(self):
        import math
        # number: 12
        # 1 occurs 1 time: (1<<1)**1 = 2**1 = 2 -> log10(2)
        # 2 occurs 1 time: 2**1 = 2
        # diff: |log10(2) - 2|
        expected = abs(math.log10(2) - 2)
        self.assertAlmostEqual(process_number(12), expected)

    def test_process_number_custom(self):
        import math
        # 0 occurs 3 times: 7**3 = 343 -> log10(343)
        # 1 occurs 5 times: 32**5 = 33554432 -> log10(33554432)
        # Diff: |log10(33554432) - log10(343)|
        expected = abs(math.log10(33554432) - math.log10(343))
        self.assertAlmostEqual(process_number(11111000), expected)

    def test_generate_big_int(self):
        # Test generation
        num = generate_big_int()
        self.assertTrue(num >= 0)

if __name__ == '__main__':
    unittest.main()
