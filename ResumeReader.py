#ask for help with regex of address
#ask how to get last name also with this regex
#ask how to write into analysis box of GUI

import tkinter as tk
from tkinter import filedialog, END
import re
import PyPDF2
import os
file_path = ""


#REGULAR EXPRESSIONS

zipRegex = r"\b\d{5}(?:-\d{4})?\b" #working
nameRegex = r'[A-Za-z]{2,20}\s( ?[A-Za-z]{2,20})(\s[A-Za-z]{2,20})?\b' #working 
phoneRegex = r'\s*(\+1\s*)?(?:\(\d{3}\)|\d{3})[-\s]*\d{3}[-\s]*\d{4}[-\s]' #working 
emailRegex = r'[A-Za-z][A-Za-z0-9._%+-]*?\.? ?[A-Za-z0-9._%+-]* ?@ ?[A-Za-z0-9.-]+ ' #working
addressRegex = r'\d+\s+[\w\s]+[,.]?\s*\w+\s*[,.]?\s*\w+\s*[,.]?\s+\d{5}(-\d{4})?' #working 

analysisGPA = r'\b\d\.\d{2}\b' # gpa of greater than 3.50, working
analysisRegexLocal = r'(MN|Minnesota)(?=\s[,.]?\s*\d{5}(-\d{4})?)' # mn address, working
analysisRegexProjects= r'(?i:project|projects)' # provides examples of projects , working
analysisRegexBachelor = r'(?i)\Bachelor of Computer Science\b' # has bachelor degree for CS, working
analysisRegexPython = r'(?i)python' # specific programming language: python, working 


def browse_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    file_name_label.config(text='File: ' + os.path.basename(file_path))

