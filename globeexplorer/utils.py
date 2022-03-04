import re
from hashlib import md5
import uuid
from urllib.parse import urlparse
from os.path import exists

from globeexplorer.output import Output


def get_https_domain(domain):
    if 'http' not in domain:
        return 'https://' + domain
    else:
        return domain


def get_without_https_domain(domain):
    if 'http' in domain:
        return domain.replace('https://', '').replace('http://', '')
    else:
        return domain


def get_string_without_special_chars(mystring):
    return re.sub('[^A-Za-z0-9]+', '', mystring)


def get_random_file_name(string_length = 16):
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.


def construct_command(command, url):
    url_without_http = get_without_https_domain(url)
    new_command = command.replace('GLOBEEXPLORER_URL_WITH_HTTP', url).replace('GLOBEEXPLORER_URL_WITHOUT_HTTP', url_without_http)
    return new_command


def get_urls_from_string(inputString):
    regex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
    matches = re.findall(regex, inputString)
    return matches


def get_main_domain(url):
    return urlparse(url).scheme + '://' + urlparse(url).hostname


def validate_url(url):
    if 'http://' not in url and 'https://' not in url:
        output = Output()
        output.print_error_end_exit('Please provide a valid url with http or https protocol.')

def validate_wordlist(path_to_file):
    if path_to_file:
        if not exists(path_to_file):
            output = Output()
            output.print_error_end_exit('Please provide a valid path to the wordlist file.')
