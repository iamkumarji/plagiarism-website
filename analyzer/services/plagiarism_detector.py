import re
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class PlagiarismDetector:
    """
    Detects plagiarism by comparing text against a corpus of documents.
    Uses TF-IDF and cosine similarity for comparison.
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            stop_words='english',
            min_df=1
        )
        self.corpus = []
        self.corpus_sources = []

    def add_to_corpus(self, text: str, source: str = "Unknown"):
        """Add a document to the comparison corpus"""
        self.corpus.append(text)
        self.corpus_sources.append(source)

    def preprocess_text(self, text: str) -> str:
        """Clean and normalize text"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def get_sentences(self, text: str) -> list:
        """Split text into sentences"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def get_ngrams(self, text: str, n: int = 5) -> set:
        """Generate n-grams from text for comparison"""
        words = text.split()
        if len(words) < n:
            return {tuple(words)}
        return {tuple(words[i:i+n]) for i in range(len(words) - n + 1)}

    def analyze(self, text: str) -> dict:
        """
        Analyze text for potential plagiarism.
        Returns score and detailed breakdown.
        """
        if not text.strip():
            return {
                'score': 0.0,
                'flagged_sentences': [],
                'details': 'Empty text provided'
            }

        processed_text = self.preprocess_text(text)
        sentences = self.get_sentences(text)

        result = {
            'score': 0.0,
            'flagged_sentences': [],
            'sentence_scores': [],
            'common_phrases': [],
            'details': {}
        }

        # Check against corpus if available
        if self.corpus:
            result.update(self._check_against_corpus(processed_text, sentences))

        # Check for common academic phrases (often indicates copied content)
        common_phrases = self._detect_common_phrases(text)
        result['common_phrases'] = common_phrases

        # Calculate overall score
        internal_score = self._calculate_internal_similarity(sentences)
        result['internal_similarity'] = internal_score

        # Weighted final score
        if self.corpus:
            result['score'] = min(100, result.get('corpus_score', 0) * 0.7 + len(common_phrases) * 5)
        else:
            result['score'] = min(100, len(common_phrases) * 10 + internal_score * 0.3)

        return result

    def _check_against_corpus(self, text: str, sentences: list) -> dict:
        """Compare text against stored corpus"""
        all_texts = self.corpus + [text]

        try:
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]

            flagged = []
            for i, (sim, source) in enumerate(zip(similarities, self.corpus_sources)):
                if sim > 0.3:  # Threshold for flagging
                    flagged.append({
                        'source': source,
                        'similarity': float(sim),
                        'match_index': i
                    })

            max_similarity = float(max(similarities)) if len(similarities) > 0 else 0.0

            return {
                'corpus_score': max_similarity * 100,
                'flagged_matches': flagged
            }
        except ValueError:
            return {'corpus_score': 0, 'flagged_matches': []}

    def _detect_common_phrases(self, text: str) -> list:
        """Detect commonly copied academic phrases"""
        common_patterns = [
            r'according to (the )?(research|study|findings)',
            r'it (is|has been) (widely )?(known|accepted|believed)',
            r'in (this|the) (context|regard|respect)',
            r'(plays|play) (a |an )?(important|crucial|vital|key) role',
            r'in (recent|modern) (years|times)',
            r'(has|have) (become|been) (increasingly|more)',
            r'it (is|can be) (argued|said|noted) that',
            r'(first|second|third)(ly)?[,\s]',
            r'in (conclusion|summary)',
            r'on the other hand',
            r'as (a |)result',
            r'due to (the fact|this)',
        ]

        found_phrases = []
        text_lower = text.lower()

        for pattern in common_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                found_phrases.append({
                    'pattern': pattern,
                    'count': len(matches)
                })

        return found_phrases

    def _calculate_internal_similarity(self, sentences: list) -> float:
        """Check for repetitive content within the document"""
        if len(sentences) < 2:
            return 0.0

        try:
            tfidf_matrix = self.vectorizer.fit_transform(sentences)
            similarity_matrix = cosine_similarity(tfidf_matrix)

            # Get upper triangle (excluding diagonal)
            upper_triangle = similarity_matrix[np.triu_indices(len(sentences), k=1)]

            if len(upper_triangle) == 0:
                return 0.0

            # High internal similarity might indicate repetition
            return float(np.mean(upper_triangle) * 100)
        except ValueError:
            return 0.0
