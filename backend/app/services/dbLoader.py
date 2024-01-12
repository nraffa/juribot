from utils.dbLoaderHelper import vectorStoreLoader

LOADING_DIRECTORY = input("Do you want to load a directory? (y/n): ")

if LOADING_DIRECTORY == "y":
    vectorStoreLoader("chroma-db", 8000, directory=True)
else:
    vectorStoreLoader("chroma-db", 8000)
