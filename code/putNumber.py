import os
import PyPDF2
from fpdf import FPDF


class NumberPDF(FPDF):
    def __init__(self, numberOfPages):
        super(NumberPDF, self).__init__()
        self.numberOfPages = numberOfPages

    # Overload Header
    def header(self):
        pass

    # Overload Footer
    def footer(self):
        self.set_fill_color(251,128,114)
        self.set_draw_color(190, 75, 66)
        
        self.set_y(-15)
        self.set_x(-10)
        self.set_font('Arial', 'I', 8)
        #self.cell(-5, 3, f"Page {self.page_no()} of {self.numberOfPages}", 1, 1, 'C',fill=True,)
        self.cell(-25, 3, str(self.page_no()), 1, 1, 'C',fill=True,)
        
        #self.rect(x=100, y=100, w=400, h=200, round_corners=True)
        #self.rect(x=100, y=600, w=400, h=200, round_corners=("TOP_LEFT", "BOTTOM_RIGHT"))


def putNumberPages(path_original,outputFile):
    # Grab the file you want to add pages to
    #inputFile = PyPDF2.PdfReader("original.pdf")
    inputFile = PyPDF2.PdfReader(path_original)
    #outputFile = "originalWithPageNumbers.pdf"

    # Create a temporary numbering PDF using the overloaded FPDF class, passing the number of pages
    # from your original file
    tempNumFile = NumberPDF(len(inputFile.pages))

    # Add a new page to the temporary numbering PDF (the footer function runs on add_page and will 
    # put the page number at the bottom, all else will be blank
    for page in range(len(inputFile.pages)):
        tempNumFile.add_page()

    # Save the temporary numbering PDF
    tempNumFile.output("tempNumbering.pdf")

    # Create a new PDFFileReader for the temporary numbering PDF
    mergeFile = PyPDF2.PdfReader("tempNumbering.pdf")

    # Create a new PDFFileWriter for the final output document
    mergeWriter = PyPDF2.PdfWriter()

    # Loop through the pages in the temporary numbering PDF
    for x, page in enumerate(mergeFile.pages):
        # Grab the corresponding page from the inputFile
        inputPage = inputFile.pages[x]
        # Merge the inputFile page and the temporary numbering page
        inputPage.merge_page(page)
        # Add the merged page to the final output writer
        mergeWriter.add_page(inputPage)

    # Delete the temporary file
    os.remove("tempNumbering.pdf")

    # Write the merged output
    with open(outputFile, 'wb') as fh:
        mergeWriter.write(fh)