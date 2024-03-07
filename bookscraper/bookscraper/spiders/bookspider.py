import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
            book_link = book.css("h3 a::attr(href)").get()
            yield response.follow(book_link, self.parse_book)


        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page, self.parse)


    def parse_book(self, response):
        yield {
            "title": response.css("div.product_main h1::text").get(),
            "description": response.xpath('//article[@class="product_page"]/p/text()').get(),
            "upc": response.css("table.table-striped td::text").get(),
            "product_type": response.css("table.table-striped td::text")[1].get(),
            "catagory": response.xpath('//ul[@class="breadcrumb"]/li[@class="active"]/preceding-sibling::li[1]/a/text()').get(),
            "price_excl_tax": response.css("table.table-striped td::text")[2].get(),
            "price_incl_tax": response.css("table.table-striped td::text")[3].get(),
            "tax": response.css("table.table-striped td::text")[4].get(),
            "availability": response.css("table.table-striped td::text")[5].get(),
            "number_of_reviews": response.css("table.table-striped td::text")[6].get(),
        }


