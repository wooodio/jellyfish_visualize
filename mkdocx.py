from pdf2docx import Converter
from pandas import Series, DataFrame

pdf_file = r'C:\Users\wjg\Desktop\해파리\24.08.14_해파리+주간보고(15차) (1).pdf'
docx_file = r'C:\Users\wjg\Desktop\해파리\24.08.14_해파리+주간보고.docx'

#cv = Converter(pdf_file)
# cv.convert(docx_file)
# cv.close()
cv = Converter(docx_file)
tables = cv.extract_tables(start=0, end=3)

data = DataFrame(tables[1])
print(data)
