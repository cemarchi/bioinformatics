import unittest
from typing import List
from parameterized import parameterized, param

from src.ec_number_similarity import ECNumberSimilarity


class TestECNumberSimilarity(unittest.TestCase):
    def setUp(self):
        self.__ec_number_classes = {
        '1': 'oxidoreductases',
        '1.1': 'acting on the ch-oh group of donors',
        '1.1.1': 'with nad+ or nadp+ as acceptor',
        '1.1.3': "with oxygen as acceptor",
        '1.2': 'acting on the aldehyde or oxo group of donors',
        '1.2.1': 'with nad+ or nadp+ as acceptor',
        '2': 'transferases',
        '2.1': 'transferring one-carbon groups',
        '2.1.1': 'methyltransferases',
    }

    @parameterized.expand([
        ('1.1.1.1', '1.1.1.15'),
        ('1.1.1.1', '1.2.1.15'),
        ('1.1.1.1', '2.1.1.15'),
    ])
    def test_are_similar_returns_similarity(self, ec_number1:str, ec_number2:str):       
        ec_number_similarity = ECNumberSimilarity(self.__ec_number_classes)
        
        similarity = ec_number_similarity.are_similar(ec_number1, ec_number2)

        self.assertIsNotNone(similarity)