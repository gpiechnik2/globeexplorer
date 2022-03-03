from core.utils import get_without_https_domain

class Scenario:
    def __init__(self, scenario):
        self.scenario = scenario

    def get_name(self):
        return self.scenario['name']

    def get_module_name(self):
        return self.scenario['module_name'] if 'module_name' in self.scenario else False

    def get_url_type(self):
        return self.scenario['url_type'] if 'url_type' in self.scenario else 'all'

    def get_command(self, url):
        return self.scenario['command']

    def get_assertions(self):
        return self.scenario['assertions']

    def is_single(self):
        if 'single' in self.scenario:
            return True if self.scenario["single"] == True else False

    def get_log_name(self, index, url):
        url_without_characters = get_without_https_domain(url)
        return self.get_name() + '_{}_{}'.format(url_without_characters, index).replace(' ', '')

    def get_scenario_type(self):
        return self.scenario['type']
