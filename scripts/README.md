# Scripts

## optimize-images.py

Free local image optimization using ImageMagick `magick` and `cwebp`.

```bash
npm run optimize:images -- assets/raw public/images
npm run optimize:images -- assets/raw public/images -- --max-width 1600 --quality 78
```

Behavior:

- jpg/jpeg/png/webp: auto-orient, strip metadata, resize down to `--max-width`, compress
- jpg/jpeg/png: also creates a `.webp` sibling
- svg/gif/avif: copied unchanged
- unknown file types: skipped and listed

Security/privacy rule: never run this on private client/customer photos unless the project scope explicitly allows those files to be processed and committed. Optimized public assets may be committed; raw private sources should stay out of git.
