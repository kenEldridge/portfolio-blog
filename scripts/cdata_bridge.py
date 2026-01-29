#!/usr/bin/env python3
"""
CData Bridge Module for the-derple-dex.

This module implements the "bridge pattern" for using cdata as a library.
Instead of reading Parquet files from cdata's storage, we:
1. Create SourceConfig objects programmatically
2. Use cdata's registry to fetch data
3. Return DataFrames that match the expected schema
4. Let the-derple-dex own its configuration and storage

See: https://github.com/kenEldridge/cdata/issues/4
"""

from datetime import datetime
from typing import Optional
import pandas as pd

from cdata.core.registry import get_registry
from cdata.config.schema import SourceConfig


class CDataBridge:
    """
    Bridge between the-derple-dex and cdata framework.

    This class provides high-level methods for fetching data from various sources
    using cdata as the fetch engine, while keeping configuration ownership in
    the-derple-dex application.
    """

    def __init__(self):
        """Initialize the bridge with lazy-loaded registry."""
        self._registry = None

    @property
    def registry(self):
        """Lazy-load the cdata registry on first access."""
        if self._registry is None:
            self._registry = get_registry()
        return self._registry

    def _create_source_config(self, source_id: str, source_type: str, config: dict,
                             primary_keys: list, incremental: bool = False) -> SourceConfig:
        """
        Create a SourceConfig object programmatically.

        Args:
            source_id: Unique identifier for this source
            source_type: Type of source (yfinance, fred, bls, rss, fed_stress)
            config: Configuration dict specific to the source type
            primary_keys: List of column names that uniquely identify records
            incremental: Whether to support incremental fetching

        Returns:
            SourceConfig object ready to be used by the registry
        """
        return SourceConfig(
            id=source_id,
            name=source_id,
            type=source_type,
            config=config,
            primary_keys=primary_keys,
            incremental=incremental
        )

    def _fetch_with_config(self, source_id: str, source_type: str, config: dict,
                          primary_keys: list, incremental: bool = False,
                          **fetch_kwargs) -> pd.DataFrame:
        """
        Generic fetch method that creates a source and returns data as DataFrame.

        Args:
            source_id: Unique identifier for this source
            source_type: Type of source (yfinance, fred, bls, rss, fed_stress)
            config: Configuration dict specific to the source type
            primary_keys: List of column names that uniquely identify records
            incremental: Whether to support incremental fetching
            **fetch_kwargs: Additional keyword arguments to pass to source.fetch()

        Returns:
            DataFrame with fetched data
        """
        # Create source config
        source_config = self._create_source_config(
            source_id=source_id,
            source_type=source_type,
            config=config,
            primary_keys=primary_keys,
            incremental=incremental
        )

        # Create source instance from registry
        source = self.registry.create_source(source_config)

        # Merge config with fetch kwargs
        fetch_params = {**config, **fetch_kwargs}

        # Fetch data
        result = source.fetch(**fetch_params)

        # Convert FetchResult to DataFrame
        if not result.records:
            return pd.DataFrame()

        # Add metadata columns
        data_rows = []
        for record in result.records:
            row = record.data.copy()
            row['_source_id'] = source_id
            row['_fetched_at'] = datetime.utcnow().isoformat()
            data_rows.append(row)

        return pd.DataFrame(data_rows)

    # ===================
    # YFINANCE (OHLCV)
    # ===================

    def fetch_yfinance_data(self, source_id: str, symbols: list,
                           period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """
        Fetch OHLCV data from Yahoo Finance.

        Args:
            source_id: Dataset identifier (e.g., "us_indices")
            symbols: List of ticker symbols (e.g., ["^GSPC", "^DJI"])
            period: Time period (e.g., "1y", "5y", "max")
            interval: Data interval (e.g., "1d", "1wk", "1mo")

        Returns:
            DataFrame with columns: symbol, date, open, high, low, close, volume
        """
        return self._fetch_with_config(
            source_id=source_id,
            source_type="yfinance",
            config={"symbols": symbols, "period": period, "interval": interval},
            primary_keys=["symbol", "date"],
            incremental=True
        )

    # ===================
    # RSS NEWS
    # ===================

    def fetch_rss_data(self, source_id: str, feeds: list) -> pd.DataFrame:
        """
        Fetch RSS feed data.

        Args:
            source_id: Dataset identifier (e.g., "fed_news")
            feeds: List of feed dicts with 'name' and 'url' keys

        Returns:
            DataFrame with columns: feed_name, feed_url, title, link, summary,
                                   author, published, id
        """
        return self._fetch_with_config(
            source_id=source_id,
            source_type="rss",
            config={"feeds": feeds},
            primary_keys=["id"]
        )

    # ===================
    # FRED ECONOMIC DATA
    # ===================

    def fetch_fred_data(self, source_id: str, series: list) -> pd.DataFrame:
        """
        Fetch economic data from FRED (Federal Reserve Economic Data).

        Args:
            source_id: Dataset identifier (e.g., "fred_gdp")
            series: List of FRED series IDs (e.g., ["GDP", "UNRATE"])

        Returns:
            DataFrame with columns: series_id, date, value, title, units, frequency
        """
        return self._fetch_with_config(
            source_id=source_id,
            source_type="fred",
            config={"series": series},
            primary_keys=["series_id", "date"],
            incremental=True
        )

    # ===================
    # BLS LABOR STATISTICS
    # ===================

    def fetch_bls_data(self, source_id: str, series: list) -> pd.DataFrame:
        """
        Fetch labor statistics from BLS (Bureau of Labor Statistics).

        Args:
            source_id: Dataset identifier (e.g., "bls_cpi")
            series: List of BLS series IDs (e.g., ["CUSR0000SA0"])

        Returns:
            DataFrame with columns: series_id, date, value, title, units, frequency
        """
        return self._fetch_with_config(
            source_id=source_id,
            source_type="bls",
            config={"series": series},
            primary_keys=["series_id", "date"],
            incremental=True
        )

    # ===================
    # FED STRESS TESTS
    # ===================

    def fetch_fed_stress_data(self, source_id: str, years: list,
                             scenarios: list) -> pd.DataFrame:
        """
        Fetch Federal Reserve stress test scenarios.

        Args:
            source_id: Dataset identifier (e.g., "fed_stress_scenarios")
            years: List of years (e.g., [2024, 2025])
            scenarios: List of scenario names (e.g., ["baseline_domestic"])

        Returns:
            DataFrame with columns: year, table, date, variable, value, scenario
        """
        return self._fetch_with_config(
            source_id=source_id,
            source_type="fed_stress",
            config={"years": years, "scenarios": scenarios},
            primary_keys=["year", "table", "date"]
        )


# Global bridge instance (singleton pattern)
_bridge = None

def get_bridge() -> CDataBridge:
    """Get or create the global CDataBridge instance."""
    global _bridge
    if _bridge is None:
        _bridge = CDataBridge()
    return _bridge


# Convenience functions for direct use
def fetch_data(source_id: str, source_type: str, config: dict,
              primary_keys: list, incremental: bool = False) -> pd.DataFrame:
    """
    Convenience function to fetch data using the global bridge.

    Args:
        source_id: Dataset identifier
        source_type: Type of source (yfinance, fred, bls, rss, fed_stress)
        config: Configuration dict specific to the source type
        primary_keys: List of column names that uniquely identify records
        incremental: Whether to support incremental fetching

    Returns:
        DataFrame with fetched data
    """
    bridge = get_bridge()
    return bridge._fetch_with_config(
        source_id=source_id,
        source_type=source_type,
        config=config,
        primary_keys=primary_keys,
        incremental=incremental
    )
