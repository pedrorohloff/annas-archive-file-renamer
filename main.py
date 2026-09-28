import os

source = "/home/phr/Documents/books"
target_dir = os.path.join(source, "formatted_books")

for filename in os.listdir(source):
    old_path = os.path.join(source, filename)

    if not os.path.isfile(old_path):
        continue

    new_name = filename.split(" -- ")[0] + "." + filename.split('.')[1] if " -- " in filename else filename

    new_path = os.path.join(source, new_name)
    os.rename(old_path, new_path)
print("Done.")
