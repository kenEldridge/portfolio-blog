# the-derple-dex - Project Guide for AI Assistants

This is a technical blog and data showcase site built with Astro. It displays financial and economic data managed by [cdata](https://github.com/kenEldridge/cdata) initialized locally.

## Architecture Overview

**Current Approach:** Bridge Pattern (cdata as Library)

- cdata is used as a **library** via the bridge pattern (not file-based)
- Dataset configurations are in `scripts/dataset_config.py` (Python)
- Data is fetched programmatically at build time (no file storage)
- Bridge module creates SourceConfig objects and fetches data on-demand
- prepare-data-v3.py uses bridge to fetch data and converts to JSON for the static site

**Key Files:**
- `scripts/dataset_config.py` - Dataset definitions (28 sources, Python dicts)
- `scripts/cdata_bridge.py` - Bridge module connecting to cdata registry
- `scripts/prepare-data-v3.py` - Uses bridge to fetch data, transforms to JSON
- `public/data/*.json` - JSON files for client-side visualization (generated)
- `src/data/datasets.json` - Summary for static site generation
- `src/pages/data/[dataset].astro` - Dynamic dataset pages

## Current Data Flow (Bridge Pattern)

```
Dataset Configuration (scripts/dataset_config.py)
  ↓ 28 data sources defined as Python dicts
  ↓
prepare-data-v3.py
  ↓ Imports dataset_config and cdata_bridge
  ↓ For each dataset:
  │   ├─→ Bridge creates SourceConfig programmatically
  │   ├─→ Registry creates source instance (YFinanceSource, FREDSource, etc.)
  │   ├─→ Source.fetch() retrieves data from API
  │   └─→ Returns DataFrame directly (no file storage)
  ↓ Transforms DataFrames to JSON
  ↓ Writes to: public/data/*.json + src/data/datasets.json
  ↓
Astro Build
  ↓ Generates 32 static HTML pages from datasets.json
  ↓ Includes full data JSON files for client-side Plotly charts
  ↓
GitHub Pages (deployed site)
```

**Key Difference from Previous Approach:**
- No Parquet file storage
- No `cdata fetch all` command
- Data fetched on-demand at build time
- Configuration owned by the-derple-dex (not YAML files)

## cdata Integration (Bridge Pattern)

This project uses cdata as a **library** via the bridge pattern. Instead of reading files, it programmatically creates data sources and fetches on-demand.

### Benefits of Bridge Pattern

| Aspect | Description |
|--------|-------------|
| **Decoupling** | No dependency on cdata's file structure or storage location |
| **Ownership** | the-derple-dex owns its dataset configuration |
| **Simplicity** | Single project, one repository |
| **Flexibility** | Can customize fetching without modifying cdata |
| **Testing** | Easy to mock the bridge for testing |
| **No File Storage** | Data fetched on-demand, no Parquet files to manage |

### Bridge Architecture

```python
# dataset_config.py defines datasets
DATASETS = {
    "us_indices": {
        "type": "yfinance",
        "config": {"symbols": ["^GSPC", "^DJI"], ...}
    }
}

# cdata_bridge.py provides fetch methods
bridge = get_bridge()
df = bridge.fetch_yfinance_data(
    source_id="us_indices",
    symbols=["^GSPC", "^DJI"],
    period="1y"
)

# prepare-data-v3.py uses bridge
for name, config in DATASETS.items():
    df = bridge.fetch_*_data(...)  # Fetch on-demand
    dataset = prepare_*_dataset(name, df, config)
    write_json(dataset)
```

See [cdata issue #4](https://github.com/kenEldridge/cdata/issues/4) for bridge pattern details.

## Working with Data

### Initial Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Set up API keys (required for FRED, BLS)
cp .env.example .env
# Edit .env and add your FRED_API_KEY

# Fetch data and generate JSON (bridge pattern)
python3 scripts/prepare-data-v3.py

# Build site
npm run build
```

### Updating Data

With the bridge pattern, data is fetched fresh at build time:

```bash
# Fetch latest data and regenerate JSON (one command)
python3 scripts/prepare-data-v3.py

# Or rebuild site (automatically runs prepare-data-v3.py first)
npm run build

# For local development (includes data fetch)
npm run dev
```

**Note:** Unlike the old file-based approach, there's no separate `cdata fetch all` command. The prepare-data script fetches data directly using the bridge.

### Adding New Data Sources

1. Edit `scripts/dataset_config.py`:
   ```python
   DATASETS = {
       # ... existing datasets ...
       "my_new_source": {
           "type": "yfinance",  # or fred, bls, rss, fed_stress
           "description": "Description here",
           "primary_keys": ["symbol", "date"],
           "incremental": True,
           "config": {
               "symbols": ["AAPL", "MSFT"],
               "period": "1y",
               "interval": "1d"
           }
       }
   }
   ```

2. Add to appropriate dataset category:
   ```python
   OHLCV_DATASETS = {"us_indices", ..., "my_new_source"}
   ```

3. Regenerate and rebuild:
   ```bash
   python3 scripts/prepare-data-v3.py
   npm run build
   ```

No YAML files to edit, no separate fetch commands. The bridge pattern keeps everything in Python.

### Data Freshness

- Data is fetched fresh at each build
- Metadata includes `fetched_at` timestamp in JSON output
- DataFreshness.astro component shows age indicators on site
- For incremental support, cdata sources can track `last_record_date` internally

## Dataset Types

### OHLCV (Price Data)
- **Sources:** yfinance
- **Columns:** symbol, date, open, high, low, close, volume
- **Examples:** us_indices, commodities, bond_etfs
- **Processing:** `prepare_ohlcv_dataset()` computes per-symbol statistics

### RSS (News Feeds)
- **Sources:** RSS feeds
- **Columns:** title, link, published, feed_name, author
- **Examples:** fed_news, financial_news, economics_news
- **Processing:** `prepare_rss_dataset()` shows recent 30 articles

### FRED (Federal Reserve Economic Data)
- **Sources:** FRED API
- **Columns:** series_id, date, value, title, units, frequency
- **Examples:** fred_gdp, fred_employment, fred_inflation
- **Processing:** `prepare_fred_dataset()` computes per-series statistics
- **Note:** Requires FRED_API_KEY in .env

### BLS (Bureau of Labor Statistics)
- **Sources:** BLS API
- **Columns:** series_id, date, value, title, units
- **Examples:** bls_cpi, bls_employment, bls_wages
- **Processing:** Same as FRED (uses `prepare_fred_dataset()`)

### Fed Stress Test Scenarios
- **Sources:** Federal Reserve DFAST stress test data
- **Columns:** year, scenario, table, date, variable, value
- **Example:** fed_stress_scenarios
- **Processing:** Not yet implemented in prepare-data-v2.py

## Development Workflow

### Local Development

```bash
# Start dev server (use Windows Node for proper networking)
"/mnt/c/Program Files/nodejs/npm" run dev --host

# Available at: http://localhost:4321/the-derple-dex
```

### Adding Visualizations

1. Create component in `src/components/data/`
2. Use Plotly.js for interactive charts
3. Follow existing patterns:
   - `TimeSeriesPlot.astro` - Line/candlestick charts
   - `NewsTimeline.astro` - Article lists
   - `DatasetStats.astro` - Summary tables

### Component Architecture

```
src/pages/data/
  ├── index.astro           # Landing page listing all datasets
  └── [dataset].astro       # Dynamic pages for each dataset

src/components/data/
  ├── DatasetCard.astro     # Preview card on landing page
  ├── DataFreshness.astro   # Shows data age/staleness
  ├── DatasetStats.astro    # Summary statistics table
  ├── TimeSeriesPlot.astro  # Plotly line/candlestick charts
  └── NewsTimeline.astro    # RSS article list
```

## Current Datasets

**Total:** 28 datasets, 233K initial records

**Market Data (8):**
- us_indices - Major US equity indices (S&P 500, Dow, NASDAQ, Russell 2000, VIX)
- global_indices - International indices (FTSE, DAX, Nikkei, etc.)
- treasury_yields - Treasury yield curve (13-week, 5Y, 10Y, 30Y)
- bond_etfs - Fixed income ETFs (TLT, AGG, HYG, etc.)
- currencies - Dollar index and major pairs
- commodities - Gold, silver, oil, copper, etc.
- sector_etfs - S&P 500 sector performance
- macro_proxies - ETFs tracking macro themes

**News Feeds (3):**
- fed_news - Federal Reserve press releases and speeches
- financial_news - Market news (Yahoo, Seeking Alpha, CNBC)
- economics_news - Economic analysis (Calculated Risk, Marginal Revolution)

**FRED Economic Data (11):**
- fred_gdp - GDP and output measures
- fred_employment - Employment and labor market
- fred_inflation - CPI, PCE, PPI inflation measures
- fred_rates - Fed funds, Treasury yields, spreads
- fred_money - M1, M2, Fed balance sheet
- fred_housing - Housing starts, sales, prices
- fred_consumer - Retail sales, consumer sentiment
- fred_banking - H.8 commercial banking data
- fred_stress_index - Financial stress indices
- fred_mev - Macro scenario variables
- fred_market - Market snapshot (S&P 500, VIX, spreads)

**BLS Labor Data (5):**
- bls_cpi - Consumer Price Index
- bls_employment - Employment and unemployment
- bls_wages - Hourly and weekly earnings
- bls_ppi - Producer Price Index
- bls_jolts - Job openings and labor turnover

**Fed Stress Tests (1):**
- fed_stress_scenarios - DFAST stress test scenarios (baseline & severely adverse)

## Environment & Dependencies

**Node.js:** Use Windows Node (not WSL) for proper networking
- Location: `/mnt/c/Program Files/nodejs/npm`
- Reason: WSL networking issues with Astro dev server

**Python Dependencies:**
```
cdata @ git+https://github.com/kenEldridge/cdata.git@dev
pandas>=2.0
pyarrow>=14.0
python-dotenv>=1.0
```

**Astro Dependencies:**
- See `package.json` for full list

**API Keys Required:**
- `FRED_API_KEY` - Free from https://fred.stlouisfed.org/docs/api/api_key.html
- Store in `.env` file at project root

## Deployment

- **Host:** GitHub Pages
- **URL:** https://keneldridge.github.io/the-derple-dex/
- **CI/CD:** GitHub Actions on push to master
- **Base Path:** `/the-derple-dex` (configured in astro.config.mjs)
- **Build:** ~101 seconds (includes data generation)
- **Output:** 32 HTML pages, 46MB total

### CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/deploy.yml`):
1. Set up Python and install dependencies (`pip install -r requirements.txt`)
2. Set FRED_API_KEY secret in `.env` file
3. Run `python3 scripts/prepare-data-v3.py` to fetch data via bridge
4. Run `npm run build` to build Astro site
5. Deploy dist/ to GitHub Pages

**Bridge Pattern CI/CD:**
- No `cdata fetch all` command (bridge fetches on-demand)
- No Parquet files to commit or cache
- Fresh data on every build
- Build time includes API fetch time (~2-5 minutes)

## File Size Summary

| Location | Size | Description |
|----------|------|-------------|
| `public/data/*.json` | ~36MB | JSON for client-side charts (generated, 27 files) |
| `src/data/datasets.json` | ~50KB | Summary metadata for static generation |
| `dist/` | ~46MB | Built static site (32 HTML pages) |

**Bridge Pattern - No File Storage:**
- No Parquet files (data fetched on-demand)
- JSON generated fresh at each build
- Trade-off: Longer build time vs. simpler architecture

## Git Ignore Strategy

**Current approach:**
- `public/data/*.json` - Excluded (generated at build time)
- `src/data/datasets.json` - Excluded (generated at build time)
- `dist/` - Excluded (build output)
- No `data/` directory (bridge pattern has no file storage)

**Rationale:** With bridge pattern, all data files are build artifacts and regenerated fresh each time.

## Known Issues

1. **Yahoo Finance Date Errors:** Some symbols show "possibly delisted" errors when fetching incrementally (start date > end date). This is a Yahoo Finance API quirk and doesn't affect data quality.

2. **Fed Stress Scenarios:** Not yet handled in prepare-data-v2.py. Need to add processing function for this dataset type.

3. **Pandas Future Warnings:** Mixed timezone warnings in date parsing. Non-breaking but should be fixed with `utc=True` parameter.

## Future Enhancements

- [ ] Add fed_stress processing function
- [ ] Implement data download functionality (CSV/JSON)
- [ ] Add client-side filtering/search
- [ ] Add comparison charts (multiple series overlaid)
- [ ] Add technical indicators (SMA, RSI, Bollinger Bands)
- [ ] Add SEC EDGAR company filings integration
- [ ] Add NIC BHC bank holding company data
- [ ] Optimize JSON file sizes (chunking, lazy loading)

## Related Resources

- [cdata repository](https://github.com/kenEldridge/cdata)
- [cdata issue #4: Bridge Pattern Discussion](https://github.com/kenEldridge/cdata/issues/4)
- [Astro documentation](https://docs.astro.build)
- [Plotly.js documentation](https://plotly.com/javascript/)
- [FRED API documentation](https://fred.stlouisfed.org/docs/api/fred/)
- [BLS API documentation](https://www.bls.gov/developers/)

## Troubleshooting

**"ModuleNotFoundError: No module named 'cdata'"**
- Run `pip install -r requirements.txt` to install dependencies
- For local development: `pip install -e ../cdata` (editable mode)

**"ImportError: cannot import name 'get_registry'"**
- Ensure cdata is installed from dev branch: `git+https://github.com/kenEldridge/cdata.git@dev`
- Check that cdata version supports bridge pattern

**Build fails with memory errors**
- Large JSON files can cause OOM during build
- Consider reducing dataset sizes or limiting time periods
- Exit code 137 usually indicates OOM killer

**Missing FRED data / 0 records fetched**
- Ensure `FRED_API_KEY` is set in `.env` file
- Check that `.env` file is in project root
- Verify API key is valid at https://fred.stlouisfed.org/
- Check prepare-data-v3.py output for API errors

**Empty datasets or missing JSON files**
- Check prepare-data-v3.py output for fetch errors
- Verify dataset is in `DATASETS` dict in `dataset_config.py`
- Verify dataset is in appropriate category (OHLCV_DATASETS, etc.)
- API may be rate-limiting or temporarily unavailable
