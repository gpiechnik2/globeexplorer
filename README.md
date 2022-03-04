<h1 align="center">
  <img src="static/logo.jpg" alt="globeexplorer" width="260px"></a>
  <br>
</h1>

<h4 align="center">A framework for performing automated penetration tests.</h4>
      
<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#setup">Setup</a> •
  <a href="#commands">Commands</a> •
  <a href="#running">Running</a> •
  <a href="#running-with-docker">Running with Docker</a> •
  <a href="#tools-used">Tools used</a> •
  <a href="#license">License</a>
</p>

---


Globeexplorer is an extremely extensible framework for automating the running of different types of vulnerability and web risk scanners. The framework is dedicated to **Continous Integration & Continous Security** (CI&CS) and daily **penetration testing of web applications**. Thanks to automation of security scanners we are able to optimize our work and become more efficient.

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

# Installation
For the tool to work, you need to have two tools installed locally. These are ffuf and subfinder. We recommend using our prepared Dockerfile instead. 

If you don't want to use docker, install subfinder and ffuf first (on kali linux they are installed by default). Then download globexplorer with the command:

```
git clone https://github.com/gpiechnik2/globeexplorer.git
```

Go to the repository

```
cd globeexplorer
```

And install the tool locally

```
pip install --editable .
```

# Setup
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
        }
    ]
}
```

Let's discuss each element of the test in turn:
1. **name (required)** - test name
2. **module_name (optional)** - if the command uses files (e.g. script.py) to run the tool, the file should be in a newly created directory in the modules directory. Then module_name will be the name of the modules directory,
3. **type (required)** - the type of threat that the test checks for. Possible values are "risk" and "vulnerability",
4. **url_type (optional)** - type of url on which the test should be run. If the tool uses only parameters for vulnerability checking, the url_type value will be "params". If url_type is not defined, the test will use any url type. The available values for url_type are:
    1. **params** - url addresses using parameters (e.g. `https://example.pl?s=test`),
    2. **js** - url addresses leading to javascript file (e.g. `https://example.pl/test.js`),
    3. **static** - url addresses leading to static files on the website (e.g. `https://example.pl/test.jpg`),
    4. **simple** - simple url's (e.g. `https://example.pl/test`),
    5. **all** - all url's.
5. **command (required)** - command that will be executed in the terminal. Two variables are used to define the url: `GLOBEEXPLORER_URL_WITH_HTTP` and `GLOBEEXPLORER_URL_WITHOUT_HTTP`. Example command: `python3 script.py --url GLOBEEXPLORER_URL_WITH_HTTP`,
6. **assertions (required)** - a list with at least one element that is a type and an assertion value. Available types:
    1. **contain** - checks if a given phrase appears in the standard output of the tool,
    2. **not_contain** - checks if the phrase does not appear in the standard output of the tool,
    3. **regex** - checks if the given regex exists in the standard output of the tool.
7. **single (optional)** - if you want the tool to run only once on the main domain, the value of "single" should be true. The default is false.

An example script (scenarios.json) with existing tests can be found in the examples directory.

## Modules
In order for the tool to work, you need to create a modules directory in the same directory as the test file. Ultimately, the structure should look as follows:

```
+ modules
  + module1
  + module2
scenarios.json
wordlist.txt
```

Where `module1` and `module2` are the values used by the `module_name` parameter in the tests from the scenarios.json file

# Commands
```sh
globeexplorer --help
```
This will display help for the tool. To run the tool, you need to specify three parameters.

| Parameter                     | Description                                                     |
| ----------------------------- | --------------------------------------------------------------- |
| SCENARIO                      | A file with the extension .json that holds the list of tests    |
| URL                           | Url with http or https protocol                                 |
| WORDLIST                      | Wordlist path                                                   |

Here are all the flags it supports.

| Flag                                  | Description                                                                                               |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| -s, --subfinder / -ns, --no-subfinder | Sets whether subfinder should check all subdomains. Disabled by default.                                  |
| -f, --ffuf / -df, --no-ffuf           | Sets whether ffuf should be run on each domain. Enabled by default.                                       |
| -c, --crawler / -nc, --no-crawler     | Sets whether the crawler should be started on each domain. Enabled by default.                            |
| -t, --threads INTEGER                 | Maximum number of threads used at once to run tests (default 10).                                         |
| -c, --convert / -nc, --no-convert     | Sets whether the URL specified by the user should be converted to the root endpoint of his domain.        |
| --version                             | Show the version and exit.                                                                                |

# Running
To use the tool, use the following command:

```console
globeexplorer scenario.json https://bugspace.pl wordlist.txt 
     _     _                   _                 
 ___| |___| |_ ___ ___ _ _ ___| |___ ___ ___ ___ 
| . | | . | . | -_| -_|_'_| . | | . |  _| -_|  _|
|_  |_|___|___|___|___|_,_|  _|_|___|_| |___|_|   v1.0 by @gpiechnik2
|___|                     |_|                    
                                                 
⌾ [08:27:29] Scenario data.........: scenario: script.json; url: https://bugspace.pl; subfinder: disabled; ffuf: enabled; crawler: enabled; wordlist: wordlist.txt; threads: 10; convert: enabled;
⌾ [08:27:29] Initial module started: ffuf; great tool used for fuzzing;
⌾ [08:27:30] Initial module started: crawler; web crawling tool;
⌾ [08:29:29] Added to the queue....: 6 tests based on 111 urls of 1 domains;
⌾ [08:29:29] Please be patient. If a risk or vulnerability is discovered, we will let you know;

⌾ [08:29:29] Risk found............: Damn small JS scanner; python3 dsjs.py -u https://bugspace.pl; not_contain; no vulnerabilities found;             
```

The `/tmp` directory contains all the sorted test logs.

# Running with Docker
Pull the latest tagged [globeexplorer](https://hub.docker.com/gpiechnik2/globeexplorer) docker image:

```sh
docker pull gpiechnik2/globeexplorer:latest
```

Running globeexplorer using docker image:

```sh
docker -t gpiechnik2/globeexplorer:latest scenario.json https://example.pl wordlist.txt
``` 

Remember that the scenario.json and wordlist.txt file must be inside the built docker image.

# Tools used
The framework for the application reconnaissance part uses 2 github repositories. These are:

| Tool      | Description                                                                                   | Repository                                    |
| ----------| --------------------------------------------------------------------------------------------- | --------------------------------------------- |
| subfinder | Discovering passive subdomains of websites by using digital sources like Censys, Chaos, Recon | https://github.com/projectdiscovery/subfinder |
| ffuf      | Tool used for fuzzing                                                                         | https://github.com/ffuf/ffuf                  |

# TODO
- Create a log from the main console
- Create asynchronous crawling
- Deploy to PyPi
- Add the example script together with modules and Dockerfile in the examples directory
- Add Dockerfile.base and push it to to the dockerhub

# License
Not included yet
