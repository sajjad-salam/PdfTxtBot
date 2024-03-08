from PdfTxtBot import PDFBot
from config import TOKEN

if __name__=='__main__':
    ob=PDFBot(TOKEN)
    ob.app.run_polling()