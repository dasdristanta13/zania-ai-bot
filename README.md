# QA Bot Project

This repository contains two implementations of a Question Answering (QA) Bot designed to extract information from PDF documents and answer user queries.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/dasdristanta13/zania-ai-bot.git
   cd zania-ai-bot
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt 
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   OPENAI_API_KEY=your_openai_api_key
   SLACK_BOT_TOKEN=your_slack_bot_token
   ```


## Use Cases

1. **Solution1**: A comprehensive QA system with advanced features
   - Located in: `/solution-1`
   - Key features: PDF extraction, text chunking, vectorization, question answering using GPT-3.5-turbo, result caching, and Slack integration
   - Output:
  ```{
  "What is the name of the company?": {
    "answer": "Zania, Inc.",
    "sources": [
      "Page 4",
      "Page 44",
      "Page 33",
      "Page 27",
      "Page 32"
    ]
  },
  "Who is the CEO of the company?": {
    "answer": "Shruti Gupta",
    "sources": [
      "Page 44"
    ]
  },
  "What is their vacation policy?": {
    "answer": "Vacation granted during your first year of employment will be prorated based on your hire date.",
    "sources": [
      "Page 24"
    ]
  },
  "What is the termination policy?": {
    "answer": "The termination policy is that employees are requested to provide a minimum of two weeks' notice of resignation, with managers requested to provide a minimum of four weeks' notice. Failure to provide the requested notice may result in the employee being deemed ineligible for rehire, depending on the circumstances.",
    "sources": [
      "Page 14",
      "Page 1",
      "Page 12"
    ]
  }
}
```

2. **Solution2**: An enhanced QA system with additional capabilities
   - Located in: `/solution-2`
   - Key features: Hybrid retrieval (dense and sparse), contextual compression, section-aware responses, and robust error handling
   - Output:
```   {
  "What is the name of the company?": {
    "answer": "The name of the company is Zania, Inc. (Section 2.0)",
    "sources": [
      "Section 2.0, Page 4",
      "Section N/A, Page 33",
      "Section 9.2, Page 27",
      "Section N/A, Page 32"
    ]
  },
  "Who is the CEO of the company?": {
    "answer": "Shruti Gupta is the CEO of Zania, Inc.",
    "sources": [
      "Section N/A, Page 44",
      "Section N/A, Page 9"
    ]
  },
  "What is their vacation policy?": {
    "answer": "Vacation granted during the first year of employment will be prorated based on the hire date.",
    "sources": [
      "Section N/A, Page 24"
    ]
  },
  "What is the termination policy?": {
    "answer": "The termination policy is not explicitly stated in the provided context. Data Not Available.",
    "sources": [
      "Section 6.4, Page 14",
      "Section 1.0, Page 1",
      "Section 5.11, Page 12"
    ]
  }
}
```

## Key Differences

- **Retrieval Method**: Solution1 uses vector-based retrieval, while Solution2 implements a hybrid approach combining dense and sparse retrieval methods.
- **Context Processing**: Solution2 adds contextual compression to refine retrieved information before answer generation.
- **Architecture**: Solution2 has a more modular architecture with separate components for different functionalities.
- **Error Handling**: Solution2 emphasizes robust error handling and logging throughout the system.

Choose the solution that best fits your specific requirements and level of complexity needed.
