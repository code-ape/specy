
from specy import end, when, item


class Book():
    def __init__(self, title, author, category):
        pass

    def read(self, page):
        return "WORDS are on page {}".format(page)



def describe(s=Book):
    def before_each():
        book = Book("Title", "Author", "category")
        return {"book": book}
    end()
    
    def new():
        def it(desc="returns a new book object"):
            item(book).should.be.instance_of(Book)
        end()

        def it(desc="throws an ArgumentError when given fewer than 3 parameters"):
            when(Book).called_with("Title", "Author").then.raises(TypeError)
            when(Book).init_with("Title").it.fails()
            when(Book).init_with("Title").it.fails_with(TypeError)
        end()
    end()

    def read():
        def it(desc="returns WORDS when called"):
            when(book.read).called_with(1).it.returns("WORDS are on page 1")
        end()
    end()


end()


