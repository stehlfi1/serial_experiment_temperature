"""
Simple BLEU calculator for Python code similarity.
Implements standard BLEU metric without external dependencies.
"""

import math
from collections import Counter
from typing import List, Tuple


class BLEUCalculator:
    """Calculate BLEU score for code similarity."""

    def __init__(self, max_n: int = 4):
        """
        Initialize BLEU calculator.

        Args:
            max_n: Maximum n-gram size (default 4 for BLEU-4)
        """
        self.max_n = max_n

    def tokenize(self, code: str) -> List[str]:
        """
        Tokenize code into words/tokens.
        Simple whitespace and punctuation-aware tokenization.
        """
        # Split on whitespace and common separators
        import re
        # Keep important separators as tokens
        tokens = re.findall(r'\w+|[^\w\s]', code)
        return [t for t in tokens if t.strip()]

    def get_ngrams(self, tokens: List[str], n: int) -> Counter:
        """
        Extract n-grams from token list.

        Args:
            tokens: List of tokens
            n: N-gram size

        Returns:
            Counter of n-grams
        """
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i+n])
            ngrams.append(ngram)
        return Counter(ngrams)

    def modified_precision(self, reference_ngrams: Counter,
                          candidate_ngrams: Counter) -> Tuple[int, int]:
        """
        Calculate modified precision for n-grams.

        Returns:
            Tuple of (clipped_count, total_count)
        """
        clipped_count = 0
        total_count = sum(candidate_ngrams.values())

        for ngram, count in candidate_ngrams.items():
            # Clip count to reference count (modified precision)
            ref_count = reference_ngrams.get(ngram, 0)
            clipped_count += min(count, ref_count)

        return clipped_count, total_count

    def brevity_penalty(self, ref_len: int, cand_len: int) -> float:
        """
        Calculate brevity penalty.
        Penalizes candidates shorter than reference.
        """
        if cand_len > ref_len:
            return 1.0
        elif cand_len == 0:
            return 0.0
        else:
            return math.exp(1 - ref_len / cand_len)

    def calculate_bleu(self, reference: str, candidate: str) -> float:
        """
        Calculate BLEU score between reference and candidate code.

        Args:
            reference: Reference code string
            candidate: Candidate code string

        Returns:
            BLEU score (0.0 to 1.0)
        """
        # Tokenize
        ref_tokens = self.tokenize(reference)
        cand_tokens = self.tokenize(candidate)

        if not ref_tokens or not cand_tokens:
            return 0.0

        # Calculate n-gram precisions
        precisions = []
        for n in range(1, self.max_n + 1):
            ref_ngrams = self.get_ngrams(ref_tokens, n)
            cand_ngrams = self.get_ngrams(cand_tokens, n)

            if not cand_ngrams:
                precisions.append(0.0)
                continue

            clipped, total = self.modified_precision(ref_ngrams, cand_ngrams)

            if total == 0:
                precisions.append(0.0)
            else:
                precisions.append(clipped / total)

        # Calculate geometric mean of precisions
        # Use log to avoid underflow
        if any(p == 0.0 for p in precisions):
            # If any precision is 0, BLEU is 0 (with smoothing we could handle this)
            geo_mean = 0.0
        else:
            log_sum = sum(math.log(p) for p in precisions)
            geo_mean = math.exp(log_sum / len(precisions))

        # Apply brevity penalty
        bp = self.brevity_penalty(len(ref_tokens), len(cand_tokens))

        return bp * geo_mean

    def calculate_from_files(self, ref_path: str, cand_path: str) -> float:
        """
        Calculate BLEU score from file paths.

        Args:
            ref_path: Path to reference code file
            cand_path: Path to candidate code file

        Returns:
            BLEU score (0.0 to 1.0)
        """
        with open(ref_path, 'r', encoding='utf-8') as f:
            reference = f.read()
        with open(cand_path, 'r', encoding='utf-8') as f:
            candidate = f.read()

        return self.calculate_bleu(reference, candidate)


if __name__ == "__main__":
    # Test the BLEU calculator
    calc = BLEUCalculator()

    # Test 1: Identical code
    code1 = """
def add(a, b):
    return a + b

result = add(1, 2)
print(result)
"""
    bleu1 = calc.calculate_bleu(code1, code1)
    print(f"Identical code BLEU: {bleu1:.4f}")

    # Test 2: Similar code (renamed variables)
    code2 = """
def add(x, y):
    return x + y

result = add(1, 2)
print(result)
"""
    bleu2 = calc.calculate_bleu(code1, code2)
    print(f"Similar code BLEU: {bleu2:.4f}")

    # Test 3: Different code
    code3 = """
def multiply(a, b):
    result = a * b
    return result
"""
    bleu3 = calc.calculate_bleu(code1, code3)
    print(f"Different code BLEU: {bleu3:.4f}")
