"""
Bypass los paginas que requieren una cuenta.
Funciona bien con Medium.

Usage:
    membership_articles.py -u <url> [-f <file> or -d <directory>] [-o]
    membership_articles.py -h | --help
    membership_articles.py --version

Options:
    -h --help          Show this screen.
    --version          Show version.
    -u <url>           Url of the article.
    -f <file>          File to save the article.
    -o                 Open the article.
    -d <directory>     Directory to save the article.
"""


import requests
import os
import codecs
import webbrowser

from lxml.html import fromstring
from args import Args


version = "0.1"


def grab_article(url, directory=None, file=None):
    """
    Grab the article.

    Returns:
        str: The path to the article.
    """
    # Make the request
    r = requests.get(url)
    content = r.text
    directory = directory or os.getcwd()

    # Check if the request was successful
    if r.status_code != 200:
        raise Exception("Error al obtener el articulo.")

    # Chequea si el arhcivo esta vacio
    if file is None:
        # Hacemos un parse del r.content para obtener el titulo
        tree = fromstring(r.content)
        title = tree.findtext(".//title")
        file = "".join(title.split('.')[0]) + ".html"

    content = content.replace('<script src="https://cdn-client.medium.com/lite/static/js/manifest.b9d2c389.js"></script>', '')
    # Save the article
    with codecs.open(f"{directory}/{file}", "w", "utf-8") as f:
        f.write(content)
    return file


def open_file_in_browser(file):
    """
    Open the file in the browser.
    """
    # Busca el path absoluto del archivo
    path = "file://" + os.path.abspath(file)

    webbrowser.open(path)


if __name__ == "__main__":
    args =[
        {
            "name": "url",
            "short": "-u",
            "long": "--url",
            "required": True
        },
        {
            "name": "file",
            "short": "-f",
            "long": "--file",
            "required": False
        },
        {
            "name": "open",
            "short": "-o",
            "default": "0"
        },
        {
            "name": "directory",
            "short": "-d",
            "long": "--directory",
            "required": False
        }
    ]
    arg_parser = Args(args, __doc__, version, "membership_articles.py")
    options = arg_parser.parse()

    file_path = grab_article(options.url, options.directory, options.file)
    print("Articulo guardado en: {}".format(file_path))
    
    # Chequea si teneoms que abrir el archivo
    if options.open == "1":
        open_file_in_browser(file_path)