import random
import string
import shutil
import time
import os


DOWNLOAD_ROOT = os.path.join(os.path.abspath(os.path.curdir))
DOWNLOAD_DEBUG = True


class Downloader:
    """
    Helper for managing downloaded files from chrome crawls.
    """
    def __init__(self):
        self.path_id = ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 16))
        self.path = os.path.join(DOWNLOAD_ROOT, self.path_id)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def filename(self):
        """Returns name of the most recent downloaded file (if any) from the download_path above."""
        fnames = [os.path.join(self.path, fname) for fname in os.listdir(self.path)]
        return max(fnames, key=os.path.getctime) if fnames else ''

    def basename(self):
        """Returns just the base name of the file."""
        return os.path.basename(self.filename())

    def in_progress(self):
        """Whether a file download is in progress."""
        INPROGRESS = ['.crdownload', '.com.google.Chrome']
        return any(word in self.filename() for word in INPROGRESS)

    def open_file(self, timeout=150):
        """Makes sure the most recent downloaded file is fully downloaded, then returns a file object."""
        count = 0
        while self.in_progress() or not self.filename():
            if count > timeout:
                raise Exception('Download of file timed out.')
            time.sleep(1)
            count += 1
        if DOWNLOAD_DEBUG:
            print('opening {} | file: {}'.format(self.path_id, self.basename()))
        return open(self.filename())

    def clean_up(self):
        """Removes downloaded files and directory."""
        try:
            shutil.rmtree(self.path)
        except OSError:
            pass
