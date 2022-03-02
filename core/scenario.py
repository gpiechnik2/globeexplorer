
class Scenario:
    def __init__(self, scenario):
        self.scenario = scenario

    def get_name(self):
        return self.scenario['name']

    def get_module_name(self):
        return self.scenario['module_name']

    def get_url_type(self):
        return self.scenario['url_type']

    def get_command(self, url):
        url_without_https = get_without_https_domain(url)
        command = self.scenario['command']
        command = command.replace('GE_WITH_HTTPS', url).replace('GE_WITHOUT_HTTPS', url_without_https)
        return command

    def get_assertions(self):
        return self.scenario['assertions']

    def is_single(self):
        if single in self.scenario:
            return True if scenario["single"] == 'true' else False

    def get_log_name(self, index, url):
        url_without_characters = get_without_https_domain(url)
        return self.get_name() + '_{}_{}'.format(url_without_characters, index).replace(' ', '')
