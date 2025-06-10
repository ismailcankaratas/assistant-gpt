# Assistant GPT

A Flask-based Python API that integrates OpenAI's Assistant API to deliver intelligent, file-aware chat capabilities. This project provides a simple yet powerful interface for building, managing, and extending AI-driven conversational experiences.


## OpenAI Documents

- [Quickstart](https://platform.openai.com/docs/assistants/quickstart)
- [Assistants](https://platform.openai.com/docs/api-reference/assistants/listAssistants)
- [Files](https://platform.openai.com/docs/api-reference/files/create)
- [Creating Vector Stores And Adding Files](https://platform.openai.com/docs/assistants/tools/file-search/creating-vector-stores-and-adding-files)
- [Assistant Stream](https://github.com/openai/openai-python/blob/main/examples/assistant_stream.py)
- [Python Production Deploy](https://flask.palletsprojects.com/en/3.0.x/tutorial/deploy/)
- [Actions](https://platform.openai.com/docs/actions/introduction)
- [Function Calling](https://platform.openai.com/docs/assistants/tools/function-calling)
nut- [Create Image](https://platform.openai.com/docs/api-reference/images/create)

- [Objects](https://platform.openai.com/docs/assistants/overview/objects)

## Education

For detailed information about GPT Actions and Function Calling, please refer to our [Education Guide](/docs/education.md). This guide covers:

- GPT Actions Overview
- Function Call Lifecycle
- Data Flow Diagrams
- Implementation Examples

## Quick Start

```bash
# Clone the repository
git clone https://github.com/ismailcankaratas/assistant-gpt.git
cd assistant-gpt

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Key Features

- 🤖 AI-powered conversations using OpenAI's Assistant API
- 📝 Thread management and message handling
- 📁 File upload and vector store integration
- ⚡ GPT Actions and function calling support

## API Reference

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/threads` | POST | Create new conversation thread |
| `/messages` | POST | Send message in thread |
| `/messages` | GET | Retrieve thread messages |
| `/files` | POST | Upload files for assistant |

## Documentation

- [API Documentation](docs/api.md)
- [Setup Guide](docs/setup.md)
- [Contributing Guide](CONTRIBUTING.md)

## Requirements

- Python 3.8+
- OpenAI API key

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📚 [Documentation](docs/)
- 💬 [Discussions](https://github.com/ismailcankaratas/assistant-gpt/discussions)
- 🐛 [Issues](https://github.com/ismailcankaratas/assistant-gpt/issues)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## Acknowledgments

- OpenAI for the Assistant API
- Flask team for the web framework
- All contributors and users of this project
