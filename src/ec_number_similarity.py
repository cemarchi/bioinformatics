from typing import List, Dict
from statistics import mean
import numpy as np
from itertools import zip_longest, chain
from rdkit import DataStructs

class ECNumberSimilarity:
    def __init__(self, all_ec_number_classes:Dict[str, str]):
        self.__all_ec_number_classes = all_ec_number_classes
        self.__all_ec_classes = list(sorted(set(all_ec_number_classes.values())))

    def __extract_ec_numbers(self, ec_number:str) -> List[str]:
        levels = ec_number.split(".")
        return  [".".join(levels[:i]) for i in range(1, len(levels))]
    
    def __ec_number_to_classes(self, ec_numbers:List[str]):
        return [self.__all_ec_number_classes[ec_number] for ec_number in ec_numbers]        

    def __create_bitvector(self, ec_number_classes:List[str]):
        ec_class_bitvector = DataStructs.ExplicitBitVect(len(self.__all_ec_classes))
        i = 0

        for ec_class in self.__all_ec_classes:
            if ec_class in ec_number_classes:
                ec_class_bitvector.SetBit(i)
            i+=1

        return ec_class_bitvector

    def __tanimoto_similarity(self, ec_classes1:List[str], ec_classes2:List[str]):
        ec_classes_bitvector1 = self.__create_bitvector(ec_classes1)
        ec_classes_bitvector2 = self.__create_bitvector(ec_classes2)

        return DataStructs.TanimotoSimilarity(ec_classes_bitvector1, ec_classes_bitvector2)

    def are_similar(self, ec_number1:str, ec_number2:str) -> float:
        ec_numbers1 = self.__extract_ec_numbers(ec_number1)
        ec_numbers2 = self.__extract_ec_numbers(ec_number2)

        ec_classes1 = self.__ec_number_to_classes(ec_numbers1)
        ec_classes2 = self.__ec_number_to_classes(ec_numbers2)

        return self.__tanimoto_similarity(ec_classes1, ec_classes2)