from datetime import datetime
from typing import Literal

class Poll: ...

class Mastodon:
    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        access_token: str,
        api_base_url: str,
    ) -> None: ...
    def toot(self, status: str) -> dict[str, object]: ...
    def status_post(  # noqa: PLR0913
        self,
        status: str,
        in_reply_to_id: str | None = None,
        media_ids: list[str] | None = None,
        sensitive: bool = False,  # noqa: FBT001, FBT002
        visibility: Literal['direct', 'private', 'unlisted', 'public']
        | None = None,
        spoiler_text: str | None = None,
        language: str | None = None,
        idempotency_key: str | None = None,
        content_type: str | None = None,
        scheduled_at: datetime | None = None,
        poll: Poll | None = None,
        quote_id: str | None = None,
    ) -> dict[str, object]: ...
