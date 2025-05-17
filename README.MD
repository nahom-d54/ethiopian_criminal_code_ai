# Ethiopian Criminal Code Legal Assistance

#### [🔗 DEMO URL](https://ai.astu.pro.et/)

## Group Members

| No  | Name           | ID No.       |
| --- | -------------- | ------------ |
| 1.  | Helen Benti    | Ugr/25417/14 |
| 2.  | Helena Beruke  | Ugr/26430/13 |
| 3.  | Nahom Dereje   | Ugr/26395/14 |
| 4.  | Tsion Ketema   | Ugr/26087/14 |
| 5.  | Abel Alemayehu | Ugr/25383/14 |

This project provides a legal assistance platform for the Ethiopian Criminal Code. It includes a backend API for indexing and searching legal documents using FAISS, a frontend built with React and Vite, and tools for training and embedding legal text data.

## Project Structure

```
.
├── alembic/                # Database migrations
├── frontend/               # Frontend application
├── seeder/                 # Data seeding scripts
├── src/                    # Backend source code
├── trainer/                # Training and embedding scripts
├── main.py                 # Backend entry point
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── README.MD               # Project documentation
```

### Key Components

#### Backend

- **Framework**: Python with FastAPI
- **Database**: PostgreSQL with Alembic for migrations
- **Search Engine**: FAISS for efficient similarity search
- **Main File**: [`main.py`](main.py)

#### Frontend

- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **Entry Point**: [`frontend/src/App.tsx`](frontend/src/App.tsx)

#### Trainer

- **Embedding**: SentenceTransformer for text embeddings
- **Indexing**: FAISS for building and saving indices
- **Script**: [`trainer/embed_index.py`](trainer/embed_index.py)

## Setup Instructions

### Backend

1. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

2. Set up the database:

   - Configure the database URL in `alembic.ini` under `sqlalchemy.url`.
   - Run migrations:
     ```sh
     alembic upgrade head
     ```

3. Start the backend server:
   ```sh
   python main.py
   ```

### OR ForBackend alternative Using Docker

```sh
docker build -t aiapp .
# run the app give database url as env
docker run -d -p 8000:8000 -e DATABASE_URL=postgresql+asyncpg://...:5432/database aiapp
```

### Frontend

1. Navigate to the `frontend` directory:

   ```sh
   cd frontend
   ```

2. Install dependencies:

   ```sh
   npm install
   ```

3. Start the development server:
   ```sh
   npm run dev
   ```

### Trainer

1. Prepare your corpus file (JSON format).
2. Run the embedding and indexing script:
   ```sh
   python trainer/embed_index.py <corpus_file> <index_file> <metadata_file>
   ```

## Usage

- Access the frontend at `http://localhost:3000`.
- Use the backend API to query indexed legal documents.
- Train and update the FAISS index using the trainer scripts.

## Development

### Linting and Formatting

- Backend: Use `black` for formatting and `ruff` for linting.
- Frontend: ESLint with React and TypeScript plugins.

### Testing

- Backend: Use `pytest` for unit tests.
- Frontend: Use `vitest` for testing React components.

## Deployment

- Use the provided `Dockerfile` to containerize the application.
- Deploy the backend and frontend using your preferred cloud provider.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
