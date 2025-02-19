import datetime
import time
import json
import cloudscraper

def generate_time_ranges(start_dt, end_dt, increment_hours):
    """
    Yield (start_str, end_str) time chunks between start_dt and end_dt
    in increments of `increment_hours`.

    Both `start_dt` and `end_dt` should be datetime.datetime objects.
    The returned strings are in the format "YYYY-MM-DD HH:MM:SS".
    """
    current = start_dt
    delta = datetime.timedelta(hours=increment_hours)

    while current < end_dt:
        next_dt = current + delta
        if next_dt > end_dt:
            next_dt = end_dt
        # Format as "YYYY-MM-DD HH:MM:SS"
        start_str = current.strftime("%Y-%m-%d %H:%M:%S")
        end_str = next_dt.strftime("%Y-%m-%d %H:%M:%S")
        yield (start_str, end_str)
        current = next_dt

def scrape_time_chunk(scraper, start_str, end_str, text="elon", boards="pol"):
    """
    Paginate through the 4plebs search API for a given start/end time range,
    collecting all posts. Returns a list of post records.
    """
    base_url = "https://archive.4plebs.org/_/api/chan/search/"
    all_records = []
    page = 1

    while True:
        params = {
            'text': text,
            'boards': boards,
            'start': start_str,  # e.g. "2025-01-20 00:00:00"
            'end': end_str,      # e.g. "2025-01-20 04:00:00"
            'results': 'post',
            'page': page
        }

        print(f"Requesting page {page} for range {start_str} to {end_str}...")

        response = scraper.get(base_url, params=params)
        print("Status code:", response.status_code)

        if response.status_code != 200:
            print("Non-200 status code, stopping pagination for this chunk.")
            break

        data = response.json()
        page_records = data.get('0', {}).get('posts', [])
        record_count = len(page_records)
        print(f"Page {page} returned {record_count} records.")

        # Add them to our master list
        all_records.extend(page_records)

        # If fewer than 25 records, assume no more pages
        if record_count < 25:
            print("Fewer than 25 records returned; stopping pagination for this chunk.")
            break

        page += 1

        # Sleep to respect rate limiting
        time.sleep(5)

    return all_records

def scrape_4plebs_date_range(
    start_date="2025-01-20 00:00:00",
    end_date="2025-01-21 00:00:00",
    increment_hours=4,
    text="elon",
    boards="pol"
):
    """
    Scrape the 4plebs search endpoint in increments of `increment_hours` within
    the given date/time range. Accumulate all posts and save to a file.
    """

    # 1) Convert input strings to datetime objects
    #    Accepts "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"
    fmt = "%Y-%m-%d %H:%M:%S" if " " in start_date else "%Y-%m-%d"
    start_dt = datetime.datetime.strptime(start_date, fmt)
    end_dt = datetime.datetime.strptime(end_date, fmt)

    # 2) Initialize cloudscraper
    scraper = cloudscraper.create_scraper(browser='chrome')

    # 3) Set up a unique user agent
    unique_user_agent = (
        "MyResearchScraper/1.0 "
        "(Email: my_email@example.com; "
        "Purpose: 4plebs research project Jan 2025)"
    )
    scraper.headers.update({
        "User-Agent": unique_user_agent,
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,image/apng,*/*;"
            "q=0.8,application/signed-exchange;v=b3;q=0.7"
        ),
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
    })

    # 4) Generate time chunks and scrape each one
    all_results = []
    for (start_str, end_str) in generate_time_ranges(start_dt, end_dt, increment_hours):
        chunk_records = scrape_time_chunk(scraper, start_str, end_str, text=text, boards=boards)
        all_results.extend(chunk_records)

    # 5) Save final results to JSON
    out_filename = (
    "4plebs_"
    + start_date.replace(" ", "_").replace(":", "-")
    + "_to_"
    + end_date.replace(" ", "_").replace(":", "-")
    + ".json")

    with open(out_filename, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n[+] Done. Collected {len(all_results)} records total.")
    print(f"    Saved to {out_filename}")

if __name__ == "__main__":
    # Example usage:
    # Scrape from "2025-01-20 00:00:00" to "2025-01-21 00:00:00" in 4-hour increments
    scrape_4plebs_date_range(
        start_date="2025-01-20 00:00:00",
        end_date="2025-01-20 23:59:59",
        increment_hours=4,
        text="elon",
        boards="pol"
    )
