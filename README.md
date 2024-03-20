## ML Engineering by Modules
- **List of Modules**:
    1. [*Core Ideas & Preparation for the course*](#core-ideas)
    2. [*Containerization*](#container)
    


### <a name="core-ideas">Core Ideas & Preparation for the course</a>
- **Installing docker** <br>
On macOS system I used terminal (command-line) to install Docker with the help of Homebrew. I've had Homebrew already installed and because the Docker for macOS is a GUI tool the command `brew install docker` doesn't work. So I used `--cask` option of the `brew install` command that's responsible for installing GUI tools. Here's the full command I used:
```bash
brew install --cask docker
```
**Alternatively we can use GUI option of installation (drag-and-dropping)* <br>
After installing Docker I validated successfull installation using ```docker --version``` command that gives the current version of my Docker.
- Working on terminal![](Module1/docker_terminal.jpg)
- Working on Docker Desktop GUI![](Module1/docker_gui.jpg)

### <a name="container">Containerization</a>