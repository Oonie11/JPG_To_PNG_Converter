import os
from PIL import Image

def list_folders(path='.'):
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    return folders

def select_folder(prompt, folders):
    while True:
        print("\n" + prompt)
        for i, folder in enumerate(folders, 1):
            print(f"{i}. {folder}")
        print(f"{len(folders) + 1}. Enter a custom path")
        print(f"{len(folders) + 2}. Rescan for new folders")
        
        try:
            choice = int(input("Enter your choice (number): "))
            if 1 <= choice <= len(folders):
                return folders[choice - 1]
            elif choice == len(folders) + 1:
                custom_path = input("Enter the custom path: ").strip()
                if os.path.isdir(custom_path):
                    return custom_path
                else:
                    print("Invalid path. Please try again.")
            elif choice == len(folders) + 2:
                print("Rescanning for folders...")
                return "rescan"
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_output_folder():
    while True:
        choice = input("Do you want to (1) choose an existing folder or (2) create a new folder for output? Enter 1 or 2: ").strip()
        if choice == '1':
            folders = list_folders()
            selected = select_folder("Choose an output folder:", folders)
            if selected != "rescan":
                return selected
        elif choice == '2':
            new_folder = input("Enter the name for the new output folder: ").strip()
            full_path = os.path.join('.', new_folder)
            os.makedirs(full_path, exist_ok=True)
            return new_folder
        else:
            print("Invalid choice. Please enter 1 or 2.")

def convert_jpg_to_png(image_folder, converted_folder):
    # Check if the output folder exists, if not create it.
    if not os.path.exists(converted_folder):
        os.makedirs(converted_folder)

    conversion_count = 0
    # Convert and save to png image
    for file_name in os.listdir(image_folder):
        if file_name.lower().endswith(('.jpg', '.jpeg')):
            img = Image.open(os.path.join(image_folder, file_name))
            name, _ = os.path.splitext(file_name)
            img.save(os.path.join(converted_folder, f"{name}.png"), 'PNG')
            print(f'Converted {file_name} to PNG')
            conversion_count += 1

    print(f'All done! Converted {conversion_count} images.')
    return conversion_count

def get_user_input():
    print('\n' + '='*40)
    print('Welcome to JPEG to PNG Converter!')
    print('='*40)
    print('Instructions:')
    print('1. You will choose the input folder containing JPEG files.')
    print('2. You will then choose or create an output folder for PNG files.')
    print('3. Confirm to start the conversion process.')
    print('='*40)

    input_folder = None
    while input_folder is None:
        input_folders = list_folders()
        selected = select_folder("Choose an input folder containing JPEG files:", input_folders)
        if selected != "rescan":
            input_folder = selected

    output_folder = None
    while output_folder is None:
        output_folder = get_output_folder()

    while True:
        user_confirmation = input("\nReady to start converting? (yes/no): ").lower().strip()
        if user_confirmation == 'yes':
            print("\nStarting conversion process...")
            return input_folder, output_folder
        elif user_confirmation == 'no':
            print("\nExiting program. No files were converted.")
            return None, None
        else:
            print("\nInvalid input. Please answer only 'yes' or 'no'.")

def main():
    while True:
        input_folder, output_folder = get_user_input()
        if input_folder and output_folder:
            try:
                converted_count = convert_jpg_to_png(input_folder, output_folder)
                print(f"\nSuccessfully converted {converted_count} images from '{input_folder}' to '{output_folder}'.")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Conversion cancelled.")
        
        while True:
            choice = input("\nDo you want to (1) convert more images or (2) exit the program? Enter 1 or 2: ").strip()
            if choice == '1':
                print("\nRestarting the program...")
                break
            elif choice == '2':
                print("\nThank you for using the JPEG to PNG Converter. Goodbye!")
                return
            else:
                print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
