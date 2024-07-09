import unittest
from typing import List
from parameterized import parameterized, param

from src.atc_similarity import ATCSimilarity


class TestATCSimilarity(unittest.TestCase):
    @parameterized.expand([
        (['A02BC51', 'A02BD05'], ['L004AB04']),
        (['L02BB05'], ['L004AB04']),
        (['A02BC51', 'A02BD05'], ['A02BD04', 'A02BC02'])
    ])
    def test_are_similar_returns_similarity(self, drug_atc_codes1:List[str], drug_atc_codes2:List[str]):       
        atc_similarity = ATCSimilarity()
        
        similarity = atc_similarity.are_similar(drug_atc_codes1, drug_atc_codes2, 4)

        self.assertIsNotNone(similarity)
        self.assertGreaterEqual(similarity, 0)