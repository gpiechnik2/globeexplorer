from files import Files
from database import Database
from threads import PreconditionThreads, Threads


def main(scenario_script, url, subfinder_enabled, ffuf_enabled, crawler_enabled, wordlist, threads, debug):
    # create tmp files directory
    files = Files()
    files.create_tmp_files_structure()

    # create database with tables
    database = Database()
    database.create_initial_tables()

    # validate file
    files.validate_scenario_content(scenario_script)
    scenarios = files.get_scenarios(scenario_script)

    # preconditions
    precondition_threads = PreconditionThreads(url, subfinder_enabled, ffuf_enabled, crawler_enabled, wordlist, debug)
    precondition_threads.start_preconditions()

    # run scenarios
    threads = Threads(scenarios)
    threads.start_threads()

main('script.json', 'https://bugspace.pl', True, True, True, 'test.txt', 5, False)
