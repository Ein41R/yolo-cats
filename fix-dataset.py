import os
from sys import argv

exception_list = []

for option in argv:
    if option.startswith("--path="):
        label_path = option.split("=")[1]
    else:
        label_path = "datasets/train/labels"

print(f"Processsing labels in {label_path}...")
input("Press Enter to continue...")

labels = sorted(os.listdir(label_path))

for label in labels:
    label_file = os.path.join(label_path, label)
    #print(f"Fixing: {label_file}...")
    with open(label_file, "r") as f:
        lines = f.readlines()
        new_lines = []
        for idx, line in enumerate(lines):
            if line.startswith("25 "):
                #overwrite to 0 
                f.close()
                
                new_lines.append(line.replace("25 ", "0 "))
            else:
                new_lines.append(line)
                exception_list.append(label_file)

        with open(label_file, "w") as fi:
            fi.writelines(new_lines)
        f.close()

print(f"Processed {len(labels)} labels. {len(exception_list)} exceptions found.")
print("Writing exceptions to exceptions.txt...")
with open("exceptions.txt", "w") as f:
    for exception in exception_list:
        f.write(exception + "\n")
print("Done.")