from fontTools.ttLib import TTFont
import os
import random
import re
import json

# 加载字体文件（替换为你的 .ttf 路径）
ttf_path = "../resource/simkai.ttf"
font = TTFont(ttf_path)

# 输出目录
output_dir = "html_output"
os.makedirs(output_dir, exist_ok=True)
json_output_path = os.path.join(output_dir, "output.json")

# 字体支持的字符映射
cmap = font["cmap"].getBestCmap()

# 随机字体选项
font_families = [
    ('"宋体"', '"SimSun"'),
    ('"楷体"', '"KaiTi"'),
    ('"黑体"', '"SimHei"')
]
font_weights = ["normal", "bold", "lighter"]

# HTML 模板
html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>{char}字展示</title>
  <style>
    .container {{
      font-family: {family1}, {family2}, serif;
      font-size: {fontsize}px; 
      font-weight: {weight};
      color: black;
    }}
  </style>
</head>
<body>
  <div class="container">
    {char}
  </div>
</body>
</html>'''

# 判断字符是否合法作为文件名
def safe_filename(char):
    return not re.match(r'[<>:"/\\|?*\x00-\x1F]', char)

# 存储所有 json 数据
data_list = []

# 遍历生成 HTML + instruction + JSON
for codepoint in cmap:
    if (0x4E00 <= codepoint <= 0x9FFF) or (0x3400 <= codepoint <= 0x4DBF):
        try:
            char = chr(codepoint)
            if not safe_filename(char):
                continue  # 跳过非法文件名字符

            family1, family2 = random.choice(font_families)
            fontsize = random.randint(100, 200)
            weight = random.choice(font_weights)

            filename = f"{char}.html"
            filepath = os.path.join(output_dir, filename)

            html_content = html_template.format(
                char=char,
                family1=family1,
                family2=family2,
                fontsize=fontsize,
                weight=weight
            )

            # 写 HTML 文件
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)

            # 构造 instruction
            if weight == "bold":
                weight_zh = "加粗"
            elif weight == "normal":
                weight_zh = "常规"
            else:
                weight_zh = "较细"

            font_zh = family1.replace('"', '')

            instruction = f"生成一个{weight_zh}、字号{fontsize}px、样式为{font_zh}的“{char}”字的 HTML 代码"

            # 添加到 JSON 列表
            data_list.append({
                "instruction": instruction,
                "input": "",
                "output": html_content
            })

        except Exception as e:
            print(f"跳过字符 {codepoint}: {e}")

# 保存 JSON 文件
with open(json_output_path, "w", encoding="utf-8") as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=2)

print(f"✅ 生成完毕，共生成 {len(data_list)} 个 HTML 文件，并写入 JSON 至：{json_output_path}")
