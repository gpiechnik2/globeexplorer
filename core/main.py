from files import Files
from database import Database
from threads import PreconditionThreads, Threads


def main(scenario_script, url, subfinder_enabled, ffuf_enabled, gospider_enabled, wordlist, threads):
    # create tmp files directory
    files = Files()
    files.create_tmp_files_structure()

    # create database with tables
    database = Database()
    database.create_initial_tables()

    # validate file
    files.validate_file_content(scenario_script)

    # preconditions
    precondition_threads = PreconditionThreads(url, subfinder_enabled, ffuf_enabled, gospider_enabled, wordlist)
    precondition_threads.start_preconditions()

    # run scenarios
    threads = Threads()

main('testScript.json', 'https://example.pl', True, True, True, 'wordlist/test,.txt', 5)
