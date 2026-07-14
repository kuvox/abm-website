"""HTML bodies for gated Notion-derived resource posts and guides."""

from __future__ import annotations


def _img(slug: str, filename: str, alt: str) -> str:
    return (
        f'<figure class="guide-figure">'
        f'<img src="../images/resources/{slug}/{filename}" alt="{alt}" loading="lazy">'
        f"</figure>"
    )


# ---------- Fix Cart Data Errors ----------

CART_DATA_FAQS = [
    (
        "What stops Cart Data from reaching Google Ads?",
        "When item IDs in Google Merchant Center do not match item IDs received by the Google Ads tracking tag, conversions show Missing Cart Data errors.",
    ),
    (
        "What is Cart Data and why add it?",
        "Cart Data shows which Shopping ad products were clicked versus which products were actually purchased, including cross-sell revenue.",
    ),
    (
        "Why should you not change item IDs in Google Merchant Center?",
        "Changing an item ID makes Google treat the product as new and drops historic clicks and conversion data tied to the old ID.",
    ),
]

CART_DATA_PREVIEW = """    <p>Watch the tutorial in the hero video, then unlock the full step-by-step checklist below.</p>
    <p>When Google Ads shows <strong>Missing Cart Data</strong> on conversions, your Merchant Center product IDs and your site&rsquo;s tracking tag IDs don&rsquo;t match. This guide walks through why that happens and two ways to fix it without losing historic performance data.</p>

    <h2 id="the-problem">The Problem</h2>
    <details class="guide-details">
      <summary>What stops Cart Data reaching Google Ads?</summary>
      <p>When <strong>item IDs</strong> in Google Merchant Center (GMC) do not match <strong>item IDs</strong> received by the GTAG tag (Google Ads tracking tag), you&rsquo;ll see a warning like the below in Google Ads.</p>
""" + _img(
    "fix-cart-data-errors-google-ads",
    "missing-cart-data-error.png",
    "Google Ads Missing Cart Data error message",
) + """      <p>For example, if your GMC account uses this item ID format <code>shopify_US_123456789_123456789</code> but your GTAG sees <code>shopify_ZZ&hellip;</code>, Cart Data cannot match item IDs to Google Ads conversion events like purchases and add-to-carts.</p>
    </details>"""

