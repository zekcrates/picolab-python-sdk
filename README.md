# PicoLab Python SDK 

We will be able to login/get/push/test/ the files 


## Install

```python 
pip install picolab-sdk 
```

## Use cases 

### Login 

```python 
picolab login <api-key>
```

### Get 

```python 
picolab get <project_name>

```

### Push 

```python 
picolab push <project_name>

```


## Local Setup 

```python 
git clone https://github.com/zekcrates/picolab-python-sdk

cd picolab-python-sdk
```

```python 
uv venv 

# Windows
.venv/Scripts/activate
```

```python 
uv pip install -r requirements.txt 

```

```python 
# Install in Editable Mode 
uv pip install -e . 

```