from Bio import Align
from typing import Tuple


class SequenceAligner:
    def align_local_dna_sequence(self, seq1:str, seq2: str) -> Tuple[Align.Alignment, float]:
        max_length = max(len(seq1), len(seq2))

        aligner = Align.PairwiseAligner()
        aligner.mode = 'local'
        
        alignments = aligner.align(seq1, seq2)
       
        best_alignment = max(alignments, key=lambda x: x.score)
        best_normalized_score = best_alignment.score / max_length

        return best_alignment, best_normalized_score
