# Contributing to Neural Vault

Thank you for contributing to **Neural Vault** — the 100% offline, private RAG desktop application built as **Artifact 1** of the MasterDexter 8-Week AI Engineer Accelerator (2026 Cohort).

This document outlines the exact process for team members to pick issues, build features, create Pull Requests, and get their code merged.

## Getting Started

1. Fork the repository or clone it if you have access.
2. Clone your copy:
   ```bash
   git clone https://github.com/YOUR-USERNAME/neural-vault.git
   cd neural-vault
   ```
3. Set up the environment (Mac M1/M2/M3):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
4. Install dependencies with Metal acceleration:
   ```bash
   CMAKE_ARGS="-DGGML_METAL=on" pip install -U llama-cpp-python --no-cache-dir --force-reinstall
   pip install -r requirements.txt
   ```
5. Download the model (see README.md for detailed instructions).
6. Create a new branch before making any changes.

---

## Development Workflow

- `main` branch is protected and always stable.
- All development happens in **feature branches**.
- Never push directly to `main`.

---

## How to Pick and Work on an Issue

1. Go to the [Issues](https://github.com/hemansnation/neural-vault/issues) tab.
2. Choose an open issue (preferably labeled `good first issue` or `help wanted`).
3. Comment on the issue:  
   **"I would like to work on this issue. Assigning to myself."**
4. Wait for Himanshu to assign the issue to you.
5. Once assigned, proceed to create your branch.

---

## Working with Claude in VS Code (Recommended)

You can use **Claude (Claude.dev or Claude Code)** directly inside VS Code to help you build the feature faster and cleaner.

### How to use Claude in VS Code:

1. Open the project in VS Code.
2. Open the Claude extension (or Claude.dev sidebar).
3. Start a new chat with Claude and give clear, detailed prompts like:

   **Example Prompts you can copy-paste:**

   - "Implement the feature described in issue #42: Add support for multiple PDF uploads with proper error handling and progress indicators in app.py. Use existing code style."

   - "Refactor src/document_processor.py to improve chunking logic with better sentence boundary detection. Keep it simple and efficient."

   - "Add proper typing, docstrings, and error handling to the VectorStore class in src/vector_store.py."

   - "Write unit tests for the RAGPipeline.query method."

4. After Claude generates code:
   - Review the code carefully.
   - Test it locally by running `streamlit run app.py`.
   - Make improvements if needed.
   - Ask Claude follow-up questions in the same chat for fixes.

**Tip:** Always mention "Follow the existing code style and structure" in your prompts.

---

## Commit Guidelines (Step-by-Step)

Follow these steps **exactly** for every commit:

### Step 1: Create a Feature Branch
```bash
git checkout main
git pull origin main
git checkout -b feature/issue-42-add-pdf-metadata
```

**Branch naming convention:**
- `feature/issue-XXX-short-description`
- `fix/issue-XXX-description`
- `docs/issue-XXX-description`
- `refactor/issue-XXX-description`

### Step 2: Make Your Changes
- Work only on the assigned issue.
- Keep changes focused and minimal.
- Use Claude in VS Code to help write clean code.

### Step 3: Test Locally
```bash
streamlit run app.py
```
- Upload PDFs
- Test queries
- Ensure no errors in terminal
- Response should stream properly

### Step 4: Commit Your Changes (Very Important)

Use **Conventional Commits** format:

```bash
git add .
git commit -m "type(scope): short meaningful description

Detailed explanation of changes made.
- What was added/fixed
- Why it was needed
- Any important technical decisions

Closes #42"
```

**Allowed types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `refactor`: Code changes that neither fix a bug nor add a feature
- `style`: Formatting changes
- `test`: Adding tests
- `chore`: Maintenance tasks

**Good Commit Examples:**
- `feat(document-processor): add metadata support for uploaded PDFs`
- `fix(llm-engine): handle model not found error gracefully`
- `docs(readme): update model download section`

**Bad Examples (Never Use):**
- "fixed code"
- "update"
- "changes"

### Step 5: Push the Branch
```bash
git push origin feature/issue-42-add-pdf-metadata
```

---

## Pull Request Process

1. Go to your GitHub fork.
2. Click **"Compare & pull request"**.
3. Use the following PR Title format (same as commit):
   `feat(vector-store): add support for document metadata`

4. In the PR description, include:
   - Link to the issue (`Closes #42`)
   - Clear description of what you changed
   - How you tested it
   - Any screenshots or demo (strongly recommended)
   - Mention if you used Claude for assistance

5. Assign the PR to **@hemansnation**
6. Add label `ready-for-review`

Himanshu will review your PR and either merge it or request changes with clear feedback.

---

## After Your PR Gets Merged

1. Switch back to main:
   ```bash
   git checkout main
   git pull origin main
   ```
2. Delete your feature branch:
   ```bash
   git branch -d feature/issue-42-add-pdf-metadata
   git push origin --delete feature/issue-42-add-pdf-metadata
   ```
3. Pick the next issue and repeat!

---

## Final Notes

- Quality over quantity. One clean, well-tested PR is better than multiple sloppy ones.
- If you're stuck, comment on the issue or ask in the Accelerator group.
- Using Claude in VS Code is encouraged, but **you must understand** the code before committing.

Happy building!  
Your contributions will become part of your production-grade AI portfolio.

— Himanshu Ramchandani  
Microsoft MVP | Creator, MasterDexter AI Engineer Accelerator
```

**This is the complete, ready-to-use `CONTRIBUTING.md` file.**

Just create the file in your project root and paste the entire content above.  
It includes everything you asked for: detailed commit steps, PR process, and specific instructions on using Claude in VS Code with example prompts.