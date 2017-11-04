import os
root_dir = r"X:\library_GUI2\Assets"
dst_dir = r"D:\assets_library"
for root, dirs, files in os.walk(root_dir):

    rel_path = root[len(root_dir)+1:]
    if not rel_path:
        rel_path = dst_dir
    else:
        rel_path = os.path.join(dst_dir, rel_path)

    for d in dirs:
        sub_dir = os.path.join(rel_path, d)
        os.mkdir(sub_dir)

    for f in files:
        f_path = os.path.join(rel_path, f)
        open(f_path, "w").close()

print "copy files and dirs from 'cosmos laundromat' done!"