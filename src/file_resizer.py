"""
Resize images.

Usage:
    file_resizer.py -s <size>
    file_resizer.py -s <size> -p <new_path>
    file_resizer.py -s <size> -d <new_directory>

    file_resizer.py -h | --help
    file_resizer.py --version

Options:
    -h --help          Show this screen.
    --version          Show version.
    -s <size>          Size of the image.
    -p <new_path>      New path of the image.
    -d <new_directory> New directory of the image. Must be base path otherwise will use current directory.
    -r <rename>        Rename the file or not. 1 for yes, 0 for no. Default is 1.
"""


from glob import glob
from pathlib import Path
from PIL import Image
import os

from args import Args


def resize_image(file, size, path=None, add_extension=False):
    """
    Esta funcion redimensiona una imagen.
    """
    new_path = path or file
    if add_extension:
        # Si el nombre del archivo debe ser differente a la imagen original.
        new_path = "_resized.".join(new_path.split('.'))

    image = Image.open(file)
    image = image.resize(size, Image.NEAREST)
    image.save(new_path)


def grab_images():
    """
    Esta funcion obtiene todas las imagenes del directorio actual.
    """
    # Los archivos son todos los imagens que estan en la carpeta actual.
    files = glob('*.jpg')
    files.extend(glob('*.png'))
    files.extend(glob('*.jpeg'))
    return files


if __name__ == "__main__":
    # Los argumentos del script
    args = [
        {
            "name": "size",
            "short": "-s",
            "required": True,
        },
        {
            "name": "file",
            "short": "-f",
            "long": "--file"
        },
        {
            "name": "rename",
            "short": "-r",
            "long": "--rename",
            "default": '1'
        },
        {
            "name": "path",
            "short": "-p",
        },
        {
            "name": "directory",
            "short": "-d",
        },
    ]
    # Un parse de los args
    arg_parse = Args(args, __doc__, version="0.1", prog="file_resizer.py")
    # Los opciones
    options = arg_parse.parse()
    # Chequea los opciones
    if options.file is None:
        files = grab_images()
    else:
        files = [options.file]

    if options.directory is not None:
        # Check if the directory exists
        # If the directory doesn't exist, create it
        if not Path(options.directory).exists():
            os.mkdir(options.directory)
        file_path = options.directory
    else:
        file_path = os.getcwd()

    for file in files:
        resize_image(
            file,
            tuple(
                map(
                    lambda x: int(x),
                    options.size.split(',')
                )
            ),
            f"{file_path}/{file}",
            options.rename == '1'
        )
