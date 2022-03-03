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
        print("""
     _     _                   _                 
 ___| |___| |_ ___ ___ _ _ ___| |___ ___ ___ ___ 
| . | | . | . | -_| -_|_'_| . | | . |  _| -_|  _|
|_  |_|___|___|___|___|_,_|  _|_|___|_| |___|_|   v1.0 by @gpiechnik2
|___|                     |_|                     
""")

    def print_data(self, domain, ):


    def print_added_to_queue(self, urls_quantity):
        purple_semicolon = self.get_purple_semicolon()
        print('{} [{}] {} {}{}'.format(
            self.purple('⌾'),
            self.get_time(),
            'Added to the queue....:',
            str(urls_quantity) + ' tests',
            purple_semicolon
        ))
        print('{} [{}] {} {}'.format(
            self.purple('⌾'),
            self.get_time(),
            'Please be patient. If a risk or vulnerability is discovered, we will let you know',
            purple_semicolon
        ))

    def print_vulnerability_found(self, name, process_args, assertion):
        purple_semicolon = self.get_purple_semicolon()
        print('{} [{}] {} {}{} {}{} {}{} {}{}'.format(
            self.purple('⌾'),
            self.get_time(),
            self.red('Vulnerability found...:'),
            name,
            purple_semicolon,
            process_args,
            purple_semicolon,
            assertion['type'],
            purple_semicolon,
            assertion['value'],
            purple_semicolon
        ))

    def print_risk_found(self, name, process_args, assertion):
        purple_semicolon = self.get_purple_semicolon()
        print('{} [{}] {} {}{} {}{} {}{} {}{}'.format(
            self.purple('⌾'),
            self.get_time(),
            self.red('Risk found............:'),
            name,
            purple_semicolon,
            process_args,
            purple_semicolon,
            assertion['type'],
            purple_semicolon,
            assertion['value'],
            purple_semicolon
        ))

    def print_risk_or_vulnerability_found(self, scenario_type, name, process_args, assertion):
        if scenario_type == 'risk':
            self.print_risk_found(name, process_args, assertion)
        elif scenario_type == 'vulnerability':
            self.print_vulnerability_found(name, process_args, assertion)    

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

    def print_error_end_exit(error):
        print(self.red(error))
        exit()
