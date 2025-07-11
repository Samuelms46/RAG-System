# RAG System

A Retrieval-Augmented Generation (RAG) system built during the AFTA bootcamp, featuring a Streamlit UI and ChromaDB for vector embeddings storage. This system enables intelligent document retrieval and question-answering capabilities.

## 🚀 Features

- **Document Processing**: Text preprocessing and tokenization
- **Vector Embeddings**: Generate and store embeddings using ChromaDB
- **Similarity Search**: Efficient document retrieval based on semantic similarity
- **Interactive UI**: Streamlit-based web interface for easy interaction
- **RAG Pipeline**: Complete retrieval-augmented generation workflow
- **Multiple Model Support**: Compatible with various embedding and language models
- **Real-time Chat**: Conversational interface with context-aware responses

## 📋 Requirements

- Python 3.8+
- Streamlit
- ChromaDB
- LangChain

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/Samuelms46/RAG-System.git
cd RAG-System

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Quick Start

### Running the Application

```bash
# Start the Streamlit application
streamlit run Frontend/page.py
```

### Basic Usage

1. **Upload Documents**: Add your documents to the system for processing
2. **Ask Questions**: Use the chat interface to ask questions about your documents
3. **Get Answers**: Receive contextually relevant answers based on document content

## 📁 Project Structure

```
RAG-System/
├── Frontend/
│   └── page.py              # Streamlit UI and main application logic
├── data/                # Document storage and processed data
├── rag_pipeline.ipynb/      # Jupyter notebook for experimentation
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## 🔧 Core Components

### 1. Document Retrieval System

The system uses ChromaDB to store and retrieve relevant documents:

```python
def get_relevant_docs(query):
    # Retrieves semantically similar documents
    # Returns top-5 most relevant documents
```

### 2. Response Generation

Combines retrieved documents with user queries to generate contextual responses:

```python
def generate_response(msg: str):
    relevant_docs = get_relevant_docs(HumanMessage(content=msg))
    combined_sys_message = f"""{system_message.content}

Use the following documents to answer the question:
{"\n".join(doc.page_content for doc in relevant_docs)}"""
    
    messages = [SystemMessage(content=combined_sys_message)] + st.session_state.messages
    response = llm.invoke(messages)
    return response
```

### 3. Streamlit Interface

- Interactive chat interface
- Document upload functionality
- Real-time response generation
- Session state management

## 🎯 Usage Examples

### Basic Question Answering

1. Start the application
2. Upload your documents or ensure they're in the data directory
3. Ask questions in natural language
4. Receive answers based on document content

### Advanced Features

- **Context Preservation**: Maintains conversation history
- **Multi-document Support**: Queries across multiple documents
- **Semantic Search**: Finds relevant information even with different wording

## 🔧 Configuration

### Environment Setup

Create a `.env` file for configuration:

```env
# Model configurations
EMBEDDING_MODEL=your-embedding-model
LLM_MODEL=your-language-model

# ChromaDB settings
CHROMA_DB_PATH=./chroma_db
```

### Customizing Models

Modify the model configurations in your main application file to use different:
- Embedding models (e.g., sentence-transformers, OpenAI embeddings)
- Language models (e.g., GPT, Claude, local models)

## 📊 Performance

- **Vector Storage**: Efficient similarity search with ChromaDB
- **Response Time**: Optimized for real-time interactions
- **Scalability**: Handles large document collections

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- AFTA Bootcamp for the learning opportunity
- ChromaDB for vector storage capabilities
- Streamlit for the intuitive UI framework
- LangChain for RAG pipeline components
- EON Reality White paper used in this project

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This RAG system was developed as part of the AFTA bootcamp curriculum and demonstrates practical implementation of retrieval-augmented generation techniques.
