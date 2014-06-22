
from core import end, when, item


class Book():
    def __init__(self, title, author, category):
        pass


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
end()


