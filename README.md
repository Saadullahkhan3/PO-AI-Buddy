# Introducing the 'PO'

`PO`, the **AI Integrated Terminal**, no more juggling with different windows, just mention different model with your very own alias. We let you to manage your own context.

## Installation

You need to run below command(if you are on TestPyPI, don't run above provided command). The reason is that `PO` itself is on `TestPyPI` while its dependencies are on `PyPI`, so to enable PyPI also, we need below command
```bash
pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  po-ai-buddy --upgrade
```

- Check version
```bash
po --version  # if installation is correct, output version like `po-ai-buddy 1.1.1`
```

## Bring Your Own Keys!
You need to give your own keys as environmnet variables. See <a href="#env-var">Environment variables</a>

**Important:** The AI models you use must support **function calling/tool calling** (also known as structured outputs). Most modern models support this, but verify with your provider before use.

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

You can start this program via 2 methods.

### 1. Quick Start

When user invoke our **PO** via `PO` and give query on-the-fly/while Invoke-ing the program, this becomes a *short-hand* which you can use to increase efficency. This will start a _REPL_ with context memory that can be discarded when user want.

> Note: Make sure to wrap queries in ""/'' especially On Windows PowerShell as `@` will be treated as special character and may even not pass it to PO.

```bash
PO "@ai how at delete a file?"
Processing query: @ai how at delete a file?   # DEBUG
AI: To delete a file, use the 'rm' command followed by the file name.
    CMD: rm
Run[y] abort[n] [type more]: n
$ q
Thanks for Using :)
```

### 2. Invoke Based
When user invoke our **PO** via `PO` this will start a _REPL_ with context memory that can be discarded when user want.
    

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


### Notes: 
- Before executing the cmd, program will show the cmd and ask for permission, 

### Input Options

| Option | Effect |
|---|---|
| y | Will run the shown command, discard the context memory and exit AI loop(not PO itself) |
| n | Will discard the context memory and exit AI loop(not PO itself) |
| type more | Write your query to model as feedback, this will also use your current context, continues the AI loop


## Multiple-Model without losing context

You can change model on-the-fly, just my mentioning it. If user is already in loop(talking) and not mention any model, we will use previously used model.

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

_If you don't have any API keys, I recommended you to use Groq's API for demo_

> Note: Not full list.

_Make sure that your selected model support 'tooling' and supported by PO_

- **Groq:** `GROQ_API_KEY`

- **OpenAI:** `OPENAI_API_KEY`

- **Anthropic:** `ANTHROPIC_API_KEY`

- **Google (Gemini):** `GOOGLE_API_KEY`

- **Mistral:** `MISTRAL_API_KEY`

- **Ollama:** Not required.

- **OpenRouter:** `OPENROUTER_API_KEY`

- **Perplexity:** `PERPLEXITY_API_KEY`

- **xAI:** `XAI_API_KEY`

- **DeepSeek:** `DEEPSEEK_API_KEY`


## FAQs

### Q: Why does `@ai` get stripped when I type it in PowerShell/Terminal?
**A:** PowerShell treats `@` as a special operator. Always wrap your queries in quotes: `PO "@ai your query"`. This may also be happened with other terminals so always wrap Quick Start queries in quotes.

### Q: I'm getting "Provider might be wrong configured/un-supported" error. What's wrong?
**A:** This usually means:
1. Your model doesn't support function calling/tool calling (structured outputs)
2. The provider's Python library isn't installed (e.g., `pip install openai`)
3. Your API key environment variable isn't set correctly

Use models that support tooling, such as `groq/llama-3.1-8b-instant` or `openai/gpt-4`.

### Q: Can I use this offline?
**A:** Yes(not quite)! Install Ollama locally and use the `ollama/*` provider. No API key needed. But you need a HEAVY computer to handle models.

### Q: How do I clear my conversation context?
**A:** Type `n` when prompted, or the context automatically clears after running a command with `y`.

### Q: Why add `@` every time when I want to talk to AI?
**A:** The answer is your question, you only need to add `@` when you want to talk to AI, for convience, if you entered in AI loop(start talking to AI) you don't need to write `@` again and again, just write your query, you only need it if your want to change your model.


---

Nobody has asked anything, these FAQs are self-assumed :)

---

## [PO — AI Buddy](https://github.com/Saadullahkhan3/PO-AI-Buddy)