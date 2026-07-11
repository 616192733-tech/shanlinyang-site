# Shanlinyang Apparel Website

Static marketing and product website for [shanlinyang.com](https://www.shanlinyang.com/), deployed automatically to Vercel from the `main` branch.

## Structure

- `index.html` — homepage
- `products/` — product category pages
- `blog/` — buyer and sourcing guides
- `img/` — image assets
- `fonts/` — self-hosted fonts
- `css/` — shared styles
- `contact.html` — inquiry form
- `sitemap.xml` — search engine sitemap
- `robots.txt` — crawler policy
- `llms.txt` — concise AI assistant reference
- `vercel.json` — deployment, caching, rewrite, and security-header configuration

## Publishing

1. Create a branch from `main`.
2. Make and review changes on the branch.
3. Confirm canonical URLs, internal links, metadata, and structured data.
4. Open a pull request.
5. Merge after the Vercel preview is verified.
6. Confirm the production deployment is `READY`.

Latest production publish trigger: 2026-07-11 SEO/AEO regional and conversion optimization.

## SEO Quality Checklist

Before publishing a new page:

- Give it a unique title, description, canonical URL, and primary heading.
- Add useful original information, examples, evidence, or buyer guidance.
- Link it from at least one relevant product, guide, or navigation page.
- Add it to `sitemap.xml` with an accurate modification date.
- Use descriptive image alternative text and optimized image dimensions.
- Validate structured data and avoid duplicate schema blocks.
- Check the mobile layout and inquiry calls to action.

## Content Guidelines

- Prioritize buyer usefulness over keyword volume.
- Do not create country pages by only replacing the country name.
- Regional pages should include relevant sizing, shipping, customs, lead-time, and buyer information.
- Keep company claims, contact details, MOQ, pricing, and lead times consistent across pages.
- Review time-sensitive articles and dates regularly.

## Contact and Conversion Checks

After changes to `contact.html`, test:

- Form submission
- WhatsApp links
- Email links
- Required-field validation
- Mobile keyboard and layout behavior
- Thank-you or error response

## Deployment

Vercel project: `shanlinyang-site`

Production domains:

- `www.shanlinyang.com`
- `shanlinyang.com`
- `shanlinyang-site.vercel.app`
