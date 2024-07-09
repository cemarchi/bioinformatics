from typing import List
from statistics import mean
import numpy as np
from itertools import zip_longest, chain
from rdkit import DataStructs

class ATCSimilarity:
    def __parse_atc_code(self, drug_atc_code:str, level:bool) -> List[str]:
        return [drug_atc_code[:1], drug_atc_code[1:3], drug_atc_code[3:4], drug_atc_code[4:5], drug_atc_code[5:]][:level]

    def __create_bitvector(self, drug_atc_code: List[str], all_atc_codes: List[str]):
        drug_bitvector = DataStructs.ExplicitBitVect(len(list(chain(*all_atc_codes))))
        i = 0
        j = 0

        for atc_codes in all_atc_codes:
            for atc_code in atc_codes:
                if atc_code == drug_atc_code[i]:
                    drug_bitvector.SetBit(j)
                j+=1
            i+=1

        return drug_bitvector

    def __tanimoto_similarity(self, drug_atc_code1: List[str], drug_atc_code2: List[str], level: int):
        drug_atc_code1 = self.__parse_atc_code(drug_atc_code1,4)
        drug_atc_code2 = self.__parse_atc_code(drug_atc_code2,4)

        all_atc_codes = [list(set(atc_codes)) for atc_codes in zip_longest(drug_atc_code1, drug_atc_code2, fillvalue=None)]

        drug_atc_code_bitvector1 = self.__create_bitvector(drug_atc_code1, all_atc_codes)
        drug_atc_code_bitvector2 = self.__create_bitvector(drug_atc_code2, all_atc_codes)

        return DataStructs.TanimotoSimilarity(drug_atc_code_bitvector1, drug_atc_code_bitvector2)

    def are_similar(self, drug_atc_codes1: List[str], drug_atc_codes2: List[str], level: int) -> float:
        similaties = [self.__tanimoto_similarity(drug_atc_code1, drug_atc_code2, level) 
                        for drug_atc_code1 in drug_atc_codes1 
                        for drug_atc_code2 in drug_atc_codes2]
                        
        return mean(similaties)