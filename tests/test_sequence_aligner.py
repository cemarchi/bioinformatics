import unittest
from parameterized import parameterized, param

from src.sequence_aligner import SequenceAligner


class TestSequenceAligner(unittest.TestCase):

    @parameterized.expand([
        ('AGCTGACCTGACTGACGTCA', 'AGCTGACCTGACTGACGTCA'),
        ('AGCTGACCTGACTGACGTCA', 'AGCTGACCTGACTGACGT'),
        ('AGCTGACCTGACTGACGTCA', 'GCTGACTGACGTCACTGACC'),
        ('AGCTGACCTGACTGACGTCA', 'GCTGACTGACGTCAC'),
        ('AGCTGACCTGACTGACGTCA', 'GCTGACTGACG'),
        ('AGCTGACCTGACTGACGTCA', 'GTCCTGAAATCG')])
    def test_local_dna_sequence_align_returns_best_alignment_and_normalized_score(self, seq1:str, seq2:str):
        aligner = SequenceAligner()
        best_alignment, normalized_score = aligner.align_local_dna_sequence(seq1, seq2)

        self.assertIsNotNone(best_alignment)
        self.assertGreaterEqual(normalized_score, 0)

    @parameterized.expand([
        ('MKTIIALSYIFCLVFADYKDDDDK', 'MKTIIALSYIFCLVFADYKDDDDK'),
        ('MKTIIALSYIFCLVFADYKDDDDK', 'MKTIIALSYIFCLVFADYKKD'),
        ('MEEPQSDPSVEPPLSQETFS', 'MDDLMLSPDDIEQWFTEDPG'),
        ('MEEPQSDPSVEPPLSQETFS', 'MFCQLAKTCPVQLWVDSTPP'),
        ('MEEPQSDPSVEPPLSQETFS', 'HYNYMCNSSCMGGMNRRPIL'),
        ('MEEPQSDPSVEPPLSQETFS', 'MEEPQSDPSVEPPLSQETFS')])
    def test_align_local_protein_sequence_returns_best_alignment_and_normalized_score(self, seq1:str, seq2:str):
        aligner = SequenceAligner()
        best_alignment, normalized_score = aligner.align_local_protein_sequence(seq1, seq2)

        self.assertIsNotNone(best_alignment)
        self.assertGreaterEqual(normalized_score, 0)