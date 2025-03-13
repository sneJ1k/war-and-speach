import html
import re
import requests


urls = [
    "http://az.lib.ru/t/tolstoj_lew_nikolaewich/text_0039.shtml",
    "http://az.lib.ru/t/tolstoj_lew_nikolaewich/text_0040.shtml",
    "http://az.lib.ru/t/tolstoj_lew_nikolaewich/text_0050.shtml",
    "http://az.lib.ru/t/tolstoj_lew_nikolaewich/text_0060.shtml",
    "http://az.lib.ru/t/tolstoj_lew_nikolaewich/text_0070.shtml",
    "http://az.lib.ru/t/tolstoj_lew_nikolaewich/text_0080.shtml",
    "http://az.lib.ru/t/tolstoj_lew_nikolaewich/text_0090.shtml",
    "http://az.lib.ru/t/tolstoj_lew_nikolaewich/text_1860_dekabristy.shtml",
]


# * Скачивание страниц из urls как .html файлы
def download(url):
    return requests.get(url).text

# * Собираем регулярное выражение для очистки верстки от тегов, комментариев и т.д.
striptags_re = re.compile(r"(<!--.*?-->|<[^>]*>)")

# * Очищаем верстку из переменной s с помощью метода .sub и востанавливаем закодированные сущности с помощью .unescape
def to_text(s):
    return html.unescape(striptags_re.sub("", s))

def beautify(s):
    lines = [x.strip() for x in s.split("\n") if x.strip() != ""] # * Разбиваем страницу по строкам и удаляем \n
    for i in range(min(100, len(lines))):
        if lines[i] == "-->":
            break
    return "\n".join(lines[i + 1 :] if i < 100 else lines) # * Если найден -->(конец комментария) игнорируем все строки до него. Иначе оставляем текст без изменений.

with open("dataset.txt", "w", encoding="utf-8") as f:
    for u in urls:
        text = beautify(to_text(download(u)))
        f.write(text + "\n\n")