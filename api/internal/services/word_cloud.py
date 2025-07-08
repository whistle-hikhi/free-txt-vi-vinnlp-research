from collections import Counter
from typing import List
from scipy.stats import chi2
import math
import re
from collections import Counter
from internal.common.schemas.free_txt import WordCloudRequest, WordStat
from internal.common.exceptions.free_txt import ExceptionNoReferenceTextWordCloud
from vncorenlp import VnCoreNLP
import spacy
from itertools import islice
import os


class WordCloud:
    def __init__(self):
        self.vncorenlp = VnCoreNLP(
            "internal/services/vncorenlp/VnCoreNLP-1.2.jar",
            annotators="wseg,pos",
            max_heap_size="-Xmx2g",
        )
        self.nlp_en = spacy.load("en_core_web_sm")

    async def remove_stopwords(tokens, language):
        vi_stopwords = set(
            [
                "và",
                "là",
                "của",
                "cho",
                "trong",
                "một",
                "các",
                "những",
                "này",
                "đã",
                "đang",
                "sẽ",
                "với",
                "khi",
                "vì",
                "nên",
                "rằng",
                "được",
                "có",
                "từ",
                "thì",
            ]
        )

        en_stopwords = set(
            [
                "the",
                "is",
                "and",
                "of",
                "in",
                "to",
                "a",
                "for",
                "on",
                "that",
                "this",
                "with",
                "as",
                "by",
                "are",
                "an",
                "at",
                "be",
                "from",
                "has",
                "it",
                "was",
            ]
        )
        if language == "vi":
            return [token for token in tokens if token.lower() not in vi_stopwords]
        if language == "en":
            return [token for token in tokens if token.lower() not in en_stopwords]
        return tokens

    async def generate_ngrams(self, tokens, n):
        return [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]

    async def filter_by_cloud_type(self, pos_list, cloud_type, language):
        if cloud_type == "ALL_WORDS":
            return [word for word, pos in pos_list]

        pos_map_vi = {
            "NOUNS": ["N"],
            "PROPER_NOUNS": ["Np"],
            "ADJECTIVES": ["A"],
            "VERBS": ["V"],
            "ADVERBS": ["R"],
            "NUMBERS": ["M"],
        }

        pos_map_en = {
            "NOUNS": ["NOUN"],
            "PROPER_NOUNS": ["PROPN"],
            "ADJECTIVES": ["ADJ"],
            "VERBS": ["VERB"],
            "ADVERBS": ["ADV"],
            "NUMBERS": ["NUM"],
        }

        if "CLUSTER" in cloud_type:
            n = int(cloud_type.split("_")[0])
            return await self.generate_ngrams([word for word, _ in pos_list], n)

        tag_map = pos_map_vi if language == "vi" else pos_map_en
        wanted_tags = tag_map.get(cloud_type, [])
        return [word for word, pos in pos_list if pos in wanted_tags]

    async def tokenize(self, text: str, language: str, cloud_type: str, remove_sw=True):
        if language == "vi":
            annotated = self.vncorenlp.annotate(text)["sentences"]
            pos_list = [
                (tok["form"], tok["posTag"]) for sent in annotated for tok in sent
            ]
        else:
            doc = self.nlp_en(text)
            pos_list = [
                (token.text, token.pos_)
                for token in doc
                if not token.is_punct and not token.is_space
            ]

        filtered_tokens = await self.filter_by_cloud_type(
            pos_list, cloud_type, language
        )

        if remove_sw:
            filtered_tokens = await self.remove_stopwords(filtered_tokens, language)

        return filtered_tokens

    async def count_words(self, tokens):
        return Counter(tokens)

    async def gen_wordcloud(self, data: WordCloudRequest):
        tokens = await self.tokenize(
            data.text, data.language, data.cloud_type, data.remove_stopwords
        )
        target_counter = await self.count_words(tokens)
        if data.measurement_type == "FREQUENCY":
            scores = await self.get_frequency_stats(target_counter)
        else:
            if not data.reference_text:
                raise ExceptionNoReferenceTextWordCloud(
                    "Reference text is required for log-likelihood or keyness measurement."
                )
            ref_tokens = await self.tokenize(
                data.reference_text,
                data.language,
                data.cloud_type,
                data.remove_stopwords,
            )
            ref_counter = await self.count_words(ref_tokens)

            if data.measurement_type == "LOG_LIKELIHOOD":
                scores = await self.get_log_likelihood_stats(
                    target_counter, ref_counter
                )
            elif data.measurement_type == "KEYNESS":
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
            ll = 2 * (
                (o1 * math.log((o1 + 1e-10) / (e1 + 1e-10)))
                + (o2 * math.log((o2 + 1e-10) / (e2 + 1e-10)))
            )
            result[word] = ll
        return result

    async def get_keyness_stats(self, target_counter: Counter, ref_counter: Counter):
        return await self.get_log_likelihood_stats(target_counter, ref_counter)