CART_DATA_GATED = """    <details class="guide-details">
      <summary>What is &ldquo;Cart Data&rdquo; and why add it?</summary>
      <p>A user can click one item in Shopping Ads, then purchase a different item on your website. Cart Data allows Google (and you) to see which items were clicked versus which items were purchased.</p>
      <p>It&rsquo;s important to know when this is happening so you can optimize the shopping ad products that get the most clicks, knowing that those products lead to sales of other products on your site.</p>
    </details>
    <details class="guide-details">
      <summary>Why you should not change item IDs in GMC</summary>
      <p>When you change an item ID in Google Merchant Center, Google sees it as a completely different product even if the title, description, URL, etc. remain unchanged. Even capitalization changes (<code>shopify_US&hellip;</code> to <code>shopify_us&hellip;</code>) are considered a changed ID.</p>
      <p>When you change item IDs, GMC considers that a new item. All historic clicks and conversions data is lost (you can restore the old item ID to get the data back, but only if you saved the old item ID).</p>
    </details>

    <h2 id="the-solution">The Solution</h2>
    <p>There are two methods you can use. Option 1 is simpler and requires no maintenance when done. Option 1 is the right choice for most stores.</p>

    <h3 id="option-1">Option 1: change item IDs gradually</h3>
    <p>It&rsquo;s a bad idea to switch item IDs all at once. However, you can switch them slowly over time which reduces or eliminates the impact on Google Ads from changing item IDs.</p>
    <p>We use DataFeedWatch at my company. The same principle applies without it.</p>
    <details class="guide-details">
      <summary>Step-by-step implementation process</summary>
      <ul class="checklist">
        <li>Step 1: pause the channels you&rsquo;re working on</li>
        <li>Step 2: make a &ldquo;New ID&rdquo; master field in DFW (example: <code>shopify_ZZ&hellip;</code>) and &ldquo;Old ID&rdquo; master field (example: <code>shopify_US&hellip;</code>)</li>
        <li>Step 3: make the <em>use new item ID, if is in list</em> rule (see example screenshot below)
          <ul>
            <li>Sample G-Sheet for the &ldquo;if is in list&rdquo; DFW rule: <a href="https://docs.google.com/spreadsheets/d/1RuuDWkVGQaHDRycdmtnfv1EGovUG-CYBFm_zFoxOwM0/edit?gid=1836322950#gid=1836322950" target="_blank" rel="noopener">[Sample] Swap Item IDs</a></li>
          </ul>
        </li>
      </ul>
""" + _img(
    "fix-cart-data-errors-google-ads",
    "dfw-swap-item-id-rule.png",
    "DataFeedWatch swap item ID rule in channels section",
) + """      <ul class="checklist">
        <li>Step 4: download item IDs by revenue from last 90 days into your Swap Item IDs sheet</li>
        <li>Step 5: test deleting some item IDs from your Swap Item IDs sheet and preview results</li>
        <li>Step 6: enable the channel once you&rsquo;re done with Steps 1 to 5</li>
        <li>Step 7: start deleting old IDs out of the list on a weekly cadence</li>
        <li>Step 8: continue deleting more item IDs from the Swap Item IDs sheet till you&rsquo;re done</li>
      </ul>
      <blockquote><p>I recommend deleting ~10&ndash;15% of item IDs per week till you reach the last 20% items. For the last 20% (top sellers), delete fewer item IDs per week till done.</p></blockquote>
    </details>
    <details class="guide-details">
      <summary>11-week example timeline</summary>
      <ol>
        <li>1&ndash;15% of low-selling items switched to new item ID format</li>
        <li>16&ndash;30%</li>
        <li>30&ndash;45%</li>
        <li>45&ndash;60%</li>
        <li>60&ndash;75%</li>
        <li>75&ndash;80%</li>
        <li>80&ndash;85%</li>
        <li>85&ndash;90%</li>
        <li>90&ndash;95%</li>
        <li>95&ndash;98%</li>
        <li>98&ndash;100% &mdash; last top-selling items switched</li>
      </ol>
    </details>

    <h3 id="option-2">Option 2: send different item IDs in the Google Tag</h3>
    <p>This version is complicated and Elevar has already posted an excellent guide. See the <a href="https://docs.getelevar.com/docs/version-20-how-to-change-product-ids-from-sku-to-shopify-ids-to-match-merchant-center-products" target="_blank" rel="noopener">Elevar guide</a>. You must maintain those tags going forward. Option 1 is the best choice for most people.</p>

    <h2 id="cross-sell-reports">How to read cross-sell reports in Google Ads</h2>
    <p>Cross-sell reports take time to understand. Here&rsquo;s how to read the &ldquo;Products &ndash; Cart Item&rdquo; report.</p>
    <ul>
      <li><strong>Product ad:</strong> the item in shopping ad results that was clicked.</li>
      <li><strong>Revenue column:</strong> total sales attributed to a click on the product ad.</li>
      <li><strong>Lead revenue column:</strong> revenue when the <em>same product</em> was purchased.</li>
      <li><strong>Cross-sell revenue column:</strong> revenue when a <em>different product</em> was purchased.</li>
    </ul>
""" + _img(
    "fix-cart-data-errors-google-ads",
    "products-cart-item-report.png",
    "Products Cart Item report showing lead and cross-sell revenue",
) + """
    <h2 id="sources-cited">Sources cited</h2>
    <ul>
      <li><a href="https://support.google.com/google-ads/answer/9028254" target="_blank" rel="noopener">About Conversions With Cart Data</a></li>
      <li><a href="https://support.google.com/google-ads/answer/9028614" target="_blank" rel="noopener">Set up and test reporting with conversions with cart data</a></li>
      <li><a href="https://docs.getelevar.com/docs/version-20-how-to-change-product-ids-from-sku-to-shopify-ids-to-match-merchant-center-products" target="_blank" rel="noopener">How to Change Product IDs from SKU to Shopify IDs (Elevar)</a></li>
    </ul>
    <p>Related: <a href="google-merchant-center-setup-2026.html">2026 Google Merchant Center Full Setup</a> &middot; <a href="../guides/conversion-tracking-shopify-2026.html">2026 Conversion Tracking Guide</a></p>"""


# ---------- GMC SFTP Upload ----------

