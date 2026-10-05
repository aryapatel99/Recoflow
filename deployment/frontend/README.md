# Frontend image

The storefront is Next.js SSR, so it is deployed as a Node container rather
than as a static S3 website. Set `NEXT_PUBLIC_API_URL` to the public backend
origin before building the image:

```powershell
$env:NEXT_PUBLIC_API_URL = "https://api.example.com"
docker build -f deployment/frontend/Dockerfile -t recoflow-frontend:local .
```

The public API origin is baked into the Next.js build. Rebuild the image when
that origin changes.

