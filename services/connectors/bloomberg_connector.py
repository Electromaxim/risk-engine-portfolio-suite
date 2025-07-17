import pdblp
from lib_utils.logger import get_logger

logger = get_logger(__name__)

class BloombergConnector:
    def __init__(self, host: str = "localhost", port: int = 8194):
        self.con = pdblp.BCon(host=host, port=port)
        self.con.start()

    def fetch_equity_data(self, tickers: list, fields: list) -> pd.DataFrame:
        try:
            logger.info(f"Fetching Bloomberg data for {len(tickers)} assets")
            return self.con.bdh(tickers, fields, start_date="20200101")
        except pdblp.BlpapiException as e:
            logger.error(f"Bloomberg API error: {e}")
            raise ConnectionError("Failed to connect to Bloomberg") from e

    def close(self):
        self.con.stop()