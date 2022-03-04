<h1 align="center">
  <img src="static/logo.jpg" alt="globeexplorer" width="260px"></a>
  <br>
</h1>

<h4 align="center">A framework for performing automated penetration tests.</h4>
      
<p align="center">
  <a href="#features">Features</a> •
  <a href="#setup">Setup</a> •
  <a href="#dockerfile">Dockerfile</a> •
  <a href="#running">Running</a> •
  <a href="#todo">Todo</a> •
  <a href="#license">License</a>
</p>

---


Globeexplorer is an extremely extensible framework for automating the running of different types of vulnerability and web risk scanners. The framework is dedicated to Continous Integration & Continous Security (CI&CS) and daily penetration testing of web applications. Thanks to automation of security scanners we are able to optimize our work and become more efficient.

In the example directory you can find test scenarios with tool modules consisting of 12 security scanners. 

# Features
The framework has several distinctive features, which include:
- automatic extraction of application endpoints using subfinders, fuzzing (ffuf) and crawling (custom)
- dynamically determining the URLs on which a given scanner should be run based on data in the scenario (e.g. running the scanner only where there are parameters in the URL)
- easy writing of dynamic test scenarios (see the "examples" directory for more)
- quick, easy to use and not very demanding command line interface
- compiled logs of all actions, which can be used later on
- clear console reporting
- Possibility of integration with SQLite database

# Setup
To run the framework, you need to have two tools installed locally. This is subfinder for searching subdomains and ffuf for fuzzing. These tools are installed by default on kali linux. However, we recommend using Dockerfile.

subfinder: https://github.com/projectdiscovery/subfinder </br>
ffuf: https://github.com/ffuf/ffuf

# Dockerfile
A base Dockerfile has been included in the project, from which a proper Dockerfile can be created. The Dockerfile example is located in the "examples" directory, which holds an example application of the framework.

To use the Dockerfile in the examples directory, you must first build a docker image using the following command.

```console
docker build -t globeexplorerscenarios -f Dockerfile .
```

Then, after checking the newly created image ID with the `docker images` command, run the tool with the (for example) command:

```console
docker run -it IMAGE_ID script.py https://example.pl
```

# Running
To run a prepared scenario you need to have two things prepared. This is the test scenario and the "modules" directory that holds the modules that will be used in the test file (if it uses them).

## Scenario file
A test scenario is a .json file that holds all the tests. For the framework to work, the file is mandatory. Its structure looks like the example below:

```
{
    "scenarios": [
        {
            "name": string,
            "module_name": string,
            "type": string,
            "url_type": string,
            "command": "command",
            "assertions": [
                {
                    "type": string,
                    "value": string
                }
            ],
            "single": boolean
        },
    ]
}
```

Omowmy po kolei kazdy z elementow testu:
1. name (required) - 
2. module_name (optional) - if the command uses files (e.g. script.py) to run the tool, the file should be in a newly created directory in the modules directory. Then module_name will be the name of the modules directory,
3. type (required) - the type of threat that the test checks for. Possible values are "risk" and "vulnerability",
4. url_type (optional) - type of url on which the test should be run. If the tool uses only parameters for vulnerability checking, the url_type value will be "params". If url_type is not defined, the test will use any url type. The available values for url_type are:
- params - url addresses using parameters (e.g. https://example.pl?s=test),
- js - url addresses leading to javascript file (e.g. https://example.pl/test.js),
- static - url addresses leading to static files on the website (e.g. https://example.pl/test.jpg),
- simple - simple url's (e.g. https://example.pl/test),
- all - all url's.
5. command (required) - command that will be executed in the terminal. Two variables are used to define the url: `GLOBEEXPLORER_URL_WITH_HTTP` and `GLOBEEXPLORER_URL_WITHOUT_HTTP`. Example command: `python3 script.py --url GLOBEEXPLORER_URL_WITH_HTTP`,
6. assertions (required) - a list with at least one element that is a type and an assertion value. Available types:
- contain - checks if a given phrase appears in the standard output of the tool,
- not_contain - checks if the phrase does not appear in the standard output of the tool,
- regex - checks if the given regex exists in the standard output of the tool.
7. single (optional) - if you want the tool to run only once on the main domain, the value of "single" should be true. The default is false.

An example script with existing tests can be found in the examples directory under the name scenarios.py.

## Modules


## Commands
```sh
globeexplorer --help
```
This will display help for the tool. Here are all the flags it supports.

| Flag                                  | Description                                                                                   |
| ------------------------------------- | --------------------------------------------------------------------------------------------- |
| -s, --subfinder / -ns, --no-subfinder | Sets whether subfinder should check all subdomains. Disabled by default.                      |
| -f, --ffuf / -df, --no-ffuf           | Sets whether ffuf should be run on each domain. Enabled by default.                           |
| -c, --crawler / -nc, --no-crawler     | Sets whether the crawler should be started on each domain. Enabled by default.                |
| -w, --wordlist PATH                   | The path specified to the wordlist. If it is not present, the default wordlist will be used. |
| -t, --threads INTEGER                 | Maximum number of threads used at once to run tests (default 10).                             |
| -c, --convert / -nc, --no-convert     | Sets whether the URL specified by the user should be converted to the root endpoint of his domain.                   |
| --version                             | Show the version and exit.                                                                    |


# todo
- make crawling asynchronous
- setup.py
- add Dockerfile.base
- add Dockerfile and modules in the example directory

# License
Not included yet
