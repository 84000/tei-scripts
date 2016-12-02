# Glossary conversion

This script are used to convert an Excel glossary into xml.

# Dependencies

The scripts are written in Python3, but does not need any module. The different variables are hardcoded so that it can run directly from the Windows Explorer, without the need for command-line arguments.

# Use

These instructions are for non-Python-savvy users, Unix and Python savvy will see more direct and simple methods

## Conversion from csv format

#### CSV conversion

The first step is to convert the glossary into one `.csv` file.

Several methods are possible, here is the one using [LibreOffice](https://www.libreoffice.org/):
 * select the first sheet of the Excel file
 * 'File -> Save As...' and save as `input.csv`, using the default options (UTF-8 is important)
 * you'll get a warning stating that only the current sheet has been exported, that's fine
 * do the same operation with the other sheets, saving them as `input-2.csv` and `input-3.csv`
 * open `input.csv` with your favorite text editor (try [Notepad++](https://notepad-plus-plus.org/fr/) if you don't have any)
 * append the content of `input-2.csv` and `input-3.csv` to `input.csv`, keeping the first lines
 
 #### Script use

  * copy the `convert-glossary-from-csv.py` file in the same folder as the `input.csv` file
  * change the `glossname` variable to fit the ID of the glossary you're working on
  * run the script (double clicking it)
 
This will produce an `output.xml` file with the final TEI markup.

## Conversion from TEI

First convert your excel file to TEI (method to be documented), then:

 * rename you TEI file `input.xml`
 * run `convert-glossary-from-tei.py` in the same folder
 * enjoy you `output.xml`