SFTP_PREVIEW = """    <p>Upload pricing and inventory to Google Merchant Center multiple times per day using SFTP. Watch the tutorial in the hero video, then unlock the full checklist for Google and Microsoft Merchant Center.</p>

    <h2 id="know-before">Know Before Implementing</h2>
    <p>Using the FTP upload system for Merchant Center entails two important changes to how your feed works:</p>
    <ol>
      <li>When you apply a change to your feed in DataFeedWatch (DFW), those changes immediately process and send to Merchant Center. <strong>You will not have a chance to review changes before the updated feed data is sent unless you &ldquo;Pause&rdquo; the DFW channel first.</strong></li>
      <li>You can add multiple daily feed updates to align with your internal product update schedule. For example, if you update shop product data at 8:00 am and 4:00 pm, set DFW to download at 9:00 am and 5:00 pm.</li>
    </ol>"""

SFTP_GATED = """""" + _img(
    "google-merchant-center-sftp-upload",
    "dfw-multiple-daily-updates.png",
    "DataFeedWatch multiple daily updates schedule",
) + """
    <h3 id="important-terms">Important Terms</h3>
    <ul>
      <li><strong>Sending data source:</strong> in the video, the sending source is the DataFeedWatch Google Ads Channel.</li>
      <li><strong>SFTP:</strong> Secure File Transfer Protocol &mdash; used to send data to Google Merchant Center.</li>
    </ul>

    <h2 id="google-merchant-center">Google Merchant Center</h2>
    <p>See Microsoft instructions below.</p>
    <h3 id="gmc-steps">Steps</h3>
    <ul class="checklist">
      <li>Go to <a href="https://merchants.google.com" target="_blank" rel="noopener">merchants.google.com</a> &rarr; Gear Icon &rarr; Data Sources &rarr; &ldquo;Add product source&rdquo; &rarr; Add products from a file</li>
      <li>Select &ldquo;Add a file use SFTP or Google Cloud Storage&rdquo;</li>
    </ul>
    <details class="guide-details">
      <summary>Where to view and record username, port, and password</summary>
""" + _img(
    "google-merchant-center-sftp-upload",
    "gmc-add-file-sftp.png",
    "Google Merchant Center add file via SFTP",
) + """
      <p>When you click View SFTP and Google Cloud Storage Details, write down:</p>
      <pre><code>Server partnerupload.google.com
Port 19321
Username mc-sftp-XXXXXXXX
Password (mix of numbers, letters, symbols)
Exact File Name: your-feed.xml</code></pre>
      <p>You can reset the password anytime, but you must update it in your sending data source or uploads will stop.</p>
""" + _img(
    "google-merchant-center-sftp-upload",
    "gmc-sftp-details.png",
    "Google Merchant Center SFTP connection details",
) + """    </details>
    <p>Add your username, password, port, etc. into your sending data source. In DataFeedWatch, combine Server and Port like <code>partnerupload.google.com:19321</code>.</p>
""" + _img(
    "google-merchant-center-sftp-upload",
    "dfw-sftp-settings.png",
    "DataFeedWatch SFTP settings for Google Merchant Center",
) + """
    <h3 id="gmc-last-steps">Last Steps</h3>
    <ul class="checklist">
      <li>Data has been received by Google Merchant Center</li>
      <li>Product status is approved or &ldquo;pending initial review&rdquo;</li>
      <li>The latest Google SFTP password is in your sending data source</li>
    </ul>

    <h2 id="microsoft-merchant-center">Microsoft Merchant Center</h2>
    <h3 id="microsoft-steps">Steps</h3>
    <ul class="checklist">
      <li>Go to <a href="https://ui.ads.microsoft.com/" target="_blank" rel="noopener">Microsoft Advertising</a> &rarr; Merchant Center &rarr; your store &rarr; feed &rarr; &ldquo;Update feed&rdquo;</li>
      <li>Select &ldquo;Upload via FTP/SFTP&rdquo;</li>
      <li>Create a memorable filename</li>
    </ul>
""" + _img(
    "google-merchant-center-sftp-upload",
    "microsoft-feed-settings.png",
    "Microsoft Merchant Center update feed settings",
) + """
    <p>Click &ldquo;change the FTP/SFTP account settings&rdquo; and save:</p>
    <pre><code>File name: storeNameFeed.xml
SFTP Server name: sftp.ads.microsoft.com
SFTP Port: 19321
Username: (from Microsoft screen)
Password: (strong password)</code></pre>
""" + _img(
    "google-merchant-center-sftp-upload",
    "microsoft-sftp-details.png",
    "Microsoft Merchant Center SFTP account details",
) + """
    <p>In DataFeedWatch, under FTP Address select <code>sftp://</code> then enter <code>sftp.ads.microsoft.com:19321</code>, username, password, and filename. Click Update Channel.</p>
""" + _img(
    "google-merchant-center-sftp-upload",
    "dfw-microsoft-ftp-settings.png",
    "DataFeedWatch Microsoft SFTP settings",
) + """
    <p>Click the &ldquo;FTP Upload&rdquo; button in DataFeedWatch to send the feed.</p>
""" + _img(
    "google-merchant-center-sftp-upload",
    "dfw-ftp-upload-button.png",
    "DataFeedWatch FTP upload button",
) + """
    <h3 id="microsoft-last-steps">Last Steps</h3>
    <ul class="checklist">
      <li>Wait 2&ndash;3 minutes and check for your SFTP file name in the Merchant Center Feed summary</li>
      <li>Keep checking daily until items are approved for ads</li>
    </ul>
""" + _img(
    "google-merchant-center-sftp-upload",
    "microsoft-feed-summary.png",
    "Microsoft Merchant Center feed summary after SFTP upload",
) + """
    <h2 id="resources-cited">Resources Cited</h2>
    <ul>
      <li><a href="https://support.google.com/merchants/answer/13813117?hl=en" target="_blank" rel="noopener">Submit product data sources using SFTP (Google)</a></li>
      <li><a href="https://www.datafeedwatch.com/blog/google-merchant-center-ftp" target="_blank" rel="noopener">FTP Connections and Google Merchant Center (DataFeedWatch)</a></li>
    </ul>
    <p>Related: <a href="google-merchant-center-setup-2026.html">2026 Google Merchant Center Full Setup</a></p>"""


