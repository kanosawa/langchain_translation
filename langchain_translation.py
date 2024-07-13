import os
from langchain_openai import ChatOpenAI
from langchain.prompts import FewShotPromptTemplate, SystemMessagePromptTemplate, PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate


def translate(input_jp, input_en):

    system_message = SystemMessagePromptTemplate.from_template("""
    あなたはアニメの翻訳家です。
    固有名詞の翻訳は以下の通りです。
    カイ,Kai,凯
    スイリン,Suirin,睡莲
    シェンファ,Shenhua,深华
    ラオ,Rao,劳
    リク,Riku,陆
    リンばあ,Rinba,琳婆
    マサヒデ,Masahide,马正德
    サハナ,Sahana,萨哈娜
    アオイ,Aoi,澳依
    ジン,Jin,金
    ノブカゼ,Nobukaze,信风
    スオウ,Suou,苏欧
    リハク,Rihaku,李白
    倉敷,Kurashiki,仓敷
    天久佐,Amakusa,天久佐
    蘇芳,Suou,苏芳
    日ノ和,Hinowa,日之和
    洲謁領,Shuetsuryo,洲谒领
    公,lord,公
    高家,renowned family,高家
    権門,powerful family,权门
    旧家,old family,旧家
    名家,prestigious family,名家
    三門,Mikado,三门
    従士,Retainer,从士
    """)

    examples = [
        {
            "jp": "ありゃ、どうしたの？カイがそんなこと言うなんて珍しいね。",
            "en": "Huh, what's wrong?That's rare coming from you, Kai.",
            "cn": "哎呀，怎么了？凯你说这种话真是稀奇啊。"
        },
        {
            "jp": "いや、特に意味はないんだけどね。スイリンのそばにいると、安心するから。",
            "en": "No, nothing in particular.I just feel relaxed when I'm near you, Suirin.",
            "cn": "没有，特别的意思。只是在睡莲你身边，感觉很安心。"
        },
        {
            "jp": "でも僕にはラオがいる。シェンファがいる。リンばあやリクや村のみんながいる。",
            "en": "But I have Rao with me. I have Shenhua with me.I have Rinba, Riku, everyone in the village.",
            "cn": "但是我有劳在身边。我有深华在身边。我有琳婆，陆，还有村子里的所有人。"
        },
        {
            "jp": "身を盾にして公を守る従士となる。",
            "en": "Trying to act as the shield for her lord, becoming his retainer.",
            "cn": "以身为盾，保护公，成为他的从士。"
        },
        {
            "jp": "公に対し直接的発言権と相続権を持つ三つの家柄、三門である倉敷、天久佐、蘇芳。",
            "en": "Three families have a direct say and inheritance rights over the lordship of the country, also known as the Mikado: the Kurashiki, the Amakusa and the Suou.",
            "cn": "对公有直接发言权和继承权的三个家族，也称为三门：仓敷，天久佐，苏芳。"
        },
        {
            "jp": "旧家と名家。公の正統な血族ではない家柄、その中にはこの日ノ和という国を転覆させようとする輩もいる。",
            "en": "We have both old and prestigious families. Families that are not blood relatives of the Lord, and there's even families that are trying to overthrow Hinowa itself.",
            "cn": "旧家和名家。并非公的正统血亲的家族，其中甚至有人想颠覆这个叫做日之和的国家。"
        },
        {
            "jp": "マサヒデ様は自室に戻り、私はアオイの部屋に来ていた。",
            "en": "Masahide-sama went back to his room, I went to Aoi's room.",
            "cn": "马正德大人回到了他的房间，我来到了澳依的房间。"
        },
        {
            "jp": "ジン様はリハク……ご当主様と、サハナ様をお待ちになられております。",
            "en": "Jin-sama is with Rihaku... with the Head of the family. They are waiting for you Sahana-sama.",
            "cn": "金大人正在和李白……家主大人在一起。他们正在等你，萨哈娜大人。"
        },
    ]

    prompt = PromptTemplate(
        input_variables=["jp", "en", "cn"],
        template="日本語:{jp}\n英語:{en}\n簡体字:{cn}",
    )

    prefix = """
    以下の同一の意味を持つ日本語と英語に基づいて、簡体字に翻訳して。
    ただし、指定された固有名詞の翻訳を使用してください。
    また、日本語が与える印象や感情を重視しつつ、主語や目的語が省略されている場合は英語を参照してください。
    日本語での「」は中国語でも「」にしてください。
    "」"の前には"。"はつけないでください。
    """

    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=prompt,
        prefix=prefix,
        suffix="日本語:{input_jp}\n英語:{input_en}\n簡体字:",
        input_variables=["input_jp", "input_en"],
    )

    chat_prompt = ChatPromptTemplate.from_messages([
        system_message,
        HumanMessagePromptTemplate(prompt=few_shot_prompt)
    ])

    llm = ChatOpenAI(
        openai_api_key=os.environ.get('OPENAI_API_KEY'),
        model="gpt-4"
    )

    formatted_prompt = chat_prompt.format_prompt(
        input_jp=input_jp,
        input_en=input_en
    )

    result = llm.invoke(formatted_prompt.to_messages())
    return result.content


if __name__ == '__main__':
    result = translate('サハナ', 'Sahana')
    print(result)
