#!/usr/bin/env python3

import os
import requests


def download_file(url: str, file_name: str) -> bool:
    """Download file from given URL to local directory.

    :param url: The url of the PDF file to be downloaded
    :return: True if file was successfully downloaded, otherwise False.
    """

    # Request URL and get response object
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        # Save in current working directory
        # filepath = os.path.join(os.getcwd(), file_name)
        with open(file_name, 'wb') as file_object:
            file_object.write(response.content)
            print(f'{file_name} was successfully saved!')
            return True
    else:
        print(f'Uh oh! Could not download {file_name}')
        print(f'HTTP response status code: {response.status_code}')
        return False


if __name__ == '__main__':
    # URL from which pdfs to be downloaded
    ten_k_list_file = "../data/source/10K-pdf.txt"
    download_dir = "../data/10K/pdf"

    file_list = open(ten_k_list_file, "r").read().splitlines()
    for file_link in file_list:
        file_split = file_link.split("|")
        company = file_split[0].strip()
        file_url = file_split[1].strip()
        file_name = file_name = os.path.basename(file_url)

        try:
            file_name_split = file_name.split(".")
            file_extension = file_name_split[1]
            if "?" in file_extension:
                file_extension = "pdf"
        except IndexError:
            file_extension = "pdf"

        file_save_name = f"{download_dir}/{company}-10k-2022.{file_extension}"
        # print("file URL:", file_url)
        # print("file name:", file_save_name)
        print(f"Downloading standard file from: {file_save_name}")
        download_file(file_url, file_save_name)