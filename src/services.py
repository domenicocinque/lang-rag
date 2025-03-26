import re
import logging
from collections import Counter
from typing import List

logger = logging.getLogger(__name__)


def _get_ngrams(words: List[str], n: int) -> List[str]:
    """
    Generate n-grams from a list of words.

    Args:
        words (List[str]): List of words to generate n-grams from.
        n (int): The size of the n-grams to generate.

    Returns:
        List[str]: List of n-grams.
    """
    return [" ".join(words[i : i + n]) for i in range(len(words) - n + 1)]


def detect_stammering(sentence: str) -> bool:
    """
    Detect if a sentence contains stammering patterns.

    Args:
        sentence (str): The sentence to check for stammering.

    Returns:
        bool: True if stammering is detected, False otherwise.
    """
    if not sentence.strip():
        raise ValueError("Input sentence cannot be empty")

    try:
        words = sentence.lower().split()

        ngrams = []
        for n in (2, 3):
            ngrams.extend(_get_ngrams(words, n))

        ngram_counts = Counter(ngrams)
        if any(count >= 2 for count in ngram_counts.values()):
            logger.debug(f"Detected repeated n-grams in sentence: {sentence}")
            return True

        if re.search(r"(.)\1{5,}", sentence):
            logger.debug(f"Detected repeated characters in sentence: {sentence}")
            return True

        return False
    except Exception as e:
        logger.error(f"Error detecting stammering in sentence '{sentence}': {e}")
        raise
