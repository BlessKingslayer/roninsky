1. django-admin 中， 若带有 choices 属性的字段时，Django 会自动调用 get_status_display 方法，无需手动配置
2. 在 form 中使用 raise forms.ValidationError('错误信息') 的方式返回错误信息，这个信息会存储在 Form 中，最终可以渲染到页面上
3. 继承 forms.ModelForm 的子类中，
    * 可以通过 self.cleaned_data['字段名'] 来获取字段数据
    * 可以定义 clean_字段名 的方法来处理字段，Form会自动调用
4. 通过 django.urls 中的 reverse 方法，传入路由名, 可以获取指定定义的url, 如 reverse('index')
5. {% csrf_token %} 是 Django 对提交数据安全性的校验, 如果没有这个 token，提交过去的数据则是无效的, 是用来防止跨站伪造请求攻击的一个手段
---
6. 每一个 test_ 开头的函数都是独立运行的，因此 setup 和 teardown 也会在每个函数运行时被执行
7. 单元测试 https://www.jianshu.com/p/34267dd79ad6
    ```
    # 测试整一个工程
    $ ./manage.py test 

    # 只测试某个应用
    $ ./manage.py test app --keepdb


    # 只测试一个Case
    $ ./manage.py test animals.tests.StudentTestCase

    # 只测试一个方法
    $ ./manage.py test animals.tests.StudentTestCase.test_add
    ```
8. python3 中 response.content 的内容是 bytes 类型, 所以需要在要对比的字符串前面加b来声明它是 bytes 而不是 str
9. 编码规范
    * 标准库导入
    * 相关第三方库导入
    * 本地应用/库特定导入 
    * 你应该在每一组导入之间加入空行。
    * 避免通配符的导入（from import *），因为这样做会不知道命名空间中存在哪些名字，会使得读取接口和许多自动化工具之间产生混淆
10. Django 引用顺序
    ```python
    # future
    from __future__ import unicode_literals

    # standard library
    import json
    from itertools import chain

    # third-party
    import bcrypt

    # Django
    from django.http import Http404
    from django.http.response import (
        Http404, HttpResponse, HttpResponseNotAllowed, StreamingHttpResponse, cookie,
    )

    # local Django
    from .models import LogEntry

    # try/except
    try:
        import yaml
    except ImportError:
        yaml = None

    CONSTANT = 'foo'


    class Example:
        pass
    ```