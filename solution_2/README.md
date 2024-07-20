# QA Bot: Intelligent Question Answering System

## Table of Contents
1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Key Components](#key-components)
4. [Workflow](#workflow)
5. [Advanced Features](#advanced-features)
6. [Setup and Usage](#setup-and-usage)
7. [Error Handling and Logging](#error-handling-and-logging)
8. [Customization and Extension](#customization-and-extension)

## Introduction

The QA Bot is an advanced question-answering system designed to extract information from PDF documents and provide accurate answers to user queries. It utilizes state-of-the-art natural language processing techniques, including hybrid retrieval methods and contextual compression, to deliver high-quality responses.

## System Architecture

The system is composed of several interconnected components, each responsible for a specific part of the question-answering process:

1. PDF Extractor
2. Vector Store
3. Chain Manager
4. Cache Manager
5. Slack Integration

## Key Components

### 1. PDF Extractor (`pdf_extractor.py`)

The PDF Extractor is responsible for processing the input PDF document and preparing it for analysis. Key features include:

- **Text Extraction**: Uses PyPDFLoader to extract text from PDF files.
- **Text Chunking**: Implements RecursiveCharacterTextSplitter to break the text into manageable chunks.
- **Section Extraction**: Identifies section numbers (e.g., 1.0, 1.1) within the text to provide context.
- **Deduplication**: Removes duplicate text chunks to improve efficiency.
- **Vector Store Creation**: Generates embeddings for text chunks using OpenAI's embeddings and stores them in a Chroma vector store.

### 2. Chain Manager (`chain.py`)

The Chain Manager orchestrates the question-answering process. It includes:

- **Advanced Chain Creation**: Sets up a sophisticated retrieval and answering pipeline.
- **Hybrid Retrieval**: Combines dense (vector-based) and sparse (BM25) retrieval methods for improved accuracy.
- **Contextual Compression**: Applies LLM-based compression to focus on the most relevant information.
- **Custom Prompts**: Utilizes carefully crafted prompts to guide the language model's responses.

### 3. Cache Manager (`cache_manager.py`)

The Cache Manager improves efficiency by storing and retrieving previously answered questions:

- **SQLite Database**: Uses a local SQLite database to store question-answer pairs.
- **Caching Logic**: Implements methods to store and retrieve cached answers.

### 4. Slack Integration (`slack_post.py`)

Enables the bot to post results directly to a Slack channel:

- **Message Formatting**: Prepares results in a Slack-friendly format.
- **API Integration**: Uses Slack's API to post messages to a specified channel.

## Workflow

1. **PDF Processing**:
   - The system loads a PDF document and extracts its text.
   - The text is split into chunks, with section numbers identified.
   - Duplicate chunks are removed.
   - A vector store is created from the unique chunks.

2. **Question Processing**:
   - For each question, the system first checks the cache for an existing answer.
   - If not found in the cache, it proceeds with the retrieval and answering process.

3. **Retrieval**:
   - The system uses a hybrid approach, combining:
     a) Dense retrieval: Uses the vector store to find semantically similar text chunks.
     b) Sparse retrieval: Applies BM25 algorithm for keyword-based matching.
   - The results from both methods are combined using an ensemble approach.

4. **Contextual Compression**:
   - Retrieved documents are passed through an LLM-based extractor to focus on the most relevant parts.

5. **Answer Generation**:
   - The compressed, relevant text is passed to the language model along with carefully crafted prompts.
   - The model generates an answer based on the provided context.

6. **Result Handling**:
   - The answer is cached for future use.
   - Results are formatted and can be posted to a Slack channel.

## Advanced Features

1. **Hybrid Retrieval**: Combines dense and sparse retrieval methods for more comprehensive information retrieval.
2. **Contextual Compression**: Uses an LLM to extract the most relevant parts of retrieved documents, improving answer quality.
3. **Section-aware Responses**: Includes section numbers in responses when available, providing additional context.
4. **Caching**: Improves efficiency by storing and retrieving previously answered questions.
5. **Robust Error Handling**: Implements comprehensive error checking and logging throughout the system.

## Setup and Usage

1. Install required dependencies (list them in a requirements.txt file).
2. Set up environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `SLACK_BOT_TOKEN`: Your Slack bot token (if using Slack integration)
3. Prepare your PDF document and place it in the `data/` directory.
4. Run the main script: `python main.py`

## Error Handling and Logging

The system implements robust error handling and logging throughout:

- Each major component (PDF Extractor, Chain Manager, etc.) includes try-except blocks to catch and log errors.
- Logged information includes warnings for unexpected input types and errors for processing failures.
- The main script includes checks at each stage of processing to ensure data integrity.

## Customization and Extension

- **PDF Processing**: Modify the `PDFExtractor` class to handle different document structures or extract additional metadata.
- **Retrieval Methods**: Adjust the weights of dense and sparse retrievers in the `ChainManager` class.
- **Prompts**: Customize the prompt templates in the `ChainManager` class to tailor the system's responses.
- **Caching**: Modify the `CacheManager` class to implement different caching strategies or storage methods.
- **Output**: Extend the system to support additional output methods beyond Slack (e.g., email, API endpoints).

By leveraging these components and features, the QA Bot provides a powerful and flexible system for extracting and presenting information from PDF documents.
