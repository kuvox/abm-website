# Archived pages

Pages here are not deployed or linked from the live site. They are kept for possible reactivation later.

## Amazon Ads service page

**File:** `services/amazon-ads.html`

### Reactivation checklist

1. Move `amazon-ads.html` back to `services/` at the repo root.
2. Re-add the service entry to `schema/entities.json`:
   ```json
   {
     "slug": "amazon-ads",
     "name": "Amazon Ads",
     "description": "Amazon advertising optimized around ad spend efficiency and ACOS targets aligned to business goals."
   }
   ```
3. Re-add the `makesOffer` item in `index.html` (see `schema/jsonld.py` → `homepage_schema()` for reference):
   ```json
   {
     "@id": "https://abeckermarketing.com/services/amazon-ads.html#service"
   }
   ```
4. Re-add the URL to `sitemap.xml` and the bullet to `llms.txt`.
5. Restore the entry in `build_pages.py` if that generator is still in use.
