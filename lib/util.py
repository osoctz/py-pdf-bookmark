import os


class Utils:
    @staticmethod
    def write_file(file_name, data, mode):

        f = open(file_name, mode, encoding='utf8')
        f.write(data)
        f.close()

    @staticmethod
    def list_files(dir_name, suffixes):
        result = []

        for maindir, subdir, file_name_list in os.walk(dir_name):

            for filename in file_name_list:
                _path = os.path.join(maindir, filename)
                if os.path.splitext(_path)[1] in suffixes:
                    result.append(_path)

        return result
