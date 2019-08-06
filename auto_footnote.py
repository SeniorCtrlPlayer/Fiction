import re
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    # file name:
    parser.add_argument('--name', dest='name', type=str, help="File name")
    #
    # parser.add_argument('--c', dest='chapter', type=str, help="The chapter number in file name")
    # outname:
    parser.add_argument("--outname", dest='outname', type=str, default="",
                        help="the name of numbered file."
                             "If outname is set, the origin file won't be delete")

    _options = parser.parse_args()
    return _options


def getindex(raw, pattern):
    """
    获取markdown文档中需要编号的词组的尾部索引
    :param raw: str形式的markdown原文
    :param pattern: 标记部分的匹配模式，默认匹配加粗标记
    :return: 所有加粗标记的尾部索引
    """
    regex = re.compile(pattern, re.S)
    all = regex.finditer(raw)
    last_index = []
    for x in all:
        last_index.append(x.span()[1] - 1)
    return last_index


def reset(text, pattern):
    """
    去掉符合pattern的字符串
    :param text:
    :param pattern:
    :return:
    """
    regex = re.compile(pattern, re.S)
    return regex.sub("", text)


def footnote(text):
    """
    对markdown文档部分的加粗词组重新脚注编号
    :param filename: markdown文件名
    :return: 教主编号后的str形式的markdown内容
    """
    text = reset(text, '\[\^\d+\]')
    last_index = getindex(text, '\*\*[^0-9a-zA-Z]')
    after = list(text)
    max = len(last_index)
    for _ in range(max):
        after.insert(last_index.pop(), '[^{}]'.format(max))
        max -= 1
    return "".join(after)


if __name__ == '__main__':

    options = parse_args()
    if options.name is None:
        raise Exception("请输入文件名")
    name = options.name
    with open(name, 'r', encoding='utf-8') as file:
        after = footnote(file.read())

    if options.outname != "":
        name = options.outname
    with open(name, 'w', encoding='utf-8') as file:
        file.write(after)
