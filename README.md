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
Do uruchomienia frameworka potrzebne jest posiadanie dwoch narzedzi lokalnie. Jest to subfinder

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

## Modules

## Scenario file

## Commands



# todo
- clearing /tmp and database
- validate scenario file
- threads check
- make crawling asynchronous
- change maximum asynchronous calls
- add wordlist argument (path have to be defined by the user)
- setup.py
- cli.py
- delete try/catch in run_command functions
- dodac optymalizacje bazy danych (usuwanie doubled records)

# Thanks to


# License
Not included yet
