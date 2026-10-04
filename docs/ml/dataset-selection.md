# RecoFlow Dataset Selection

## Primary Dataset

**Amazon Reviews 2023 — Electronics**

### Sources

Official project:

https://amazon-reviews-2023.github.io/

Hugging Face:

https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023

---

# 1. Why This Dataset

RecoFlow requires two important types of data:

1. Historical user-item interaction data for recommendation models.
2. Rich product information for the e-commerce shopping interface.

Amazon Reviews 2023 provides both interaction/review information and rich product metadata.

Important review fields include:

- user ID
- product ID
- timestamp
- rating
- verified purchase
- review information

Important product metadata can include:

- product title
- description
- features
- price
- images
- categories
- product details
- store

---

# 2. Electronics Domain

Electronics is selected because it directly fits the e-commerce recommendation use case.

It also provides a broad product catalog that can support:

- Product browsing
- Product search
- Similar-product recommendations
- Personalized recommendations
- Category-based recommendations

---

# 3. Dataset Scale

The complete Electronics dataset is very large.

RecoFlow will therefore NOT blindly download the entire raw dataset.

Instead, we will inspect an appropriate benchmark/sample and determine a practical working subset.

The goal is not maximum dataset size.

The goal is:

- sufficient recommendation quality
- sufficient interaction density
- useful product metadata
- manageable local processing
- fast experimentation
- compatibility with AWS deployment

---

# 4. Historical Data Role

Historical data will be used for:

- recommendation model training
- offline evaluation
- product catalog bootstrapping
- historical preference analysis
- feature engineering
- baseline comparison

---

# 5. Historical Data vs Live Application Events

The historical dataset is not treated as a complete clickstream.

RecoFlow will generate its own live application events:

- product_view
- product_click
- search
- add_to_cart
- purchase
- wishlist_add
- recommendation_impression
- recommendation_click

These events will enter through the actual FastAPI Event API.

---

# 6. Important Modeling Decision

An Amazon review is not equivalent to:

- product view
- product click
- search
- add to cart

Therefore, historical reviews will be treated as historical preference signals.

The application event system will separately capture real-time behavioral signals.

This separation is important for a realistic recommendation architecture.

---

# 7. Dataset Inspection Criteria

Before finalizing the working subset, we will measure:

- number of users
- number of products
- number of interactions
- interactions per user
- interactions per product
- rating distribution
- timestamp distribution
- sparsity
- duplicate records
- missing values
- product metadata coverage
- image coverage
- description coverage
- category coverage
- price coverage

---

# 8. Working Subset

Current status:

**Local catalog sample imported**

For local catalog development, a bounded byte-range sample of the Electronics
metadata file is stored outside Git at:

`data/raw/meta_Electronics.sample.jsonl`

The reproducible importer is:

`scripts/import_products.py`

It preserves existing products, imports up to 92 additional records, maps
records to the existing catalog categories, and keeps source image URLs. The
full metadata source remains the Amazon Reviews 2023 Electronics metadata file;
the multi-gigabyte source is not downloaded for this local catalog step.

The final working subset will be selected based on:

- recommendation suitability
- catalog quality
- metadata coverage
- temporal evaluation suitability
- computational feasibility
- local development speed

---

# 9. Raw Data Policy

Raw datasets will not be committed to GitHub.

Large processed datasets will also remain outside Git.

The repository should contain:

- code
- configuration
- documentation
- tests
- architecture
- small metadata files

---

# 10. Day 1 Decision

RecoFlow will proceed with:

**Amazon Reviews 2023 — Electronics**

as the primary historical dataset family.

The exact working subset will be finalized after local inspection.