import unittest
from typing import Dict
from parameterized import parameterized, param

from src.side_effect_similarity import SideEffectSimilarity


class TestSideEffectSimilarity(unittest.TestCase):
    def setUp(self):
       all_side_effects = ['headache', 'abdominal_pain', 'gastrointestinal_pain', 'nausea', 'diarrhoea', 'vomiting', 
                           'rhinitis', 'back_pain', 'cough', 'aggression', 'anxiety', 'mental disorder', 'dry_eye', 
                           'hallucination', 'liver_disorder', 'neoplasm', 'pain', 'sleep_disorder', 'tremor', 
                           'vertigo', 'agitation', 'eye_irritation', 'insomnia', 'gastritis', 'bone_disorder', 
                           'ear_pain', 'hypertension', 'irritability', 'urine_output_increased', 'vaginal_inflammation', 
                           'weight_decreased', 'increased_appetite', 'depression', 'asthma', 'hepatitis', 'pancreatitis', 
                           'urinary_retention', 'vision_blurred', 'anaemia', 'bronchitis', 'libido_decreased', 
                           'hair_disorder', 'hypersensitivity', 'hypotension']  

       self.__side_effect_similarity = SideEffectSimilarity(all_side_effects)

    @parameterized.expand([
        ({'headache': 0.78, 'nausea': 0.66, 'diarrhoea': 0.21, 'vomiting': 0.08, 'rhinitis': 0.32, 'vertigo': 0.03, 'depression': 0.1}, 
         {'headache': 0.53, 'nausea': 0.26, 'anxiety': 0.41, 'cough': 0.08, 'rhinitis': 0.37, 'vertigo': 0.03, 'depression': 0.18}),
        ({'headache': 0.22, 'nausea': 0.78, 'diarrhoea': 0.01, 'vomiting': 0.08, 'libido_decreased': 0.32, 'vertigo': 0.03, 'sleep_disorder': 0.1},
         {'headache': 0.09, 'nausea': 0.88, 'anxiety': 0.02, 'vomiting': 0.08, 'rhinitis': 0.22, 'vertigo': 0.03, 'depression': 0.1}),
        ({'headache': 0.35, 'sleep_disorder': 0.12, 'diarrhoea': 0.07, 'vomiting': 0.08, 'rhinitis': 0.18, 'vertigo': 0.03, 'depression': 0.56},
         {'weight_decreased': 0.78, 'nausea': 0.37, 'cough': 0.81, 'vomiting': 0.08, 'rhinitis': 0.15, 'hypertension': 0.03, 'depression': 0.76})
    ])
    def test_are_similar_returns_similarity(self, drug_side_effects1:Dict[str, float], drug_side_effects2:Dict[str, float]):        
        similarity = self.__side_effect_similarity.are_similar(drug_side_effects1, drug_side_effects2)

        self.assertIsNotNone(similarity)
        self.assertGreaterEqual(similarity, 0)