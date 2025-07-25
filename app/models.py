import datetime

class URLMapping:
    """
    Holds data for one URL-shortener entry.

    Attributes:
        original_url (str): The full destination URL.
        created_at (str): ISO-formatted UTC timestamp of creation.
        clicks (int): Number of times this short URL has been used.
    """

    def __init__(self, original_url: str):
        self.original_url = original_url
        self.created_at = datetime.datetime.utcnow().isoformat()
        self.clicks = 0

    def increment_clicks(self):
        """Increase the click counter by one."""
        self.clicks += 1

    def to_dict(self):
        """
        Convert this mapping into a JSON-serializable dict.
        """
        return {
            "url": self.original_url,
            "created_at": self.created_at,
            "clicks": self.clicks,
        }
