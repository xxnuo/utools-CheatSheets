# -*- coding: utf-8

import os
import sys

from pathlib import Path
from rich import print

indexhtmlhead = """
<html lang="zh-cn">
<head>
<meta content="text/html; charset=utf-8" http-equiv="content-type" />
</head>
<body>
"""
indexhtmla = """
<a href="%s">%s</a></br>
"""
indexhtmlend = """
</body>
</html>
"""


def md2html(mdstr):
    import markdown

    exts = [
        "markdown.extensions.extra",
        "markdown.extensions.codehilite",
        "markdown.extensions.tables",
        "markdown.extensions.toc",
    ]

    html = """
    <html lang="zh-cn">
    <head>
    <meta content="text/html; charset=utf-8" http-equiv="content-type" />
    <link href="RELATIVE_CSS_PATH@BE027565916C40D6BA33DAAE4407A294" rel="stylesheet">
    </head>
    <body>
    %s
    </body>
    </html>
    """

    ret = markdown.markdown(mdstr, extensions=exts)
    return html % ret


if __name__ == "__main__":
    exceptFiles = ["LICENSE", "awesome.png", "python.tex", ".git"]
    # 遍历awesome-cheatsheets目录下的所有文件
    for root, dirs, files in os.walk("awesome-cheatsheets"):
        for file in files:
            # print(root, file)
            if file not in exceptFiles:
                # 原完整路径 awesome-cheatsheets\tools\tmux.txt
                fileFullPath = Path(root, file)
                fileName = fileFullPath.stem  # 文件名 tmux
                fileSuffix = fileFullPath.suffix  # 后缀 .txt
                # 父目录 awesome-cheatsheets\tools
                fileParentPath = str(fileFullPath.parent)

                # awesome-cheatsheets\tools\ => pubilc\tools
                newFileParentPath = str(fileParentPath).replace(
                    "awesome-cheatsheets", "public"
                )
                newFileFullPath = Path(
                    newFileParentPath,
                    fileName + fileSuffix + ".html",
                )
                # pubilc/tools 相对于 ../css/dark.css 的相对路径
                relativeCssPath = "css/dark.css"
                for i in range(newFileParentPath.count(os.path.sep)):
                    relativeCssPath = "../" + relativeCssPath

                # 创建目录
                newFileFullPath.parent.mkdir(parents=True, exist_ok=True)
                if fileSuffix == ".md":
                    with open(fileFullPath, "r", encoding="utf-8") as f:
                        mdstr = f.read()
                    html = md2html(mdstr)
                    html = html.replace(
                        "RELATIVE_CSS_PATH@BE027565916C40D6BA33DAAE4407A294",
                        relativeCssPath,
                    )
                    with open(newFileFullPath, "w", encoding="utf-8") as f:
                        f.write(html)
                else:
                    os.system(
                        "pygmentize -f html -O full -o %s %s"
                        % (newFileFullPath, fileFullPath)
                    )
                # done
                indexhtmla = (
                    indexhtmla
                    % (str(newFileFullPath)[len("public/") :], fileName + fileSuffix)
                    + indexhtmla
                )
    # 生成index.html
    indexhtml = indexhtmlhead + indexhtmla + indexhtmlend
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(indexhtml)