# ---------- GMC Full Setup ----------

GMC_SETUP_PREVIEW = """    <p>Complete checklist for sending optimized Shopify product data to Google Merchant Center in 2026 &mdash; without breaking historic sales data tied to existing product IDs. Watch the tutorial in the hero video.</p>

    <h2 id="before-you-begin">Before you begin</h2>
    <blockquote><p><strong>You will lose historical click and sales data by changing product IDs.</strong> If you have historic sales data, don&rsquo;t change product IDs. See the full YouTube guide to learn how to re-create existing product_ID formats.</p></blockquote>
    <ul class="checklist">
      <li>Make a note of an existing Google Merchant Center account&rsquo;s product_ID format</li>
      <li>If your GMC product_ID is another code (like PN2019), identify where it comes from: MPN, Barcode, or SKU</li>
      <li>Save a copy of the existing feed before sending a new feed</li>
    </ul>
    <p>Oftentimes the product_ID in GMC is <code>shopify_US</code> + product id + variant id. If you created your store in 2026, it&rsquo;s likely <code>shopify_ZZ</code>, not <code>shopify_US</code>.</p>"""

GMC_SETUP_GATED = """
    <h2 id="shopify-setup">Shopify Setup</h2>
    <ul class="checklist">
      <li>Install the <a href="https://apps.shopify.com/google" target="_blank" rel="noopener">Google &amp; YouTube Sales Channel</a> on Shopify</li>
      <li>Connect the Google &amp; YouTube sales channel to Google Merchant Center (requires Super Admin for Business Manager GMC accounts, or Admin for regular GMC)</li>
      <li>Turn <strong>Off</strong> Product sync settings if using DataFeedWatch &mdash; we&rsquo;ll add products via DFW</li>
      <li>Leave remaining settings under &ldquo;Your product feed settings&rdquo; unchanged in most cases</li>
    </ul>
    <details class="guide-details">
      <summary>How to enable products in sales channels (if not using DataFeedWatch)</summary>
""" + _img(
    "google-merchant-center-setup-2026",
    "shopify-sales-channel-toggle.png",
    "Enable products in Shopify sales channels details toggle",
) + """    </details>
""" + _img(
    "google-merchant-center-setup-2026",
    "google-youtube-channel-product-sync.png",
    "Google and YouTube channel product sync settings in Shopify",
) + """
    <h2 id="datafeedwatch-setup">DataFeedWatch Setup</h2>
    <p>Whether or not you use DataFeedWatch, we recommend a third-party product data feed management tool to optimize product data.</p>
    <ul class="checklist">
      <li>Install the DataFeedWatch app on Shopify (<a href="https://www.datafeedwatch.com/pricing?via=austin-youtube" target="_blank" rel="noopener">referral link</a> for extended trial)</li>
      <li>Review and edit Master Fields</li>
      <li>Create a channel for your sales channel &mdash; ensure product_IDs match existing product_IDs</li>
      <li>Review and optimize attributes per <a href="https://support.google.com/merchants/answer/7052112?hl=en" target="_blank" rel="noopener">Google&rsquo;s product data specification</a></li>
      <li>Apply exclusions (gift cards, shipping add-ons, etc.)</li>
      <li>Add product categories (Google and Meta require these)</li>
    </ul>

    <h2 id="submit-feeds">Submit product data feeds</h2>
    <p>Plan to be online for several hours after submitting a new feed so you can troubleshoot issues.</p>
    <ul class="checklist">
      <li>Delete any old feeds. If you previously connected the Google &amp; YouTube sales channel to GMC, delete the data source, then set Product sync to Manually sync your products</li>
      <li>Submit product data feeds by file upload or <a href="google-merchant-center-sftp-upload.html">SFTP upload</a> for intraday updates</li>
      <li>Confirm items are approved or pending (wait up to 5 business days if pending)</li>
    </ul>

    <h2 id="troubleshooting">Troubleshooting</h2>
    <p>Items could be rejected, or the entire account suspended. <a href="../contact.html">Reach out to us</a> or use the tips below.</p>
    <h3 id="rejected-items">What if items are rejected?</h3>
    <p>Check the &ldquo;Needs attention&rdquo; report. Misformatted attributes are often the culprit &mdash; e.g. <code>price = 99.95</code> should be <code>price = 99.95 USD</code>.</p>
    <h3 id="suspended-account">What if my GMC account is suspended?</h3>
    <p>Read Google&rsquo;s <a href="https://support.google.com/merchants/answer/6149970?hl=en" target="_blank" rel="noopener">Shopping ads policies</a> carefully. Remove trigger words from descriptions (e.g. mentioning a banned substance even to say a product does <em>not</em> contain it).</p>
    <h3 id="health-disapprovals">Health-related disapprovals</h3>
    <ul>
      <li><a href="https://support.google.com/merchants/answer/6165956" target="_blank" rel="noopener">Unapproved pharmaceuticals and supplements</a></li>
      <li><a href="https://support.google.com/merchants/answer/6150151" target="_blank" rel="noopener">Healthcare &amp; medicines</a></li>
    </ul>
    <h3 id="misrepresentation">Misrepresentation</h3>
    <p>Typically caused by insufficient contact information or a mismatch between your shop name and URL. See <a href="https://support.google.com/merchants/answer/6150127" target="_blank" rel="noopener">Misrepresentation policy</a>. Add real contact info &mdash; not a PO Box or virtual address.</p>

    <h2 id="sources-cited">Sources cited</h2>
    <ul>
      <li><a href="https://support.google.com/merchants/answer/7052112?hl=en" target="_blank" rel="noopener">Product data specification (Google)</a></li>
      <li><a href="https://support.google.com/merchants/answer/6324415" target="_blank" rel="noopener">Title attribute</a></li>
      <li><a href="https://support.google.com/merchants/answer/6324371" target="_blank" rel="noopener">Price attribute</a></li>
      <li><a href="https://www.facebook.com/business/help/120325381656392" target="_blank" rel="noopener">Meta catalog product data specifications</a></li>
      <li><a href="https://www.datafeedwatch.com/pricing?via=austin-youtube" target="_blank" rel="noopener">DataFeedWatch pricing (referral)</a></li>
    </ul>
    <p>Related: <a href="google-merchant-center-sftp-upload.html">GMC SFTP File Upload</a> &middot; <a href="fix-cart-data-errors-google-ads.html">Fix Cart Data Errors</a> &middot; <a href="../guides/conversion-tracking-shopify-2026.html">2026 Conversion Tracking Guide</a></p>"""


