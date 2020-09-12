import json
import re
import sys
import time
import requests

"""
<p>This script takes text file as input containing IP addresses on new line 
and scrapes the Geo location data of a IP addresses and write them into 
output file as comma separated values.</p>

Command to Run: python3 ip-api.py input_file.txt output_file.txt


@author: amol52d
@since: 07/09/20
"""


def update_ip_file(updated_ip_list, file):
    """
    This method updates the source file by removing the successfully scraped IP address
    :param updated_ip_list: Latest IP address list
    :param file: Source file path
    """
    del updated_ip_list[0]
    new_file = open(file, "w+")
    for ip_add in updated_ip_list:
        new_file.write(ip_add)
    new_file.close()


def read_ip_list(file_source_path):
    """
    Reads the input file and returns the list of IPs in that file
    :param file_source_path:
    :return: List of IPs
    """
    try:
        with open(file_source_path) as file:
            return file.read().splitlines()
    except IOError:
        sys.stderr.write('Unable to open IP file {}\n'.format(file_source_path))
        exit(1)


def get_ip_api(ip_address, file):
    """
    This method scrapes IP address details
    :param ip_address: IP address that needed to be scraped
    :param file: Destination File object where the respective IP address details has to be written
    :return: returns True on successful scrape either False
    """
    try:
        # scraping the IP address from ip-api APIs
        response = requests.get('http://ip-api.com/json/' + ip_address)
        status_code = response.status_code
        if status_code == 200:
            content = json.loads(response.content)

            # removing any special characters that may conflict while importing csv to excel
            content['city'] = re.sub("[\"\']+", "", content['city'])
            content['regionName'] = re.sub("[\"\']+", "", content['regionName'])
            content['country'] = re.sub("[\"\']+", "", content['country'])
            content['isp'] = re.sub("[\"\']+", "", content['isp'])

            # writing the scrapped data into destination file
            file.write("{},{},{},{},{},{},{}\n".format(ip_address,
                                                       content['city'],
                                                       content['regionName'],
                                                       content['country'],
                                                       content['isp'],
                                                       content["lat"],
                                                       content["lon"]))
        else:
            file.write("{},{},{},{},{},{},{}".format(ip_address, status_code, "ERR", "ERR", "ERR", "ERR", "ERR", "ERR"))
        return True
    except requests.exceptions.ConnectionError as p:
        print("Internet disconnected while scraping IP address: " + ip_address)
        return False
    except Exception as e:
        print("Exception %s caught while scrapping IP: %s", e, ip_address)
        return False


def init_ip_scrape():
    # path of source file getting
    source_file_path = sys.argv[1]
    # path of destination file getting
    destination_file_path = sys.argv[2]

    # list of IP address
    ip_list = read_ip_list(source_file_path)

    updated_ip_list = open(source_file_path, "r").readlines()

    count = 0
    destination_file = open(destination_file_path, "a")
    for ip in ip_list:
        count = count + 1
        if get_ip_api(ip, destination_file):
            # updating the source file on successful scrape
            update_ip_file(updated_ip_list, source_file_path)
            print(count, ip, "Success")
        else:
            print(count, ip, "Failed")
        time.sleep(1.5)
    destination_file.close()


if __name__ == "__main__":
    init_ip_scrape()
