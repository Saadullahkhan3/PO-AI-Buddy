# Introducting the 'PO'

`PO`, the **AI Integrated Terminal**, no more juggling with different windows, just mention different model with your very own alias. We let you to manage your own context.


## Bring Your Own Keys!
You need to give your own keys as environmnet variables. See <a href="env-var">Environment variables</a>

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
<the-example-soon>
```


### Example:
```bash
<example-here>
```

---




<h2 id="env-var">Environment Variables for API Keys:</h2>
We follow BYOK model and thus you need to give API keys as environment variables.

> These variables names are opiniated by instructor library.

Linux/MacOS:
```bash
export API_KEY_NAME=<your-api-key-here>
```

Windows:
```bash
setx API_KEY_NAME "your-api-key-here"
```

Variables Names:
- GROQ_API_KEY
- OPENAI_API_KEY
- DEEPSEEK_API_KEY
- TOGETHER_API_KEY

