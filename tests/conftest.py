import json

import pytest


@pytest.fixture
def mock_collection_stats_response():
    class MockResponse:
        content = json.dumps(
            {
                "status": 1,
                "data": {
                    "results": {
                        "_id": "mock_id",
                        "collection_id": "mock_collection_id",
                        "collection": "Mock Collection",
                        "creator_id": "mock_creator_id",
                        "media": "mock_media",
                        "description": "A mock description",
                        "blurhash": "mock_blurhash",
                        "cover": "mock_cover",
                        "socialMedia": {
                            "twitter": "",
                            "discord": "",
                            "website": "https://mockproject.com/",
                        },
                        "updatedAt": 1666183589497,
                        "is_creator": True,
                        "floor_price": "8000000000000000000000000",
                        "has_floor_price": True,
                        "avg_price": "10829638340311804008908440",
                        "avg_price_usd": 116.0863919054166,
                        "owner_ids": ["mock_owner1", "mock_owner2", "mock_owner3"],
                        "total_cards": 4188,
                        "total_owners": 1236,
                        "total_sales": 4490,
                        "volume": "mock_volume",
                        "volume_usd": 521227.89965532057,
                        "updated_at": 1703368214552,
                        "total_card_sale": 337,
                        "total_card_not_sale": 3851,
                    }
                },
            }
        )

    return MockResponse()


@pytest.fixture
def mock_collection_data(mock_collection_stats_response):
    return json.loads(mock_collection_stats_response.content).get("data").get("results")
