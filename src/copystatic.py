
import os
import shutil
def recursive_copy(source,dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
        
        
        
    for name in os.listdir(source):
        full_path = os.path.join(source,name)
        if os.path.isfile(full_path):
            shutil.copy(full_path,dest)
        else:
            recursive_copy(full_path,os.path.join(dest,name))