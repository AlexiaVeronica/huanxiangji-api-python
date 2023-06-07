# 项目文档

## 概述

本项目为基于 Python 的幻想姬小说三方接口，能够提供以下功能：

- 获取指定书籍的信息
- 获取指定书籍章节内容
- 搜索书籍
- 添加书籍到书架
- 注册账号
- 获取书架

## 使用说明

### Book 类

#### `get_book_info(book_id: str) -> dict`

- 获取指定书籍的信息

  - 参数：
      - `book_id`：要获取信息的书籍 ID（字符串）

  - 返回值：
      - 字典类型，包含如下键值对：
          - `"code"`：http 响应码（整数）
          - `"book_name"`：书籍名称（字符串）
          - `"book_author"`：作者（字符串）
          - `"book_state"`：状态（字符串）
          - `"book_update"`：最后更新时间（字符串）
          - `"book_introduce"`：简介（字符串）
          - `"book_img"`：封面图片链接（字符串）
          - `"book_catalogue"`：目录列表（列表），每个元素是一个字典类型，包含如下键值对：
              - `"index"`：章节序号（整数）
              - `"chapter_id"`：章节 ID（字符串）
              - `"chapter_name"`：章节名称（字符串）

#### `get_chapter_content(book_id: str, chapter_id: str) -> dict`

- 获取指定书籍章节内容

  - 参数：
      - `book_id`：书籍 ID（字符串）
      - `chapter_id`：章节 ID（字符串）

  - 返回值：
      - 字典类型，包含如下键值对：
          - `"book_id"`：书籍 ID（字符串）
          - `"chapter_id"` 章节 ID（字符串）
          - `"chapter_content"`：章节内容（字符串）

 

### Search 类
 
#### `post_search(search_key: str) -> List[Dict[str, Any]]`
  - 搜索书籍
  
  - 参数：
      - `search_key: str` - 搜索关键字
  
  - 返回值：
      - `List[Dict[str, Any]]` - 包含搜索结果的列表，每个元素是一个包含以下字段的字典：
          - `index: int` - 搜索结果在结果列表中的序号（从0开始）
          - `book_id: int` - 书籍id
          - `book_name: str` - 书籍名称


### Account 类 

#### `add_bookshelf(book_id: int) -> Dict[str, Union[int, str]]`
  - 添加书籍到书架
  
  - 参数：
      - `book_id: int` - 书籍id
  
  - 返回值：
      - `Dict[str, Union[int, str]]` - 添加结果，包含以下字段：
          - `code: int` - HTTP状态码
          - `msg: str` - 添加结果信息

#### `register(username: str, password: str, email: str) -> Dict[str, Union[int, str, None]]`
- 注册账号

  - 参数：
      - `username: str` - 用户名
      - `password: str` - 密码
      - `email: str` - 邮箱
  
  - 返回值：
      - `Dict [str, Union[int, str, None]]` - 注册结果，包含以下字段：
          - `code: int` - HTTP状态码
          - `msg: str` - 注册结果信息
          - `cookie: str` - 注册成功时返回的token，失败时为None
          

#### `get_bookshelf() -> dict`
  - 该方法用于获取用户书架信息，返回一个字典类型包含以下字段：
    - `code`：状态码，成功返回200，未登录返回403。
    - `book_list`：书架列表，包含多本书籍信息，每一本书籍信息包含以下字段：
        - `index`：书籍在书架中的索引。
        - `author`：作者姓名。
        - `book_id`：书籍ID。
        - `shelf_id`：书架ID。
        - `book_name`：书籍名称。

  - 参数无需传入参数。