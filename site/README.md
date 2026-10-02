# Bits and Bytes lesson site

Next.js app that renders the markdown lessons in the repository `guide/` directory.

## Local development

```bash
cd site
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). Lesson files are read from `../guide` at build and request time.

## Deploy on Vercel

The repository root includes `vercel.json` with `"rootDirectory": "site"` so Vercel builds this app while still checking out the full repo (including `guide/`). No database or environment variables are required.
