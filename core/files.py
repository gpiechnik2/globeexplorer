from pathlib import Path
import os
import json

from database import Database
from utils import get_https_domain

class Files:
    def __init__(self):
        self.TMP_DIRECTORY = self.get_script_directory() + '/tmp'
        self.TMP_VULNERABIBILES_DIRECTORY = self.TMP_DIRECTORY + '/vulnerabilities'
        self.TMP_RISKS_DIRECTORY = self.TMP_DIRECTORY + '/risks'
        self.TMP_ERRORS_DIRECTORY = self.TMP_DIRECTORY + '/errors'
        self.TMP_LOGS_DIRECTORY = self.TMP_DIRECTORY + '/logs'
        self.MODULES_DIRECTORY = '/modules/'
        self.database = Database()

    def create_directory_if_does_not_exists(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_script_directory(self):
        return str(Path.cwd())

    def create_tmp_txt_file(self, data, file_name):
        directory = get_script_directory() + self.TMP_DIRECTORY
        with open(directory + '/' + file_name, "a") as file:
            file.write(data.replace(r'\n', '\n').replace(r'\r', '\n'))

    def create_tmp_files_structure(self):
        # logs directories
        self.create_directory_if_does_not_exists(self.TMP_DIRECTORY)
        self.create_directory_if_does_not_exists(self.TMP_VULNERABIBILES_DIRECTORY)
        self.create_directory_if_does_not_exists(self.TMP_RISKS_DIRECTORY)
        self.create_directory_if_does_not_exists(self.TMP_ERRORS_DIRECTORY)
        self.create_directory_if_does_not_exists(self.TMP_LOGS_DIRECTORY)

        # initial module
        self.create_directory_if_does_not_exists(self.get_ffuf_directory_path())

    def create_error_file(self, log, file_name):
        self.create_tmp_txt_file(log, self.TMP_ERRORS_DIRECTORY + file_name)

    def create_log_file(self, log, file_name):
        self.create_tmp_txt_file(log, self.TMP_LOGS_DIRECTORY + file_name)

    def create_vulnerability_log_file(self, log, file_name):
        self.create_tmp_txt_file(log, self.TMP_VULNERABIBILES_DIRECTORY + file_name)

    def create_risk_log_file(self, log, file_name):
        self.create_tmp_txt_file(log, self.TMP_RISKS_DIRECTORY + file_name)

    def create_risk_or_vulnerability_file(self, scenario_type, log, file_name):
        if scenario_type == 'risk':
            self.create_risk_log_file(log, file_name)
        elif scenario_type == 'vulnerability':
            self.create_vulnerability_log_file(log, file_name)    

    def get_modules_directory_path(self):
        return self.get_script_directory() + self.MODULES_DIRECTORY

    def get_tmp_directory_path(self):
        return self.TMP_DIRECTORY

    def get_ffuf_directory_path(self):
        return self.get_tmp_directory_path() + '/ffuf'

    def get_files_in_directory(self, directory):
        return os.listdir(directory)

    def get_json_data_from_tmp_file(self, path):
        with open(path, 'r',) as file:
            return json.load(file)

    def add_urls_from_ffuf_file(self):
        ffuf_directory = self.get_ffuf_directory_path()
        ffuf_files = self.get_files_in_directory(ffuf_directory)
        for file in ffuf_files:
            json_data = self.get_json_data_from_tmp_file(ffuf_directory + '/' + file)
            for result in json_data['results']:
                url = result['url']
                self.database.add_url(url)

    def get_wordlist_path(self, wordlist):
        return self.get_script_directory() + '/core/wordlists/' + wordlist

    def validate_scenario_content(self, scenario_script):
        pass

    def get_scenarios(self, scenario_script):
        with open(self.get_script_directory() + "/" + scenario_script, 'r',) as file:
            return json.load(file)

    def add_urls_from_list(self, urls):
        for url in urls:
            self.database.add_url(get_https_domain(url))
