import re
import sys
import os
import requests
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.geometry("800x600")
# bg_image = tk.PhotoImage(file="path_to_image.png")
root.configure(bg='black')
root.title("Codeforces Solution Downloader")

handle_label = tk.Label(root, text="Enter your Codeforces handle: ", fg='white', bg='black')
handle_label.pack(pady=10)

handle_entry = tk.Entry(root, width=30)
handle_entry.pack(pady=5)

status_label = tk.Label(root, text=" Status of download ", bg='white', height=2 , width=50)
status_label.pack(pady=10)

# repo_url_label = tk.Label(root, text="Enter your GitHub repository URL: ", fg='white', bg='black')
# repo_url_label.pack(pady=10)

# repo_url_entry = tk.Entry(root, width=30)
# repo_url_entry.pack(pady=5)


folder_path = tk.StringVar()


def browse_button():
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    path_label.config(textvariable=folder_path)

browse_button = tk.Button(root, text="Select Folder", command=browse_button, fg='white', bg='blue')
browse_button.pack(pady=5)

path_label = tk.Label(root, text="Please select a folder", fg='white', bg='black')
path_label.pack(pady=10)

def get_accepted_submissions():
    handle = handle_entry.get()
    url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=10000"

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    data = response.json()

    submissions = []
    for submission in data['result']:
        if submission['verdict'] == 'OK':
            submissions.append(submission)

    return submissions

def remove_special_chars(name):
    # remove special characters from name
    return re.sub(r'[^\w\s-]', '', name)

EXT = {'C++': 'cpp', 'C': 'c', 'Java': 'java', 'Python': 'py', 'Delphi': 'dpr', 'FPC': 'pas', 'C#': 'cs'}
EXT_keys = EXT.keys()

def get_Ext(lang):
    if 'C++' in lang:
        return 'cpp'
    for key in EXT_keys:
        if key in lang:
            return EXT[key]
    return ""

def download_solution(submission, folder_path):
    contest_id = str(submission['contestId'])
    problem_index = submission['problem']['index']
    solution_id = str(submission['id'])
    problem_name = submission['problem']['name']
    problem_name = remove_special_chars(problem_name) # remove special chars from problem name
    prog_lang = submission['programmingLanguage']
    ext = get_Ext(prog_lang)

    filename = f"{contest_id}_{problem_index}_{problem_name}_{solution_id}.{ext}"
    file_path = os.path.join(folder_path, filename)

     # Check if the file already exists
    if os.path.exists(file_path):
        print(f"{filename} already exists. Skipping download...")
        return filename


    url = f"https://codeforces.com/contest/{contest_id}/submission/{solution_id}"
    response = requests.get(url)

       
    success_count = 0
    fail_count = 0

    if response.status_code != 200:
        print(f"Error downloading solution for {submission['problem']['name']}")
        fail_count+=1
        status_label.config(text=f"Failed to download {fail_count} files.", fg='red')
        return

    code_start = response.text.find("<pre id=\"program-source-text\" class=\"prettyprint lang-cpp linenums program-source\" style=\"padding: 0.5em;\"")
    code_end = response.text.find("</pre>")
    source_code = response.text[code_start:code_end]

    with open(file_path, 'w', encoding='utf-8') as f:
        success_count += 1
        status_label.config(text=f"Downloaded {success_count} files successfully!", fg='green')
        f.write(source_code)
        # push_to_github(source_code , filename) 

    return filename

def download_all_solutions():
    submissions = get_accepted_submissions()

    if not submissions:
        print("No accepted submissions found.")
        return
 

    downloaded_ids = [] # create an empty list to save the ids of downloaded files

    for submission in submissions:
        filename = download_solution(submission, folder_path.get())
        if filename: # check if the file was downloaded successfully
            solution_id = submission['id']
            downloaded_ids.append(solution_id) # append the id of downloaded file to the list

    print("All solutions downloaded successfully!")
    saved_label.config(text="All solutions downloaded successfully!", fg='green')

    # save the ids to a file
   # Get the absolute path of the directory where the Python file is located
    file_dir = os.path.dirname(os.path.abspath(__file__))
    # Create the file path for downloaded_ids.txt in the same directory as the Python file
    downloaded_ids_file_path = os.path.join(file_dir, 'downloaded_ids.txt')
    # Open downloaded_ids.txt file in write mode and write the downloaded ids to it
    with open(downloaded_ids_file_path, 'w') as f:
        for id in downloaded_ids :
            f.write(str(id) + '\n')


download_button = tk.Button(root, text="Download All Solutions", command=download_all_solutions, fg='white', bg='green')
download_button.pack(pady=20)

saved_label = tk.Label(root, text="", fg='white', bg='black')
saved_label.pack(pady=10)

root.mainloop()
