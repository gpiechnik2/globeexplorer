import click

from globeexplorer.files import Files
from globeexplorer.threads import PreconditionThreads, Threads
from globeexplorer.utils import get_main_domain, validate_url, validate_wordlist
from globeexplorer.database import Database
from globeexplorer.output import Output


@click.version_option('1.0')
@click.command()
@click.argument("scenario", type=str)
@click.argument("url", type=str)
@click.argument("wordlist", type=str)
@click.option('--subfinder/--no-subfinder', '-s/-ns', default=False,
              help='Sets whether subfinder should check all subdomains. Disabled by default.')
@click.option('--ffuf/--no-ffuf', '-f/-df', default=True,
              help='Sets whether ffuf should be run on each domain. Enabled by default.')
@click.option('--crawler/--no-crawler', '-c/-nc', default=True,
              help='Sets whether the crawler should be started on each domain. Enabled by default.')
@click.option('--threads', '-t', default=10,
              help='Maximum number of threads used at once to run tests (default 10).')
@click.option('--convert/--no-convert', '-c/-nc', default=True,
              help='Sets whether the URL specified by the user should be converted to the root endpoint of his domain.')
def cli(scenario, url, wordlist, subfinder, ffuf, crawler, threads, convert):
    """globeexplorer

    globeexplorer is a simple tool for writing test scenarios 
    and automating web vulnerability scanning tools. To run
    a vulnerability scan, create a test scenario and then run
    it with the run command.

    """

    validate_url(url)
    validate_wordlist(wordlist)

    if convert:
        url = get_main_domain(url)

    # create tmp files directory and validate scenario script
    files = Files()
    files.validate_scenario_content(scenario)
    files.clear()
    files.create_tmp_files_structure()

    # create database with tables
    database = Database()
    database.create_initial_tables()

    # print data
    output = Output()
    output.print_logo()
    output.print_data(scenario, url, subfinder, ffuf, crawler, wordlist, threads, convert)

    # preconditions
    precondition_threads = PreconditionThreads(url, subfinder, ffuf, crawler, wordlist, convert)
    precondition_threads.start_preconditions()

    # run scenarios
    scenarios = files.get_scenarios(scenario)["scenarios"]
    threads_obj = Threads(scenarios)
    commands = threads_obj.prepare_commands()
    threads_obj.start_threads(commands, threads)

if __name__ == '__main__':
    cli()
