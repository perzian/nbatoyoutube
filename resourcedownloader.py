def get_filename_from_cd(cd):
    import re
    if not cd:
        return None
    file_name = re.findall('filename=(.+)', cd)
    if len(file_name) == 0:
        return None
    return file_name[0]


def download_file(url, name="tempfile.ext"):
    print ("Downloading..." + url)
    import requests
    import random
    r = requests.get(url, allow_redirects=True)
    filename = get_filename_from_cd(r.headers.get('content-disposition'))
    if filename is None:
        filename = name
    open(filename, 'wb').write(r.content)
    return filename
