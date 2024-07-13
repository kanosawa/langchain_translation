import re
from langchain_translation import translate


def extract_jp_lines(readed_lines, output_lines, line_idx):
    return extract_lang_lines(readed_lines, output_lines, line_idx, '[else]')


def extract_en_lines(readed_lines, output_lines, line_idx):
    return extract_lang_lines(readed_lines, output_lines, line_idx, '[endif]')


def extract_lang_lines(readed_lines, output_lines, line_idx, target_str):
    lang_lines = []
    while True:
        line_idx += 1
        line = readed_lines[line_idx]
        if line.find(target_str) >= 0:
            break
        output_lines.append(line)
        lang_lines.append(line)
    return lang_lines, line_idx


def remove_tags(lines):
    line = "".join(lines).replace('\n', '').replace('_　', '')
    output_line = re.sub(r'\[.*?\]', '', line)
    return output_line


def main():

    with open('Event_h_01_1.ks', encoding='utf-8') as fr:
        readed_lines = fr.readlines()
        line_num = len(readed_lines)
        line_idx = 0
        output_lines = []
        while line_idx < line_num:
            line = readed_lines[line_idx]
            output_lines.append(line)
            if line.find("exp=\"sf.lang==\'ja\'\"") >= 0:
                jp_lines, line_idx = extract_jp_lines(readed_lines, output_lines, line_idx)
                output_lines.append("""[elsif exp="sf.lang=='en'"]\n""")
                en_lines, line_idx = extract_en_lines(readed_lines, output_lines, line_idx)
                output_lines.append("[else]\n")

                # 名前欄の翻訳
                if jp_lines[0][0] == '#':
                    cn_name = '#'
                    if len(jp_lines[0]) > 2:
                        jp_name, en_name = jp_lines[0][1:-1], en_lines[0][1:-1]
                        cn_name += translate(jp_name, en_name)
                    cn_name += '\n'
                    output_lines.append(cn_name)
                    jp_lines = jp_lines[1:]
                    en_lines = en_lines[1:]

                # 文章の翻訳
                jp_line = remove_tags(jp_lines)
                en_line = remove_tags(en_lines)
                cn_line = translate(jp_line, en_line)
                output_lines.append(cn_line + '[l]\n')
                output_lines.append("[endif]\n")
            line_idx += 1
    with open('Event_h_01_1_.ks', 'w', encoding='utf-8') as fw:
        fw.write("".join(output_lines))


if __name__ == '__main__':
    main()
