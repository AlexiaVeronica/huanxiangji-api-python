import re
from lib import request

from scrapy import Selector


#
class Book:

    @staticmethod
    def get_book_info(book_id) -> dict:
        """
        获取书籍信息
        :param book_id: 书籍id
        :return: 书籍信息
        """
        response = request.get('/book/{}/'.format(book_id))
        if response.status_code == 200:
            selector = Selector(text=str(response.text))
            root_xpath = "/html/body/div[3]/div[1]/div/div/div"
            return {
                "code": response.status_code,
                "book_name": selector.xpath(root_xpath + "[2]/div[1]/h1/text()").get(),
                "book_author": selector.xpath(root_xpath + "[2]/div[1]/div/p[1]/text()").get().replace("作者：", ""),
                "book_state": selector.xpath(root_xpath + "[2]/div[1]/div/p[3]/text()").get().replace("状态：", ""),
                "book_update": selector.xpath(root_xpath + "[2]/div[1]/div/p[5]/text()").get().replace("最后更新：", ""),
                "book_introduce": "\n".join(selector.xpath(root_xpath + "[3]/div/text()").getall()),
                "book_img": selector.xpath(root_xpath + "[1]/img/@src").get(),
                "book_catalogue": [
                    {"index": index, "chapter_id": info.xpath('@href').get(),
                     "chapter_name": info.xpath('text()').get()}
                    for index, info in enumerate(selector.xpath('//*[@id="section-list"]/li/a'), start=1)
                ]
            }

    @staticmethod
    def get_chapter_content(book_id: str, chapter_id: str) -> dict:
        """
        获取章节内容
        :param book_id: 书籍id
        :param chapter_id: 章节id
        :return: 章节内容
        """
        response = request.get("/book/{}/{}".format(book_id, chapter_id))
        if response.status_code == 200:
            return {
                "book_id": book_id,
                "chapter_id": chapter_id,
                "chapter_content": Selector(text=str(response.text)).xpath('//*[@id="content"]').get(),
            }


class Search:
    @staticmethod
    def post_search(search_key: str):
        """
        搜索书籍
        :param search_key: 搜索关键字
        :return: 书籍列表
        """
        response = request.post('/modules/article/search.php', data={'searchkey': search_key})
        return [{"index": index, "book_id": book_id, "book_name": book_name} for index, (book_id, book_name) in
                enumerate(re.findall(r"<a href=\"http://www.huanxiangji.com/book/(\d+)/\">(.*?)</a>", response.text))]


class Account:

    @staticmethod
    def add_bookshelf(book_id: int) -> dict:
        """
        添加书籍到书架
        :param book_id: 书籍id
        :return: 添加结果
        """
        if request.DEFAULT_COOKIE == "":
            return {"code": 403, "msg": "请先登录"}
        response = request.post('/modules/article/addbookcase.php', {
            "action": "addbookmark",
            "bid": book_id,
            "cid": 0,
            "chapterName": ""
        })
        if response.text.find("恭喜您，该文章已经加入书架，您可以关闭本窗口！") != -1:
            return {"code": response.status_code, "msg": "添加成功"}
        else:
            return {"code": response.status_code, "msg": "添加失败"}

    @staticmethod
    def register(username: str, password: str, email: str) -> dict:
        """
        注册账号
        :param username: 用户名
        :param password: 密码
        :param email: 邮箱
        :return: 注册结果, cookie
        """
        response = request.post('/register.php', {
            "username": username,
            "password": password,
            "repassword": password,
            "email": email,
            "action": "newuser"
        })
        if response.status_code == 200:
            if response.text.find("注册成功") != -1:
                request.DEFAULT_COOKIE = response.headers['Set-Cookie']
                return {"code": response.status_code, "msg": "注册成功", "cookie": response.headers['Set-Cookie']}
            else:
                return {"code": response.status_code, "msg": "注册失败", "data": None}

    @staticmethod
    def get_bookshelf() -> dict:
        """
        获取书架
        :return: 书架列表
        """
        if request.DEFAULT_COOKIE == "":
            return {"code": 403, "msg": "请先登录"}
        response = request.get('/modules/article/bookcase.php')
        if response.status_code == 200:
            author_list = re.findall(r"<td class=\"xs-hidden\">(.+)</td>", response.text)
            book_list = re.findall(
                r'<td><a href="http://www.huanxiangji.com/modules/article/readbookcase.php\?aid=(.+)&bid=(.+)">(.+)</a>',
                response.text)
            index = 0
            bookshelf = []
            for i in range(len(book_list)):
                if book_list[i][1].find('cid') != -1:
                    continue
                index += 1
                bookshelf.append({
                    "index": index,
                    "author": author_list[i],
                    "book_id": book_list[i][0],
                    "shelf_id": book_list[i][1],
                    "book_name": book_list[i][2],
                })
            return {"code": response.status_code, "book_list": bookshelf}
