import time


def retry_invalid_response(callback):
    def wrapper(spider, response):
        if response.status >= 400:
            if response.status == 404:
                print('Page not 404')
                return

            retry_times = response.meta.get('retry_times', 0)
            if retry_times < 3:
                time.sleep(2)
                response.meta['retry_times'] = retry_times + 1
                return response.request.replace(dont_filter=True, meta=response.meta)

            print("Dropped after 3 retries. url: {}".format(response.url))
            response.meta.pop('retry_times', None)
        return callback(spider, response)

    return wrapper
