from Bio import Align
from Bio.Align import substitution_matrices
from typing import Tuple


class SequenceAligner:
    def align_local_dna_sequence(self, seq1:str, seq2: str) -> Tuple[Align.Alignment, float]:
        min_length = min(len(seq1), len(seq2))

        aligner = Align.PairwiseAligner()       
        aligner.mode = 'local'
        
        alignments = aligner.align(seq1, seq2)
       
        best_alignment = max(alignments, key=lambda x: x.score)
        best_normalized_score = best_alignment.score / min_length

        return best_alignment, best_normalized_score
    
    def align_local_protein_sequence(self, seq1:str, seq2: str, blossum_matrix: str ='BLOSUM62') -> Tuple[Align.Alignment, float]:
        shorter_seq = seq2 if len(seq2) < len(seq1) else seq1
        blosum_matrix = substitution_matrices.load(blossum_matrix)

        aligner = Align.PairwiseAligner()
        aligner.substitution_matrix = blosum_matrix
        aligner.mode = 'local'
        
        alignments = aligner.align(seq1, seq2)
       
        best_alignment = max(alignments, key=lambda x: x.score)
        max_score = sum(blosum_matrix[(x, x)] for x in shorter_seq)
    
        best_normalized_score = best_alignment.score / max_score

        return best_alignment, best_normalized_score
    
