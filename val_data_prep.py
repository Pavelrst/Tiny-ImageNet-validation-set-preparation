import os
import sys

CLASSES_IN_TINY_IMAGENET = 200
IMAGET_IN_VAL_SET = 10000

def get_subdirectories_names(path):
    '''
    :param path: path to val_annotations.txt file
    :return:
    '''
    with open(path) as f:
        subfolders_list = []
        file_vs_dist_list = []
        for line in f:
            line_list = line.split('\t', -1)
            file_name = line_list[0]
            folder = line_list[1]
            file_vs_dist_list.append((file_name, folder))
            if folder not in subfolders_list:
                subfolders_list.append(folder)
    if len(subfolders_list) != CLASSES_IN_TINY_IMAGENET:
        print("subfolders_list is shorter than 200 -> something went wrong!")
    if len(file_vs_dist_list) != IMAGET_IN_VAL_SET:
        print("file_vs_dist_list is shorter than 10000 -> something went wrong!")
    return subfolders_list, file_vs_dist_list


def put_files_in_subfolders(path, subfolders_list, file_vs_dist_list):
    '''
    :param path: A path to files we want to move
    :param subfolders_list: A list with subfolders we want to create
    :param file_vs_dist_list: List of tuples which contain file and where to move it
    :return:
    '''
    for sub_name in subfolders_list:
        try:
            if sys.platform == "linux" or sys.platform == "linux2":
                os.mkdir(path+'/'+sub_name)
            else:
                os.mkdir(path + '\\' + sub_name)
        except OSError:
            print("Creation of the directory", sub_name, "failed")
        else:
            print("Successfully created the directory", sub_name)

    for file, dist in file_vs_dist_list:
        if sys.platform == "linux" or sys.platform == "linux2":
            src = path+'/'+file
            dist = path+'/'+dist+'/'+file
        else:
            src = path + '\\' + file
            dist = path + '\\' + dist + '\\' + file
        try:
            os.rename(src, dist)
        except OSError:
            print("OSError during moving file", file)
        else:
            print(file, "Successfully moved")


def main():
    path = sys.argv[1]
    if sys.platform == "linux" or sys.platform == "linux2":
        anno_path = path + "/val_annotations.txt"
    else:
        anno_path = path + "\\val_annotations.txt"
    subfolders_list, file_vs_dist_list = get_subdirectories_names(anno_path)
    if sys.platform == "linux" or sys.platform == "linux2":
        img_path = path + "/images"
    else:
        img_path = path + "\\images"
    put_files_in_subfolders(img_path, subfolders_list, file_vs_dist_list)


if __name__ == "__main__":
    main()

