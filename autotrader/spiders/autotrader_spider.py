import json
import os
from copy import deepcopy
from pathlib import Path

from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess

from autotrader.autotrader.core.decorators import retry_invalid_response
from autotrader.autotrader.static import listings_filters_data, handle_httpstatus_list, details_data, fuel_types, \
    manufacturers


def get_cur_dir_abs_path():
    # return os.path.dirname(__file__)
    # return str(Path().absolute())
    return "/".join(str(Path.cwd()).split('/')[:-1])


def get_current_file_name():
    return os.path.basename(__file__)


class AutotraderCoUkSpider(Spider):
    name = "autotrader_co_uk_spider"
    filepath = '../output/autotrader_cars.csv'
    images_dir = f"{get_cur_dir_abs_path()}/images"
    base_url = "https://www.autotrader.co.uk/"
    listings_url = "https://www.autotrader.co.uk/at-gateway?opname=SearchResultsListingsGridQuery"
    overview_url_t = "https://www.autotrader.co.uk/product-page/v1/advert/{advert_id}?channel=cars"
    details_url = "https://www.autotrader.co.uk/at-graphql?opname=FPADataQuery"
    vehicle_url_t = "https://www.autotrader.co.uk/car-details/{id}"

    csv_headers = [
        "id", "type", "advert_id", "title", "sub_title", "mileage", "mileage_unit", "attention_grabber",
        "vehicle_location", "discount", "price_indicator_rating", "battery_capacity", "battery_capacity_unit",
        "usable_capacity", "usable_capacity_unit", "range", "range_unit", "price", "price_excluding_vat",
        "vat_to_be_paid_upfront", "vat_status", "registration_year", "registration_date", "plate", "license_number",
        "registration_hidden", "link", "vehicle_check_status", "seller_name", "seller_type", "seller_rating",
        "seller_phone_one", "seller_phone_two", "colour", "condition", "emission_class", "seats", "doors",
        "body_type", "cab_type", "fuel", "transmission", "style", "make", "model", "image_urls", "all_image_urls",
        "image_paths",
    ]

    meta = {
        'handle_httpstatus_list': handle_httpstatus_list,
    }

    feeds = {
        filepath: {
            'format': 'csv',
            'encoding': 'utf8',
            'fields': csv_headers,
            'indent': 4,
            'overwrite': True,
        }
    }

    custom_settings = {
        # 'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 2,
        'FEEDS': feeds,

        'ITEM_PIPELINES': {
            'autotrader.autotrader.pipelines.DownloadImagesPipeline': 100,
        },

        'IMAGES_STORE': images_dir,
        'IMAGES_URLS_FIELD': 'image_urls',
        'IMAGES_RESULT_FIELD': 'images',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://www.autotrader.co.uk',
        'priority': 'u=1, i',
        'referer': 'https://www.autotrader.co.uk/',
        'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'x-sauron-app-name': 'sauron-search-results-app',
        'x-sauron-app-version': '730384378d',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not os.path.exists(self.images_dir):
            os.mkdir(self.images_dir)

    async def start(self):
        yield Request(url=self.base_url, callback=self.parse, headers=self.headers, meta=self.meta)

    def parse(self, response, **kwargs):
        # for year in range(2017, 2025):
        for year in range(2020, 2025):
            for fuel in fuel_types:
                body = deepcopy(listings_filters_data)

                for i, rec in enumerate(body[0]['variables']['filters']):
                    self.update_filters(body, ['max_year_manufactured', 'min_year_manufactured'], f'{year}')

                    if rec['filter'] in ['max_year_manufactured', 'min_year_manufactured']:
                        body[0]['variables']['filters'][i]['selected'] = [f'{year}']
                    self.add_or_update_filter(body, 'fuel_type', fuel)

                    # for make in manufacturers['filters'][0]['options']:
                    #     req_body = deepcopy(body)
                    #     self.add_or_update_filter(req_body, 'make', make['value'])
                    #
                    #     meta = deepcopy(self.meta)
                    #     meta['req_body'] = deepcopy(req_body)
                    #
                    #     yield Request(url=self.listings_url, callback=self.parse_listings, headers=self.headers,
                    #                   method='POST', body=json.dumps(req_body), meta=meta)

                meta = deepcopy(self.meta)
                meta['req_body'] = deepcopy(body)
                yield Request(url=self.listings_url, callback=self.parse_search_results, headers=self.headers,
                              method='POST', body=json.dumps(body), meta=meta)
                return

    @retry_invalid_response
    def parse_search_results(self, response):
        data = json.loads(response.text)

        if data[0]['data']['searchResults']['page']['count'] < 100:
            yield from self.parse_listings(response)
        else:
            for make in manufacturers['filters'][0]['options']:
                req_body = deepcopy(response.meta['req_body'])
                self.add_or_update_filter(req_body, 'make', make['value'])

                meta = deepcopy(self.meta)
                meta['req_body'] = req_body

                yield Request(url=self.listings_url, callback=self.parse_listings, headers=self.headers,
                              method='POST', body=json.dumps(req_body), meta=meta)

    @retry_invalid_response
    def parse_listings(self, response):
        data = json.loads(response.text)

        for result in data:
            if 'listings' not in result['data']['searchResults']:
                continue
            for r in result['data']['searchResults']['listings'][:]:
                try:
                    item = {}
                    item["type"] = r["type"]
                    item["advert_id"] = r["advertId"]
                    item["title"] = r["title"]
                    item["sub_title"] = r.get('subTitle') or ''
                    item["attention_grabber"] = r.get('attentionGrabber') or ''
                    item["price"] = r["price"]
                    item["image_urls"] = [img.replace('{resize}/', '') for img in r['images'] if img]
                    item["vehicle_location"] = r.get('vehicleLocation') or ''
                    item["discount"] = r.get("discount") or ''
                    item["price_indicator_rating"] = r.get('priceIndicatorRating') or ''
                    item["seller_type"] = r.get("sellerType") or ''
                    item["seller_rating"] = (r.get('dealerReview') or {}).get('overallReviewRating') or ''

                    meta = deepcopy(self.meta)
                    meta['item'] = item

                    body = deepcopy(details_data)
                    self.update_variable_value('advertId', r["advertId"], body)
                    yield Request(url=self.details_url, callback=self.parse_details, method="POST",
                                  headers=self.headers, body=json.dumps(body), meta=meta)
                except Exception as err:
                    print(err)
                    a = 0

        total_pages_count = data[0]['data']['searchResults']['page']['count']
        next_page_number = self.get_and_update_next_page_count(response.meta['req_body'])
        response.meta.setdefault('total_pages', 0)

        if not response.meta['total_pages'] and total_pages_count:
            response.meta['total_pages'] = total_pages_count

        if next_page_number > total_pages_count and next_page_number > response.meta['total_pages']:
            return

        # yield Request(url=self.listings_url, callback=self.parse_listings, headers=self.headers,
        #               method='POST', body=json.dumps(response.meta['req_body']), meta=response.meta)

    def parse_details(self, response):
        data = json.loads(response.text)
        rec = data[0]['data']['search']['advert']
        specs = rec.get('specification') or {}

        item = response.meta['item']
        item["id"] = rec['id']
        item["vat_status"] = rec.get('vatStatus') or ''
        item["mileage"] = (rec.get('mileage') or {}).get('mileage') or ''
        item["mileage_unit"] = (rec.get('mileage') or {}).get('unit') or ''
        item["registration_hidden"] = rec['registration']
        item["registration_date"] = rec["dateOfRegistration"]
        item["registration_year"] = rec["year"]
        item["is_part_ex_available"] = rec.get("isPartExAvailable") or ""
        item["is_finance_available"] = rec.get("isFinanceAvailable") or ""
        item["finance_provider"] = rec.get("financeProvider") or ""
        item["vehicle_check_status"] = rec.get("vehicleCheckStatus") or ""
        item["price_excluding_vat"] = rec.get("priceExcludingVat") or ""
        item["vat_to_be_paid_upfront"] = rec.get("vatToBePaidUpfront") or ""
        item["seller_name"] = rec.get("sellerName") or ""
        item["seller_type"] = rec.get("sellerType") or ""
        item["seller_phone_one"] = (rec.get("sellerContact") or {}).get('phoneNumberOne')
        item["seller_phone_two"] = (rec.get("sellerContact") or {}).get('phoneNumberTwo')
        item["colour"] = rec.get("colour") or ""
        item["condition"] = rec.get("condition") or ""
        item["emission_class"] = rec.get("emissionClass") or ""
        item["seats"] = specs.get("seats") or ""
        item["doors"] = specs.get("doors") or ""
        item["body_type"] = specs.get("bodyType") or ""
        item["cab_type"] = specs.get("cabType") or ""
        item["fuel"] = specs.get("fuel") or ""
        item["transmission"] = specs.get("transmission") or ""
        item["make"] = specs.get("make") or ""
        item["model"] = specs.get("model") or ""
        item['link'] = self.vehicle_url_t.format(**rec)
        item['all_image_urls'] = [r['url'].replace('{resize}/', '') for r in
                                  (rec.get('imageList') or {}).get('images') or []]
        item['license_number'] = ""
        return item

    def get_and_update_next_page_count(self, req_body):
        req_body[0]['variables']['page'] += 1
        return req_body[0]['variables']['page']

    def update_variable_value(self, var_name, var_value, data):
        data[0]['variables'][var_name] = var_value
        return data

    def update_filters(self, body, filter_names, value):
        for i, rec in enumerate(body[0]['variables']['filters']):
            if rec['filter'] in filter_names:
                body[0]['variables']['filters'][i]['selected'] = [value]

    def add_or_update_filter(self, body, name, value):
        for i, rec in enumerate(body[0]['variables']['filters']):
            if rec['filter'] == name:
                body[0]['variables']['filters'][i]['selected'] = [value]
                return

        new_filter = {
            'filter': name,
            'selected': [
                value,
            ],
        }

        body[0]['variables']['filters'].append(new_filter)
        a = 0


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(AutotraderCoUkSpider)
    process.start()
