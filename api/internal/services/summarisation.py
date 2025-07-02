from nltk import sent_tokenize
from summa.summarizer import summarize as summa_summarizer


class Summarizer:

    async def summarizer_summa(self, input_text, chosen_ratio):

        # Convert input_text to a string if it isn't already
        if not isinstance(input_text, str):
            input_text = " ".join(map(str, input_text))

        # Ensure the chosen_ratio is at least 0.1
        chosen_ratio = max(chosen_ratio, 0.1)

        # Get the summary using the text_rank_summarize function
        summary = summa_summarizer(input_text, chosen_ratio)

        # Tokenize input_text to sentences
        sentences = sent_tokenize(input_text)

        # Return the summary or fallback if the summary is empty
        if summary:
            return summary
        elif len(sentences) > 1:
            return sentences[0]
        else:
            return "Unable to summarize the input text."
