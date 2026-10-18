# Local AI Assistant

A command-line chat assistant that runs a local language model with [Ollama](https://ollama.com/). It uses Ollama's OpenAI-compatible API through the Python `openai` package. The assistant can also call tools for the local time and live weather.

## Prerequisites

- Python 3.10 or newer
- macOS with Ollama installed and running
- Enough memory and disk space for the model you choose. Model requirements vary by size and quantization.

### Install Ollama on macOS

1. Download the macOS app from [ollama.com/download](https://ollama.com/download).
2. Open the downloaded file and move Ollama to **Applications** if macOS prompts you to do so.
3. Launch Ollama from **Applications**. Keep it running; it provides the local model service and makes the `ollama` command available in Terminal.

Check that installation worked from Terminal:

```zsh
ollama --version
```

## Download and start a model

This example uses `qwen3:8b`, which supports tool calling:

```zsh
ollama pull qwen3:8b
ollama list
```

The pull downloads the model files locally and may take a while. Check the exact tag shown by `ollama list`; the `MODEL` setting below must match it.

The Ollama app starts the local service. If you need to start it manually, quit the app first, then run this in Terminal:

```zsh
ollama serve
```

You can optionally check the model from Ollama's interactive CLI:

```zsh
ollama run qwen3:8b
```

Type `/bye` to leave the Ollama prompt.

## Configure and run the assistant

Open Terminal, go to the project directory, and create and activate a virtual environment:

```zsh
python3 -m venv .venv
source .venv/bin/activate
```

Install the Python dependencies:

```zsh
python -m pip install --upgrade pip
python -m pip install openai python-dotenv requests
```

Create a `.env` file in the project directory with:

```dotenv
BASE_URL=http://localhost:11434/v1
API_KEY=ollama
MODEL=qwen3:8b
```

`API_KEY` is required by the OpenAI client but, for a local Ollama server, can be any non-empty value. If you pulled a different model, replace `MODEL` with its exact tag from `ollama list`.

Start the assistant:

```zsh
python simple_ai_assistant.py
```

Enter a prompt at `Anuj :`. Enter `exit`, `quit`, `bye`, or `goodbye` to close it. The assistant is instructed to keep responses under 40 words.

## Call Ollama's API directly

With Ollama running and the model downloaded, you can test the OpenAI-compatible chat endpoint without starting the Python assistant:

```zsh
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3:8b",
    "messages": [{"role": "user", "content": "Say hello in one sentence."}]
  }'
```

## Built-in tools and network use

- `get_current_time` returns the system's local date and time.
- `get_city_weather` requests the current weather from [wttr.in](https://wttr.in/) and therefore needs an internet connection.

The language model runs locally, but weather lookups are not offline.

## Troubleshooting

- **`ollama: command not found`:** Launch Ollama from **Applications**. If it remains unavailable, quit and reopen Terminal after installing Ollama.
- **Connection refused:** Make sure the Ollama app is running (or start `ollama serve` in Terminal) and `BASE_URL` is `http://localhost:11434/v1`.
- **Model not found:** Run `ollama pull qwen3:8b`, or update `MODEL` to exactly match the tag reported by `ollama list`.
- **Python import error:** Activate the virtual environment and install the dependencies listed above.
- **Slow responses or out-of-memory errors:** Try a smaller Ollama model and set `MODEL` to its exact tag.
