import asyncio
from pdf2jpg import pdf2jpg

async def extractImg(filename):
    output=f"PdfTxtBot\\Docs"
    page=pdf2jpg.convert_pdf2jpg(filename,output,dpi=300,pages="ALL")
    return page
        
if __name__=='__main__':
    asyncio.run(extractImg("PdfTxtBot\sample.pdf"))