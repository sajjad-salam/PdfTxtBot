from PyPDF2 import PdfReader


class TextExtractor:
    def __init__(self, filename:str) -> None:
        self.__doc__ = PdfReader(filename)

    @property
    def extract(self) -> str:
        pages = len(self.__doc__.pages)
        outpub = ""
        try:
            for i in range(pages):
                outpub += self.__doc__.pages[i].extract_text()
            return outpub
        except Exception as e:
            print(e)


if __name__ == '__main__':
    txt = TextExtractor("https://api.telegram.org/file/bot6000547107:AAGQFqWez7wUDmT2xSWMS5GG_1tRH691cFk/documents/file_0.pdf")
    print(txt.extract)
