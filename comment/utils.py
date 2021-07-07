import os
import random
import string
from datetime import datetime

from django.conf import settings
from django.template.defaultfilters import slugify


def get_upload_file_path(upload_name):
    # Generate date based path to put uploaded file.
    date_path = datetime.now().strftime('%Y/%m/%d')

    # Complete upload path (upload_path + date_path).
    upload_path = os.path.join(settings.UPLOAD_URL, date_path)
    full_path = os.path.join(settings.BASE_DIR, upload_path)
    make_sure_path_exist(full_path)
    file_name = slugify_filename(upload_name)
    return os.path.join(full_path, file_name), os.path.join(upload_path, file_name)


def slugify_filename(filename):
    """ Slugify filename """
    name, ext = os.path.splitext(filename)
    slugified = get_slugified_name(name)
    return slugified + ext


def get_slugified_name(filename):
    slugified = slugify(filename)
    return slugified or get_random_string()


def get_random_string():
    return ''.join(random.sample(string.ascii_lowercase * 6, 6))


def make_sure_path_exist(path):
    if os.path.exists(path):
        return
    os.makedirs(path, exist_ok=True)
