import scrapy

class LawinfoSpider(scrapy.Spider):
    name = 'lawinfo'
    allowed_domains = ['moleg.go.kr']
    start_urls = ['https://www.moleg.go.kr/lawinfo/nwLwAnList.mo?mid=a10106020000']

    def parse(self, response):
        # 안건 목록에서 안건 번호와 안건 명 추출
        for row in response.xpath('//*[@id="content_detail"]/div[2]/div/table/tbody/tr'):
            item = {}

            # 안건번호 추출 (두 번째 td에서 텍스트 추출)
            item['안건번호'] = row.xpath('.//td[2]/text()').get().strip() if row.xpath('.//td[2]/text()').get() else 'No Title'

            # 안건명 추출 (세 번째 td에서 a 태그 텍스트 추출)
            item['안건명'] = row.xpath('.//td[3]//a/text()').get().strip() if row.xpath('.//td[3]//a/text()').get() else 'No Title'

            # 항목 확인용 로그 추가
            self.log(f"Scraped item: {item}")

            # 안건번호 클릭 후, 상세 페이지로 이동하여 질의요지, 회답, 이유 추출
            detail_url = row.xpath('./td[2]/a/@href').get()
            if detail_url:
                yield response.follow(detail_url, callback=self.parse_detail, meta={'item': item})

        # 다음 페이지로 넘어가는 로직 추가 필요 (선택 사항)
        next_page = response.xpath('//*[@id="content_detail"]/div[2]/div/div/a[contains(text(), "다음")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        # 질의요지, 회답, 이유 추출
        item['질의요지'] = response.xpath('//*[@id="listForm"]/div/div[2]/strong/text()').get().strip() if response.xpath('//*[@id="listForm"]/div/div[2]/strong/text()').get() else 'No Question'
        item['회답'] = response.xpath('//*[@id="listForm"]/div/div[3]/strong/text()').get().strip() if response.xpath('//*[@id="listForm"]/div/div[3]/strong/text()').get() else 'No Answer'
        item['이유'] = response.xpath('//*[@id="listForm"]/div/div[4]/strong/text()').get().strip() if response.xpath('//*[@id="listForm"]/div/div[4]/strong/text()').get() else 'No Reason'

        yield item
