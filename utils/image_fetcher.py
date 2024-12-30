import os
from icrawler.builtin import BingImageCrawler  # Import the BingImageCrawler for fetching images

def fetch_images_bing(search_query, num_images, download_folder):
    """
    Fetches images from Bing based on the given search query.

    Parameters:
        search_query (str): The term to search for images.
        num_images (int): The number of images to fetch.
        download_folder (str): The folder where images will be saved.
    """
    # Create a BingImageCrawler instance with the specified download folder
    crawler = BingImageCrawler(storage={"root_dir": download_folder})

    # Use the crawl method to search and download images
    # - keyword: The term to search for on Bing
    # - max_num: The maximum number of images to download
    crawler.crawl(keyword=search_query, max_num=num_images)

    # No return value since images are saved directly to the folder