# ---------- Meta Creative Checklist ----------

META_CREATIVE_PREVIEW = """    <p>Use this checklist to prepare image and video assets for Meta ads. Provide assets at least <strong>7 days prior</strong> to launching new sales promotion campaigns.</p>

    <h2 id="creative-inspiration">Creative Inspiration</h2>
    <p>View sample ads that convert and Meta&rsquo;s recommended creative themes:</p>
    <ul>
      <li><a href="https://www.facebook.com/business/m/small-business/creative-differentiation" target="_blank" rel="noopener">Maximize conversions with differentiated ad creative</a></li>
      <li><a href="https://www.facebook.com/business/inspiration" target="_blank" rel="noopener">Meta Creative Center: Inspiration</a></li>
    </ul>"""

META_CREATIVE_GATED = """""" + _img(
    "meta-creative-assets-checklist",
    "creative-differentiation.png",
    "Meta creative differentiation examples",
) + """
    <h2 id="creative-checklist">Creative Asset Checklist</h2>
    <p>Share a shared online drive folder with the video and image assets below. Ask us for an upload link if you don&rsquo;t have one.</p>

    <h3 id="videos">Videos</h3>
    <p>Minimum dimensions (larger is fine if ratios match):</p>
    <ul class="checklist">
      <li>Portrait (9:16): 1440 &times; 2560 pixels</li>
      <li>Square (1:1): 1440 &times; 1440</li>
      <li>Portrait (4:5): 1440 &times; 1800</li>
      <li>(Optional) Landscape (1.91:1): 2750 &times; 1440</li>
    </ul>
    <p><strong>File type:</strong> MP4, MOV, or GIF. <strong>Settings:</strong> H.264, square pixels, fixed frame rate, progressive scan, stereo AAC at 128kbps+.</p>
    <h4 id="safe-zones">Safe zones</h4>
    <p>Don&rsquo;t place text or important visuals outside the safe zone &mdash; doing so limits Reels and Stories placements.</p>
""" + _img(
    "meta-creative-assets-checklist",
    "meta-video-safe-zones.png",
    "Meta video ad safe zone specifications",
) + """
    <p>Provide videos <strong>without</strong> captions and without overlaid text. We add captions on our end.</p>
    <details class="guide-details">
      <summary>Themes for effective video ads</summary>
      <ul>
        <li>Comparisons: your product vs. competitor products</li>
        <li>Reviews: explain features and benefits</li>
        <li>How-tos: demonstrate product use</li>
        <li>Free resource offers: highlight a lead magnet in exchange for email</li>
      </ul>
    </details>

    <h3 id="images">Images</h3>
    <p>Provide at least <strong>3 unique</strong> images in each of the three dimensions below (9 images total) for maximum placement coverage:</p>
    <ul class="checklist">
      <li>Portrait (9:16): 1440 &times; 2560 pixels</li>
      <li>Square (1:1): 1440 &times; 1440</li>
      <li>Portrait (4:5): 1440 &times; 1800</li>
    </ul>
    <p><strong>File type:</strong> JPG or PNG. Minimum 1440px on either height or width.</p>

    <h2 id="sales-promotion">Sales Promotion Checklist</h2>
    <p>For a short-term sales promotion, collect and send:</p>
    <ul class="checklist">
      <li>Creatives: video and image (all sizes)</li>
      <li>Dates/Times (e.g. 1/1/2025 12:00am to 1/10/2025 11:59pm ET)</li>
      <li>Coupon codes (e.g. SAVE10)</li>
      <li>Specific products/collections</li>
      <li>Landing page URL</li>
      <li>Exclusions (e.g. accessories excluded from sale)</li>
    </ul>

    <h2 id="references">References</h2>
    <ul>
      <li><a href="https://www.facebook.com/business/ads-guide/update" target="_blank" rel="noopener">Meta Ads Creative Dimensions</a></li>
      <li><a href="https://www.facebook.com/business/m/small-business/creative-differentiation" target="_blank" rel="noopener">Maximize conversions with differentiated ad creative</a></li>
      <li><a href="https://www.facebook.com/business/inspiration" target="_blank" rel="noopener">Meta Creative Center: Inspiration</a></li>
    </ul>"""


