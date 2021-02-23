import scrapy


class PitchforkSpider(scrapy.Spider):
    name = "pitchfork"

    def start_requests(self):
        i = 1
        while i < 10:
            i += 1
            urls = [
                "https://pitchfork.com/reviews/albums/?page={}".format(i)
            ]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        album_links = {}
        for review in response.css('div.review').css('a.review__link::attr(href)').getall():
            album_links['album_name'] = review
            yield response.follow(album_links['album_name'], callback=self.parse_albums)

    def parse_albums(self, response):
        yield {
            'artist': response.css("ul.artist-links").css("a::text").get(),
            'best_new_music': response.css('p.bnm-txt::text').get(),
            'album_name': response.css('h1.single-album-tombstone__review-title::text').get(),
            'album_score': response.css('span.score::text').get(),
            'album_label': response.css('li.labels-list__item::text').get(),
            'album_release_year': response.css('span.single-album-tombstone__meta-year::text').getall()[3],
            'pitchfork_author': response.css('a.authors-detail__display-name::text').getall(),
            'pitchfork_author_title': response.css('span.authors-detail__title::text').getall(),
            'genre': response.css('a.genre-list__link::text').getall(),
            'review_timestamp': response.css('time.pub-date::text').get(),
            'review_abstract': response.css('div.review-detail__abstract').css('p::text').getall(),
            'review_text': response.css('div.review-detail__text').css('p::text').getall()

        }
