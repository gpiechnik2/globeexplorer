from datetime import datetime
import threading
import re
import subprocess
import sys

from database import Database
from output import Output
from files import Files
from utils import get_https_domain, get_without_https_domain, get_string_without_special_chars
from crawler import get_links
from scenario import Scenario


threadLimiter = threading.BoundedSemaphore(10)

class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)

class Thread: 
    def __init__(self, name, url, url_type, scenario_type, module_name, command, assertions, log_name):
        self.name = name
        self.url = url
        self.url_type = url_type
        self.scenario_type = scenario_type
        self.module_name = module_name
        self.command = command
        self.assertions = assertions
        self.log_name = log_name
        self.output = Output()
        self.files = Files()

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
        return ansi_escape.sub('', output)

    def get_last_element_of_url(self, url):
        return url.rsplit('/', 1)[-1]

    def validate_url(self):
        last_part_of_url = self.get_last_element_of_url(self.url)

        if '?' in url and '.js' in url:
            return ['params', 'js', 'static']
        elif '?' in url and '.' in last_part_of_url:
            return ['params', 'static']
        elif '?' in url:
            return ['params']
        elif '.html' in last_part_of_url or '.htm' in last_part_of_url:
            return ['static', 'simple']
        elif '.js' in url:
            return ['js', 'static']
        elif '.' in last_part_of_url:
            return ['static']
        elif not '?' in url and not '.' in last_part_of_url:
            return ['simple']
        else:
            return ['all']

    def run_command(self, commands):
        validate_url = self.validate_url()
        if validate_url in self.url_type or url_type == None:
            try:
                if not self.module_name:
                    self.module_name = '/'

                modules_path = '{}'.format(self.files.get_modules_directory_path())
                process = subprocess.Popen(
                    command.split(),
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=modules_path +
                    self.module_name)

                process.wait()
                output, error = process.communicate()

                if error:
                    error_data = self.delete_asnci_excape_squences_from_output(error)
                    self.files.create_error_file(error_data)
                    return error_data
                else:
                    return self.delete_asnci_excape_squences_from_output(output)

            except Exception as error:
                error_data = self.delete_asnci_excape_squences_from_output(error)
                self.files.create_error_file(error_data)
                return error_data            

    def assert_data(self, thread_results):
        for assertion in self.assertions:
            if assertion['type'] == 'contain' and assertion['value'] in thread_results:
                self.output.print_risk_or_vulnerability_found(self.scenario_type, self.name, self.url, assertion)
                self.files.create_risk_or_vulnerability_file(self.scenario_type, thread_results, self.file_name)
            elif assertion['type'] == 'not_contain' and assertion['value'] not in thread_results:
                self.output.print_risk_or_vulnerability_found(self.scenario_type, self.name, self.url, assertion)
            elif assertion['type'] == 'regex':
                regexp = re.compile(assertion['value'])
                if regexp.search(thread_results):
                    self.output.print_risk_or_vulnerability_found(self.scenario_type, self.name, self.url, assertion)

    def add_thread(self):
        thread = ThreadWithResult(target = self.run_command, args = (self.command, ))
        thread.start()
        thread.join()
        threadLimiter.acquire()
        self.output.print_added_to_queue(self.name, self.url, self.command)
        thread_results = thread.result()
        threadLimiter.release()
        self.assert_data(thread_results)
        self.files.create_tmp_txt_file(self.file_name)


class Threads:
    def __init__(self, scenarios):
        self.scenarios = scenarios

    def get_urls(self):
        database = Database()
        return database.get_urls() 
    
    def start_threads(self):
        urls = self.get_urls()
        
        for scenario in self.scenarios:            
            scenario_obj = Scenario(scenario)
            name = scenario_obj.get_name()
            url_type = scenario_obj.url_type()
            module_name = scenario_obj.get_command()
            assertions = scenario_obj.get_assertions()

            for index, url in urls:
                log_name = scenario_obj.get_log_name(index, url)
                thread = Thread(name, url, url_type, module_name, command, assertions, log_name)
                validate_url = thread.validate_url()
                if url_type in validate_url:
                    thread.add_thread()
    

class PreconditionThreads:
    def __init__(self, url, subfinder_enabled, ffuf_enabled, crawler_enabled, wordlist, debug):
        self.subfinder_enabled = subfinder_enabled
        self.ffuf_enabled = ffuf_enabled
        self.crawler_enabled = crawler_enabled
        self.url = url
        self.wordlist = wordlist
        self.debug = debug
        self.output = Output()
        self.files = Files()
        self.database = Database()
    
    def debug_command(self, process):
        # TODO: create debug version
        if self.debug:
            while process.stdout.readable():
                line = process.stdout.readline()
                if not line:
                    break
                another_line = str(line.strip())
                print(another_line)

    def run_command(self, command):
        print('running: {}'.format(command))
        process = subprocess.Popen(
            command,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        
        # self.debug_command(process)
        process.wait()
        output, error = process.communicate()
        print(output)
        print(error)
        print(":))")
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

                for domain in domains:
                    # sometimes there are empty urls
                    if domain:
                        domain = get_https_domain(domain)
                        self.database.add_domain(domain)
                        self.database.add_url(get_https_domain(domain))
            if error:
                self.output.print_error_while_running_command(command, error)
        else:
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
        ffuf_cmd = ['ffuf', '-u', 'GLOBEEXPLORER_DOMAIN' + '/FUZZ', '-w', self.files.get_wordlist_path(self.wordlist), '-o', self.files.get_ffuf_directory_path() + '/FFUF_DOMAIN.json', '-of', 'json']

        self.run_subfinder(subfinder_cmd)    
        self.run_ffuf(ffuf_cmd)
        self.run_crawler()
