#!/usr/bin/env python3
"""
Dataset configuration for the-derple-dex.

This module defines all data sources that will be fetched via the cdata bridge.
Previously these were defined in cdata's YAML files, but now the-derple-dex
owns its own configuration.
"""

# Dataset definitions
# Each dataset specifies its type, description, and configuration parameters
DATASETS = {
    # ===================
    # US EQUITY INDICES
    # ===================
    "us_indices": {
        "type": "yfinance",
        "description": "Major US equity indices",
        "primary_keys": ["symbol", "date"],
        "incremental": True,
        "config": {
            "symbols": ["^GSPC", "^DJI", "^IXIC", "^RUT", "^VIX"],
            "period": "1y",
            "interval": "1d"
        }
    },

    # ===================
    # GLOBAL EQUITY INDICES
    # ===================
    "global_indices": {
        "type": "yfinance",
        "description": "Major international equity indices",
        "primary_keys": ["symbol", "date"],
        "incremental": True,
        "config": {
            "symbols": ["^FTSE", "^GDAXI", "^FCHI", "^N225", "^HSI", "^STOXX50E", "FXI", "EEM"],
            "period": "1y",
            "interval": "1d"
        }
    },

    # ===================
    # US TREASURY YIELDS
    # ===================
    "treasury_yields": {
        "type": "yfinance",
        "description": "Treasury yield curve data",
        "primary_keys": ["symbol", "date"],
        "incremental": True,
        "config": {
            "symbols": ["^IRX", "^FVX", "^TNX", "^TYX"],
            "period": "1y",
            "interval": "1d"
        }
    },

    # ===================
    # BOND ETFs
    # ===================
    "bond_etfs": {
        "type": "yfinance",
        "description": "Fixed income ETFs across durations and types",
        "primary_keys": ["symbol", "date"],
        "incremental": True,
        "config": {
            "symbols": ["TLT", "IEF", "SHY", "AGG", "LQD", "HYG", "TIP", "MUB"],
            "period": "1y",
            "interval": "1d"
        }
    },

    # ===================
    # CURRENCIES & DOLLAR
    # ===================
    "currencies": {
        "type": "yfinance",
        "description": "Dollar strength and major currency pairs",
        "primary_keys": ["symbol", "date"],
        "incremental": True,
        "config": {
            "symbols": ["DX-Y.NYB", "EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCNY=X"],
            "period": "1y",
            "interval": "1d"
        }
    },

    # ===================
    # COMMODITIES
    # ===================
    "commodities": {
        "type": "yfinance",
        "description": "Key commodity prices",
        "primary_keys": ["symbol", "date"],
        "incremental": True,
        "config": {
            "symbols": ["GC=F", "SI=F", "CL=F", "BZ=F", "NG=F", "HG=F"],
            "period": "1y",
            "interval": "1d"
        }
    },

    # ===================
    # SECTOR ETFs
    # ===================
    "sector_etfs": {
        "type": "yfinance",
        "description": "S&P 500 sector performance",
        "primary_keys": ["symbol", "date"],
        "incremental": True,
        "config": {
            "symbols": ["XLF", "XLK", "XLE", "XLV", "XLI", "XLP", "XLY", "XLU", "XLB", "XLRE"],
            "period": "1y",
            "interval": "1d"
        }
    },

    # ===================
    # MACRO INDICATOR PROXIES
    # ===================
    "macro_proxies": {
        "type": "yfinance",
        "description": "ETFs that track macro themes",
        "primary_keys": ["symbol", "date"],
        "incremental": True,
        "config": {
            "symbols": ["SPY", "QQQ", "IWM", "DBA", "UUP", "GLD", "GOVT"],
            "period": "1y",
            "interval": "1d"
        }
    },

    # ===================
    # FEDERAL RESERVE & POLICY NEWS
    # ===================
    "fed_news": {
        "type": "rss",
        "description": "Federal Reserve announcements and speeches",
        "primary_keys": ["id"],
        "config": {
            "feeds": [
                {
                    "name": "Federal Reserve Press Releases",
                    "url": "https://www.federalreserve.gov/feeds/press_all.xml"
                },
                {
                    "name": "Fed Speeches",
                    "url": "https://www.federalreserve.gov/feeds/speeches.xml"
                }
            ]
        }
    },

    # ===================
    # FINANCIAL NEWS
    # ===================
    "financial_news": {
        "type": "rss",
        "description": "Market and economic news feeds",
        "primary_keys": ["id"],
        "config": {
            "feeds": [
                {
                    "name": "Yahoo Finance",
                    "url": "https://finance.yahoo.com/news/rssindex"
                },
                {
                    "name": "Seeking Alpha Market News",
                    "url": "https://seekingalpha.com/market_currents.xml"
                },
                {
                    "name": "CNBC Top News",
                    "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114"
                }
            ]
        }
    },

    # ===================
    # ECONOMIC DATA NEWS
    # ===================
    "economics_news": {
        "type": "rss",
        "description": "Economic analysis and policy coverage",
        "primary_keys": ["id"],
        "config": {
            "feeds": [
                {
                    "name": "Calculated Risk",
                    "url": "https://www.calculatedriskblog.com/feeds/posts/default?alt=rss"
                },
                {
                    "name": "Marginal Revolution",
                    "url": "https://marginalrevolution.com/feed"
                }
            ]
        }
    },

    # ===================
    # FRED - MACRO INDICATORS
    # ===================
    "fred_gdp": {
        "type": "fred",
        "description": "Gross Domestic Product and related measures",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["GDP", "GDPC1", "A191RL1Q225SBEA", "GDPDEF"]
        }
    },

    "fred_employment": {
        "type": "fred",
        "description": "Employment, unemployment, and labor market indicators",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["UNRATE", "PAYEMS", "ICSA", "JTSJOL", "AWHAETP", "CES0500000003"]
        }
    },

    "fred_inflation": {
        "type": "fred",
        "description": "Consumer and producer price indices",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["CPIAUCSL", "CPILFESL", "PCEPI", "PCEPILFE", "PPIACO", "MICH"]
        }
    },

    "fred_rates": {
        "type": "fred",
        "description": "Federal Reserve rates and Treasury yields",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["FEDFUNDS", "DFEDTARU", "DFEDTARL", "DGS2", "DGS10", "DGS30", "T10Y2Y", "T10Y3M", "BAMLH0A0HYM2"]
        }
    },

    "fred_money": {
        "type": "fred",
        "description": "Monetary aggregates and credit conditions",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["M1SL", "M2SL", "WALCL", "TOTRESNS", "TOTALSL"]
        }
    },

    "fred_housing": {
        "type": "fred",
        "description": "Housing market indicators",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["HOUST", "PERMIT", "HSN1F", "EXHOSLUSM495S", "CSUSHPINSA", "MORTGAGE30US"]
        }
    },

    "fred_consumer": {
        "type": "fred",
        "description": "Consumer spending and sentiment",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["RSAFS", "PCE", "PSAVERT", "UMCSENT", "DSPIC96"]
        }
    },

    "fred_banking": {
        "type": "fred",
        "description": "H.8 commercial banking data and credit conditions",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["TOTBKCR", "BUSLOANS", "CONSUMER", "RESIDUAL", "TOTLL", "DPSACBW027SBOG", "RCFD2170"]
        }
    },

    "fred_stress_index": {
        "type": "fred",
        "description": "Composite financial stress and conditions indicators",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["STLFSI2", "NFCI", "CFSI"]
        }
    },

    "fred_mev": {
        "type": "fred",
        "description": "Key macroeconomic variables used in stress test scenario design",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["GDPC1", "UNRATE", "CPIAUCSL", "DGS10", "CSUSHPINSA", "MORTGAGE30US", "DTWEXBGS", "VIXCLS"]
        }
    },

    "fred_market": {
        "type": "fred",
        "description": "Broad market indicators and risk measures",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["SP500", "VIXCLS", "DTWEXBGS", "BAMLH0A0HYM2", "BAMLC0A0CM", "TEDRATE", "T10YIE"]
        }
    },

    # ===================
    # BLS - LABOR STATISTICS
    # ===================
    "bls_cpi": {
        "type": "bls",
        "description": "CPI inflation measures from Bureau of Labor Statistics",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["CUSR0000SA0", "CUSR0000SA0L1E", "CUUR0000SA0"]
        }
    },

    "bls_employment": {
        "type": "bls",
        "description": "Employment and unemployment from Bureau of Labor Statistics",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["LNS14000000", "LNS11000000", "CES0000000001", "CES0500000001"]
        }
    },

    "bls_wages": {
        "type": "bls",
        "description": "Wage and earnings data from Bureau of Labor Statistics",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["CES0500000003", "CES0500000011"]
        }
    },

    "bls_ppi": {
        "type": "bls",
        "description": "Producer prices from Bureau of Labor Statistics",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["WPUFD4", "WPSFD4", "WPUFD49104"]
        }
    },

    "bls_jolts": {
        "type": "bls",
        "description": "Job Openings and Labor Turnover Survey",
        "primary_keys": ["series_id", "date"],
        "incremental": True,
        "config": {
            "series": ["JTS000000000000000JOL", "JTS000000000000000HIR", "JTS000000000000000QUL", "JTS000000000000000TSL"]
        }
    },

    # ===================
    # FED STRESS TEST SCENARIOS
    # ===================
    "fed_stress_scenarios": {
        "type": "fed_stress",
        "description": "Federal Reserve DFAST supervisory stress test scenarios (baseline & severely adverse)",
        "primary_keys": ["year", "table", "date"],
        "config": {
            "years": [2024, 2025],
            "scenarios": [
                "baseline_domestic",
                "baseline_international",
                "severely_adverse_domestic",
                "severely_adverse_international",
                "historic_domestic",
                "historic_international"
            ]
        }
    },

    # ===================
    # FFIEC CALL REPORTS
    # ===================
    "ffiec_call_reports": {
        "type": "ffiec",
        "description": "Quarterly bank call report bulk data from FFIEC Central Data Repository",
        "primary_keys": ["product", "schedule", "IDRSSD", "reporting_period"],
        "config": {
            "products": ["call_single"]  # Single-period call report schedules
        }
    }
}

# Dataset type categorization (for processing logic)
OHLCV_DATASETS = {
    "us_indices", "global_indices", "treasury_yields", "bond_etfs",
    "currencies", "commodities", "sector_etfs", "macro_proxies"
}

RSS_DATASETS = {
    "fed_news", "financial_news", "economics_news"
}

FRED_DATASETS = {
    "fred_gdp", "fred_employment", "fred_inflation", "fred_rates",
    "fred_money", "fred_housing", "fred_consumer", "fred_banking",
    "fred_stress_index", "fred_mev", "fred_market"
}

BLS_DATASETS = {
    "bls_cpi", "bls_employment", "bls_wages", "bls_ppi", "bls_jolts"
}

FED_STRESS_DATASETS = {
    "fed_stress_scenarios"
}

FFIEC_DATASETS = {
    "ffiec_call_reports"
}
