# easyResearch
A simple researchbot with the ability to research on the internet.

## Description

This project creates a researchbot program that runs locally on CPU using the LangGraph, Ollama, and Streamlit frameworks.

## Getting Started

### Dependencies

* OS: Ubuntu (22.04, 24.04).
* Installed packages: [Ollama](https://ollama.com/download/linux), [Docker](https://docs.docker.com/engine/install/ubuntu/), [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

### How to use

1. Open a terminal and clone this repository:

```
git clone https://github.com/tomsawyer0224/easyResearch.git
cd easyResearch
```
2. Run the following command to create a virtual environment and install all requirements.
```
source init.sh
```
3. Modify the 'config.yaml' file if needed. By default, the researchbot is powered by 'llama3.2' and 'llama3.2:1b' in the Ollama framework. When using it, you can choose either of them.

4. Build a Docker image by running the command (on a terminal inside the 'easyResearch' directory):
```
python build_docker.py
```
* To start the researchbot, run command:
```
docker run --name eResearcher --rm -p 8501:8501 researchbot
```
or in background mode:
```
docker run --name eResearcher --rm -d -p 8501:8501 researchbot
```
* Access the application at http://localhost:8501.
* To stop the researchbot, run command:
```
docker stop eResearcher
```
> [!Note]
> For later use, you can publish the docker image to [Docker hub](https://hub.docker.com/). Because the researchbot runs on CPU, you should build the researchbot using minimal Ollama models (specified in the 'config.yaml' file).

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
## Acknowledgments
* [open-deep-research](https://github.com/langchain-ai/open_deep_research)
* [Streamlit](https://docs.streamlit.io/)