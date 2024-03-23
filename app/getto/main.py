from .fetch import Parser
from .gac_sach import GacSach
import click
from typing import Dict, List
class Context():
    def __init__(self, parser: Parser):
        self._parser = parser


    def run(self):
        return self._parser.get_chapter_content()

    @property
    def parser(self) -> Parser:
        return self.strategy
    
    @parser.getter
    def parser(self, parser: Parser) -> None:
        self._parser = parser

def main():
    link = "https://gacsach.online/di-qua-hoa-cuc_nguyen-nhat-anh.full"
    context = Context(GacSach(link))
    content = context.run()
    export_docx("Đi qua hoa cúc", content)


def export_docx(heading: str, content: List):
    book = Document()
    file_name = f"{heading}.docx"
    book.add_heading(heading, 0)
    for i in content:
        for (key, value) in i.items():
            if key == "title":
                book.add_heading(value, level = 1)
            if key == "content":
                book.add_paragraph(value)
    book.save(file_name)
    print(file_name)
if __name__ == "__main__":
    main()

