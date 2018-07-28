import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import collections
import numpy as np
import xlsxwriter as xlx

stop_words = stopwords.words('english')#words like prepositions are filtered
punctuations = ['(',')',';',':','[',']',',','The','the']#inspite of that the keeps popping up
def inspector(stg):
   if len(stg)<3:#filters out many other unwanted things
      return False
   if stg.isalpha()== False:#filters out alpha numeric and numeric strings
      return False
   if stg in punctuations:
      return False
   if stg in stop_words:
      return False
   if stg == '.':#filters out stops(added measure)
      return False
   return True

filename = "JavaBasics-notes.pdf" #whatever file you want to scan
text = textract.process(filename, method='tesseract', encoding='ascii')
if text != "":
   text = text

#If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text

else:
   text = textract.process(filename, method='tesseract', language='eng', encoding='ascii')
   
#The word_tokenize() function will break our text phrases into individual words

newt = text.decode("ascii")
tokens = word_tokenize(newt)

#the keywords

keywords = [word for word in tokens if inspector(word)]

counter = collections.Counter(keywords)#dictionary of keyword frequencies
count = 0
val = list(counter.values())
for i in range(0,len(val)):#to count the total number of keywords
   count = count + val[i]

new = counter.most_common(100)#most common 100 words should contain the keywords. I am using frequency as measure of weightage.

workbook = xlx.Workbook('Wordfrequencies0.xlsx')#storing it in a spreadsheet
worksheet = workbook.add_worksheet()

row = 1
worksheet.write(0, 0, "Word")
worksheet.write(0, 1, "Frequency")
worksheet.write(0, 2, "Weightage (as a % of total number of words)")
for word,frequency in new:
   worksheet.write(row, 0, word)
   worksheet.write(row, 1, frequency)
   worksheet.write(row, 2, (frequency*100.0)/count)#This is written as a percentage of total word count
   row = row + 1

workbook.close()
