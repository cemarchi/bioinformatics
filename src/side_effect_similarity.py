from typing import List, Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SideEffectSimilarity:
    def __init__(self, all_side_effects:List[str]):
        self.__all_side_effects = sorted(set(all_side_effects))
        self.__no_frequency = 0

    def __create_weighted_vector(self, profile: Dict[str, float]) -> np:
        return np.array([profile.get(effect, self.__no_frequency) for effect in self.__all_side_effects])

    def are_similar(self, drug_side_effects1: Dict[str, float], drug_side_effects2: Dict[str, float]) -> float:
        drug_side_effects1 = self.__create_weighted_vector(drug_side_effects1)
        drug_side_effects2 = self.__create_weighted_vector(drug_side_effects2)

        return cosine_similarity([drug_side_effects1], [drug_side_effects2])[0][0]