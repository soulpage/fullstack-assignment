import openai

def generate_summary(conversation_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize the following conversation:\n\n{conversation_text}",
        max_tokens=100,
        temperature=0.5,
    )
    summary = response.choices[0].text.strip()
    return summary
