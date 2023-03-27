<h1>Script to Find and Copy Newest Files to a New Folder</h1>

Have you ever had a cluttered music production folder with dozens of song folders, each containing multiple versions and bounces of the same song? It can be difficult and time-consuming to sift through all those files and determine which is the most recent version. That's where this script comes in handy!

This script will scan through your current directory and its subdirectories, find the newest audio bounce of each song, and copy it to a new folder called "Current Discography" within the current directory. You can use this for files of any type (maybe with a little adjusting), so it's something like a productivity version management tool.

Here is the script on my [GitHub](https://github.com/elliotmangini/blog-python-automation-02).

To run it-- navigate to the directory containing your many subdirectories which contain multiple versions of files-- place the script in that parent directory and run it from terminal using `python3 ExtractDiscography.py`.


And here is the full sript here before we break it down:

```py
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
```


Let's take a look at how it works.

<h2>Importing Libraries</h2>

```py
import shutil
import os
import pathlib
```

We start by importing the necessary libraries: `shutil`, `os`, and `pathlib`.

<h2>Getting the Current Directory and its Contents</h2>

```py
current_directory = os.getcwd()
cwd_as_obj = pathlib.Path(current_directory)
items = list(cwd_as_obj.iterdir())
```

Next, we use the `os` library to get the current working directory as a string. We then convert this string into a `pathlib.Path` object so we can easily manipulate it. Finally, we list all the contents of the current directory and its subdirectories using `cwd_as_obj.iterdir()`.

<h2>Initializing Counters and Creating the New Folder</h2>

```py
folder_count = 0
bounce_count = 0
found_count = 0

new_folder_path = os.path.join(current_directory, "Current Discography")
os.makedirs(new_folder_path, exist_ok=True)
```

We initialize three counters: `folder_count` to count the number of song folders found, `bounce_count` to count the number of audio bounces found, and `found_count` to count the number of newest bounces copied to the new folder.

We then create a new folder called "Current Discography" within the current directory using `os.makedirs(new_folder_path, exist_ok=True)`.

<h2>Looping through the Song Folders</h2>

Here is where the magic happens. We loop through each item in the `items` list, which contains all the contents of the current directory and its subdirectories. If an item is a directory, we increment the `folder_count` counter and create a `subitems` list containing all the contents of that directory.

```py
for item in items:
    if item.is_dir():
        folder_count += 1
        subitems = list(item.iterdir())
```


Next, we loop through each item in the subitems list. If the item is a file and its extension is one of `.mp3`, `.wav`, `.flac`, `.ogg`, we increment the `bounce_count` counter and get the birth time of the file using `os.stat(subitem).st_birthtime`. We then compare the birth time of the current file with the latest birth time we have seen so far, and if it is greater, we update `most_recent_bounce` with the current file and `latest_time` with the current birth time.

```py
for subitem in subitems:
    if subitem.is_file() and str(subitem).endswith((".mp3", ".wav", ".flac", ".ogg")):
        bounce_count += 1
        bounce_time = float(os.stat(subitem).st_birthtime)
        if bounce_time > latest_time:
            latest_time = bounce_time
            most_recent_bounce = subitem
```

If we found a file to copy, we print a success message, copy the file to a new directory named `Current Discography` located in the current directory, and increment `found_count`.

```py
if most_recent_bounce is not None:
    print(f"\u2705 Found: {most_recent_bounce.name}")
    shutil.copy2(most_recent_bounce, new_folder_path)
    found_count += 1
```

If we did not find a file to copy, we print a warning message.

```py
else:
    print(f"\U0001F6A8\U0001F6A8\U0001F6A8 No bounces found for: {subitem.name} \U0001F6A8\U0001F6A8\U0001F6A8.")
```

Finally, we print a nice little report with the total number of song folders found, the total number of audio bounces found, and the total number of newest bounces copied to the `Current Discography` directory.

```py
print(f"{folder_count} Song Folders found in this directory.")
print(f"{bounce_count} Audio Bounces found within subfolders.")
print(f"{found_count} Newest Bounces copied to {new_folder_path}.")
```

Using the script we can go from this:

to this:

<h1>Challenges</h1>

One of the challenges in implementing this script was finding a reliable way to get the creation time of a file. There are several ways to do this using Python, such as using the `os.stat()` function or the `pathlib.Path.stat()` method. However, the accuracy of these methods can vary depending on the platform and file system. Therefore, testing was necessary to ensure that we were indeed getting the most recent file when running the script. By using the `st_birthtime` attribute of `os.stat()`. In my case this was how I was able to accurately get the creation time of a file and find the most recently created audio file in each subdirectory.

Let me know if you try this out or have any thoughts or ideas,
Cheers,
-Elliot