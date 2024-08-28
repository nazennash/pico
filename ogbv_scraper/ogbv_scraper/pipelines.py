import openai

class GptPipeline:
    def __init__(self):
        # Initialize OpenAI API
        openai.api_key = 'YOUR_OPENAI_API_KEY'

    def process_item(self, item, spider):
        content = item.get('content', '')
        analysis = self.analyze_text(content)
        item['analysis'] = analysis
        return item

    def analyze_text(self, text):
        response = openai.Completion.create(
            engine="text-davinci-003",  # or "gpt-3.5-turbo" or any other model
            prompt=f"Identify and classify any abusive language in the following text:\n\n{text}",
            max_tokens=100,
            temperature=0.2
        )
        return response.choices[0].text.strip()
