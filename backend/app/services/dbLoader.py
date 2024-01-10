from utils.dbLoaderHelper import vectorStoreLoader

LOADING_DIRECTORY = input("Do you want to load a directory? (y/n): ")

if LOADING_DIRECTORY == "y":
    vectorStoreLoader("localhost", 8000, directory=True)
else:
    vectorStoreLoader("localhost", 8000)
