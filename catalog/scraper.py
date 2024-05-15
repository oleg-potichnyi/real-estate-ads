import os
import django
import datetime
import requests
import json
import time
from app.settings import REAL_ESTATE_URL
from catalog.models import Scraper

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()


def scrape_real_estate() -> list[Scraper]:
    time.sleep(1)
    # Fetch data from realtylink.org
    response = requests.get(REAL_ESTATE_URL)
    if response.status_code == 200:
        # Parse JSON response
        real_estate_data = response.json()
        real_estate_listings = []
        # Limit the number of ads to 60
        count = 0
        for listing in real_estate_data:
            if count >= 60:
                break
            # Extract required information
            url = listing.get("url")
            ad_title = listing.get("ad_title")
            region = listing.get("region")
            address = listing.get("address")
            description = listing.get("description")
            image_urls = listing.get("image_urls")
            publish_date = listing.get("publish_date")
            price = listing.get("price")
            quantity_rooms = listing.get("num_rooms")
            area = listing.get("area")

            # Create Scraper instances for new listings
            if not Scraper.objects.filter(url=url).exists():
                real_estate_listings.append(
                    Scraper(
                        url=url,
                        ad_title=ad_title,
                        region=region,
                        address=address,
                        description=description,
                        image_urls=image_urls,
                        publish_date=publish_date,
                        price=price,
                        quantity_rooms=quantity_rooms,
                        area=area,
                        datetime_found=datetime.datetime.now(),
                    )
                )
                count += 1

        return real_estate_listings
    else:
        print("Failed to fetch data from realtylink.org")
        return []


def generate_json(real_estate_listings: list[Scraper]) -> None:
    # Convert Scraper instances to JSON format
    json_data = []
    for listing in real_estate_listings:
        json_data.append(
            {
                "url": listing.url,
                "ad_title": listing.ad_title,
                "region": listing.region,
                "address": listing.address,
                "description": listing.description,
                "image_urls": listing.image_urls,
                "publish_date": listing.publish_date,
                "price": listing.price,
                "quantity_rooms": listing.quantity_rooms,
                "area": listing.area,
            }
        )

    # Save JSON data to a file
    with open("real_estate_listings.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)


if __name__ == "__main__":
    listings = scrape_real_estate()
    if listings:
        generate_json(listings)
