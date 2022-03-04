from datetime import datetime
import threading
import re
import subprocess
from subprocess import Popen, PIPE, STDOUT
from itertools import islice
import sys
from time import sleep

from core.database import Database
from core.output import Output
from core.files import Files
from core.utils import get_https_domain, get_without_https_domain, get_string_without_special_chars, get_random_file_name, construct_command
from core.crawler import get_links
from core.scenario import Scenario


class Threads:
    def __init__(self, scenarios):
        self.scenarios = scenarios
        self.files = Files()
        self.output = Output()
        self.database = Database()

    def delete_asnci_excape_squences_from_output(self, output):
        ansi_escape = re.compile(r'''
            \x1B  # ESC
            (?:   # 7-bit C1 Fe (except CSI)
                [@-Z\\-_]
            |     # or [ for CSI, followed by a control sequence
                \[
                [0-?]*  # Parameter bytes
                [ -/]*  # Intermediate bytes
                [@-~]   # Final byte
            )
        ''', re.VERBOSE)
        return ansi_escape.sub('', output.decode('utf-8'))

    def get_urls(self):
        database = Database()
        return database.get_urls() 
    
    def get_last_element_of_url(self, url):
        return url.rsplit('/', 1)[-1]

    def validate_url(self, url):
        last_part_of_url = self.get_last_element_of_url(url)

        if '?' in url and '.js' in url:
            return ['params', 'js', 'static', 'all']
        elif '?' in url and '.' in last_part_of_url:
            return ['params', 'static', 'all']
        elif '?' in url:
            return ['params', 'all']
        elif '.html' in last_part_of_url or '.htm' in last_part_of_url:
            return ['static', 'simple', 'all']
        elif '.js' in url:
            return ['js', 'static', 'all']
        elif '.' in last_part_of_url:
            return ['static', 'all']
        elif not '?' in url and not '.' in last_part_of_url:
            return ['simple', 'all']
        else:
            return ['all']

    def assert_data(self, thread_results, file_name, scenario_data, process_args):
        assertions = scenario_data["assertions"]
        name = scenario_data["name"]
        scenario_type = scenario_data["type"]

        for assertion in assertions:
            if assertion['type'] == 'contain' and assertion['value'] in thread_results:
                self.output.print_risk_or_vulnerability_found(scenario_type, name, process_args, assertion)
                self.files.create_risk_or_vulnerability_file(scenario_type, thread_results, file_name)
            elif assertion['type'] == 'not_contain' and assertion['value'] not in thread_results:
                self.output.print_risk_or_vulnerability_found(scenario_type, name, process_args, assertion)
                self.files.create_risk_or_vulnerability_file(scenario_type, thread_results, file_name)
            elif assertion['type'] == 'regex':
                regexp = re.compile(assertion['value'])
                if regexp.search(thread_results):
                    self.output.print_risk_or_vulnerability_found(scenario_type, name, process_args, assertion)
                    self.files.create_risk_or_vulnerability_file(scenario_type, thread_results, file_name)

    def handle_post_thread(self, output, error, process_args):
        scenario_data = self.files.get_scenario_from_file(self.scenarios, process_args)
        output_data = self.delete_asnci_excape_squences_from_output(output) if output else self.delete_asnci_excape_squences_from_output(error)
        file_name = get_random_file_name()

        if error:
            self.files.create_error_file(output_data, file_name)                        

        self.files.create_log_file(output_data, file_name)
        self.assert_data(output_data, file_name, scenario_data, process_args)

    def start_threads(self, commands, threads_quantity):
        processes = (Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT) for cmd in commands)
        for process in processes:
            running_processes = list(islice(processes, threads_quantity))  # start new processes
            while running_processes:
                for i, process in enumerate(running_processes):
                    if process.poll() is not None:  # the process has finished
                        output, error = process.communicate()
                    
                        self.handle_post_thread(output, error, process.args)
                        # print_test_finished?

                        running_processes[i] = next(processes, None)  # start new process
                        if running_processes[i] is None: # no new processes
                            del running_processes[i]
                            break

    def prepare_commands(self):
        urls = self.database.get_urls()
        domains = self.database.get_domains()
        commands = []

        for scenario in self.scenarios:            
            scenario_obj = Scenario(scenario)
            urls_to_test = domains if scenario_obj.is_single() else urls
            
            for index, url in enumerate(urls_to_test):
                validate_url = self.validate_url(url)
                url_type = scenario_obj.get_url_type()
                if url_type in validate_url:
                    command = construct_command(scenario_obj.get_command(url), url)
                    name = scenario_obj.get_name()
                    commands.append(command)

        self.output.print_added_to_queue(len(commands), len(urls), len(domains))
        return commands
    

