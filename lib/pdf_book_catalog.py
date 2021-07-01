import fitz
import os


def export_book_catalog(doc, start, end):
    """
    提取pdf指定页为图片
    :param doc:
    :param start:
    :param end:
    :return:
    """
    output_dir = 'output/images/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    for i in range(start, end):

        img_list = doc.getPageImageList(i)

        for j, img in enumerate(img_list):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha < 4:
                pix.writePNG(output_dir + "p%s-%s.png" % (i + 1, j + 1))
            else:
                pix0 = fitz.Pixmap(fitz.csRGB, pix)
                pix0.writePNG(output_dir + "p%s-%s.png" % (i + 1, j + 1))
                pix0 = None
            pix = None
