import unittest
from typing import List
from parameterized import parameterized, param

from src.go_similarity import GOSimilarity


class TestGoSimilarity(unittest.TestCase):

    def setUp(self):
       obo_file_path = 'go-basic.obo'
       gaf_file_path = 'goa_human.gaf'
       self.__go_similarity = GOSimilarity(obo_file_path, gaf_file_path)

    @parameterized.expand([
        ('O75884', 'Q9NQB0', 'biological_process'),
        ('O75884', 'Q9NQB0', 'cellular_component'),
        ('O75884', 'Q9NQB0', 'molecular_function')
    ])
    def test_is_semantic_similar_returns_similar_distance_rate(self, protein_id1:str, protein_id2:str, go_term_category:str):       
        score = self.__go_similarity.are_semantic_similar(protein_id1, protein_id2, go_term_category)

        self.assertIsNotNone(score)
        self.assertGreaterEqual(score, 0)

    @parameterized.expand([
        ('O75884', 'A0A287D2U3', 'biological_process'),
        ('O75884', 'A0A287D2U3', 'cellular_component'),
        ('O75884', 'A0A287D2U3', 'molecular_function')
    ])
    def test_is_semantic_similar_returns_not_similar(self, protein_id1:str, protein_id2:str, go_term_category:str):       
        score = self.__go_similarity.are_semantic_similar(protein_id1, protein_id2, go_term_category)

        self.assertIsNotNone(score)
        self.assertLess(score, 0)