from collections import Counter
from typing import List
from scipy.stats import chi2
import math
import re
from collections import Counter
from internal.common.schemas.free_txt import WordCloudRequest, WordStat
from internal.common.exceptions.free_txt import ExceptionNoReferenceTextWordCloud


class WordCloud:

    async def tokenize(self, text: str):
        # Simple tokenizer, replace with spaCy or NLTK for advanced
        tokens = re.findall(r"\b\w+\b", text.lower())
        return tokens

    async def count_words(self, tokens):
        return Counter(tokens)

    async def gen_wordcloud(self, data: WordCloudRequest):
        tokens = await self.tokenize(data.text)
        target_counter = await self.count_words(tokens)
        if data.measurement_type == "FREQUENCY":
            scores = await self.get_frequency_stats(target_counter)
        else:
            if not data.reference_text:
                raise ExceptionNoReferenceTextWordCloud
            ref_tokens = await self.tokenize(data.reference_text)
            ref_counter = await self.count_words(ref_tokens)

            if data.measurement_type == "LOG_LIKELIHOOD":
                scores = await self.get_log_likelihood_stats(
                    target_counter, ref_counter
                )
            if data.measurement_type == "KEYNESS":
                scores = await self.get_keyness_stats(target_counter, ref_counter)
        word_stats = [
            WordStat(word=w, weight=s)
            for w, s in sorted(scores.items(), key=lambda x: -x[1])
        ]
        return word_stats

    async def get_frequency_stats(self, counter: Counter):
        total = sum(counter.values())
        return {word: count / total for word, count in counter.items()}

    async def get_log_likelihood_stats(
        self, target_counter: Counter, ref_counter: Counter
    ):
        result = {}
        target_total = sum(target_counter.values())
        ref_total = sum(ref_counter.values())

        all_words = set(target_counter.keys()) | set(ref_counter.keys())
        for word in all_words:
            o1 = target_counter.get(word, 0)
            o2 = ref_counter.get(word, 0)
            e1 = (o1 + o2) * (target_total / (target_total + ref_total))
            e2 = (o1 + o2) * (ref_total / (target_total + ref_total))

            # Add a small value to avoid log(0)
            ll = 2 * (
                (o1 * math.log((o1 + 1e-10) / (e1 + 1e-10)))
                + (o2 * math.log((o2 + 1e-10) / (e2 + 1e-10)))
            )
            result[word] = ll
        return result

    async def get_keyness_stats(self, target_counter: Counter, ref_counter: Counter):
        # For simplicity, use log-likelihood as proxy for keyness (you can change this)
        return await self.get_log_likelihood_stats(target_counter, ref_counter)
