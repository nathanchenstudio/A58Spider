# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# useful for handling different item types with a single interface


class LocalLPMProxyMiddleware(object):

    def process_request(self, request, spider):
        if 'dont_proxy' in request.meta and request.meta['dont_proxy']:
            return

        request.meta['proxy'] = 'http://127.0.0.1:24000'