# ---------- 2026 Conversion Tracking Guide (guides/) ----------

CONV_TRACKING_PREVIEW = """    <p>Step-by-step checklist for Shopify conversion tracking using Customer Events for Google Ads and Microsoft Ads. Watch the video in the hero, then unlock the full written guide.</p>
    <p>This method uses Shopify&rsquo;s <strong>Google &amp; YouTube Sales Channel</strong> and <strong>Microsoft Sales Channel</strong> apps rather than editing <code>theme.liquid</code>, so tracking survives theme updates.</p>

    <h2 id="installation">Installation</h2>
    <ul class="checklist">
      <li><a href="https://apps.shopify.com/google" target="_blank" rel="noopener">Google &amp; YouTube Sales Channel</a> installed on Shopify</li>
      <li>Connect sales channel to Google Ads (requires Google Ads admin access)</li>
      <li>Google &amp; YouTube conversions sent to Google Ads</li>
      <li>&ldquo;Google Shopping App Purchase&rdquo; set to primary; rest set to secondary</li>
    </ul>"""

CONV_TRACKING_GATED = """
    <h2 id="microsoft-ads">Microsoft Ads</h2>
    <ul class="checklist">
      <li><a href="https://apps.shopify.com/microsoft-advertising" target="_blank" rel="noopener">Microsoft Sales Channel</a> installed on Shopify</li>
      <li>Connect sales channel to Microsoft Ads</li>
    </ul>

    <h2 id="last-steps">Last Steps</h2>
    <ul class="checklist">
      <li>Set the new conversion to <em>primary</em> in Google Ads and &ldquo;include in conversions&rdquo; in Microsoft</li>
      <li>Wait until the new and old conversion actions have recorded about the same number of conversions in the past 30 days before demoting the old action &mdash; Google needs data in the new action for smart bidding</li>
      <li>Remove unused conversions in Google and Microsoft Ads</li>
      <li>Remove unused conversion tracking code from Shopify</li>
    </ul>

    <details class="guide-details">
      <summary>Placeholder to save old tracking code</summary>
      <pre><code>// Paste deprecated tracking code here before removing from Shopify</code></pre>
    </details>

    <h2 id="optional-steps">Optional steps to add custom events</h2>
    <p>You probably don&rsquo;t need this. Use Customer Events custom pixels if you want unique data layers for Google Tag Manager.</p>

    <h3 id="google-optional">Google Ads optional steps</h3>
    <ul class="checklist">
      <li>Add &ldquo;GTM Enhanced Conversion Data&rdquo; Customer Event to Shopify</li>
    </ul>
    <details class="guide-details">
      <summary>Expand for GTM Customer Event code</summary>
      <p>Name the Customer Event &ldquo;GTM Enhanced Conversion Data&rdquo;. Set Data sale to <em>Data collected does not qualify as data sale</em>. Replace <code>GTM-XXXXXXXX</code> with your container ID.</p>
      <pre><code>window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}

(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&amp;l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer', 'GTM-XXXXXXXX');

gtag('consent', 'update', {
  'ad_storage': 'granted',
  'analytics_storage': 'granted',
  'ad_user_data': 'granted',
  'ad_personalization': 'granted',
});

analytics.subscribe("checkout_completed", (event) => {
  const email = event.data?.checkout?.email;
  const phone = event.data?.checkout?.phone;
  dataLayer.push({ event: 'purchase', email: email, phone: phone });
});</code></pre>
    </details>

    <h3 id="microsoft-optional">Microsoft Ads optional steps</h3>
    <p>Optional backup UET tag via Customer Events when the Microsoft Sales Channel is not sending conversion data successfully.</p>
    <details class="guide-details">
      <summary>Expand for Microsoft UET Customer Event code</summary>
      <p>Name the Customer Event &ldquo;MS Ads Conversion Tracking&rdquo;. Add your UET tag ID at <code>ti: "{xxxxxx}"</code>.</p>
    </details>

    <h2 id="resources-cited">Resources Cited</h2>
    <ul>
      <li><a href="https://help.shopify.com/en/manual/promoting-marketing/pixels/custom-pixels/gtm-tutorial" target="_blank" rel="noopener">Shopify GTM tutorial</a></li>
      <li><a href="https://developers.google.com/analytics/devguides/collection/ga4/reference/events?client_type=gtm" target="_blank" rel="noopener">GA4 reference events</a></li>
      <li><a href="https://shopify.dev/docs/api/web-pixels-api/standard-events/checkout_completed" target="_blank" rel="noopener">Shopify checkout_completed event</a></li>
      <li><a href="https://support.google.com/google-ads/answer/7548399?hl=en" target="_blank" rel="noopener">Google Ads conversion tag example</a></li>
      <li><a href="https://support.google.com/google-ads/answer/13258081" target="_blank" rel="noopener">Enhanced conversions user data</a></li>
    </ul>
    <p>Related: <a href="../resources/google-merchant-center-setup-2026.html">2026 GMC Full Setup</a> &middot; <a href="../resources/fix-cart-data-errors-google-ads.html">Fix Cart Data Errors</a></p>"""
