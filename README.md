# HDUHelp Vocabulary Saver

This is an automated browser script powered by Selenium and Google Gemini API. It logs into HDUHelp Vocabulary System and automatically answers questions using LLM inference. 

## Installation & Setup

### 1. Using Virtual Environment (Recommended)

It is recommended to create a virtual environment to avoid conflicts with system packages.

#### 1. Create a virtual environment
```bash
python3 -m venv venv
```
#### 2. Activate the virtual environment
```bash
# On macOS / Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install selenium google-generativeai google-genai
```

### 3. Install Firefox & GeckoDriver
- Install [Firefox Browser](https://www.mozilla.org/firefox/)
- Download [GeckoDriver](https://github.com/mozilla/geckodriver/releases) and place it in a system path:

  - macOS/Linux: `/usr/local/bin/`
  - Windows: e.g., `C:\WebDriver\bin` (add this to `PATH`)

### 4. Set your Gemini API Key
Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey), then replace the value in the script:
```python
client = genai.Client(api_key="your-api-key-here")
```


## Configuration

Update the following lines in the script with your HDU credentials:

```python
username = "your-student-id"
password = "your-password"
```

Select your mode, self-test or exam:
```python
MODE = "test"
```
Or
```python
MODE = "exam"
```

## How to Run
### macOS / Linux
```bash
python auto_vocab_saver.py
```

Make sure `geckodriver` is executable:

```bash
chmod +x /usr/local/bin/geckodriver
```

### Windows
Update the driver path:

```python
gecko_path = "C:\\WebDriver\\bin\\geckodriver.exe"
```

Then run the script:

```cmd
python auto_vocab_saver.py
```

## Notes
After the script completes the automatic answering process, **please manually submit the test or exam**.

## License

MIT License  
This project is intended for educational and personal use only. Use responsibly.
