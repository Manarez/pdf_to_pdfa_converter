import os

from ghostscript import Ghostscript

LICENSE = '''
The MIT License (MIT)

Copyright (c) 2025 Nikolai Kubasov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

The software utilizes Ghostscript, which is distributed under the Affero
General Public License (AGPL) or a commercial license. If you intend to use
this software or Ghostscript in a manner that constitutes distribution under
AGPL, you must ensure compliance with the terms of the AGPL license. For more
details, see https://www.ghostscript.com/.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

START_TEXT = '''
---------------------------------------------------------
\nПрограмма для конвертации файлов из формата PDF в PDF/A.
\nКонвертирует все находящиеся в папке PDF-файлы,
в том числе находящеся во вложенных папках.
\nДля начала нажмите Enter.
'''

PATH_QUESTION = '''
---------------------------------------------------------
\nВведите директорию папки с PDF-файлами:\n
'''

RESTART_QUESTION = '''
---------------------------------------------------------
\nКонвертация завершена.
\n1 - ПОВТОРИТЬ ОПЕРАЦИЮ
\n0 - ЗАКРЫТЬ ПРОГРАММУ\n
'''

DELETE_QUESTION = '''
---------------------------------------------------------
\nВы хотите удалить исходные файлы?
\n1 - ДА (файлы будут заменены на новые)
\n0 - НЕТ (будут созданы новые файлы без удаления старых)\n
'''

INPUT_VALUE = [1, 0]


def pdf_converter(input_path, delete=None):
    '''Функция, конвертирующая pdf-файлы в формат PDF/A.'''
    for file_name in os.listdir(input_path):
        path_name = os.path.join(input_path, file_name)
        if file_name.endswith('.pdf'):
            text_for_output_file = os.path.join(
                input_path, 'PDFA-' + file_name
            )
            output_file = (
                f'-sOutputFile={text_for_output_file}'
            )
            Ghostscript(
                'gs',
                '-dPDFA',
                '-dBATCH',
                '-dNOPAUSE',
                '-sProcessColorModel=DeviceRGB',
                '-sDEVICE=pdfwrite',
                output_file,
                path_name
            )
            if delete:
                os.remove(path_name)
        elif os.path.isdir(path_name):
            next_filepath = os.path.join(path_name, '')
            pdf_converter(next_filepath)
        else:
            continue


def ask_for_value(text):
    '''
    Функция, проверяющая введенные пользователем значения на корректность.
    '''
    while True:
        if text == PATH_QUESTION:
            value = os.path.join(input(text), '')
            if not os.path.isdir(value):
                print('Введенный текст не является директорией папки.')
            else:
                break
        else:
            value = int(input(text))
            if value not in INPUT_VALUE:
                print('Введено недопустимое значение.')
            else:
                break
    return value


def main():
    input_path = ask_for_value(PATH_QUESTION)
    delete = ask_for_value(DELETE_QUESTION)
    pdf_converter(input_path, delete)
    restart = ask_for_value(RESTART_QUESTION)
    if restart:
        main()


if __name__ == '__main__':
    print(LICENSE)
    input(START_TEXT)
    main()
