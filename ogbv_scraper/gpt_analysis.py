import openai
import json
import re

openai.api_key = ''

def preprocess_text(text):
    text = text.lower()  
    text = re.sub(r'\s+', ' ', text)  
    text = re.sub(r'\n', ' ', text)  
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)  
    text = re.sub(r'\d+', '', text)  
    text = text.strip()  
    return text

def analyze_text(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert at identifying abusive language."},
                {"role": "user", "content": f"Identify and classify any abusive language in the following text:\n\n{text}"}
            ],
            max_tokens=100,
            temperature=0.2
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        print(f"API request failed: {e}")
        return "Analysis could not be completed due to an error."


def main():
    results = []  

    with open('data_1724797499.json', 'r') as f:
        data = json.load(f)

    for key, values in data.items():
        if isinstance(values, list):
            for value in values:
                content = preprocess_text(value)
                analysis = analyze_text(content)
                results.append({
                    "type": key,
                    "content": value,
                    "analysis": analysis
                })
                print(f"{key.capitalize()} content: {value}")
                print(f"Analysis: {analysis}")
                print('-' * 80)

    with open('analysis_results.json', 'w') as f:
        json.dump(results, f, indent=4)

    print("Analysis saved to analysis_results.json")

if __name__ == "__main__":
    main()
