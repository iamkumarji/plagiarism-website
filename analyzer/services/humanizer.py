import re
import random


class Humanizer:
    """
    Provides suggestions for making AI-detected text more human-like.
    Educational tool to help students understand writing patterns.
    """

    def __init__(self):
        self.transition_alternatives = {
            'furthermore': ['also', 'plus', 'and', 'what\'s more'],
            'moreover': ['besides', 'also', 'and'],
            'additionally': ['also', 'plus', 'another thing is'],
            'consequently': ['so', 'because of this', 'as a result'],
            'nevertheless': ['still', 'even so', 'but'],
            'subsequently': ['then', 'after that', 'next'],
            'accordingly': ['so', 'therefore'],
            'hence': ['so', 'that\'s why'],
            'thus': ['so', 'this means'],
            'therefore': ['so', 'that\'s why', 'because of this'],
            'likewise': ['similarly', 'in the same way', 'also'],
            'however': ['but', 'still', 'yet', 'though'],
        }

        self.filler_phrase_suggestions = {
            'it is important to note': [
                'Note that',
                'Keep in mind',
                'Remember',
                'One key point:'
            ],
            'it is worth mentioning': [
                'Also',
                'Interestingly',
                'Here\'s something else:'
            ],
            'in other words': [
                'Put simply',
                'Basically',
                'This means'
            ],
            'as mentioned earlier': [
                'As I said',
                'Going back to',
                'Earlier I mentioned'
            ],
            'it goes without saying': [
                'Obviously',
                'Clearly',
                'Of course'
            ],
            'in this context': [
                'Here',
                'In this case',
                'With this'
            ],
        }

        self.sentence_variety_tips = [
            "Try starting with an action: 'Running through the data revealed...'",
            "Use a question: 'What does this mean for...?'",
            "Start with 'I' or 'We' to make it personal",
            "Begin with a short, punchy statement",
            "Try an example: 'Take the case of...'",
            "Use contrast: 'Unlike X, this Y...'",
        ]

        # Additional phrases to make text more human
        self.formal_to_casual = {
            'utilize': 'use',
            'implement': 'put in place',
            'facilitate': 'help',
            'subsequent': 'later',
            'prior to': 'before',
            'in order to': 'to',
            'due to the fact that': 'because',
            'at this point in time': 'now',
            'in the event that': 'if',
            'for the purpose of': 'to',
            'with regard to': 'about',
            'in regard to': 'about',
            'pertaining to': 'about',
            'in light of': 'because of',
            'on the basis of': 'based on',
            'in spite of the fact that': 'although',
            'a large number of': 'many',
            'a significant amount of': 'much',
            'the vast majority of': 'most',
            'plays a crucial role': 'is key',
            'plays an important role': 'matters',
            'it is evident that': 'clearly',
            'it is apparent that': 'clearly',
            'there is no doubt that': 'certainly',
            'it should be noted that': 'note that',
            'it is interesting to note that': 'interestingly',
        }

        # Sentence starters to add variety
        self.human_starters = [
            "Here's the thing:",
            "What's interesting is",
            "The key point?",
            "Simply put,",
            "Look,",
            "Think about it:",
            "Here's what matters:",
            "The reality is",
            "Let's be clear:",
            "Consider this:",
        ]

    def analyze_and_suggest(self, text: str, ai_analysis: dict) -> dict:
        """
        Generate rewriting suggestions based on AI analysis.
        Educational focus: explain WHY and HOW to improve.
        """
        if not text.strip():
            return {'suggestions': [], 'general_tips': []}

        sentences = self._get_sentences(text)

        result = {
            'suggestions': [],
            'general_tips': [],
            'learning_points': [],
            'before_after_examples': [],
            'full_humanized_text': '',
            'humanization_changes': []
        }

        # Generate sentence-level suggestions
        for i, sentence in enumerate(sentences[:15]):  # Limit processing
            suggestion = self._analyze_sentence(sentence, i)
            if suggestion:
                result['suggestions'].append(suggestion)

        # Add general writing tips based on AI analysis
        result['general_tips'] = self._generate_tips(ai_analysis)

        # Add learning points
        result['learning_points'] = self._generate_learning_points(ai_analysis)

        # Generate before/after examples
        result['before_after_examples'] = self._generate_examples(sentences[:5])

        # Generate full humanized version of the text
        humanized_text, changes = self._generate_full_humanized_text(text, sentences)
        result['full_humanized_text'] = humanized_text
        result['humanization_changes'] = changes

        return result

    def _get_sentences(self, text: str) -> list:
        """Split text into sentences"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]

    def _analyze_sentence(self, sentence: str, index: int) -> dict:
        """Analyze a single sentence and provide suggestions"""
        suggestions = []
        original = sentence
        improved = sentence

        # Check for transition words at start
        words = sentence.lower().split()
        if words:
            first_word = words[0].rstrip('.,;:')
            if first_word in self.transition_alternatives:
                alternatives = self.transition_alternatives[first_word]
                suggestions.append({
                    'issue': f"Starts with formal transition '{first_word}'",
                    'fix': f"Try: {', '.join(alternatives)}",
                    'explanation': "Formal transitions can make writing sound robotic"
                })
                # Create improved version
                alt = random.choice(alternatives)
                improved = alt.capitalize() + sentence[len(first_word):]

        # Check for filler phrases
        sentence_lower = sentence.lower()
        for phrase, alternatives in self.filler_phrase_suggestions.items():
            if phrase in sentence_lower:
                suggestions.append({
                    'issue': f"Contains filler phrase: '{phrase}'",
                    'fix': f"Try: {', '.join(alternatives)}",
                    'explanation': "This phrase adds words without adding meaning"
                })

        # Check sentence length
        word_count = len(words)
        if word_count > 35:
            suggestions.append({
                'issue': "Very long sentence",
                'fix': "Consider breaking into 2-3 shorter sentences",
                'explanation': "Long sentences can be hard to follow. Vary your length."
            })
        elif word_count < 5 and index > 0:
            suggestions.append({
                'issue': "Very short sentence",
                'fix': "This is fine! Short sentences add punch.",
                'explanation': "Mixing short and long sentences creates rhythm."
            })

        # Check for passive voice patterns
        passive_patterns = [
            r'(is|are|was|were|been|being)\s+\w+ed\b',
            r'(has|have|had)\s+been\s+\w+ed\b'
        ]
        for pattern in passive_patterns:
            if re.search(pattern, sentence_lower):
                suggestions.append({
                    'issue': "Possible passive voice",
                    'fix': "Try active voice: Subject + Verb + Object",
                    'explanation': "Active voice is usually clearer and more engaging"
                })
                break

        if not suggestions:
            return None

        return {
            'index': index,
            'original': original,
            'improved': improved if improved != original else None,
            'suggestions': suggestions
        }

    def _generate_tips(self, ai_analysis: dict) -> list:
        """Generate general writing tips based on AI analysis"""
        tips = []
        features = ai_analysis.get('statistical_features', {})

        if features.get('sentence_uniformity', 0) > 70:
            tips.append({
                'title': 'Vary Your Sentence Length',
                'tip': 'Your sentences are similar in length. Mix it up! '
                       'Use some short punchy sentences. Then follow with longer, '
                       'more detailed explanations when needed.',
                'example': 'Before: "The data shows clear patterns. The results indicate growth. '
                           'The analysis reveals trends."\n'
                           'After: "The data speaks. Clear patterns emerge - growth, trends, '
                           'undeniable progress that the numbers can\'t hide."'
            })

        if features.get('burstiness', 100) < 30:
            tips.append({
                'title': 'Add Complexity Variation',
                'tip': 'Your writing has consistent complexity throughout. '
                       'Humans naturally write with "bursts" - simple ideas followed '
                       'by complex analysis, then back to simple.',
                'example': 'Try: Start with a simple statement. Then dive deep into details. '
                           'Then come back up for air with another simple point.'
            })

        if features.get('transition_density', 0) > 3:
            tips.append({
                'title': 'Reduce Formal Transitions',
                'tip': 'You\'re using many formal transition words (furthermore, moreover, etc.). '
                       'These are fine in academic writing, but too many sounds robotic.',
                'example': 'Instead of "Furthermore, the study shows..." try "The study also shows..." '
                           'or just "Plus, ..."'
            })

        return tips

    def _generate_learning_points(self, ai_analysis: dict) -> list:
        """Generate educational takeaways"""
        points = []

        points.append({
            'concept': 'Sentence Rhythm',
            'explanation': 'Good writing has rhythm. Read your work aloud. '
                          'Does it flow naturally? Does it sound like YOU talking?',
            'exercise': 'Read one paragraph aloud. Mark sentences that feel awkward. '
                       'Rewrite those in your own voice.'
        })

        points.append({
            'concept': 'Show Your Thinking',
            'explanation': 'AI writes "correctly" but impersonally. Your unique perspective, '
                          'uncertainties, and personal examples make writing human.',
            'exercise': 'Add one personal example or opinion to each main point. '
                       'Use "I think" or "In my experience" where appropriate.'
        })

        points.append({
            'concept': 'Imperfection is Human',
            'explanation': 'Perfectly structured prose can feel artificial. '
                          'Real writing has character - informal asides, questions, '
                          'even occasional rule-breaking.',
            'exercise': 'Add a rhetorical question. Use a sentence fragment for emphasis. '
                       'Include a personal aside in parentheses.'
        })

        return points

    def _generate_examples(self, sentences: list) -> list:
        """Generate before/after rewriting examples"""
        examples = []

        for i, sentence in enumerate(sentences[:3]):
            rewrite = self._humanize_sentence(sentence)
            if rewrite != sentence:
                examples.append({
                    'before': sentence,
                    'after': rewrite,
                    'explanation': self._explain_changes(sentence, rewrite)
                })

        return examples

    def _humanize_sentence(self, sentence: str) -> str:
        """Attempt to rewrite a sentence in a more human style"""
        result = sentence

        # Replace formal transitions
        words = result.split()
        if words:
            first_word_lower = words[0].lower().rstrip('.,;:')
            if first_word_lower in self.transition_alternatives:
                alt = random.choice(self.transition_alternatives[first_word_lower])
                result = alt.capitalize() + result[len(words[0]):]

        # Replace filler phrases
        result_lower = result.lower()
        for phrase, alternatives in self.filler_phrase_suggestions.items():
            if phrase in result_lower:
                alt = random.choice(alternatives)
                result = re.sub(re.escape(phrase), alt, result, flags=re.IGNORECASE)
                break

        return result

    def _explain_changes(self, original: str, rewritten: str) -> str:
        """Explain what changed between original and rewritten"""
        explanations = []

        orig_words = original.lower().split()
        new_words = rewritten.lower().split()

        if orig_words and new_words:
            if orig_words[0] != new_words[0]:
                explanations.append(f"Changed opening from '{orig_words[0]}' to '{new_words[0]}'")

        if len(explanations) == 0:
            explanations.append("Simplified phrasing for more natural flow")

        return "; ".join(explanations)

    def _generate_full_humanized_text(self, text: str, sentences: list) -> tuple:
        """
        Generate a complete humanized version of the entire text.
        Returns (humanized_text, list_of_changes)
        """
        humanized_text = text
        changes = []

        # Step 1: Replace formal phrases with casual alternatives
        for formal, casual in self.formal_to_casual.items():
            if formal.lower() in humanized_text.lower():
                # Case-insensitive replacement
                pattern = re.compile(re.escape(formal), re.IGNORECASE)
                humanized_text = pattern.sub(casual, humanized_text)
                changes.append({
                    'type': 'phrase_replacement',
                    'original': formal,
                    'replacement': casual,
                    'reason': 'Replaced formal phrase with simpler alternative'
                })

        # Step 2: Replace formal transition words
        for formal, alternatives in self.transition_alternatives.items():
            # Match at start of sentence or after punctuation
            pattern = re.compile(r'(^|[.!?]\s+)(' + re.escape(formal) + r')(\s|,)', re.IGNORECASE)
            matches = pattern.findall(humanized_text)
            if matches:
                replacement = random.choice(alternatives)
                humanized_text = pattern.sub(r'\1' + replacement + r'\3', humanized_text)
                changes.append({
                    'type': 'transition_replacement',
                    'original': formal,
                    'replacement': replacement,
                    'reason': 'Replaced formal transition with natural alternative'
                })

        # Step 3: Replace filler phrases
        for filler, alternatives in self.filler_phrase_suggestions.items():
            if filler.lower() in humanized_text.lower():
                replacement = random.choice(alternatives)
                pattern = re.compile(re.escape(filler), re.IGNORECASE)
                humanized_text = pattern.sub(replacement, humanized_text)
                changes.append({
                    'type': 'filler_removal',
                    'original': filler,
                    'replacement': replacement,
                    'reason': 'Removed filler phrase that adds no meaning'
                })

        # Step 4: Add variety to sentence starts (for sentences that start with "The" or "This")
        humanized_sentences = []
        current_sentences = self._get_sentences(humanized_text)

        consecutive_the_count = 0
        for i, sentence in enumerate(current_sentences):
            modified_sentence = sentence

            # Check if sentence starts with "The" or "This" repeatedly
            if sentence.lower().startswith(('the ', 'this ')):
                consecutive_the_count += 1
                if consecutive_the_count >= 2 and random.random() > 0.5:
                    # Add a human starter occasionally
                    starter = random.choice(self.human_starters)
                    # Make the first letter lowercase after starter
                    if len(sentence) > 0:
                        modified_sentence = starter + " " + sentence[0].lower() + sentence[1:]
                        changes.append({
                            'type': 'variety_addition',
                            'original': sentence[:30] + '...',
                            'replacement': modified_sentence[:40] + '...',
                            'reason': 'Added variety to avoid repetitive sentence starts'
                        })
                        consecutive_the_count = 0
            else:
                consecutive_the_count = 0

            humanized_sentences.append(modified_sentence)

        # Step 5: Vary sentence length - break up very long sentences
        final_sentences = []
        for sentence in humanized_sentences:
            words = sentence.split()
            if len(words) > 40:
                # Try to split at a conjunction or comma
                mid_point = len(words) // 2
                split_words = ['and', 'but', 'which', 'that', 'because', 'while', 'although']

                split_index = None
                for sw in split_words:
                    try:
                        idx = words.index(sw)
                        if mid_point - 10 < idx < mid_point + 10:
                            split_index = idx
                            break
                    except ValueError:
                        continue

                if split_index:
                    first_part = ' '.join(words[:split_index])
                    second_part = ' '.join(words[split_index:])
                    # Capitalize second part properly
                    if second_part.startswith(('and ', 'but ')):
                        second_part = second_part[0].upper() + second_part[1:]
                    else:
                        second_part = second_part.capitalize()

                    if not first_part.endswith('.'):
                        first_part += '.'

                    final_sentences.append(first_part)
                    final_sentences.append(second_part)
                    changes.append({
                        'type': 'sentence_split',
                        'original': sentence[:40] + '...',
                        'replacement': first_part[:20] + '... | ' + second_part[:20] + '...',
                        'reason': 'Split long sentence for better readability'
                    })
                else:
                    final_sentences.append(sentence)
            else:
                final_sentences.append(sentence)

        # Reconstruct the text
        humanized_text = ' '.join(final_sentences)

        # Step 6: Add a rhetorical question if text is long enough and doesn't have questions
        if len(final_sentences) > 5 and '?' not in humanized_text:
            questions = [
                "What does this mean in practice?",
                "Why does this matter?",
                "So what's the takeaway?",
                "But here's the real question:",
            ]
            # Insert after the 3rd or 4th sentence
            insert_pos = min(3, len(final_sentences) - 1)
            question = random.choice(questions)
            final_sentences.insert(insert_pos, question)
            humanized_text = ' '.join(final_sentences)
            changes.append({
                'type': 'question_addition',
                'original': '(no questions)',
                'replacement': question,
                'reason': 'Added rhetorical question to engage reader (human writers ask questions)'
            })

        return humanized_text, changes

    def get_comparison_data(self, original_text: str, humanized_text: str) -> dict:
        """
        Generate side-by-side comparison data for display.
        """
        original_sentences = self._get_sentences(original_text)
        humanized_sentences = self._get_sentences(humanized_text)

        comparisons = []
        max_len = max(len(original_sentences), len(humanized_sentences))

        for i in range(min(max_len, 20)):  # Limit to 20 sentences
            orig = original_sentences[i] if i < len(original_sentences) else ''
            human = humanized_sentences[i] if i < len(humanized_sentences) else ''

            if orig != human:
                comparisons.append({
                    'index': i + 1,
                    'original': orig,
                    'humanized': human,
                    'changed': True
                })
            else:
                comparisons.append({
                    'index': i + 1,
                    'original': orig,
                    'humanized': human,
                    'changed': False
                })

        return {
            'comparisons': comparisons,
            'original_word_count': len(original_text.split()),
            'humanized_word_count': len(humanized_text.split()),
            'total_sentences_original': len(original_sentences),
            'total_sentences_humanized': len(humanized_sentences)
        }

    def generate_writing_exercises(self, text: str, ai_analysis: dict) -> list:
        """
        Generate interactive writing exercises based on the analyzed text.
        These help students practice improving their writing skills.
        """
        exercises = []
        sentences = self._get_sentences(text)
        features = ai_analysis.get('statistical_features', {})

        # Exercise 1: Rewrite with personal voice
        if sentences:
            sample_sentence = sentences[0] if len(sentences) > 0 else ""
            exercises.append({
                'id': 'personal_voice',
                'title': 'Add Your Personal Voice',
                'difficulty': 'Easy',
                'instruction': 'Rewrite this sentence as if you\'re explaining it to a friend. '
                              'Use "I think", "I noticed", or share a personal observation.',
                'original_sentence': sample_sentence,
                'hints': [
                    'Start with "I" or "In my view"',
                    'Add why YOU find this interesting or important',
                    'Include a personal example if relevant'
                ],
                'example_rewrite': self._create_personal_rewrite(sample_sentence),
                'learning_goal': 'Human writing includes personal perspective. AI writes objectively but impersonally.'
            })

        # Exercise 2: Vary sentence structure
        if len(sentences) >= 3:
            uniform_sentences = sentences[:3]
            exercises.append({
                'id': 'sentence_variety',
                'title': 'Create Rhythm with Variety',
                'difficulty': 'Medium',
                'instruction': 'Rewrite these 3 sentences with different lengths: '
                              'one short (under 8 words), one medium (10-15 words), one longer (20+ words).',
                'original_sentence': ' '.join(uniform_sentences),
                'hints': [
                    'Short sentences create impact: "This matters."',
                    'Medium sentences explain: "The research shows interesting patterns in the data."',
                    'Longer sentences can explore complexity with multiple clauses'
                ],
                'example_rewrite': self._create_varied_rewrite(uniform_sentences),
                'learning_goal': 'Humans naturally vary sentence length. AI tends toward uniformity.'
            })

        # Exercise 3: Remove filler words
        filler_sentence = self._find_sentence_with_filler(sentences)
        if filler_sentence:
            exercises.append({
                'id': 'remove_filler',
                'title': 'Cut the Fluff',
                'difficulty': 'Easy',
                'instruction': 'Rewrite this sentence removing unnecessary filler phrases. '
                              'Say the same thing in fewer words.',
                'original_sentence': filler_sentence,
                'hints': [
                    '"It is important to note that" → just state it',
                    '"In order to" → "to"',
                    '"Due to the fact that" → "because"'
                ],
                'example_rewrite': self._remove_fillers_from_sentence(filler_sentence),
                'learning_goal': 'Concise writing is clearer. Filler phrases are AI padding.'
            })

        # Exercise 4: Active voice conversion
        passive_sentence = self._find_passive_sentence(sentences)
        if passive_sentence:
            exercises.append({
                'id': 'active_voice',
                'title': 'Make It Active',
                'difficulty': 'Medium',
                'instruction': 'Convert this passive voice sentence to active voice. '
                              'Identify WHO is doing the action and lead with that.',
                'original_sentence': passive_sentence,
                'hints': [
                    'Find the real subject (who/what is doing the action)',
                    'Structure: Subject → Verb → Object',
                    '"The ball was thrown by John" → "John threw the ball"'
                ],
                'example_rewrite': 'Identify the actor and restructure: [Subject] [action verb] [object]',
                'learning_goal': 'Active voice is more engaging and direct. Passive voice can sound robotic.'
            })

        # Exercise 5: Add a question
        if '?' not in text and len(sentences) > 3:
            exercises.append({
                'id': 'add_question',
                'title': 'Engage with Questions',
                'difficulty': 'Easy',
                'instruction': 'Add a rhetorical question somewhere in your text to engage the reader. '
                              'Questions show you\'re thinking, not just stating facts.',
                'original_sentence': sentences[2] if len(sentences) > 2 else sentences[0],
                'hints': [
                    'Ask "why" something matters',
                    'Challenge an assumption: "But is this always true?"',
                    'Invite reflection: "What does this mean for us?"'
                ],
                'example_rewrite': 'After stating a fact, ask: "But why does this matter?" or "What does this tell us?"',
                'learning_goal': 'Human writers ask questions. It shows curiosity and engages readers.'
            })

        # Exercise 6: Contrast and comparison
        if len(sentences) >= 2:
            exercises.append({
                'id': 'add_contrast',
                'title': 'Show Both Sides',
                'difficulty': 'Hard',
                'instruction': 'Take your main point and add a contrasting perspective or nuance. '
                              'Real analysis considers multiple angles.',
                'original_sentence': sentences[0],
                'hints': [
                    'Use "however", "on the other hand", "yet"',
                    'Acknowledge limitations: "This is true, but..."',
                    'Show complexity: "While X is important, Y also matters"'
                ],
                'example_rewrite': self._add_contrast_example(sentences[0]),
                'learning_goal': 'Nuanced thinking shows depth. AI often presents one-sided statements.'
            })

        return exercises

    def _create_personal_rewrite(self, sentence: str) -> str:
        """Create an example of a personalized rewrite"""
        starters = [
            "I find it interesting that",
            "What strikes me here is that",
            "In my view,",
            "I've noticed that",
        ]
        starter = random.choice(starters)
        # Make first letter lowercase if needed
        if sentence and sentence[0].isupper():
            modified = sentence[0].lower() + sentence[1:] if len(sentence) > 1 else sentence.lower()
        else:
            modified = sentence
        return f"{starter} {modified}"

    def _create_varied_rewrite(self, sentences: list) -> str:
        """Create example with varied sentence lengths"""
        if len(sentences) < 3:
            return "Not enough sentences for this exercise."

        return (
            "Short: 'This matters.' | "
            "Medium: 'The data reveals a clear pattern here.' | "
            "Long: 'When we consider all the factors involved, including the historical context "
            "and current trends, a more nuanced picture emerges.'"
        )

    def _find_sentence_with_filler(self, sentences: list) -> str:
        """Find a sentence containing filler phrases"""
        filler_patterns = [
            'it is important to', 'it should be noted', 'in order to',
            'due to the fact', 'it is worth', 'at this point in time',
            'for the purpose of', 'in the event that'
        ]
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for filler in filler_patterns:
                if filler in sentence_lower:
                    return sentence
        # Return first sentence if no filler found
        return sentences[0] if sentences else ""

    def _remove_fillers_from_sentence(self, sentence: str) -> str:
        """Remove filler phrases from a sentence"""
        result = sentence
        for formal, casual in self.formal_to_casual.items():
            if formal.lower() in result.lower():
                pattern = re.compile(re.escape(formal), re.IGNORECASE)
                result = pattern.sub(casual, result)
        for filler, alternatives in self.filler_phrase_suggestions.items():
            if filler.lower() in result.lower():
                pattern = re.compile(re.escape(filler), re.IGNORECASE)
                result = pattern.sub(alternatives[0], result)
        return result

    def _find_passive_sentence(self, sentences: list) -> str:
        """Find a sentence with passive voice"""
        passive_patterns = [
            r'(is|are|was|were|been|being)\s+\w+ed\b',
            r'(has|have|had)\s+been\s+\w+ed\b'
        ]
        for sentence in sentences:
            for pattern in passive_patterns:
                if re.search(pattern, sentence.lower()):
                    return sentence
        return ""

    def _add_contrast_example(self, sentence: str) -> str:
        """Add a contrasting element to a sentence"""
        contrasts = [
            "However, it's worth considering that",
            "That said,",
            "On the other hand,",
            "Yet we should also note that",
        ]
        contrast = random.choice(contrasts)
        return f"{sentence} {contrast} [add your contrasting point here]."

    def generate_sentence_breakdown(self, text: str) -> list:
        """
        Generate a detailed sentence-by-sentence breakdown showing
        what makes each sentence sound AI-like or human-like.
        """
        sentences = self._get_sentences(text)
        breakdown = []

        for i, sentence in enumerate(sentences[:15]):  # Limit to 15 sentences
            analysis = {
                'index': i + 1,
                'sentence': sentence,
                'word_count': len(sentence.split()),
                'ai_indicators': [],
                'human_indicators': [],
                'suggestions': [],
                'score': 0  # 0 = neutral, negative = AI-like, positive = human-like
            }

            words = sentence.lower().split()
            sentence_lower = sentence.lower()

            # Check for AI indicators
            # 1. Formal transitions at start
            if words and words[0].rstrip('.,;:') in self.transition_alternatives:
                analysis['ai_indicators'].append({
                    'type': 'Formal transition',
                    'detail': f"Starts with '{words[0]}' - very common in AI writing",
                    'fix': f"Try: {', '.join(self.transition_alternatives.get(words[0].rstrip('.,;:'), ['alternative']))}"
                })
                analysis['score'] -= 15

            # 2. Filler phrases
            for filler in self.filler_phrase_suggestions.keys():
                if filler in sentence_lower:
                    analysis['ai_indicators'].append({
                        'type': 'Filler phrase',
                        'detail': f"Contains '{filler}' - adds words without meaning",
                        'fix': f"Replace with: {self.filler_phrase_suggestions[filler][0]}"
                    })
                    analysis['score'] -= 20

            # 3. Formal vocabulary
            for formal in self.formal_to_casual.keys():
                if formal in sentence_lower:
                    analysis['ai_indicators'].append({
                        'type': 'Overly formal',
                        'detail': f"Uses '{formal}' - unnecessarily complex",
                        'fix': f"Simpler: '{self.formal_to_casual[formal]}'"
                    })
                    analysis['score'] -= 10

            # 4. Passive voice
            passive_patterns = [r'(is|are|was|were|been|being)\s+\w+ed\b']
            for pattern in passive_patterns:
                if re.search(pattern, sentence_lower):
                    analysis['ai_indicators'].append({
                        'type': 'Passive voice',
                        'detail': 'Passive construction detected',
                        'fix': 'Convert to active voice: [Subject] [verb] [object]'
                    })
                    analysis['score'] -= 10
                    break

            # 5. Very uniform length (compared to average)
            avg_length = 15  # Approximate average
            if abs(len(words) - avg_length) < 3:
                analysis['ai_indicators'].append({
                    'type': 'Uniform length',
                    'detail': f'{len(words)} words - very average length',
                    'fix': 'Vary your sentence lengths for natural rhythm'
                })
                analysis['score'] -= 5

            # Check for human indicators
            # 1. Questions
            if '?' in sentence:
                analysis['human_indicators'].append({
                    'type': 'Question',
                    'detail': 'Contains a question - shows engagement'
                })
                analysis['score'] += 20

            # 2. Personal pronouns
            personal_pronouns = ['i ', 'i\'', 'my ', 'me ', 'we ', 'our ', 'us ']
            for pronoun in personal_pronouns:
                if pronoun in sentence_lower:
                    analysis['human_indicators'].append({
                        'type': 'Personal voice',
                        'detail': 'Uses personal pronouns - shows individual perspective'
                    })
                    analysis['score'] += 15
                    break

            # 3. Contractions
            contractions = ["n't", "'re", "'ve", "'ll", "'m", "'s"]
            for contraction in contractions:
                if contraction in sentence_lower:
                    analysis['human_indicators'].append({
                        'type': 'Contraction',
                        'detail': 'Uses contractions - natural speech pattern'
                    })
                    analysis['score'] += 10
                    break

            # 4. Short punchy sentence
            if len(words) <= 6:
                analysis['human_indicators'].append({
                    'type': 'Short sentence',
                    'detail': f'Only {len(words)} words - creates impact'
                })
                analysis['score'] += 10

            # 5. Informal expressions
            informal = ['actually', 'basically', 'honestly', 'look,', 'well,', 'so,']
            for expr in informal:
                if expr in sentence_lower:
                    analysis['human_indicators'].append({
                        'type': 'Conversational',
                        'detail': f"Uses '{expr}' - conversational tone"
                    })
                    analysis['score'] += 10
                    break

            # Determine overall assessment
            if analysis['score'] < -20:
                analysis['assessment'] = 'strongly_ai'
                analysis['assessment_text'] = 'This sentence has strong AI patterns'
            elif analysis['score'] < 0:
                analysis['assessment'] = 'slightly_ai'
                analysis['assessment_text'] = 'This sentence has some AI-like elements'
            elif analysis['score'] > 20:
                analysis['assessment'] = 'strongly_human'
                analysis['assessment_text'] = 'This sentence feels natural and human'
            elif analysis['score'] > 0:
                analysis['assessment'] = 'slightly_human'
                analysis['assessment_text'] = 'This sentence has good human elements'
            else:
                analysis['assessment'] = 'neutral'
                analysis['assessment_text'] = 'This sentence is neutral'

            breakdown.append(analysis)

        return breakdown
