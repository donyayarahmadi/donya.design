# Donya Portfolio (Static HTML)

This project is a static website ready to publish with GitHub Pages.

## Local structure

- `index.html`
- `content/` (all images used by the page)

## Publish on GitHub Pages

1. Create a new GitHub repository (public).
2. In this folder, run:

```bash
git init
git add .
git commit -m "Initial static HTML export"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

3. In GitHub, open repository settings:
   - **Settings -> Pages**
   - **Source**: `Deploy from a branch`
   - **Branch**: `main` and `/ (root)`
   - Save

Your site will be available at:
`https://<your-username>.github.io/<your-repo>/`

