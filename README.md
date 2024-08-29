
# Zulip (UniFreiburg) to PDF App 

This is a set of simple scripts that allows you to import all direct messages (DMs) and channels from the Uni Freiburg Zulip server as PDF files. Note that no OCR is performed, so each page is a screenshot of the corresponding content. While the image quality may not be perfect, I currently do not have the time to look into improving it.

### What does the `save_to_pdf.py` script do?

This script uses the Selenium driver to open a Firefox browser (though Chrome should work as well, see the line `driver=webdriver.Firefox()`). You have 15 seconds to log in with your credentials, close the top green pop-ups about notifications, and maximize the window. After 15 seconds, the script will begin taking screenshots of the page, scrolling up, and repeating this process until it reaches the top of the channel (or until the number of screenshots reaches `max_scroll_clicks=1000` as a failsafe). The files are automatically saved in the `RAW` folder within a corresponding subfolder (note that each subfolder is cleaned before every run). Once a channel is processed, the script converts all PNGs into a PDF in the `RAW` folder. Please ensure all related PDFs are closed before running the script to avoid file access conflicts. The script will then move on to the next channel or DM and repeat the process.

### Are there any pauses between scrolling?

Yes. `scroll_pause_time=1 sec` defines the pause between scrolling and taking a screenshot. `request_pause_time=2 sec` defines the pause after finishing one channel before starting the next.

### What if I can't log in within 15 seconds?

You can adjust the value of `login_pause_time` to give yourself more time to log in.

### Where does the script find the list of DMs and channels?

The script looks for a `channel_list` file in the same folder. This file should contain the list of DMs and channels in the following format: `dm/41-Viacheslav-Slesarenko` or `stream/68-MetaLab-group`. You can find the exact name of each channel in the address line in Zulip. Additionally, I've included the `parse_local_html.py` script, which can extract `channel_list.txt` from the HTML of your Zulip page.

### How do I get the channel list and use `parse_local_html.py`?

- **Option 1: Manually** - Click on the channels, look at the address line, and copy the last part. In this case, you don't need to use `parse_local_html.py`.
- **Option 2: Using the Script** - Since Zulip dynamically loads and unloads content, you can open Zulip, expand the DMs (click "More conversations"), right-click on the page, and select "Inspect." Then, find the div with `id="direct-messages-list"`, right-click, and select "Copy Inner HTML." Paste this into a file named `html_raw.txt` in the root of the project (next to the script). Then, go back to Zulip, click on "Streams," expand them, open "Inspect," search for the div with `id="stream-filters"`, right-click, and copy the Inner HTML. Append this to the same `html_raw.txt` file. Save the file and run `parse_local_html.py`—you’ll find `channel_list.txt` with all the DMs and channels listed.

### Will it work with umlauts and other special characters?

Yes, as far as I have tested, titles with umlauts should not be a problem.

### Can I save attached files as well?

YES! However, this isn't handled by the script. To save attachments, go to Zulip -> Settings -> Personal -> Uploaded files, and download them manually.

### Are there any bugs?

Possibly quite a few! I haven't had the time to implement proper exception handling (except for a few cases in file reading).

### What if PDF is not generating?

Just comment line merge_pngs_to_pdf(fname_list, output_pdf). PDF won't be generated, but you will still have all png files.

### What should I do if I find a bug or know how to improve the performance (e.g., by improving resolution)?

Feel free to email me at viacheslav.slesarenko@livmats.uni-freiburg.de or reach out on Matrix.
