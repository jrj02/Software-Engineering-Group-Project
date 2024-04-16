import os

def get_filenames(folder_path):
    return {os.path.splitext(file)[0] for file in os.listdir(folder_path)}

def compare_folders(png_folder, txt_folder):
    png_files = get_filenames(png_folder)
    txt_files = get_filenames(txt_folder)
    
    png_only = png_files - txt_files
    txt_only = txt_files - png_files
    
    return png_only, txt_only

def main():
    png_folder = "C:/Users/rayev/Desktop/folder1"
    txt_folder = "C:/Users/rayev/Desktop/folder2"
    
    if not os.path.exists(png_folder) or not os.path.exists(txt_folder):
        print("One or both of the folders do not exist.")
        return
    
    png_only, txt_only = compare_folders(png_folder, txt_folder)
    
    print("PNG files without matching TXT files:")
    for file in png_only:
        print(file)
    
    print("\nTXT files without matching PNG files:")
    for file in txt_only:
        print(file)

if __name__ == "__main__":
    main()
