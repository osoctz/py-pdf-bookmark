from lib import pdf_book_catalog as export
from lib import txt_book_catalog as extract
from lib.util import Utils
from lib.pdf_bookmarks_gen import PdfBookmarkGen

import fitz


def prepare():
    print("提取pdf的目录页")
    export.export_book_catalog(doc=fitz.open('input/软件产品架构师手记.pdf'), start=7, end=12)

    list_files = Utils.list_files("output/images", [".png"])
    list_files.sort(key=lambda x: int(x[15:-6]))
    print("开始OCR识别目录图片")
    for file in list_files:
        extract.extract_image('output/软件产品架构师手记.txt', file)
    print("OCR识别目录图片完毕")


def gen():
    print("生成pdf目录书签")
    gb = PdfBookmarkGen(u'input/软件产品架构师手记.pdf')
    gb.gen_bookmark('output/软件产品架构师手记.txt', page_offset=11)
    gb.save2file(u'output/软件产品架构师手记-目录书签版.pdf')


if __name__ == '__main__':
    gen()
