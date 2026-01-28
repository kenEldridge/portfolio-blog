# the-derple-dex - Project Guide for AI Assistants

This is a technical blog and data showcase site built with Astro. It displays financial and economic data fetched via [cdata](https://github.com/kenEldridge/cdata) using the **bridge pattern**.

## Architecture Overview

**Current Approach:** Bridge Pattern (Implemented)
- This project uses `cdata` as a library (not as a separate data pipeline)
- Dataset configurations are owned by this project in Python code
- Data is fetched programmatically at build time via the cdata registry
- Static site generation with pre-rendered data pages

**Key Files:**
- `scripts/dataset_config.py` - Dataset configurations (owns the config)
- `scripts/cdata_bridge.py` - Bridge to cdata library
- `scripts/prepare-data.py` - Fetches via bridge, transforms to JSON
- `src/pages/data/[dataset].astro` - Dynamic dataset pages
- `src/components/data/*` - Data visualization components

## Current Data Flow

```
the-derple-dex (this project)
  ↓ Owns configuration in dataset_config.py
  ↓
cdata_bridge.py
  ↓ Uses cdata registry to create sources
  ↓ Fetches data programmatically
  ↓ Returns DataFrames
  ↓
prepare-data.py
  ↓ Transforms to JSON
  ↓ Writes to: public/data/*.json + src/data/datasets.json
  ↓
Astro Build
  ↓ Generates static pages from datasets.json
  ↓ Includes full data JSON files for client-side charts
  ↓
GitHub Pages (deployed site)
```

## Bridge Pattern Implementation

This project implements the bridge pattern from cdata issue [#4](https://github.com/kenEldridge/cdata/issues/4), using `cdata` as a **library** rather than reading output files.

### Bridge Pattern Benefits (Now Realized)

| Aspect | Old (File-based) | Current (Bridge Pattern) |
|--------|------------------|--------------------------|
| **Separation** | Two projects, file coupling | Single project, API coupling ✓ |
| **Config** | YAML files in cdata | Python code in this project ✓ |
| **Storage** | cdata manages Parquet | This project manages storage ✓ |
| **Scheduling** | cdata's APScheduler | This project's control ✓ |
| **Data Flow** | Fetch → Parquet → JSON | Fetch → Custom processing → Storage ✓ |
| **Testing** | Hard to test data pipeline | Easy to mock fetches ✓ |

### Bridge Pattern Implementation

**Actual Implementation:**

`scripts/cdata_bridge.py` provides the bridge:
```python
from cdata_bridge import fetch_dataset
from dataset_config import DATASETS

# Fetch data using bridge
df, meta = fetch_dataset("us_indices", DATASETS["us_indices"])

# df is a pandas DataFrame with the fetched data
# meta contains record_count, timestamps, columns, etc.
```

`scripts/dataset_config.py` defines all datasets:
```python
DATASETS = {
    "us_indices": {
        "name": "US Market Indices",
        "type": "yfinance",
        "description": "Major US equity indices",
        "config": {
            "symbols": ["^GSPC", "^DJI", "^IXIC", "^RUT", "^VIX"],
            "period": "1y",
            "interval": "1d"
        },
        "primary_keys": ["symbol", "date"]
    },
    # ... 22 more datasets
}
```

`scripts/prepare-data.py` uses the bridge:
```python
for dataset_name, dataset_config in DATASETS.items():
    df, meta = fetch_dataset(dataset_name, dataset_config)
    # Transform to JSON as before
```

## Working with the Bridge Pattern

**To add a new data source:**
1. Add dataset config to `scripts/dataset_config.py`
2. Run `python3 scripts/prepare-data.py` to fetch and generate JSON
3. Rebuild site with `npm run build`

**To refresh data:**
```bash
# Ensure you have a FRED API key in .env
export FRED_API_KEY="your_key"

# Fetch fresh data and generate JSON
python3 scripts/prepare-data.py

# Build site (automatically runs prepare-data first)
npm run build
```

**Setup requirements:**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Or for local development, use editable install
pip install -e ../cdata  # if you have cdata checked out

# Set up API keys
cp .env.example .env
# Edit .env and add your FRED_API_KEY
```

**Data location:**
- Configuration: `scripts/dataset_config.py` (source of truth)
- Build output: `public/data/*.json` (for client-side)
- Build output: `src/data/datasets.json` (for SSG)

## Development Workflow

### Local development
```bash
# Start dev server (use Windows Node)
"/mnt/c/Program Files/nodejs/npm" run dev --host

# Available at: http://localhost:4321/the-derple-dex
```

### Adding new visualizations
1. Create component in `src/components/data/`
2. Use Plotly.js for interactive charts
3. Follow existing patterns (TimeSeriesPlot.astro, NewsTimeline.astro)

### Data freshness
- Data pages show: first_fetched, last_updated, fetch_count
- Automated via `DataFreshness.astro` component

## Known Patterns and Conventions

### Dataset Types
- **OHLCV**: Price data (open, high, low, close, volume)
- **RSS**: News feeds with title, link, published, feed_name
- **FRED/BLS**: Economic time series with series_id, date, value

### Processing Functions
- `prepare_ohlcv_dataset()` - Handles price data, computes per-symbol stats
- `prepare_fred_dataset()` - Handles FRED/BLS, computes per-series stats
- `prepare_rss_dataset()` - Handles news feeds, computes daily article counts

### Component Architecture
```
src/pages/data/
  ├── index.astro           # Landing page with all datasets
  └── [dataset].astro       # Dynamic pages for each dataset

src/components/data/
  ├── DatasetCard.astro     # Preview card on landing page
  ├── DataFreshness.astro   # Shows data age/staleness
  ├── DatasetStats.astro    # Summary statistics table
  ├── TimeSeriesPlot.astro  # Plotly line/candlestick charts
  └── NewsTimeline.astro    # RSS article list
```

## Environment & Dependencies

**Node.js:** Use Windows Node (not WSL) for proper networking
- Location: `/mnt/c/Program Files/nodejs/npm`

**Python Dependencies:**
- pandas (for Parquet reading)
- pyarrow (for Parquet backend)

**Astro Dependencies:**
- See `package.json` for full list

## Deployment

- **Host:** GitHub Pages
- **URL:** https://keneldridge.github.io/the-derple-dex/
- **CI/CD:** GitHub Actions on push to master
- **Base Path:** `/the-derple-dex` (configured in astro.config.mjs)

## Data Sources

The site currently displays 11 datasets from cdata:

**Market Data (8):** us_indices, global_indices, treasury_yields, bond_etfs, currencies, commodities, sector_etfs, macro_proxies

**News Feeds (3):** fed_news, financial_news, economics_news

All sourced via yfinance and RSS feeds. See `../cdata/config/sources/` for full configs.

## Future Enhancements

Potential improvements:
- [ ] Implement bridge pattern for real-time data fetching
- [ ] Add more economic indicators (FRED, BLS)
- [ ] Add SEC EDGAR company filings
- [ ] Add NIC BHC bank holding company data
- [ ] Client-side data filtering/search
- [ ] Data download functionality (CSV/JSON)
- [ ] Comparison charts (multiple series)
- [ ] Technical indicators (SMA, RSI, etc.)

## Related Resources

- [cdata documentation](https://github.com/kenEldridge/cdata)
- [cdata issue #4: Library Integration Guide](https://github.com/kenEldridge/cdata/issues/4)
- [Astro documentation](https://docs.astro.build)
- [Plotly.js documentation](https://plotly.com/javascript/)
