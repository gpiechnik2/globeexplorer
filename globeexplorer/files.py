from pathlib import Path
import os
import json
from shutil import rmtree

from globeexplorer.database import Database
from globeexplorer.utils import get_https_domain, construct_command, get_urls_from_string
from globeexplorer.output import Output

class Files:
    def __init__(self):
        self.TMP_DIRECTORY = self.get_script_directory() + '/tmp'
        self.TMP_VULNERABIBILES_DIRECTORY = self.TMP_DIRECTORY + '/vulnerabilities/'
        self.TMP_RISKS_DIRECTORY = self.TMP_DIRECTORY + '/risks/'
        self.TMP_ERRORS_DIRECTORY = self.TMP_DIRECTORY + '/errors/'
        self.TMP_LOGS_DIRECTORY = self.TMP_DIRECTORY + '/logs/'
        self.MODULES_DIRECTORY = '/modules/'
        self.database = Database()
        self.output = Output()

    def create_directory_if_does_not_exists(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_script_directory(self):
        return str(Path.cwd())

    def create_tmp_txt_file(self, data, file_name):
        with open(file_name, "a") as file:
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

    def validate_scenario_content(self, scenario_script):
        scenario_data = self.get_scenarios(scenario_script)

        if 'scenarios' not in scenario_data:
            self.output.print_error_end_exit('Please create a valid list with scenarios in your test file.')

        scenarios = scenario_data["scenarios"]
        for index, scenario in enumerate(scenarios):
            if 'name' not in scenario:
                self.output.print_error_end_exit('Please define the name in {} scenario'.format(
                    index
                ))
            if 'type' not in scenario:
                self.output.print_error_end_exit('Please define the type in {} scenario'.format(
                    index
                ))
            if 'command' not in scenario:
                self.output.print_error_end_exit('Please define the command in {} scenario'.format(
                    index
                ))
            # TODO: do we need that?
            # if 'GLOBEEXPLORER_URL_WITH_HTTP' not in scenario["command"] and 'GLOBEEXPLORER_URL_WITHOUT_HTTP' not in scenario["command"]:
            #     self.output.print_error_end_exit('please define GLOBEEXPLORER_URL_WITH_HTTP or GLOBEEXPLORER_URL_WITHOUT_HTTP in the command in {} scenario'.format(
            #         index
            #     ))
            if 'assertions' not in scenario:
                self.output.print_error_end_exit('Please define the assertion in {} scenario'.format(
                    index
                ))
            for assertion in scenario["assertions"]:
                if 'type' not in assertion:
                    self.output.print_error_end_exit('Please define the type of the assertion in {} scenario'.format(
                        index
                    ))
                if 'value' not in assertion: 
                    self.output.print_error_end_exit('Please define the value of the assertion in {} scenario'.format(
                        index
                    ))
                if assertion["type"] not in ['regex', 'contain', 'not_contain']:
                    self.output.print_error_end_exit('Please define the valid assertion type in {} scenario. Available types: contain, not_contain, regex'.format(
                        index
                    ))

    def get_scenarios(self, scenario_script):
        with open(self.get_script_directory() + "/" + scenario_script, 'r',) as file:
            return json.load(file)

    def add_urls_from_list(self, urls):
        for url in urls:
            self.database.add_url(get_https_domain(url))

    def get_scenario_from_file(self, scenarios, command):
        urls = self.database.get_urls()
        for scenario in scenarios:
            for url in urls:
                correct_command = construct_command(scenario["command"], url)
                if correct_command == command:
                    return scenario

        # TODO: dla kazdej domeny z domains powinienem sprawdzac,
        # poniewaz domena jest dodawana do bazy danych z parsowanych danych

    def delete_file(self, path):
        if os.path.exists(path):
            os.remove(path)

    def delete_directory(self, path):
        dirpath = Path(path)
        if dirpath.exists() and dirpath.is_dir():
            rmtree(dirpath)

    def clear(self):
        self.delete_file(self.get_script_directory() + '/' + self.database.name())
        self.delete_directory(self.TMP_DIRECTORY)
