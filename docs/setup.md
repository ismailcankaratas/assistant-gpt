# Setup Guide

This guide will help you set up and run the Assistant API on your local machine or server.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- OpenAI API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ismailcankaratas/assistant-gpt.git
   cd assistant-gpt
   ```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
### 3. Configure Environment Variables

Open the app.py file and manually update the following variables with your own credentials:
```python
API_KEY = "your_api_key_here"
CHATGPT_API_KEY = "your_chatgpt_api_key_here"
ASSISTANT_ID = "your_assistant_id_here"
VECTOR_STORE_ID = "your_vector_store_id_here"
```

## Running the Application

```bash
# Start the server
python app/app.py
```

The API will be available at `http://localhost:5000/api/assistants`

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Rate Limiting**: Configure appropriate rate limits
3. **CORS**: Configure CORS settings for your domain
4. **SSL/TLS**: Always use HTTPS in production

## Troubleshooting

If you encounter any issues:

1. Check the error messages in the console
2. Verify your OpenAI API key is valid
3. Ensure all dependencies are installed correctly
4. Open an [issue](https://github.com/ismailcankaratas/assistant-gpt/issues)

## Support

For additional support:
- Check the [documentation](api.md)
- Open an [issue](https://github.com/ismailcankaratas/assistant-gpt/issues)
