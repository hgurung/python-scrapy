from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message


class RetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response

        # this is your check
        if response.status == 200 and response.xpath(spider.retry_xpath):
            return self._retry(request, 'response got xpath "{}"'.format(spider.retry_xpath), spider) or response
        return response