import os
def remove_dir(dir):
    dir = dir.replace('\\', '/')
    if(os.path.isdir(dir)):
        for p in os.listdir(dir):
            remove_dir(os.path.join(dir,p))
        if(os.path.exists(dir)):
            os.rmdir(dir)
    else:
        if(os.path.exists(dir)):
            os.remove(dir)

def create_Or_reset_dir(dir):
    dir = dir.replace('\\', '/')
    if(os.path.isdir(dir)):
        for p in os.listdir(dir):
            remove_dir(os.path.join(dir,p))
        if(os.path.exists(dir)):
            os.rmdir(dir)
    else:
        if(os.path.exists(dir)):
            os.remove(dir)
    os.mkdir(dir)