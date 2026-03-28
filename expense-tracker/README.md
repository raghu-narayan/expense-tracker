# Family Expense Tracker

A simple web-based expense tracker for families. Built with Python Flask and SQLite.

## Features

- Add, edit, and delete expenses
- Track expenses by category (Food, Transportation, Housing, Utilities, Entertainment, Healthcare, Education, Shopping, Other)
- Assign expenses to family members
- Filter expenses by category, family member, and date range
- Summary view with total spending and breakdowns by category and family member

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and go to:
```
http://localhost:5000
```

## File Structure

```
expense-tracker/
├── api/
│   └── index.py        # Vercel serverless entry point
├── .github/
│   └── workflows/
│       └── deploy.yml  # Auto-deploy on push
├── templates/
│   └── index.html      # Single-page frontend
├── app.py              # Local Flask server
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel config
└── README.md
```

## Deploy to Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy:
```bash
vercel
```

Or deploy directly from GitHub:
1. Push this code to a GitHub repository
2. Connect the repo to Vercel dashboard
3. Select Python runtime
4. Deploy

**Note**: On Vercel's serverless platform, data is stored in `/tmp/expenses.db` which is ephemeral. Data will reset on each deployment and may not persist between requests. For production use, consider upgrading to a persistent database like Vercel KV, PlanetScale, or Supabase.

## Automatic Deployment Setup

This project includes GitHub Actions for automatic deployment to Vercel.

### Setup Steps:

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/expense-tracker.git
git push -u origin main
```

2. **Get Vercel Credentials:**
```bash
npm i -g vercel
vercel login
vercel link
```

3. **Get your tokens:**
```bash
cat .vercel/project.json    # Shows: orgId and projectId
vercel tokens create       # Creates: VERCEL_TOKEN
```

4. **Add GitHub Secrets:**
Go to GitHub repo → Settings → Secrets and variables → Actions → New repository secret:

| Secret Name | Value |
|-------------|-------|
| `VERCEL_TOKEN` | From step 3 |
| `VERCEL_ORG_ID` | From `project.json` |
| `VERCEL_PROJECT_ID` | From `project.json` |

5. **Done!** Now every push to `main` branch will automatically deploy to Vercel.

## Usage

1. **Add an Expense**: Fill in the form with amount, category, date, and family member
2. **View Expenses**: See all expenses in a table with filtering options
3. **Edit/Delete**: Use the buttons in the Actions column
4. **Summary**: Switch to the Summary tab to see spending breakdowns