from dataclasses import dataclass
import os

from src.libs import openai

GPT_40_PARAMS = dict(
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False,
)


@dataclass
class GPTVersion:
    name: str
    engine: str


GPT_VERSIONS = {
    "gpt35": GPTVersion("gpt35", "gpt-35-turbo-0613"),
    "gpt35-16k": GPTVersion("gpt35-16k", "gpt-35-turbo-16k"),
    "gpt4": GPTVersion("gpt4", "gpt-4-0613"),
    "gpt4-32k": GPTVersion("gpt4-32k", "gpt4-32k-0613"),
}


def get_simple_answer(prompt: str, stream: bool = True):
    kwargs = {**GPT_40_PARAMS, **dict(stream=stream)}

    for resp in openai.ChatCompletion.create(
        engine=GPT_VERSIONS["gpt35"].engine,
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
        **kwargs,
    ):
        choices = resp.get("choices", [])
        if not choices:
            continue
        chunk = choices.pop()["delta"].get("content")
        if chunk:
            yield chunk


def get_gpt_title(prompt: str, response: str):
    sys_msg: str = (
        "As an AI Assistant your goal is to make very short title, few words max for a conversation between user and "
        "chatbot. You will be given the user's question and chatbot's first response and you will return only the "
        "resulting title. Always return some raw title and nothing more."
    )
    usr_msg = f'user_question: "{prompt}"\n' f'chatbot_response: "{response}"'

    response = openai.ChatCompletion.create(
        engine=GPT_VERSIONS["gpt35"].engine,
        messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": usr_msg}],
        **GPT_40_PARAMS,
    )

    result = response["choices"][0]["message"]["content"].replace('"', "")
    return result


def get_gpt_summary(conversation: list[dict[str, str]]) -> str:
    """Return a concise summary of a chat transcript.

    A local fallback keeps message persistence working when the configured GPT
    provider is temporarily unavailable during development.
    """
    transcript = "\n".join(f"{message['role'].title()}: {message['content']}" for message in conversation)
    sys_msg = (
        "Summarize this conversation in two or three concise sentences. Preserve "
        "important questions, decisions, and follow-up actions. Return only the summary."
    )

    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_API_BASE"):
        return " ".join(message["content"].strip() for message in conversation if message["content"].strip())[:500]

    try:
        response = openai.ChatCompletion.create(
            engine=GPT_VERSIONS["gpt35"].engine,
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": transcript}],
            **GPT_40_PARAMS,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception:
        # Keep a useful, bounded summary even if an API key/endpoint is absent.
        return " ".join(message["content"].strip() for message in conversation if message["content"].strip())[:500]


def get_conversation_answer(conversation: list[dict[str, str]], model: str, stream: bool = True):
    kwargs = {**GPT_40_PARAMS, **dict(stream=stream)}
    engine = GPT_VERSIONS[model].engine

    for resp in openai.ChatCompletion.create(
        engine=engine,
        messages=[{"role": "system", "content": "You are a helpful assistant."}, *conversation],
        **kwargs,
    ):
        choices = resp.get("choices", [])
        if not choices:
            continue
        chunk = choices.pop()["delta"].get("content")
        if chunk:
            yield chunk
