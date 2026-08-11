# Push TrainPlex DIP to GitHub

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Enter repository name: `trainplex-dip`
3. Choose visibility (Public/Private)
4. Don't initialize with README (we already have one)
5. Click "Create repository"

## Step 2: Push to GitHub

### If using HTTPS
```bash
cd /home/nakul/idp-enterprise
git remote add origin https://github.com/YOUR_USERNAME/trainplex-dip.git
git branch -M main
git push -u origin main
```

### If using SSH
```bash
cd /home/nakul/idp-enterprise
git remote add origin git@github.com:YOUR_USERNAME/trainplex-dip.git
git branch -M main
git push -u origin main
```

## Step 3: Verify

```bash
git log --oneline
git remote -v
```

## Alternative: Create Repository from CLI

Install GitHub CLI if not installed:
```bash
# Ubuntu/Debian
sudo apt install gh

# macOS
brew install gh

# Windows
choco install gh
```

Then run:
```bash
cd /home/nakul/idp-enterprise
gh auth login
gh repo create trainplex-dip --public --source=. --remote=origin
git push -u origin main
```

## Project Structure on GitHub

```
trainplex-dip/
├── src/                      # Source code
│   ├── core/                 # Core utilities
│   ├── ml/                   # ML & OCR
│   ├── services/             # Business logic
│   ├── workers/              # Background processing
│   ├── database/             # Database layer
│   ├── api/                  # REST API
│   ├── cli/                  # CLI interface
│   ├── integrations/         # External systems
│   ├── utils/                # Utility functions
│   └── models/               # Data models
├── tests/                    # Test suite
├── docs/                     # Documentation
├── config/                   # Configuration files
├── data/                     # Sample data
├── logs/                     # Log files
├── .gitignore
├── README.md                 # Main documentation
├── ARCHITECTURE.md          # Architecture guide
├── DEVELOPMENT.md           # Development guide
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── Dockerfile               # Docker configuration
└── docker-compose.yml       # Docker Compose
```

## Branch Strategy

```
main          → Production
develop       → Development
feature/*     → New features
bugfix/*      → Bug fixes
release/*     → Release preparation
```

## Environment Variables (Optional)

Create a `.env` file locally (NOT committed to Git):

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/trainplex_dip

# API Keys (for external services)
GOOGLE_API_KEY=your_google_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret

# Redis
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO
```
