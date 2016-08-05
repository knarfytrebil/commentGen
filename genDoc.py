import sys, os
from html2text import html2text

folder = sys.argv[1]
abs_folder = os.path.abspath(folder)

def walk(path):
    for subdir, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.html'):
                print subdir, file
                abs_path = os.path.join(subdir, file)
                # print html2text.html2text("<p>Hello, world.</p>")
                f = open(abs_path, 'r')
                html = f.read().decode('utf8','ignore')
                f.close()
                md_path = abs_path.replace('/out/','/out_md/').replace('.html','.md')
                if not os.path.exists(os.path.dirname(md_path)):
                    try:
                        os.makedirs(os.path.dirname(md_path))
                    except OSError as exc: # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise
                f = open(md_path, 'w')
                md = html2text(html).encode('utf8','ignore')
                f.write(md)
                f.close()
                print abs_path

walk(abs_folder)
