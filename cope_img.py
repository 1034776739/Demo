#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
from pathlib import Path

import cv2


def suffix_to_lower(file_path):

    if file_path.exists() and file_path.is_file():
        if file_path.suffix.isupper():
            new_name = file_path.stem + file_path.suffix.lower()
            new_path = file_path.parent.joinpath(new_name)
            shutil.move(file_path, new_path)


def is_valid_jpg_image(img_path):
    end_flag = ""
    with open(img_path, 'rb') as f:
        f.seek(-2, 2)
        end_flag = f.read()
    if end_flag == b'\xff\xd9':
        return True
    else:
        return False


def move_except_images(src_path, dst_path):
    expect_list = []
    for one in src_path.iterdir():
        if one.is_file():
            if one.suffix != ".jpg":
                expect_list.append(one.name)
            else:
                if not is_valid_jpg_image(one):
                    expect_list.append(one.name)

    for item in expect_list:
        src_name = src_path.joinpath(item)
        dst_name = dst_path.joinpath(item)
        if not dst_name.exists():
            shutil.move(src_name, dst_name)


def change_name(img_path, prefix, num):
    new_name = f"{prefix}{num}{img_path.suffix}"
    new_path = img_path.parent.joinpath(new_name)

    if not new_path.exists():
        shutil.move(img_path, new_path)
    else:
        print("文件名称已经存在！请修改num")


def image_format_to_jpg(img_path, dst_path):

    if img_path.exists() and dst_path.exists():
        new_name = img_path.stem + ".jpg"
        new_path = dst_path.joinpath(new_name)

        if not new_path.exists():
            img_temp = cv2.imread(str(img_path))
            cv2.imwrite(str(new_path), img_temp)
    else:
        print("图片或者目录不存在。")


def run(dir_path, prefix, counter=0):
    # 1. 把图片后缀名统一改成小写。
    for img in dir_path.iterdir():
        if img.is_file():
            suffix_to_lower(img)

    # 2. 修改图片名称：prefix + num + suffix
    cnt = counter
    for img2 in dir_path.iterdir():
        if img2.is_file():
            cnt += 1
            change_name(img2, prefix, cnt)

    # 3. 移动异常图片或者非jpg格式的图片。
    except_folder = "except_folder"
    e_folder = dir_path.parent.joinpath(except_folder)

    if e_folder.exists():
        print("except_folder 已经存在，请检查是否需要删除。")
    else:
        os.mkdir(e_folder)
    move_except_images(dir_path, e_folder)

    # 4. 重写异常图片文件夹中的图片文件。
    for img_e in e_folder.iterdir():
        if img_e.is_file():
            image_format_to_jpg(img_e, dir_path)


if __name__ == '__main__':
    path = r""
    path_p = Path(path)

    prefix_name = ""
    count = 0
    run(path_p, prefix_name, count)
