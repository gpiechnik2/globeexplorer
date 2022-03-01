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

    def print_info(self):
        print("-------------------------------------------------------------")
        print("  globeexplorer v1.0 by @gpiechnik2")
        print("-------------------------------------------------------------")

    def print_logo(self):
        print("""

                   *#&#,                 
          .%,&#. .&%%%%%%(((/&          
       &/#%%%%/#%%%*/(#((((/////*&      
     &&&%%%%%%%(%%(%#(((//////****,%    
   &&%%%%%%%%%#///////////******,,,,,&  
  %%%%%%%%%%*/%%%%*/#/*****%*,,,,,,***% 
 &&%%%%%%%#,*****(%*#%%#*,,,,,,,******/&
.&%%%%%%/,,,,,,,,,,,,,,,%,,****%%%//%%%/
%%%%%%%%*****************%***%%%%%%/%%%&
 /&%%%%%%*/**************////%%%%%%%%%%&
 %//%%%%%%%%%%%////////////#%%%%%%%%%%%&
  #/%%%%%%%%%%%%//////////%%%%%%%%%%%%& 
   &&%%%%%%%%%%%%/////////%%/%%%%%%%%&  
     &%%%%%%%%%%%///////%%((%%%%%%&&    
       &&&%%%%%%%%%//(%%%%%%%%%%%/      
           &%%%%%%%%%%%%%%%%&&    
                           
    """)

    def print_added_to_queue(self, name, url, command):
        purple_semicolon = self.get_purple_semicolon()
        print('🌐 [{}] {} {}{} {}{} {}{}'.format(
            self.get_time(),
            'Added to the queue....:',
            name,
            purple_semicolon,
            url,
            purple_semicolon,
            command,
            purple_semicolon
        ))

    def print_vulnerability_found(self, name, url, assertion):
        purple_semicolon = self.get_purple_semicolon()
        print('🌐 [{}] {} {}{} {}{} {}{} {}{}'.format(
            self.get_time(),
            self.red('Vulnerability found...:'),
            name,
            purple_semicolon,
            url,
            purple_semicolon,
            assertion['type'],
            purple_semicolon,
            assertion['value'],
            purple_semicolon
        ))

    def print_risk_found(self, name, url, assertion):
        purple_semicolon = self.get_purple_semicolon()
        print('🌐 [{}] {} {}{} {}{} {}{} {}{}'.format(
            self.get_time(),
            self.red('Risk found............:'),
            name,
            purple_semicolon,
            url,
            purple_semicolon,
            assertion['type'],
            purple_semicolon,
            assertion['value'],
            purple_semicolon
        ))

    def print_risk_or_vulnerability_found(self, scenario_type, name, url, assertion):
        if scenario_type == 'risk':
            self.output.print_risk_found(name, url, assertion)
        elif scenario_type == 'vulnerability':
            self.output.print_vulnerability_found(name, url, assertion)    

    def print_initial_module_started(self, name, description):
        purple_semicolon = self.get_purple_semicolon()
        print('🌐 [{}] {} {}{} {}{}'.format(
            self.get_time(),
            'Initial module started:',
            name,
            purple_semicolon,
            description,
            purple_semicolon
        ))

    def print_error_while_running_command(self, command, error):
        purple_semicolon = self.get_purple_semicolon()
        print('🌐 [{}] {} {}{} {}{}'.format(
            self.get_time(),
            self.red('Error while running...:'),
            command,
            purple_semicolon,
            error,
            purple_semicolon
        ))