class PreconditionThreads:
    def __init__(self, url, subfinder_enabled, ffuf_enabled, crawler_enabled, wordlist, convert):
        self.subfinder_enabled = subfinder_enabled
        self.ffuf_enabled = ffuf_enabled
        self.crawler_enabled = crawler_enabled
        self.url = url
        self.convert = convert
        self.files = Files()
        self.wordlist = wordlist if wordlist else self.files.get_wordlist_path()
        self.output = Output()
        self.database = Database()

    def run_command(self, command):
        process = subprocess.Popen(
            command,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        
        process.wait()
        output, error = process.communicate()
        return output, error

    def replace_str_in_list(self, list_of_strings, old_string, new_string):
        new_list_of_strings = []
        for word in list_of_strings:
            new_word = word.replace(old_string, new_string)
            new_list_of_strings.append(new_word)

        return new_list_of_strings

    def run_subfinder(self, command):
        if self.subfinder_enabled:
            self.output.print_initial_module_started('subfinder', 'subdomain enumeration tool')
            output, error = self.run_command(command)
            if output:
                domains = re.search(
                    r'Enumerating subdomains for (.*?)"',
                    str(output).replace(
                        "'",
                        '"'),
                    re.DOTALL).group(1).split('\\n')

                print('data-test domains')
                for domain in domains:
                    print(domain)
                    # sometimes there are empty urls
                    if domain:
                        domain = get_https_domain(domain)
                        self.database.add_domain(domain)
                        self.database.add_url(get_https_domain(domain))
            if error:
                self.output.print_error_while_running_command(command, error)
        else:
            domain = get_https_domain(self.url)
            self.database.add_domain(domain)
            self.database.add_url(get_https_domain(domain))

    def run_ffuf(self, command):
        if self.ffuf_enabled:
            self.output.print_initial_module_started('ffuf', 'great tool used for fuzzing')
            domains = self.database.get_domains() if self.subfinder_enabled else [self.url]
            for domain in domains:
                domain = get_https_domain(domain)
                domain_without_special_characters = get_string_without_special_chars(domain)
                new_command = self.replace_str_in_list(command, 'GLOBEEXPLORER_DOMAIN', domain)
                new_command = self.replace_str_in_list(new_command, 'FFUF_DOMAIN', domain_without_special_characters)
                output, error = self.run_command(new_command)
                
                if error:
                    self.output.print_error_while_running_command(new_command, error)
        else:
            self.database.add_url(self.url)
        
        self.files.add_urls_from_ffuf_file()
    
    def run_crawler(self):
        if self.crawler_enabled:
            self.output.print_initial_module_started('crawler', 'web crawling tool')
            domains = self.database.get_domains() if self.subfinder_enabled else [self.url]
            for domain in domains:
                domain_without_https = get_without_https_domain(domain)
                domain_with_https = get_https_domain(domain)
                domain_without_special_characters = get_string_without_special_chars(domain)
                urls = get_links(domain_without_https, domain)
                self.files.add_urls_from_list(urls)

    def start_preconditions(self):
        url_without_https = get_without_https_domain(self.url)
        subfinder_cmd = ['subfinder', '-d', url_without_https]
        ffuf_cmd = ['ffuf', '-u', 'GLOBEEXPLORER_DOMAIN' + '/FUZZ', '-w', self.wordlist, '-o', self.files.get_ffuf_directory_path() + '/FFUF_DOMAIN.json', '-of', 'json']

        self.run_subfinder(subfinder_cmd)    
        self.run_ffuf(ffuf_cmd)
        self.run_crawler()
