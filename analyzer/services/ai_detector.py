import re
import math
from collections import Counter
import numpy as np


class AIDetector:
    """
    Detects AI-generated content using statistical analysis.
    Analyzes patterns that are common in AI-generated text.
    """

    def __init__(self):
        # Common AI writing patterns
        self.ai_indicators = {
            'transition_words': [
                'furthermore', 'moreover', 'additionally', 'consequently',
                'nevertheless', 'subsequently', 'accordingly', 'hence',
                'thus', 'therefore', 'likewise', 'similarly'
            ],
            'filler_phrases': [
                'it is important to note',
                'it is worth mentioning',
                'in this context',
                'in other words',
                'to put it simply',
                'as mentioned earlier',
                'as previously stated',
                'it goes without saying',
                'needless to say',
                'for the most part'
            ],
            'hedge_words': [
                'somewhat', 'relatively', 'generally', 'typically',
                'usually', 'often', 'perhaps', 'possibly', 'likely',
                'essentially', 'basically', 'fundamentally'
            ],
            'formal_constructions': [
                r'it is .+ that',
                r'there (is|are) .+ that',
                r'this (suggests|indicates|demonstrates|shows) that',
                r'(one|we) (can|could|may|might) (argue|say|suggest)',
            ]
        }

    def analyze(self, text: str) -> dict:
        """
        Analyze text for AI-generated content indicators.
        Returns comprehensive analysis with score and explanations.
        """
        if not text.strip():
            return {
                'score': 0.0,
                'indicators': [],
                'details': 'Empty text provided'
            }

        result = {
            'score': 0.0,
            'indicators': [],
            'sentence_analysis': [],
            'statistical_features': {},
            'explanation': []
        }

        sentences = self._get_sentences(text)

        # Run all analyses
        transition_score = self._analyze_transitions(text)
        filler_score = self._analyze_fillers(text)
        hedge_score = self._analyze_hedging(text)
        uniformity_score = self._analyze_sentence_uniformity(sentences)
        perplexity_estimate = self._estimate_perplexity(text)
        burstiness_score = self._calculate_burstiness(sentences)
        vocabulary_score = self._analyze_vocabulary_richness(text)

        # Store detailed metrics
        result['statistical_features'] = {
            'transition_density': transition_score,
            'filler_density': filler_score,
            'hedge_density': hedge_score,
            'sentence_uniformity': uniformity_score,
            'perplexity_estimate': perplexity_estimate,
            'burstiness': burstiness_score,
            'vocabulary_richness': vocabulary_score
        }

        # Build indicators list with explanations
        if transition_score > 3:
            result['indicators'].append({
                'type': 'High transition word density',
                'severity': 'medium' if transition_score < 5 else 'high',
                'explanation': 'AI tends to use many formal transition words'
            })

        if filler_score > 2:
            result['indicators'].append({
                'type': 'Filler phrase usage',
                'severity': 'medium' if filler_score < 4 else 'high',
                'explanation': 'Common AI padding phrases detected'
            })

        if uniformity_score > 70:
            result['indicators'].append({
                'type': 'Uniform sentence structure',
                'severity': 'medium' if uniformity_score < 80 else 'high',
                'explanation': 'Sentences are too similar in length - humans vary more'
            })

        if burstiness_score < 30:
            result['indicators'].append({
                'type': 'Low burstiness',
                'severity': 'medium' if burstiness_score > 20 else 'high',
                'explanation': 'Human writing has more variation in complexity (burstiness)'
            })

        if vocabulary_score < 0.4:
            result['indicators'].append({
                'type': 'Limited vocabulary variety',
                'severity': 'low',
                'explanation': 'AI often uses a more limited, formal vocabulary'
            })

        # Analyze individual sentences
        result['sentence_analysis'] = self._analyze_sentences(sentences)

        # Calculate final score (0-100, higher = more likely AI)
        weights = {
            'transition': 0.15,
            'filler': 0.15,
            'hedge': 0.10,
            'uniformity': 0.25,
            'burstiness': 0.20,
            'vocabulary': 0.15
        }

        # Normalize scores to 0-100
        normalized_scores = {
            'transition': min(100, transition_score * 15),
            'filler': min(100, filler_score * 20),
            'hedge': min(100, hedge_score * 15),
            'uniformity': uniformity_score,
            'burstiness': 100 - burstiness_score,  # Invert - low burstiness = more AI-like
            'vocabulary': (1 - vocabulary_score) * 100  # Invert - low variety = more AI-like
        }

        final_score = sum(
            normalized_scores[key] * weights[key]
            for key in weights
        )

        result['score'] = min(100, max(0, final_score))
        result['explanation'] = self._generate_explanation(result)

        return result

    def _get_sentences(self, text: str) -> list:
        """Split text into sentences"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]

    def _analyze_transitions(self, text: str) -> float:
        """Count transition word density"""
        words = text.lower().split()
        if not words:
            return 0

        count = sum(1 for word in words if word in self.ai_indicators['transition_words'])
        return (count / len(words)) * 100

    def _analyze_fillers(self, text: str) -> float:
        """Count filler phrase density"""
        text_lower = text.lower()
        word_count = len(text.split())
        if not word_count:
            return 0

        count = sum(1 for phrase in self.ai_indicators['filler_phrases']
                    if phrase in text_lower)
        return (count / word_count) * 100

    def _analyze_hedging(self, text: str) -> float:
        """Count hedge word density"""
        words = text.lower().split()
        if not words:
            return 0

        count = sum(1 for word in words if word in self.ai_indicators['hedge_words'])
        return (count / len(words)) * 100

    def _analyze_sentence_uniformity(self, sentences: list) -> float:
        """
        Measure how uniform sentence lengths are.
        AI tends to produce more uniform sentence structures.
        """
        if len(sentences) < 3:
            return 50  # Not enough data

        lengths = [len(s.split()) for s in sentences]
        mean_length = np.mean(lengths)
        std_dev = np.std(lengths)

        if mean_length == 0:
            return 50

        # Coefficient of variation (lower = more uniform = more AI-like)
        cv = (std_dev / mean_length) * 100

        # Invert and scale: low CV (uniform) = high score
        uniformity = max(0, 100 - cv * 2)
        return uniformity

    def _estimate_perplexity(self, text: str) -> float:
        """
        Estimate text predictability (simplified perplexity proxy).
        AI text tends to be more predictable.
        """
        words = text.lower().split()
        if len(words) < 10:
            return 50

        # Use word frequency as a proxy for predictability
        word_freq = Counter(words)
        total = len(words)
        unique = len(word_freq)

        # Entropy calculation
        entropy = -sum((count / total) * math.log2(count / total)
                       for count in word_freq.values())

        # Normalize to 0-100 scale
        max_entropy = math.log2(unique) if unique > 1 else 1
        normalized = (entropy / max_entropy) * 100 if max_entropy > 0 else 50

        return normalized

    def _calculate_burstiness(self, sentences: list) -> float:
        """
        Calculate burstiness - variation in sentence complexity.
        Human writing is more 'bursty' with varying complexity.
        """
        if len(sentences) < 3:
            return 50

        # Measure complexity by word length and sentence length
        complexities = []
        for sentence in sentences:
            words = sentence.split()
            if words:
                avg_word_length = np.mean([len(w) for w in words])
                sentence_length = len(words)
                complexity = avg_word_length * math.log(sentence_length + 1)
                complexities.append(complexity)

        if not complexities:
            return 50

        # Burstiness = variance in complexity
        variance = np.var(complexities)
        mean = np.mean(complexities)

        if mean == 0:
            return 50

        # Coefficient of variation as burstiness measure
        burstiness = (math.sqrt(variance) / mean) * 100
        return min(100, burstiness * 2)

    def _analyze_vocabulary_richness(self, text: str) -> float:
        """
        Measure vocabulary diversity.
        Type-Token Ratio (TTR) - unique words / total words
        """
        words = re.findall(r'\b[a-z]+\b', text.lower())
        if not words:
            return 0.5

        unique_words = set(words)
        ttr = len(unique_words) / len(words)

        return ttr

    def _analyze_sentences(self, sentences: list) -> list:
        """Analyze individual sentences for AI indicators"""
        analysis = []

        for i, sentence in enumerate(sentences[:20]):  # Limit to first 20
            score = 0
            flags = []

            # Check for formal constructions
            for pattern in self.ai_indicators['formal_constructions']:
                if re.search(pattern, sentence.lower()):
                    score += 20
                    flags.append('Formal construction pattern')

            # Check sentence start
            starts_with_transition = any(
                sentence.lower().startswith(word)
                for word in self.ai_indicators['transition_words']
            )
            if starts_with_transition:
                score += 15
                flags.append('Starts with transition word')

            analysis.append({
                'index': i,
                'text': sentence[:100] + '...' if len(sentence) > 100 else sentence,
                'ai_score': min(100, score),
                'flags': flags
            })

        return analysis

    def _generate_explanation(self, result: dict) -> list:
        """Generate human-readable explanation of the analysis"""
        explanations = []
        score = result['score']

        if score < 30:
            explanations.append("This text shows characteristics typical of human writing.")
        elif score < 50:
            explanations.append("This text has some AI-like patterns but also human characteristics.")
        elif score < 70:
            explanations.append("This text shows several patterns common in AI-generated content.")
        else:
            explanations.append("This text has strong indicators of AI-generated content.")

        # Add specific insights
        features = result['statistical_features']

        if features['burstiness'] < 30:
            explanations.append(
                "The writing has very consistent complexity throughout. "
                "Human writing typically varies more - some sentences simple, some complex."
            )

        if features['sentence_uniformity'] > 70:
            explanations.append(
                "Sentences are very similar in length. "
                "Try varying your sentence structure for a more natural flow."
            )

        return explanations
