# Fresh Vercel Deployment Guide

## Steps to Redeploy Website on Vercel

### 1. Delete Current Vercel Project
- Go to https://vercel.com/dashboard
- Find your `social-dots-new` project
- Go to Settings > General > Advanced
- Click "Delete Project"
- Confirm deletion

### 2. Create New Vercel Project
- Go to https://vercel.com/dashboard
- Click "Add New" > "Project"  
- Import your GitHub repository: `Social-Dots/social-dots-new`
- Configure settings:
  - **Framework Preset**: Other
  - **Build Command**: Leave empty
  - **Output Directory**: Leave empty
  - **Install Command**: `pip install -r requirements.txt`

### 3. Environment Variables (CRITICAL!)
Add these environment variables in Vercel dashboard:

```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=*.vercel.app,socialdots.ca
DATABASE_URL=sqlite:///db.sqlite3
DJANGO_SETTINGS_MODULE=socialdots.settings
```

### 4. Deploy
- Click "Deploy"
- Wait for deployment to complete
- Your site should be live with all localhost data!

## What's Included in This Deployment:

✅ **Complete localhost database** - All your blog posts, projects, services
✅ **Blog formatting JavaScript** - Articles will have proper styling  
✅ **Automatic data loading** - Fresh deployment loads your current data
✅ **All templates and styling** - Matches your localhost exactly

## Files Ready for Deployment:

- `vercel_app.py` - Loads complete localhost data automatically
- `complete_localhost_data.json` - Your complete database export
- `blog_detail.html` - Has bulletproof blog formatting JavaScript
- `requirements.txt` - All dependencies included
- `vercel.json` - Proper Vercel configuration

## After Deployment:

1. **Test the homepage** - Should load properly
2. **Test blog articles** - Click "Read Full Article" to see formatting
3. **Check all pages** - Services, Projects, Contact should work

The blog articles will automatically have:
- Blue gradient backgrounds on H1/H2 headings
- Orange gradient backgrounds on H3 headings  
- Light orange backgrounds on paragraphs
- Green backgrounds on lists

## If Issues Occur:

1. Check Vercel Function logs in dashboard
2. Verify all environment variables are set
3. Make sure GitHub repository is up to date
4. Try redeploying from dashboard

Your localhost website will be exactly replicated on Vercel!