import unittest
from itertools import islice
import solution
from itertools import cycle


def a_generator():
    while True:
        yield 'a'


def factorial():
    number = 1
    factorial = 1
    while True:
        yield factorial
        number += 1
        factorial = factorial * number


def multiples_of(num):
    i = 1
    while True:
        yield num * i
        i += 1


def ones():
    while True:
        yield 1


def naturals():
    number = 1
    while True:
        yield number
        number += 1


def endless_growing_sequences():
    for i, generator_key in enumerate(cycle(['fibonacci', 'primes'])):
        yield {'sequence': generator_key, 'length': i + 1}


class TestFibonacci(unittest.TestCase):
    def test_fibonacci(self):
        fibonacci = solution.fibonacci()
        first_five = list(islice(fibonacci, 5))
        self.assertEqual(first_five, [1, 1, 2, 3, 5])


class TestPrimes(unittest.TestCase):
    def test_primes(self):
        primes = solution.primes()
        first_five = list(islice(primes, 5))
        self.assertEqual(first_five, [2, 3, 5, 7, 11])


class TestAlphabet(unittest.TestCase):
    def test_alphabet(self):
        alphabet = solution.alphabet(code='lat')
        first_five = list(islice(alphabet, 5))
        self.assertEqual(first_five, ['a', 'b', 'c', 'd', 'e'])

    def test_alphabet_with_letters(self):
        alphabet = solution.alphabet(letters='ⰰⰱⰲⰳⰴⰵⰶⰷⰸⰹⰺⰻⰼⰽⰾⰿⱀⱁⱂⱃⱄⱅⱆⱇⱈⱉⱊⱋⱌⱍⱎⱏⱐⱑⱒⱓⱔⱕⱖⱗⱘⱙⱚⱛⱜⱝⱞ')
        first_five = list(islice(alphabet, 5))
        self.assertEqual(first_five, ['ⰰ', 'ⰱ', 'ⰲ', 'ⰳ', 'ⰴ'])

    def test_alphabet_with_bg(self):
        alphabet = solution.alphabet(code='bg')
        first_six = list(islice(alphabet, 6))
        self.assertEqual(first_six, ["а", "б", "в", "г", "д", "е"])


class TestIntertwine(unittest.TestCase):
    def test_intertwine(self):
        fibonacci_3_prime_3_bg_3 = solution.intertwined_sequences([
            {'sequence': 'fibonacci', 'length': 3},
            {'sequence': 'primes', 'length': 3},
            {'sequence': 'alphabet', 'code': 'bg', 'length': 3}
        ])

        self.assertEqual(
            list(fibonacci_3_prime_3_bg_3),
            [1, 1, 2, 2, 3, 5, 'а', 'б', 'в']
        )

    def test_intertwine_fpfpfp(self):
        fpfpfp = solution.intertwined_sequences((
            {'sequence': 'fibonacci', 'length': 1},
            {'sequence': 'primes', 'length': 1},
            {'sequence': 'fibonacci', 'length': 1},
            {'sequence': 'primes', 'length': 1},
            {'sequence': 'fibonacci', 'length': 1},
            {'sequence': 'primes', 'length': 1},
        ))
        self.assertEqual(list(fpfpfp), [1, 2, 1, 3, 2, 5])

    def test_intertwine_fpaapf(self):
        fpaapf = solution.intertwined_sequences((
            {'sequence': 'fibonacci', 'length': 1},
            {'sequence': 'primes', 'length': 1},
            {'sequence': 'alphabet', 'code': 'lat', 'length': 1},
            {'sequence': 'alphabet', 'code': 'bg', 'length': 1},
            {'sequence': 'primes', 'length': 1},
            {'sequence': 'fibonacci', 'length': 1}
        ))
        self.assertEqual(list(fpaapf), [1, 2, 'a', 'а', 3, 1])

    def test_generator_cycle(self):
        result = []
        generator = solution.intertwined_sequences(endless_growing_sequences())
        for i in range(0, 6):
            result.append(next(generator))
        self.assertEqual(result, [1, 2, 3, 1, 2, 3])

    def test_factorial(self):
        gen = solution.intertwined_sequences(
                    [
                        {'sequence': 'factorial', 'length': 4},
                        {'sequence': 'a_generator', 'length': 3},
                        {'sequence': 'multiples_of', 'length': 3, 'num': 3}
                    ],
                    generator_definitions={
                        'factorial': factorial,
                        'multiples_of': multiples_of,
                        'a_generator': a_generator
                    }
                )
        self.assertEqual(list(gen), [1, 2, 6, 24, 'a', 'a', 'a', 3, 6, 9])

    def test_two_factorial(self):
        gen = solution.intertwined_sequences(
                    [
                        {'sequence': 'factorial', 'length': 4},
                        {'sequence': 'factorial', 'length': 3},
                        {'sequence': 'factorial', 'length': 5}
                    ],
                    generator_definitions={
                        'factorial': factorial
                    }
                )
        self.assertEqual(list(gen), [1, 2, 6, 24, 1, 2, 6, 1, 2, 6, 24, 120])

    def test_multiples_of(self):
        gen = solution.intertwined_sequences(
                    [
                        {'sequence': 'multiples_of', 'length': 10, 'num': 2}
                    ],
                    generator_definitions={
                        'multiples_of': multiples_of
                    }
                )
        self.assertEqual(list(gen), [2, 4, 6, 8, 10, 12, 14, 16, 18, 20])

    def test_generator_with_parametrs_generator_a(self):
        generator = solution.intertwined_sequences(
                    [
                        {'sequence': 'multiples_of', 'length': 1, 'num': 12},
                        {'sequence': 'a_generator', 'length': 3},
                        {'sequence': 'multiples_of', 'length': 3, 'num': 3}
                    ],
                    generator_definitions={
                        'multiples_of': multiples_of,
                        'a_generator': a_generator
                    }
                )
        self.assertEqual(list(generator), [12, 'a', 'a', 'a', 3, 6, 9])

    def test_generator_with_parametrs(self):
        generator = solution.intertwined_sequences(
                    [
                        {'sequence': 'multiples_of', 'length': 5, 'num': 12},
                        {'sequence': 'ones', 'length': 3},
                        {'sequence': 'multiples_of', 'length': 3, 'num': 3}
                    ],
                    generator_definitions={
                        'multiples_of': multiples_of,
                        'ones': ones
                    }
                )
        self.assertEqual(list(generator), [12, 24, 36, 48, 60, 1, 1, 1, 3, 6, 9])


def test_generator_with_two_function(self):
    generator = solution.intertwined_sequences(
        [
            {'sequence': 'ones', 'length': 10},
            {'sequence': 'fibonacci', 'length': 3},
            {'sequence': 'natural', 'length': 4}
        ],
        generator_definitions={
            'ones': ones,
            'natural': naturals
        }
    )
    self.assertEqual(list(generator), [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 3, 4])
if __name__ == '__main__':
    unittest.main()
