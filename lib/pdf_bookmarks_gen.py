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
                segments = line.split('@')
                title = segments[0].rstrip()
                page = segments[1].strip()
                parent_page = None
                if len(segments) > 2:
                    parent_page = segments[2].strip()
            except IndexError as msg:
                print("%s,%s" % (line, msg))
                continue

            if title and page:
                try:
                    page = int(page) + page_offset
                    if parent_page:
                        parent_page = int(parent_page) + page_offset
                        bookmarks.append((title, page, parent_page))
                    else:
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
        self.parents = {}

    def save2file(self, new_file_name):

        with open(new_file_name, 'wb') as f:
            self.__writeable_pdf.write(f)
        print('目录版: {0}'.format(new_file_name))

    def add_bookmarks(self, bookmarks):

        for item in bookmarks:
            title = item[0]
            page = item[1]
            if len(item) > 2:
                parent_page = item[2]
                # parent= self.__writeable_pdf.addBookmark(title, page, parent=None, color=None, fit='/XYZ')
                parent = self.parents[str(parent_page)]
                self.__writeable_pdf.addBookmark(title, page, parent=parent, color=None, fit='/Fit')
            else:
                self.parents[str(page)] = self.__writeable_pdf.addBookmark(title, page, parent=None, color=None,
                                                                           fit='/Fit')

    def gen_bookmark(self, txt_file_path, page_offset=0):

        bookmarks = load_bookmarks_txt(txt_file_path, page_offset)
        self.add_bookmarks(bookmarks)
