# -*- coding: utf-8 -*-
import sys
import datetime
import os
from bs4 import BeautifulSoup

def fname_remove_invalid_chars(fname: str, symbol='-') -> str:
    """
    Takes a file name with potentially invalid characters, and substitutes the
    symbol in, in place of those invalid characters.
    
    Arguments:
    fname:   str (name of file)
    symbol:  str (symbol to substitute invalid characters to)
    
    Returns:
    str with the new file name containing symbol in place of any illegal
    characters
    """
    # Replace invalid characters with - to make filename valid
    INVALID_CHARS = ["/", ":"]
    for char in INVALID_CHARS:
        if (fname.find(char) != -1):
            temp = list(fname)
            temp[fname.find(char)] = symbol
            fname = "".join(temp)
    return fname

def get_HC_case(year: int, number: int, extension: str="rtf"):
    """
    Downloads an rtf or pdf file of the High Court Case with the year and
    number specified. Eg. get_HC_case(2017, 20) downloads [2017] HCA 20.
    Downloads sourced from highcourt website
    
    Arguments:
    year:      int (year of case to download)
    number:    int (judgment number in the year)
    extension: str ("rtf" or "pdf" file to download)
    
    Returns:
    "Skipped" if file already in current directory
    False     if file does not exist to be downloaded
    "Unicode" if unicode error with file name
    """
    VALID_TYPES = ["rtf", "pdf"]
    if (extension not in VALID_TYPES):
        raise Exception(f"Invalid document extension: {extension}.")

    import requests
    import time
    BASE_URL_RTF_DL = "http://eresources.hcourt.gov.au/downloadrtf/"
    BASE_URL_PDF_DL = "http://eresources.hcourt.gov.au/downloadPdf/"
    BASE_URL_INFO = "http://eresources.hcourt.gov.au/showCase/"
    COURT = "/HCA/"
    EXTENSION = extension
    
    CASE_NO_EXIST_TITLE = "View report"

    URL = ""
    if extension=="rtf":
        URL = BASE_URL_RTF_DL + str(year) + COURT + str(number)
    elif extension == "pdf":
        URL = BASE_URL_PDF_DL+ str(year) + COURT + str(number)
    else:
        raise Exception("Critical Error with extension")
    
    r = requests.get(URL)
    time.sleep(1)
    case_info = requests.get(BASE_URL_INFO + str(year) + COURT + str(number))
    case_info = BeautifulSoup(case_info.text, features="lxml")
    
    # Case for that year and number does not exist
    if(case_info.title.text == CASE_NO_EXIST_TITLE):
        print(f"[{year}] HCA {number} doesn't exist to download")
        return False

    #Append this to end of casename to create filename
    to_append = " [" + str(year) + "] HCA " + str(number) + "."
    fname = case_info.title.text + to_append + EXTENSION

    try:
        fname = fname_remove_invalid_chars(fname)
        
        # Check we don't already have file in our current directory
        if fname in os.listdir("."):
            print(f"Skipped     {fname}, already exists in directory.")
            return "Skipped"
        
        # Write downloaded rtf file here
        with open(fname, 'wb') as fp:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    fp.write(chunk)
            print(f"Downloaded: {case_info.title.text + to_append} as a {extension}")

    except KeyError:
        print(f"[{year}] HCA {number} doesn't exist to download")
        return False
    except OSError:
        print(f"Problem with filename: {fname}, probably unicode character, TODO")
        return "UniCode"

    return True

def get_HC_case_period(year_start: int, year_end: int, extension: str="pdf"):
    """
    Downloads all available High Court cases from the high court website, from
    year start to year end (inclusive), with the desired extension.
    
    Arguments:
    year_start:  int (first year to start downloading from)
    year_end:    int (last year to start downloading to)
    extension:   str ("rtf" or "pdf" file to download)
    
    Returns: void
    """
    start_time = datetime.datetime.now()
    iteration_time = start_time
    
    downloaded = 0          # Files downloaded per year
    total_downloaded = 0    # Files downloaded overall
    for year in range(year_start, year_end+1):
        i=1                 # Case number
        while(True):
            executed = get_HC_case(year, i, extension)
            if not executed:
                time = datetime.datetime.now() - iteration_time
                iteration_time = datetime.datetime.now()

                print(f"Downloaded {downloaded} cases for {year} in {time.total_seconds()} seconds", file=sys.stderr)
                break
            
            if (executed != "Skipped"):
                downloaded += 1
            i+=1
                
        total_downloaded += downloaded
        
    end_time = datetime.datetime.now()
    total_time_taken = end_time - start_time
    print(f"Downloaded a total of {total_downloaded} cases in {total_time_taken.total_seconds()} seconds", file=sys.stderr)

def main():
    """
    Calling the function like follows will download all the High Court cases
    from the High Court website from 2000—2019(inclusive).
    """
    get_HC_case_period(2000, 2019)
if __name__ == "__main__":
    main()