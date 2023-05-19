import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import re
import sys
import os
import requests
from github import Github


LARGEFONT = ("Verdana", 30)
LARGEFONT2 = ("Verdana", 10)

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Coeforces-Git-Integration")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage,GithubPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.handle = None  # Initialize handle attribute
        self.path = None  # Initialize path attribut
        # Left column with blue background

        left_frame = tk.Frame(self, bg='blue', width=self.winfo_screenwidth() // 2)
        left_frame.pack(side='left', fill='y')

        welcome_label = ttk.Label(left_frame, text="Welcome", font=LARGEFONT, foreground='white', background='blue')
        welcome_label.pack(pady=50)
        
        description_label = ttk.Label(left_frame, text="Codefroces-Git-Integration is a tool where u can synchronize \n and manage solutions submitted on Codeforces with\nyour GitHub account ", font=LARGEFONT2, foreground='white', background='blue')
        description_label.pack(pady=10)


        # Right column with labels and entry fields
        right_frame = tk.Frame(self,  bg='#F6F1F1')
        right_frame.pack(side='left', fill='y', padx=10)

        label = ttk.Label(right_frame, text="CodeForces Config", font=LARGEFONT ,background='#F6F1F1')
        label.pack(pady=10)

        handle_label = ttk.Label(right_frame, text="Enter your Codeforces handle:" ,background='#F6F1F1')
        handle_label.pack(pady=5)

        handle_entry = ttk.Entry(right_frame, width=30)
        handle_entry.pack(pady=5)

        path_label = ttk.Label(right_frame, text="Select a folder:", background='#F6F1F1')
        path_label.pack(pady=5)

        def select_folder():
            folder_path = filedialog.askdirectory()
            path_entry.delete(0, tk.END)  # Clear the entry field
            path_entry.insert(0, folder_path)  # Insert the selected folder path

        browse_button = ttk.Button(right_frame, text="Browse", command=select_folder)
        browse_button.pack(pady=5)

        path_entry = ttk.Entry(right_frame, width=30)
        path_entry.pack(pady=5)

        button1 = ttk.Button(right_frame, text="Next",
                             command=lambda: [ self.load_params(handle_entry , path_entry, controller), controller.show_frame(GithubPage)] )
        button1.pack(pady=50)

    def load_params(self , handle_entry , path_entry, controller) :
        self.handle = handle_entry.get()
        self.path = path_entry.get()
        print(self.handle)
        print(self.path)

    def get_handle(self):
        return self.handle
        
    def get_path(self):
        return self.path
       
        
    def get_startPage_labels(self):
        if self.handle and self.path:
            return {
                "handle": self.handle,
                "path": self.path
            }
        else:
            return None
        
class GithubPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#F6F1F1')
        self.token = None
        self.username = None
        self.repo = None
        self.comit = None
        
        label = ttk.Label(self, text="GitHub Configuration", font=LARGEFONT, background='#F6F1F1')
        label.pack(pady=20)

        form_frame = tk.Frame(self, bg='#F6F1F1')
        form_frame.pack(pady=10)

        token_label = ttk.Label(form_frame, text="GitHub Token:")
        token_label.pack(pady=5)

        token_entry = ttk.Entry(form_frame, width=30)
        token_entry.pack(pady=5)

        username_label = ttk.Label(form_frame, text="GitHub Username:")
        username_label.pack(pady=5)

        username_entry = ttk.Entry(form_frame, width=30)
        username_entry.pack(pady=5)

        repo_label = ttk.Label(form_frame, text="Repository Name:")
        repo_label.pack(pady=5)

        repo_entry = ttk.Entry(form_frame, width=30)
        repo_entry.pack(pady=5)

        commit_label = ttk.Label(form_frame, text="Commit Message:")
        commit_label.pack(pady=5)

        commit_entry = ttk.Entry(form_frame, width=30)
        commit_entry.pack(pady=5)

        button_frame = tk.Frame(self, bg='#F6F1F1')
        button_frame.pack(pady=10)

        button1 = ttk.Button(button_frame, text="Sync", command=lambda: [ self.load_params( token_entry ,username_entry , repo_entry , commit_entry , controller ) ,controller.show_frame(Page2)])
        button1.pack(pady=5)

        button2 = ttk.Button(button_frame, text="Back", command=lambda: controller.show_frame(StartPage))
        button2.pack(pady=5)

    def load_params(self  ,token_entry ,username_entry , repo_entry , commit_entry , controller) :
        self.token =token_entry.get()
        self.username = username_entry.get()
        self.repo = repo_entry.get()
        self.comit =commit_entry.get()

    def get_token(self):
        return self.token 
    
    def get_username(self):
        return self.username
    
    def get_repo(self) :
        return self.repo
    
    def get_comit(self) :
        return self.comit

    def get_gihtubPage_labels(self):
        if self.handle and self.path:
            return {
                "token": self.token,
                "username": self.username,
                "repo": self.repo,
                "commit": self.comit
            }
        else:
            return None

class Credential(StartPage , GithubPage):
    def __init__(self):
        super().__init__()
        #  this class will contian all the attributes to be passed to the codefores intgeration class 

class CodeForcesIntegration():
    def __init__(self , start ):
        self.handle = None
        self.path = None
        self.token= None
        self.username = None
        self.repo = None
        self.commit = None
        
    def get_accepted_submissions(self):
        
        url = f"https://codeforces.com/api/user.status?handle={self.handle}&from=1&count=10000"
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

    def get_Ext(lang):
        EXT = {'C++': 'cpp', 'C': 'c', 'Java': 'java', 'Python': 'py', 'Delphi': 'dpr', 'FPC': 'pas', 'C#': 'cs'}
        EXT_keys = EXT.keys()

        if 'C++' in lang:
            return 'cpp'
        for key in EXT_keys:
            if key in lang:
                return EXT[key]
        return ""

    def download_solution(self , submission, folder_path):
        contest_id = str(submission['contestId'])
        problem_index = submission['problem']['index']
        solution_id = str(submission['id'])
        problem_name = submission['problem']['name']
        problem_name = self.remove_special_chars(problem_name) # remove special chars from problem name
        prog_lang = submission['programmingLanguage']
        ext = self.get_Ext(prog_lang)

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
            # status_label.config(text=f"Failed to download {fail_count} files.", fg='red')
            return

        code_start = response.text.find("<pre id=\"program-source-text\" class=\"prettyprint lang-cpp linenums program-source\" style=\"padding: 0.5em;\"")
        code_end = response.text.find("</pre>")
        source_code = response.text[code_start:code_end]

        with open(file_path, 'w', encoding='utf-8') as f:
            success_count += 1
            # status_label.config(text=f"Downloaded {success_count} files successfully!", fg='green')
            f.write(source_code)
            self.push_to_github(source_code, filename)  # Upload to GitHub

        return filename

    def download_all_solutions(self):
        submissions = self.get_accepted_submissions()

        if not submissions:
            print("No accepted submissions found.")
            return
        downloaded_ids = [] # create an empty list to save the ids of downloaded files

        for submission in submissions:
            filename = self.download_solution(submission, self.path)
            if filename: # check if the file was downloaded successfully
                solution_id = submission['id']
                downloaded_ids.append(solution_id) # append the id of downloaded file to the list

        print("All solutions downloaded successfully!")
        # saved_label.config(text="All solutions downloaded successfully!", fg='green')

        # save the ids to a file
        # Get the absolute path of the directory where the Python file is located
        file_dir = os.path.dirname(os.path.abspath(__file__))
        # Create the file path for downloaded_ids.txt in the same directory as the Python file
        downloaded_ids_file_path = os.path.join(file_dir, 'downloaded_ids.txt')
        # Open downloaded_ids.txt file in write mode and write the downloaded ids to it
        with open(downloaded_ids_file_path, 'w') as f:
            for id in downloaded_ids :
                f.write(str(id) + '\n')
    
    def push_to_github(self, source_code, filename):
        if not self.token or not self.username or not self.repo:
            print("GitHub credentials not provided. Skipping upload...")
            return

        try:
            g = Github(self.token)
            user = g.get_user(self.username)
            repository = user.get_repo(self.repo)
            commit = repository.create_file(filename, "Adding solution", source_code, branch="main")
            print("Solution uploaded to GitHub successfully!")
        except Exception as e:
            print(f"Error uploading solution to GitHub: {str(e)}")


