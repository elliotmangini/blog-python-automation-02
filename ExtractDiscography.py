import shutil

import os
current_directory = os.getcwd()  # => this is a string for our current directory

import pathlib
cwd_as_obj = pathlib.Path(current_directory)  # => turn that string into a path obj
items = list(cwd_as_obj.iterdir())  # => list the paths inside our cwd

folder_count = 0
bounce_count = 0
found_count = 0

new_folder_path = os.path.join(current_directory, "Current Discography")
os.makedirs(new_folder_path, exist_ok=True)

for item in items:  # loop through the scripts siblings
    if item.is_dir():  # if this is a folder
        folder_count = folder_count + 1  # count it

        subitems = list(item.iterdir())

        most_recent_bounce = None
        latest_time = 0

        for subitem in subitems:  # looping through each item in each song folder
            # print(subitem)
            if subitem.is_file() and str(subitem).endswith((".mp3", ".wav", ".flac", ".ogg")):
                bounce_count = bounce_count + 1
                bounce_time = float(os.stat(subitem).st_birthtime)
                # print(f"current item {subitem} created {bounce_time}")
                if bounce_time > latest_time:
                    # print(f"replacing file with time {latest_time} with {bounce_time}")
                    latest_time = bounce_time
                    most_recent_bounce = subitem

        if most_recent_bounce is not None:
            print(f"\u2705 Found: {most_recent_bounce.name}")
            shutil.copy2(most_recent_bounce, new_folder_path)
            found_count = found_count + 1
        else:
            print(f"\U0001F6A8\U0001F6A8\U0001F6A8 No bounces found for: {subitem.name} \U0001F6A8\U0001F6A8\U0001F6A8.")

print(f"{folder_count} Song Folders found in this directory.")
print(f"{bounce_count} Audio Bounces found within subfolders.")
print(f"{found_count} Newest Bounces copied to {new_folder_path}.")