def extract_info(): 
   global file_path
   global zipRegex
   global nameRegex
   global addressRegex
   global phoneRegex
   global emailRegex
   global analysisGPA
   global analysisRegexLocal
   global analysisRegexBachelor
   global analysisRegexProjects
   global analysisRegexPython
   
   numReq = 0 #counter to see if applicant is worth being considered
   analysisStringRec = '' #empty string to pass if canidate is worthy
   analysisStringNoRec = '' #empty string to pass if canidate is not worthy
   
   if file_path:
        try:
            pdf_file = open(file_path, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            large_string = ""
            
            for page_num in range(len(pdf_reader.pages)):
                large_string += pdf_reader.pages[page_num].extract_text()
            
            pdf_file.close()
            
            #all data handling is found below
            print('-----------------------------------------------------------') #divider so i do not go crazy reading the terminal
            
            nameText = re.search(nameRegex, large_string) #name handling, need help
            if nameText:
                print('Name: ', nameText[0])
                name_entry.delete(0,END)
                name_entry.insert(0, nameText[0])
            else:
                print('Name: No Name Found')
                
            phoneText = re.search(phoneRegex, large_string) #phone handling 
            if phoneText:
                phone_entry.delete(0, END)
                phone_entry.insert(0, phoneText.group())
                print('Phone Number: ', phoneText.group())    
            else:
                print('No phone number found')
            
            #address handling
            addressText = re.search(addressRegex, large_string)
            if addressText:
                print('Address: ', addressText.group())
                houseRegex = r'^([^,\.]+)'
                house = re.search(houseRegex, addressText.group())
                address_entry.delete(0,END)
                address_entry.insert(0, house.group())
                cityRegex = r'(?<=[,.]\s)(\w+)'
                city = re.search(cityRegex, addressText.group())
                city_entry.delete(0,END)
                city_entry.insert(0,city.group())
                stateRegex = r'(\w+)(?=\s*[,.]?\s*\d{5}(-d{4})?$)'
                state = re.search(stateRegex, addressText.group())
                state_entry.delete(0,END)
                state_entry.insert(0,state.group())
            else:
                print('Address not found.')
            
            zipText = re.findall(zipRegex, large_string) #zip code handling
            if zipText:
                zip_entry.delete(0,END)
                zip_entry.insert(0, zipText[0])
            else:
                print('Zip not found.')
            
            emailText = re.search(emailRegex, large_string) #email handling
            if emailText:
                email_entry.delete(0,END)
                email_entry.insert(0, emailText.group())
                print('Email: ', emailText.group())
            else:
                print('Email not found.')
                
             
            #five requirements to be considered            
            analysisTextGPA = re.search(analysisGPA, large_string) # GPA Conditionals, required 1
            if analysisTextGPA:
                if float(analysisTextGPA.group()) > float(3.80):
                    print('Req. 1: PASS! GPA: ', analysisTextGPA.group(), '= High enough GPA.')
                    numReq += 1 
                else:
                    print('Req. 1: FAIL! GPA found, must be higher than 3.80. GPA Provided: ', analysisTextGPA.group())
            else:
                print('Req. 1: FAIL! GPA: No GPA Provided.')
                
            isLocal = re.search(analysisRegexLocal, large_string) #is local Conditionals, required 2
            if isLocal:
                print('Req. 2 Local: PASS! Potential emplpyee is local.')
                numReq += 1
            else:
                print('Req. 2 Local: FAIL! Potential employee is not local.')
        
            hasProjects = re.search(analysisRegexProjects, large_string) #has projects provided conditionals required 3
            if hasProjects:
                print('Req. 3 Projects: PASS! Potential employee has projects provided.')
                numReq += 1
            else:
                print('Req. 3 Projects: FAIL! Potential employee does not have projects provided.')
                
            hasBachelorCS = re.search(analysisRegexBachelor, large_string) #provides bachelor degree in CS, required 4
            if hasBachelorCS:
                print('Req. 4 Bachelor: PASS! Has a bachelor degree in CS.')
                numReq += 1
            else:
                print('Req. 4 Bachelor: FAIL! Does not have a bachelors degree in CS.')
            
            hasPython = re.search(analysisRegexPython, large_string) #has python experience, required 5
            if hasPython:
                print('Req. 5 Python: PASS! Potential employee has experience in Python.')
                numReq += 1
            else:
                print('Req. 5 Python: FAIL! Potential employee has no experience in Python.') 
            
            # Analysis box handling 
            analysisStringRec += 'Applicant has all 5 requirements. Has Python : TRUE, Has Projects: TRUE, Has bachelor in CS: TRUE, Is local to MN: TRUE, GPA is higher than 3.80: TRUE'
            analysisStringNoRec += 'Applicant does not meet requirements.' 
            if numReq == 5:
                analysis_box.delete("1.0", tk.END)
                analysis_box.insert(tk.END, analysisStringRec)  
                print('Applicant has all 5 requirements. Consider this Applicant.')
            else:
                analysis_box.delete("1.0", tk.END)
                analysis_box.insert(tk.END, analysisStringNoRec)
                print('Applicant does not have all 5 Requirements. Dont consider this Applicant.')
  
        except Exception as e:
            analysis_box.delete("1.0", tk.END)
            analysis_box.insert(tk.END, f"Error: {str(e)}")

# You need to work on this function.
def reset_memory():
    name_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    state_entry.delete(0, tk.END)
    zip_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
# Create the main window
root = tk.Tk()
root.title("Smart Resume reader")
root.geometry("650x580")

# First row: File browse button
file_button = tk.Button(root, text="Browse", command=browse_file)

file_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")

file_name_label = tk.Label(root, text="File:")

file_name_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Second row: Read button
extract_btn = tk.Button(root, text="Extract", command=extract_info)

extract_btn.grid(row=1, column=0, padx=10, pady=5, sticky="w")

reset_btn = tk.Button(root, text="Reset Meomry", command=reset_memory)

reset_btn.grid(row=1, column=4, padx=10, pady=5, sticky="w")

# Third row: Name label and text box
name_label = tk.Label(root, text="Name:")

name_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

name_entry = tk.Entry(root, width=25)

name_entry.grid(row=2, column=1, padx=10, pady=5)

# Fourth row: Address label and text box
address_label = tk.Label(root, text="Address:")

address_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

address_entry = tk.Entry(root, width=25)

address_entry.grid(row=3, column=1, padx=10, pady=5)

# Fifth row: City label and text box
city_label = tk.Label(root, text="City:")

city_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

city_entry = tk.Entry(root, width=25)

city_entry.grid(row=4, column=1, padx=10, pady=5)

# Sixth row: State label and text box
state_label = tk.Label(root, text="State:")

state_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

state_entry = tk.Entry(root, width=25)

state_entry.grid(row=5, column=1, padx=10, pady=5)

# Seventh row: Zip code label and text box
zip_label = tk.Label(root, text="Zip Code:")

zip_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")

zip_entry = tk.Entry(root, width=25)

zip_entry.grid(row=6, column=1, padx=10, pady=5)

# Eighth row: Phone number label and text box
phone_label = tk.Label(root, text="Phone Number:")

phone_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")

phone_entry = tk.Entry(root, width=25)

phone_entry.grid(row=7, column=1, padx=10, pady=5)

# Ninth row: Email address label and text box
email_label = tk.Label(root, text="Email Address:")

email_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")

email_entry = tk.Entry(root, width=25)

email_entry.grid(row=8, column=1, padx=10, pady=5)

# Tenth row: Multiline text box
text_label = tk.Label(root, text="Analysis:")

text_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")

analysis_box = tk.Text(root, width=40, height=12)

analysis_box.grid(row=9, column=1, padx=10, pady=5)

root.mainloop()