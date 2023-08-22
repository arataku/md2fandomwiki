import pyperclip
import re

lines = pyperclip.paste().replace("\r","").split('\n')
output =[]

# 見出し文字の大きさ(None->見出し文字ではない)
def get_h_level(line):
    count = 0
    for char in line:
        if char == "#":
            count += 1
        else:
            break
    if count == 0 or line[count] != " ":
        return None
    else:
        return count

def get_h_title(line):
    h_level = get_h_level(line)
    if h_level == None:
        return None
    else:
        return line[h_level+1:]

def link_convert(line):
    # [text](url)の形式をすべて[url text]に変換
    return re.sub(r"\[(.+)\]\((.+)\)", r"[\2 \1]", line)

def table_convert(lines)->list:
    tmp = []
    for i in range(len(lines)):
        line = lines[i]
        if not line.startswith("|"):
            tmp.append(line)
            continue
        line = line.replace(" ", "")
        if i == 0 or not lines[i-1].startswith("|"):
            tmp.append("{| class=\"fandom-table\"")
            tmp.append("|+")
            tmp += ["!"+i for i in line.split("|")[1:-1]]
            continue
        if line[1:-1].split("|")[0][0] == "-":
            continue
        tmp.append("|-")
        tmp += ["|"+i for i in line.split("|")[1:-1]]
        if i == len(lines)-1 or not lines[i+1].startswith("|"):
            tmp.append("|}")
    return tmp
            

for line in lines:
    count = 0
    tmp = line
    h_level = get_h_level(line)
    if h_level is not None:
        tmp = get_h_title(tmp)
        tmp = "="*(h_level+1) + " " + tmp + " " + "="*(h_level+1)
    if tmp.startswith("- "):
        tmp = "* " + tmp[2:]
    if tmp.startswith("---"):
        continue
    if tmp.startswith("title:"):
        tmp = "=" + tmp[6:] + "="
    tmp = link_convert(tmp) 
    output.append(tmp)

output = table_convert(output)

pyperclip.copy("\n".join(output))