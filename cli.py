import click


@click.group()
@click.version_option('1.0')
def cli():
    """globeexplorer

    globeexplorer is a simple tool for writing test scenarios 
    and automating web vulnerability scanning tools. To run
    a vulnerability scan, create a test scenario and then run
    it with the run command.

    """


@cli.command()
@click.argument("scenario", type=str)
@click.argument("url", type=str)
@click.option('--wordlist', '-w', default='basic',
              help='Wordlist name. Wordlists available: basic, extended, full.')
@click.option('--subfinder', '-s', default='true',
              help='Sets whether subfinder should check all subdomains. To disable, change to "disabled".')
@click.option('--ffuf', '-f', default='true',
              help='Sets whether ffuf should be run on each domain. To disable, change to "disabled".')
def run(scenario, url, wordlist, subfinder, ffuf):
    """Runs the specified test scenario on the specified url."""
    wordlists = ['basic', 'extended', 'full', 'test']
    true_false_choices = ['true', 'false', True, False]
    if 'http' not in url:
        print('{}  Please provide http or https link{}'.format(
            Colors.RED, Colors.OFF
        ))
    elif wordlist not in wordlists:
        print(
            '{}  The given wordlist is not available. Available wordlists: basic, extended, full{}'.format(
                Colors.RED,
                Colors.OFF))
    elif ffuf not in possible_choices:
        print(
            '{}  For the ffuf parameter, please use one of the available options: enabled, disabled.{}'.format(
                Colors.RED,
                Colors.OFF))
    elif subfinder not in possible_choices:
        print(
            '{}  For the subfinder parameter, please use one of the available options: enabled, disabled.{}'.format(
                Colors.RED,
                Colors.OFF))
    else:
        run_scenario(scenario, url, wordlist, ffuf, subfinder)
