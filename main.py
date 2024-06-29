import os
from langchain_openai import OpenAI
from langchain.prompts import FewShotPromptTemplate, SystemMessagePromptTemplate, PromptTemplate

system_message = SystemMessagePromptTemplate.from_template("""
あなたはアニメの翻訳家です。
キャラクター名の翻訳は以下の通りです。
カイ, Kai, 凯
スイリン, Suirin, 睡莲
シェンファ, Shenpha, 深华
ラオ, Rao, 劳
リク, Riku, 陆
リン, Rin, 琳
マサヒデ, Masahide, 马正德
サハナ, Sahana, 萨哈娜
アオイ, Aoi, 澳依
ジン, Jin, 金
ノブカゼ, Nobukaze, 信风
スオウ, Suou, 苏欧
リハク, Rihaku, 李白
""")

examples = [
    {
        "jp": "こんにちは。",
        "en": "Hello",
        "cn": "你好。"
    },
    {
        "jp": "マサヒデ様。",
        "en": "Masahide-sama.",
        "cn": "马正德大人。"
    },
    {
        "jp": "……サハナか、入れ。",
        "en": "....Sahana, come in.",
        "cn": "……萨哈娜，进来。"
    },
    {
        "jp": "ありゃ、どうしたの？カイがそんなこと言うなんて珍しいね。",
        "en": "Huh, what's wrong?That's rare coming from you, Kai.",
        "cn": "咦，怎么了？凯说这样的话倒挺少见的。"
    }
]

prompt = PromptTemplate(
    input_variables=["jp", "en", "cn"],
    template="日本語:{jp}\n英語:{en}\n簡体字:{cn}",
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=prompt,
    prefix="以下の同一の意味を持つ日本語と英語に基づいて、簡体字に翻訳して出力して。ただし、キャラクター名は指定された翻訳を使用すること。",
    suffix="日本語:{input_jp}\n英語:{input_en}\n簡体字:",
    input_variables=["input_jp", "input_en"],
    partial_variables={"system": system_message.format(role="アシスタント")}
)

llm = OpenAI(openai_api_key=os.environ.get('OPENAI_API_KEY'))

input_jp = "いや、特に意味はないんだけどね。スイリンのそばにいると、安心するから。"
input_en = "No, nothing in particular.I just feel relaxed when I'm near you, Suirin."

formatted_prompt = few_shot_prompt.format(
    input_jp=input_jp,
    input_en=input_en
)

result = llm.invoke(formatted_prompt)
print(result)
