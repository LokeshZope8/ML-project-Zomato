from setuptools import setup, find_packages
from typing import List

REQUIREMENTS_FILE_NAME = "requirements.txt"

#to install requirements.txt on single time
HYPHEN_E_DOT = "-e ."

#in this function we are doing
# open requirements.txt 
# read requirements.txt
#replace /n in requirements.txt file with null
def get_requirements_list()->List[str]:#-> indicates returns list of string
    with open(REQUIREMENTS_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
        requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
        if HYPHEN_E_DOT in requirement_list:#to install requirements.txt on single time
            requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list    

    
setup(
    name = "Machine Learining Project Zomato", 
    version = "0.0.1", 
    description = "This is a Machine Learining Project for Zomato in modular code", 
    author = "Lokesh", 
    author_email = "lokeshz9999@gmail.com", 
    packages = find_packages(), 
    install_requires = get_requirements_list(),
    
    )