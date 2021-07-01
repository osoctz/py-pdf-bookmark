from PyPDF2 import PdfFileReader as reader, PdfFileWriter as writer
import os


def load_bookmarks_txt(txt_file_path, page_offset=0):

    bookmarks = []
    with open(txt_file_path, 'r') as fin:
        for line in fin:
            line = line.rstrip()
            if not line:
                continue

            try:
                title = line.split('@')[0].rstrip()
                page = line.split('@')[1].strip()
            except IndexError as msg:
                print("%s,%s" %(line,msg))
                continue

            if title and page:
                try:
                    page = int(page) + page_offset
                    bookmarks.append((title, page))
                except ValueError as msg:
                    print(msg)

    return bookmarks


class PdfBookmarkGen(object):

    def __init__(self, pdf_file_path):

        self.__pdf = reader(pdf_file_path)
        self.file_name = os.path.basename(pdf_file_path)
        self.metadata = self.__pdf.getXmpMetadata()
        self.doc_info = self.__pdf.getDocumentInfo()
        self.pages_num = self.__pdf.getNumPages()
        self.__writeable_pdf = writer()
        for idx in range(self.pages_num):
            page = self.__pdf.getPage(idx)
            self.__writeable_pdf.insertPage(page, idx)

    def save2file(self, new_file_name):

        with open(new_file_name, 'wb') as f:
            self.__writeable_pdf.write(f)
        print('目录版: {0}'.format(new_file_name))

    def add_bookmarks(self, bookmarks):

        for title, page in bookmarks:
            self.__writeable_pdf.addBookmark(title, page, parent=None, color=None, fit='/Fit')

    def gen_bookmark(self, txt_file_path, page_offset=0):

        bookmarks = load_bookmarks_txt(txt_file_path, page_offset)
        self.add_bookmarks(bookmarks)


# if __name__ == '__main__':
#     pdf_handler = PdfBookmarkGen(u'/Users/zantang/PycharmProjects/py-pdf-bookmark/input/软件产品架构师手记.pdf')
#     pdf_handler.gen_bookmark('/Users/zantang/PycharmProjects/py-pdf-bookmark/output/软件产品架构师手记.txt', page_offset=11)
#     pdf_handler.save2file(u'软件产品架构师手记-目录书签版.pdf')
