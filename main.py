import app
from rich import print

if __name__ == '__main__':
    app.Account.register("", "", "@qq.com")
    print(app.Account.add_bookshelf(65))
    print(app.Account.add_bookshelf(44))
    print(app.Account.add_bookshelf(33))
    print(app.Account.get_bookshelf())
