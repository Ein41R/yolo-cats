import os

exception_list = []

#label_path = "dataset/labels/"
label_path = "mock-data/labels"

labels = os.listdir(label_path)
for label in labels:
    label_file = os.path.join(label_path, label)
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
        f.close
