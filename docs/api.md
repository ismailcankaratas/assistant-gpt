# API Documentation

This document provides detailed information about the Assistant API endpoints, their parameters, and example usage.

## Base URL

```
http://00.000.00.000:5000/api/assistants/
```

## Authentication

The API uses Bearer Token authorization. You will need to provide the Bearer Token in the headers of your requests.

### Example Authorization Header:

```http
Authorization: Bearer <token>
```

## Endpoints

### 1. Create Thread

- **Endpoint**: `/threads`
- **Method**: `POST`
- **Description**: This endpoint creates a new chat thread and returns the thread ID.

### 2. Send Message

- **Endpoint**: `/chat/message`
- **Method**: `POST`
- **Description**: This endpoint sends a message to the assistant in a specific chat thread and returns the assistant's response.

**Request Body**
```json
{
    "message": "<Your message>",
    "threadId": "<thread_ID>"
}
```

### 3. Get Messages

- **Endpoint**: `/chat/messages/<threadId>`
- **Method**: `GET`
- **Description**: This endpoint retrieves all messages in a specific chat thread using the `threadId`.

## Example Requests

### Create Thread (POST)

```http
POST /threads
Authorization: Bearer <token>
```

### Send Message (POST)

```http
POST /chat/message
Authorization: Bearer <token>
Content-Type: application/json

{
    "message": "Test",
    "threadId": "thread_CMmShYlw54KaPCUf3ZQEzEPF"
}
```

### Get Messages (GET)

```http
GET /chat/messages/thread_CMmShYlw54KaPCUf3ZQEzEPF
Authorization: Bearer <token>
```

## Notes

- Ensure that the Bearer Token is provided in every request.
- The API is hosted locally, so be sure the server is running at the specified base URL.

## SDK Examples

### Python
```python
import requests

API_KEY = "your_api_key"
BASE_URL = "http://00.000.00.000:5000/api/assistants"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Create a thread
response = requests.post(
    f"{BASE_URL}/threads",
    headers=headers
)
thread_id = response.json()["thread_id"]

# Send a message
response = requests.post(
    f"{BASE_URL}/chat/message",
    headers=headers,
    json={
        "message": "Hello, how can you help me?",
        "threadId": thread_id
    }
)
```

### JavaScript
```javascript
const API_KEY = 'your_api_key';
const BASE_URL = 'http://00.000.00.000:5000/api/assistants';

const headers = {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
};

// Create a thread
fetch(`${BASE_URL}/threads`, {
    method: 'POST',
    headers
})
.then(response => response.json())
.then(data => {
    const threadId = data.thread_id;
    
    // Send a message
    return fetch(`${BASE_URL}/chat/message`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
            message: 'Hello, how can you help me?',
            threadId: threadId
        })
    });
})
.then(response => response.json())
.then(data => console.log(data));
```
