import fastsemsim
import numpy as np

class GOSimilarity:
    MOLECULAR_FUNCTION_CATEGORY = 'molecular_function'
    BIOLOGICAL_PROCESS_CATEGORY = 'biological_process'
    CELLULAR_COMPONENT = 'cellular_component'

    def __init__(self, obo_file, gaf_file):
        self.__ontology = fastsemsim.load_ontology(source_file=obo_file, file_type='obo', ontology_type='GeneOntology')
        self.__annotation_corpus = fastsemsim.load_ac(self.__ontology, source_file=gaf_file, file_type='gaf-2.0')
            
    def is_semantic_similar(self, protein_id1:str, protein_id2:str, go_term_category:str='molecular_function'):           
        go_semantic_similarity = fastsemsim.init_batchsemsim(ontology=self.__ontology, 
                                                             ac=self.__annotation_corpus, 
                                                             semsim_type = 'obj', 
                                                             semsim_measure = 'Resnik', 
                                                             mixing_strategy = 'BMA')

        go_semantic_similarity.set_root(go_term_category)
        go_semantic_similarity_result = go_semantic_similarity.SemSim(query=[protein_id1, protein_id2], query_type='pairwise')

        score = go_semantic_similarity_result.loc[(go_semantic_similarity_result['obj_1'] == protein_id1) & 
                                                  (go_semantic_similarity_result['obj_2'] == protein_id2), 'ss'].values[0]

        if np.isnan(score):
            return -1

        max_score = go_semantic_similarity_result.loc[(go_semantic_similarity_result['obj_1'] == protein_id1) & 
                                                      (go_semantic_similarity_result['obj_2'] == protein_id1), 'ss'].values[0]

        #normalized score
        return score / max_score 