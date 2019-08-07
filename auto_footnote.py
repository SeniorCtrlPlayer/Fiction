import re
import argparse
import glob
import platform


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', dest='mode', type=str, help="")
    # file name:
    parser.add_argument('--name', dest='name', type=str, help="File name")
    # parser.add_argument('--c', dest='chapter', type=str, help="The chapter number in file name")
    # outdir:
    parser.add_argument("--outdir", dest='outdir', type=str, default="post",
                        help="the name of numbered file."
                             "If outdir is set, the origin file won't be delete")
    parser.add_argument("--b", dest="batch_size", type=int, default=None,
                        help="The size of per batch")
    parser.add_argument("--dir", dest="dir", type=str, default=".",
                        help="The batch_file's dir, only name, no \"/\" or \"\\")

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
    :return: 注脚编号后的str形式的markdown内容
    """
    text = reset(text, '\[\^\d+\]')
    last_index = getindex(text, '\*\*[^0-9a-zA-Z]')
    after = list(text)
    max = len(last_index)
    for _ in range(max):
        after.insert(last_index.pop(), '[^{}]'.format(max))
        max -= 1
    return "".join(after)


def re_num(text):
    text = reset(text, '\d+')
    last_index = getindex(text, '\[\^\]')
    after = list(text)
    max = len(last_index)
    for _ in range(max):
        after.insert(last_index.pop(), str(max))
        max -= 1
    return "".join(after).replace("\n\n", "\n")


if __name__ == '__main__':

    options = parse_args()
    if options.batch_size is None:
        if options.name is None:
            raise Exception("请输入文件名")
        name = options.name
        with open(name, 'r', encoding='utf-8') as file:
            after = footnote(file.read())

        # if options.outdir != "":
        #     name = options.outdir
        with open(name, 'w', encoding='utf-8') as file:
            file.write(after)
    else:
        ## 只获取文件名，不包含文件路径
        dir = options.dir
        filenames = glob.glob(dir+"/"+"*.md")
        if platform.system()=="Windows":
            startindex = len(dir)+1
        else:
            startindex = len(dir)
        # 按文件名进行排序
        filenames.sort(key=lambda x:int(x[startindex:-3]))
        # 对文件进行分批合并
        f_batch = lambda a:map(lambda b:a[b:b+options.batch_size],
                         range(0,len(filenames),options.batch_size))
        filenames = list(f_batch(filenames))
        for i, batch_files in enumerate(filenames):
            merge_cont1 = []
            merge_cont2 = []
            for file in batch_files:
                with open(file, 'r',encoding="utf-8") as f:
                    content = f.read()
                    cont1, cont2 = content.split("\n:pencil:\n")[:]
                    merge_cont1.append(cont1)
                    merge_cont2.append(cont2)
            merge_content = [footnote("\n".join(merge_cont1)), re_num("".join(merge_cont2))]
            merge_content = "\n:pencil:\n".join(merge_content)
            with open(options.outdir+"/"+"{}-{}.md".format(str(options.batch_size*i+1),
                                        str((i+1)*options.batch_size)),'w',encoding="utf-8") as f:
                f.write(merge_content)