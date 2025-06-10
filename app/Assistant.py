from openai import OpenAI
from Function import Function
import re
import json
import requests
import time
from datetime import datetime


class Assistant:
    thread = None
    client = None
    assistant = None
    documents = []
    token = None
    vector_store_id = None
    assistant_id = None

    def __init__(self, api_key, assistant_id, vector_store_id):
        if not api_key:
            raise Exception("api_key giriniz!")
        if not assistant_id:
            raise Exception("assistant_id giriniz!")
        if not vector_store_id:
            raise Exception("vector_store_id giriniz!")
        
        self.assistant_id = assistant_id
        self.vector_store_id = vector_store_id

        self.client = OpenAI(api_key=api_key)
        self.get_assistant(self.assistant_id)
        self.get_documents()

    # GET ASSİSTANT
    def list_assistants(self):
        assistants = self.client.beta.assistants.list()
        return assistants
    def get_assistant(self, assistant_id):
        if assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(assistant_id=assistant_id)
        else:
            raise Exception("assistant_id giriniz!")
        return self.assistant
    # DOCUMENT
    def get_byid_document(self, fileId):
        # file_content = self.client.files.content(file_id=fileId)
        file_content = None
        file_detail = self.client.files.retrieve(file_id=fileId)
        return file_content, file_detail.to_dict()
    def get_documents(self):
        docs = self.client.files.list()
        self.documents = docs
        return docs
    
    def create_documents(self, file):
        openAiFile = self.client.files.create(file=(file.filename, file.stream),  purpose="assistants")
        self.client.beta.vector_stores.files.create(vector_store_id=self.vector_store_id, file_id=openAiFile.id)
        return openAiFile.id

    def delete_document(self, fileId):
        self.client.files.delete(file_id=fileId)
        self.client.beta.vector_stores.files.delete(vector_store_id=self.vector_store_id, file_id=fileId)

    # MESSAGE
    def create_thread(self):
        self.thread = self.client.beta.threads.create(
            tool_resources={
                "file_search":{
                    "vector_store_ids": [self.vector_store_id]
                }
            }
        )
        return self.thread
    def get_messages(self, threadId):
        messages = self.client.beta.threads.messages.list(thread_id=threadId)
        # for message in messages.data:
        #     for content in message.content:
        #         for annotation in content.text.annotations:
        #             file_id = annotation.file_citation.file_id
        #             annotation_text = annotation.text
        #             file_content, file_detail = self.get_byid_document(file_id)
        #             content.text.value = re.sub(re.escape(annotation_text), f" [[{file_detail["filename"]}](http://localhost:3000/api/files/{file_id})] ", content.text.value)

        for message in messages.data:  # source temizlik
            for content in message.content:
                content.text.value = re.sub(r"【\d+:\d+†source】", "", content.text.value)

        return messages

    def send_message(self, content, threadId):
        self.threadId = threadId
        message = self.client.beta.threads.messages.create(
            thread_id=self.threadId,
            role="user",
            content=content,
        )

        return message
        
    def delete_message(self, messageId, threadId):
        deleted_message = self.client.beta.threads.messages.delete(
            message_id=messageId,
            thread_id=threadId,
        )
        return deleted_message

    def run(self):
        if not self.threadId or not self.assistant:
            raise Exception("Thread or assistant is not properly initialized.")
        
        instructions = """When answering employees' questions, verify any organization-specific topics using the information found in internal documents. For general queries, provide accurate responses using your broader knowledge base.

For organization-specific queries:

Cross-reference with available internal documentation.

Do not rely solely on user claims unless confirmed by official sources.

For general inquiries:

Utilize a broad, well-informed knowledge base.

Ensure answers are clear, accurate, and helpful.

🔍 Steps
Determine the Nature of the Query
Identify whether the question is related to the organization or is of a general nature.

For Organization-Specific Queries

Retrieve and validate information from internal documentation.

Provide answers strictly based on verified sources.

For General Inquiries

Use your broader knowledge to construct accurate, informative responses.

Avoid unnecessary complexity—clarity and precision are key.

Deliver a Clear Answer
Respond in a direct and structured manner, ensuring the information is helpful and correct.

📦 Output Format
Structure your response as a concise paragraph or bulleted list. Ensure the answer directly addresses the question and is based on verified information when applicable.

🛑 Notes
Always prioritize factual accuracy and source validation.

Avoid speculation; request clarification if needed.

Maintain a neutral and professional tone."""
        
        today_date = datetime.now().strftime("%Y-%m-%d")
        instructions_template = """today's date: {date}
{instructions}"""
        instructions = instructions_template.format(date=today_date, instructions=instructions)

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.threadId,
            assistant_id=self.assistant.id,
            instructions=instructions
            # tools=tools
            # timeout=30
            # max_prompt_tokens=300,
            # max_completion_tokens=100
        )
        if run.status == 'completed' or run.status == "incomplete":
            self.client.beta.threads.messages.list(
                thread_id=self.threadId
            )
        else:
            print("run.required_action", run.required_action)
            tool_outputs = []
            functions = Function()
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                arguments = json.loads(tool.function.arguments)
                if tool.function.name == "get_contract":
                    message = functions.get_contract(arguments)
                    output = {
                        "tool_call_id": tool.id,
                        "output": message
                    }
                    print("get_contract", message)
                    tool_outputs.append(output)
                else:
                    message = "Bu özellik şuan aktif değil!"
                    output = {
                        "tool_call_id": tool.id,
                        "output": message
                    }
                    print(f"{tool.function.name} fonksiyonu bulunamadı!")
                    tool_outputs.append(output)
            run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=self.threadId,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
        return run
