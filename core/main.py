from core.files import Files
from core.database import Database
from core.threads import PreconditionThreads, Threads


def main(scenario_script, url, subfinder_enabled, ffuf_enabled, crawler_enabled, wordlist, threads_quantity, ignore_domain):
    # create tmp files directory and validate scenario script
    files = Files()
    files.validate_scenario_content(scenario_script)
    files.create_tmp_files_structure()

    # create database with tables
    database = Database()
    database.create_initial_tables()

    # preconditions
    precondition_threads = PreconditionThreads(url, subfinder_enabled, ffuf_enabled, crawler_enabled, wordlist, ignore_domain)
    precondition_threads.start_preconditions()

    # run scenarios
    scenarios = files.get_scenarios(scenario_script)
    threads = Threads(scenarios)
    commands = threads.prepare_commands()
    threads.start_threads(commands, threads_quantity)


main('script.json', 'https://bugspace.pl', True, True, True, 'test.txt', 5, False)
