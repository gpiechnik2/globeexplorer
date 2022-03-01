import re


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

