# Introducing the 'PO'

`PO`, the **AI Integrated Terminal**, no more juggling with different windows, just mention different model with your very own alias. We let you to manage your own context.

## Installation
```bash
pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  po-ai-buddy --upgrade
po --version  # if installation is correct, output version like `po-ai-buddy 1.1.1`
```

## Bring Your Own Keys!
You need to give your own keys as environmnet variables. See <a href="#env-var">Environment variables</a>

## Configuration
- **Configuration file:** Contains the alias for specified models, default model, indicator(e.g _$_)
- **Config File path:** This file path can be global or where from PO called like current directory.
- **Config file name:** `.po.json`


If no config file found, it will ask for permission to create a global level config. see below:

### Global level config(default):

**Windows:**
`Path.home() / "AppData" / "Roaming" / "po" / ".po.json"`

**Linux/MacOS:**
`Path.home() / ".config" / "po" / ".po.json"`


### Invoke/Project level config:
If `PO` found its config file where from it called, it will take that config. This allow flexibility.

Example: 
```bash
$ pwd
/home/myuser/
$ ls
.po.json
$ PO    # This will pick pwd config file
```


## How it works?

When user invoke our **PO** via `PO` this will start a _REPL_ with context memory that can be discarded when user want.
    

Notes: 
1. Before executing the cmd, program will show the cmd and ask for permission
2. Context Management: 

```bash
PO
No config found, do you want to create a global level config?
(y/n): y
$ @bhai How to push git tags?   # Used alias
AI: To push a git tag, use the following command: git push --tags. This will push all local tags to the remote repository.
    CMD: git push --tags    # CMD that AI have given
Run[y] abort[n] [type more]: what --tags do?    # y for Run, n for cancel, type anything else to keep talking(context maintained)
AI: The  --tags  option with git push tells Git to push all local tags. Using  git push origin --tags  would specifically push tags to the 'origin' repository.
    CMD: git push origin --tags
Run[y] abort[n] [type more]: n  # aborted and clear context
$ @bhai How to print "Hello world" in terminal?
AI: Hello world
    CMD: echo 'Hello world'
Run[y] abort[n] [type more]: y      # Yes, run the cmd and clear context
$ echo 'Hello world'    # Written by progra,
'Hello world'
$ q     # quit
Thanks for Using :)
```

### Multiple-Model without losing context
> Note: I know this example is slightly weird
```bash
PO
$ @bro How to merge two branches?
groq/llama-3.3-70b-versatile    # DEBUG: Model choosed
AI: To merge two branches, you can use the 'git merge' command. First, check out the branch you want to merge into, then use 'git merge <branch-name>' to merge the other branch into it. For example: git checkout main && git merge feature/new-feature
    CMD: git checkout main && git merge feature/new-feature
Run[y] abort[n] [type more]: @bhai What is your name?
groq/llama-3.1-8b-instant     # DEBUG: Changed the model, but context maintained
AI: I am an AI assistant, I don\'t have a personal name, but I can help you with any questions or tasks you have.
abort[n] [type more]: n
$
```

---




<h2 id="env-var">Environment Variables for API Keys:</h2>
We follow BYOK model and thus you need to give API keys as environment variables.

> These variables names are opinionated by instructor library.

Linux/MacOS:
```bash
export API_KEY_NAME=<your-api-key-here>
```

Windows:
```bash
setx API_KEY_NAME "your-api-key-here"
```

### API KEYS


You need to provider API keys as environment variables. Below you can the corresponding variable name.

> Note: Not full list.

_Make sure that your selected model support 'tooling' and supported by PO_

- **Groq:**
  - `GROQ_API_KEY`

- **OpenAI:**
  - `OPENAI_API_KEY`

- **Anthropic:**
  - `ANTHROPIC_API_KEY`

- **Google (Gemini):**
  - `GOOGLE_API_KEY`

- **Mistral:**
  - `MISTRAL_API_KEY`

- **Ollama:**
  - Not required.

- **OpenRouter:**
  - `OPENROUTER_API_KEY`

- **Perplexity:**
  - `PERPLEXITY_API_KEY`

- **xAI:**
  - `XAI_API_KEY`

- **DeepSeek:**
  - `DEEPSEEK_API_KEY`

