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

In the Vercel project settings, set the **Root Directory** to `site`. Vercel still checks out the repository root, so this app can read the sibling `guide/` directory at build time. The root `vercel.json` selects the Next.js framework and build commands; it does not configure the project root directory. No database or environment variables are required.
