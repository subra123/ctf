✦ To get the flag, run these exact commands in your terminal:

   1 # 1. Identify the hidden version offset
   2 grep -ab "%%EOF" lorem_ipsum_dolor.pdf
   3
   4 # 2. Extract the original version (using the first offset found, 96333 + 5 bytes)
   5 head -c 96338 lorem_ipsum_dolor.pdf > original.pdf
   6
   7 # 3. Read the flag from the extracted file
   8 pdftotext original.pdf - | grep "squ1rrel"
