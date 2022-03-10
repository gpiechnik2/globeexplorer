from datetime import datetime


class Output:
    def __init__(self):
        self.PURPLE = '\u001b[38;5;93m'
        self.OFF = '\033[0m'
        self.RED = '\u001b[38;5;124m'
        self.GREEN = '\u001b[38;5;35m'
        self.WHITE = '\u001b[37m'

    def red(self, text):
        return "{}{}{}".format(
            self.RED,
            text,
            self.OFF
        )

    def green(self, text):
        return "{}{}{}".format(
            self.GREEN,
            text,
            self.OFF
        )

    def purple(self, text):
        return "{}{}{}".format(
            self.PURPLE,
            text,
            self.OFF
        )
    
    def get_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def get_purple_semicolon(self):
        return self.purple(';')

    def print_logo(self):
        print(" ")
        print("     _     _                   _                 ")
        print(" {}| |___| |_ ___ ___ _ _ ___| |___ ___ ___ ___ ".format(self.purple("___")))
        print("{} | . | . | -_| -_|_'_| . | | . |  _| -_|  _|".format(self.purple("| . |")))
        print("{}_|___|___|___|___|_,_|  _|_|___|_| |___|_|   v1.0 by @gpiechnik2".format(self.purple("|_  |")))
        print("{}                     |_|                    ".format(self.purple("|___|")))
        print("                                                 ")

    def print_data(self, scenario, url, subfinder, ffuf, crawler, wordlist, threads, convert):
        subfinder = self.purple('enabled') if subfinder else self.purple('disabled')
        ffuf = self.purple('enabled') if ffuf else self.purple('disabled')
        crawler = self.purple('enabled') if crawler else self.purple('disabled')
        wordlist = self.purple(wordlist) if wordlist else self.purple('common.txt')
        convert = self.purple('enabled') if convert else self.purple('disabled')

        purple_semicolon = self.get_purple_semicolon()
        print('{} [{}] {} {}{}'.format(
            self.purple('⌾'),
            self.get_time(),
            'Scenario data.........:',
            'scenario: ' + self.purple(scenario) + purple_semicolon + ' url: ' + self.purple(url) + purple_semicolon + ' subfinder: ' + subfinder + purple_semicolon + ' ffuf: ' + ffuf + purple_semicolon + ' crawler: ' + crawler + purple_semicolon + ' wordlist: ' + wordlist + purple_semicolon + ' threads: ' + self.purple(str(threads)) + purple_semicolon + ' convert: ' + convert,
            purple_semicolon
        ))

    def print_added_to_queue(self, tests_quantity, urls_quantity, domains_quantity):
        purple_semicolon = self.get_purple_semicolon()
        print('{} [{}] {} {}{}'.format(
            self.purple('⌾'),
            self.get_time(),
            'Added to the queue....:',
            self.purple(str(tests_quantity)) + ' tests based on ' + self.purple(str(urls_quantity)) + ' urls of ' + self.purple(str(domains_quantity)) + ' domains',
            purple_semicolon
        ))
        print('{} [{}] {}{}{}'.format(
            self.purple('⌾'),
            self.get_time(),
            'Please be patient. If a risk or vulnerability is discovered, we will let you know',
            purple_semicolon,
            '\n'
        ))

    def print_vulnerability_found(self, name, file_name, assertion):
        purple_semicolon = self.get_purple_semicolon()
        print('{} [{}] {} {}{} {}{} {}{} {}{}'.format(
            self.purple('⌾'),
            self.get_time(),
            self.red('Vulnerability found...:'),
            name,
            purple_semicolon,
            file_name,
            purple_semicolon,
            assertion['type'],
            purple_semicolon,
            assertion['value'],
            purple_semicolon
        ))

    def print_risk_found(self, name, file_name, assertion):
        purple_semicolon = self.get_purple_semicolon()
        print('{} [{}] {} {}{} {}{} {}{} {}{}'.format(
            self.purple('⌾'),
            self.get_time(),
            self.red('Risk found............:'),
            name,
            purple_semicolon,
            file_name,
            purple_semicolon,
            assertion['type'],
            purple_semicolon,
            assertion['value'],
            purple_semicolon
        ))

    def print_risk_or_vulnerability_found(self, scenario_type, name, file_name, assertion):
        if scenario_type == 'risk':
            self.print_risk_found(name, file_name, assertion)
        elif scenario_type == 'vulnerability':
            self.print_vulnerability_found(name, file_name, assertion)    

    def print_initial_module_started(self, name, description):
        purple_semicolon = self.get_purple_semicolon()
        print('{} [{}] {} {}{} {}{}'.format(
            self.purple('⌾'),
            self.get_time(),
            'Initial module started:',
            name,
            purple_semicolon,
            description,
            purple_semicolon
        ))

    def print_error_while_running_command(self, command, error):
        purple_semicolon = self.get_purple_semicolon()
        print('{} [{}] {} {}{} {}{}'.format(
            self.purple('⌾'),
            self.get_time(),
            self.red('Error while running...:'),
            command,
            purple_semicolon,
            error,
            purple_semicolon
        ))

    def print_error_end_exit(self, error):
        print(self.red(error))
        exit()

    def print_tests_finished(self):
        purple_semicolon = self.get_purple_semicolon()
        print('{} [{}] {}{}'.format(
            self.purple('⌾'),
            self.get_time(),
            self.green('The launch of the test scenarios has just finished!'),
            purple_semicolon
        ))
