def file_path(file):
    from os.path import join, dirname
    fp = join(dirname(__file__), file)
    return fp