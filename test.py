import os
from openai import OpenAI

client = OpenAI(
    api_key="c3dc550d-ae81-42a5-bf63-4fc1bddac1c1",
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

# Non-streaming:
print("----- standard request -----")
completion = client.chat.completions.create(
    model="ep-20241231020502-wfrtb",  # your model endpoint ID
    messages=[
        {"role": "system", "content": "你是一位资深医师和翻译工作者，根据要求翻译以下，内容需要符合正常的表达习惯，不需要输出额外内容，en指英语，ch指中文"},
        {"role": "user", "content": "从{en}到{ch}: {What drug does second liver take}"},
    ],
    temperature=0.7  # 设置 temperature 为 0.7
)
print(completion.choices[0].message.content)
print()
