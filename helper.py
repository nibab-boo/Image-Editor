import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# check if file is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
