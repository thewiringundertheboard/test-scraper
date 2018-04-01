import scrapy


class TestScraperSpider(scrapy.Spider):

    name = 'test_scraper'
    url = 'http://testing-ground.scraping.pro'

    start_urls = [
        url
    ]

    def parse(self, response):

        if response.url == self.url:

            # follow links to individual pages
            for link in response.xpath('//div[@id="content"]/div[@class="caseblock"]'):

                # extract the label and url
                label = link.xpath('./div[@class="casedescr"]/text()').extract_first()
                url = link.xpath('./a/@href').extract_first()

                # follow the table report url
                if label == 'complicated block layout presented as a price list':
                    yield response.follow(url, callback=self.parse)
        else:

            # loop through the two cases
            for case_array in response.xpath('//div[@id="case_blocks"]/*[starts-with(@id, "case")]'):

                # retrieve the current case ID
                case = case_array.xpath('@id').extract_first()

                # extract differently depending on case
                if case == 'case1':

                    # loop through the products, ignore ads
                    for product in case_array.xpath('./div[starts-with(@class, "prod")]'):
                        name = product.xpath('./span/div[@class="name"]/text()').extract_first()
                        desc = product.xpath('./span[1]/text()').extract_first()
                        price = product.xpath('./span[2]/text()').extract_first()

                        yield {
                            'name': name,
                            'desc': desc,
                            'price': price
                        }

                if case == 'case2':

                    # loop through each class="left" div
                    for div in case_array.xpath('//div[@class="left"]'):
                        # set a row number so we can find the corresponding price row
                        row = 1
                        # loop through each product within
                        for product in div.xpath('./*[starts-with(@class, "prod")]'):

                            name = product.xpath('./div[@class="name"]/text()').extract_first()
                            desc = product.xpath('./text()').extract_first()

                            # find the price in the corresponding class="right" div
                            price = div.xpath('./following-sibling::div[1][@class="right"]/\
                            div[starts-with(@class, "price")][' + str(row) + ']\
                                              /text()').extract_first()
                            row += 1

                            yield {
                                'name': name,
                                'desc': desc,
                                'price': price
                            }