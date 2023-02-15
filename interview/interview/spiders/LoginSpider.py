import scrapy


class LoginSpider(scrapy.Spider):
    name = "Login_spider"
    allowed_domains = ["demo.microdev.cd"]
    start_urls = ["http://demo.microdev.cd/"]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                "email": "esaie@microdev.cd",
                "password": "soleil"
            },
            callback=self.after_login
        )

    def after_login(self, response):
        if b"authentication failed" in response.body:
            self.logger.error("Login Failed")
            return
        else:
            self.logger.error("Login succeeded")
            return scrapy.Request(url="https://demo.microdev.cd/liste.php", callback=self.start_scrapping)

    @staticmethod
    def start_scrapping(response):
        cities_selector = 'ul'
        city_names = 'li::text'
        for city in response.css(cities_selector):
            yield {
                "cities": city.css(city_names).extract(),
            }
