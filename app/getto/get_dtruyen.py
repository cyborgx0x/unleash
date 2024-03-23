from fetch import Parser

tag = {
    "title": "title",
    "description": ".description",
    "author": ".author",
    "category": ".story_categories",
    "view": ".fa-eye",
    "rate": ".rate.rate-holder",
}

link = "https://dtruyen.com/yeu-em-sau-tan-sao-troi-kia/"
r = Parser(link, tag)
print(r.get_data())