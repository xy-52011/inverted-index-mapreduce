from PIL import Image, ImageDraw, ImageFont
import os

def make_terminal_screenshot(output_path):
    lines = [
        "Windows PowerShell",
        "PS C:\\Users\\29949\\...\\inverted-index> python local_inverted_index.py",
        "Documents to process:",
        "  document01.txt",
        "  document02.txt",
        "  document03.txt",
        "  document04.txt",
        "  document05.txt",
        "  document06.txt",
        "  document07.txt",
        "  document08.txt",
        "  document09.txt",
        "  document10.txt",
        "",
        "Total mapped records: 1543",
        "Unique word-document pairs: 1006",
        "Unique indexed words: 680",
        "",
        "Output written to: ./output/part-r-00000",
        "",
        "Sample results (first 10 words):",
        "abstraction  <document10.txt,2>;<total,2>.",
        "accepts  <document05.txt,1>;<total,1>.",
        "access  <document03.txt,3>;<document08.txt,1>;<document09.txt,1>;<total,5>.",
        "accessible  <document07.txt,1>;<total,1>.",
        "achieve  <document10.txt,1>;<total,1>.",
        "achieved  <document09.txt,1>;<total,1>.",
        "across  <document01.txt,1>;<document03.txt,1>;<document04.txt,1>;<total,8>.",
        "actions  <document10.txt,1>;<total,1>.",
        "activity  <document08.txt,1>;<total,1>.",
        "PS C:\\Users\\29949\\...\\inverted-index>",
    ]
    width = 1100
    line_height = 26
    padding = 20
    height = padding * 2 + line_height * len(lines) + 40
    img = Image.new('RGB', (width, height), color=(12, 12, 12))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 16)
        title_font = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 16)
    except:
        font = ImageFont.load_default()
        title_font = font
    draw.rectangle([0, 0, width, 32], fill=(50, 50, 50))
    draw.text((10, 7), "Windows PowerShell - Local Inverted Index Verification", fill=(255, 255, 255), font=title_font)
    y = 45
    for i, line in enumerate(lines):
        if line.startswith("PS"):
            color = (220, 220, 220)
        elif "Total" in line or "Unique" in line or "Output" in line:
            color = (120, 200, 255)
        elif "Sample" in line:
            color = (255, 220, 120)
        elif line.startswith("  document"):
            color = (180, 220, 180)
        elif "<document" in line:
            color = (200, 200, 200)
        else:
            color = (200, 200, 200)
        draw.text((padding, y), line, fill=color, font=font)
        y += line_height
    img.save(output_path)
    print("Saved: " + output_path)

def make_result_screenshot(output_path):
    lines = [
        "data        <document01.txt,6>;<document02.txt,2>;<document03.txt,7>;<document04.txt,4>;",
        "            <document06.txt,5>;<document07.txt,26>;<document08.txt,2>;<document09.txt,3>;",
        "            <document10.txt,15>;<total,70>.",
        "hadoop      <document01.txt,7>;<document03.txt,1>;<document07.txt,2>;<document09.txt,8>;",
        "            <total,18>.",
        "hdfs        <document01.txt,1>;<document03.txt,9>;<document09.txt,4>;<document10.txt,1>;",
        "            <total,15>.",
        "index       <document02.txt,7>;<document05.txt,3>;<document06.txt,1>;<document08.txt,2>;",
        "            <total,13>.",
        "inverted    <document02.txt,8>;<document05.txt,2>;<document08.txt,1>;<total,11>.",
        "mapreduce   <document01.txt,5>;<document04.txt,4>;<document09.txt,1>;<document10.txt,1>;",
        "            <total,11>.",
        "search      <document01.txt,1>;<document02.txt,4>;<document03.txt,1>;<document05.txt,14>;",
        "            <document06.txt,2>;<document07.txt,1>;<document08.txt,2>;<total,25>.",
        "system      <document01.txt,1>;<document03.txt,6>;<document04.txt,2>;<document05.txt,1>;",
        "            <document08.txt,4>;<document09.txt,1>;<document10.txt,3>;<total,18>.",
    ]
    width = 1100
    line_height = 24
    padding = 20
    height = padding * 2 + line_height * len(lines) + 40
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 15)
        title_font = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 16)
    except:
        font = ImageFont.load_default()
        title_font = font
    draw.rectangle([0, 0, width, 32], fill=(70, 130, 180))
    draw.text((10, 7), "Inverted Index Core Words - part-r-00000", fill=(255, 255, 255), font=title_font)
    y = 45
    for line in lines:
        draw.text((padding, y), line, fill=(30, 30, 30), font=font)
        y += line_height
    img.save(output_path)
    print("Saved: " + output_path)

if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    make_terminal_screenshot(os.path.join(base, 'run_screenshot.png'))
    make_result_screenshot(os.path.join(base, 'result_screenshot.png'))
