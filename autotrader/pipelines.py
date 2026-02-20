import os
import time
from pathlib import Path
from urllib.parse import urlparse

from scrapy.spiders import Request
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline


from autotrader.autotrader.static import headers, handle_httpstatus_list


def get_images_dir_path():
    # return os.path.dirname(__file__)
    # return str(Path().absolute())
    return "/".join(str(Path.cwd()).split('/')[:-1]) + "/images"


class DownloadImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        keyword = request.meta['kw']
        img_id = request.meta['img_id']
        ex = os.path.basename(urlparse(request.url).path).split('.')[-1]
        # return f"{keyword}/{img_id}_{os.path.basename(urlparse(request.url).path)}"
        return f"{keyword}/{img_id}.{ex}"

    def get_media_requests(self, item, info):
        for i, url in enumerate(item['image_urls'], start=1):
            if not url:
                continue
            meta = {
                'kw': item['id'],
                'img_id': f"{i}",
                'handle_httpstatus_list': handle_httpstatus_list,
            }
            yield Request(url=url, headers=headers, meta=meta)

    def item_completed(self, results, item, info):
        image_paths = [f"{get_images_dir_path()}/{x['path']}" for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter['image_paths'] = image_paths
        return item
