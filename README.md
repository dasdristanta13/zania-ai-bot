# QA Bot Project

This repository contains two implementations of a Question Answering (QA) Bot designed to extract information from PDF documents and answer user queries.

## Use Cases

1. **Solution1**: A comprehensive QA system with advanced features
   - Located in: `/solution-1`
   - Key features: PDF extraction, text chunking, vectorization, question answering using GPT-3.5-turbo, result caching, and Slack integration

2. **Solution2**: An enhanced QA system with additional capabilities
   - Located in: `/solution-2`
   - Key features: Hybrid retrieval (dense and sparse), contextual compression, section-aware responses, and robust error handling

## Key Differences

- **Retrieval Method**: Solution1 uses vector-based retrieval, while Solution2 implements a hybrid approach combining dense and sparse retrieval methods.
- **Context Processing**: Solution2 adds contextual compression to refine retrieved information before answer generation.
- **Architecture**: Solution2 has a more modular architecture with separate components for different functionalities.
- **Error Handling**: Solution2 emphasizes robust error handling and logging throughout the system.

Choose the solution that best fits your specific requirements and level of complexity needed.
