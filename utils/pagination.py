'''
依赖于bootstrap样式
使用： pages = Pagination(all_depart.count(), request.GET.get('page', 1)， per_num=10, page_disply=11)
数据[page.start:page.end]
前端展示 HTML page.page_html
'''

from django.utils.safestring import mark_safe
class Pagination:
    def __init__(self, total_count, page_num, per_num=10, page_disply=11):
        # 获取url中的页面数，如果不是指定数字类型，就赋值为第一页
        try:
            self.page_num = int(page_num)
        except Exception as e:
            self.page_num = 1

        self.total_count = total_count  # 获取queryset对象中的数据数量
        self.per_num = per_num  # 每页显示的数据条数
        self.page_disply = page_disply  # 显示的总分页数
        self.half_per = page_disply // 2
        self.page_total_num, more = divmod(total_count, per_num)  # 除法运算，返回两个数据，第一个为整除结果，第二个为余数

        # 如果有余数，页面数+1
        if more:
            self.page_total_num += 1

    @property      # 添加装饰器，直接转化为静态属性去调用
    def start(self):
        return (self.page_num - 1) * self.per_num

    @property
    def end(self):
        return self.page_num * self.per_num

    @property
    def page_html(self):
        # 如果总页数小于要显示的页数，就显示全部分页号
        if self.page_total_num < self.page_disply:
            page_start = 1
            page_end = self.page_total_num

        # 如果总页数大于等于显示的固定页数，就自动向前后移动固定间隔的页码
        else:

            # 限制显示的负数页码
            if self.page_num <= self.half_per:
                page_start = 1
                page_end = self.page_disply

            # 限制超出页码
            elif self.page_num >= self.page_total_num - self.half_per:
                page_start = self.page_total_num - self.page_disply + 1
                page_end = self.page_total_num
            else:
                page_start = self.page_num - self.half_per
                page_end = self.page_num + self.half_per

        # 点击分页按钮的选中效果
        page_list = []

        # 添加向前翻页效果，在第一页时禁止向前翻页
        if self.page_num == 1:
            page_list.append(
                '<li class="disabled"><a aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            page_list.append(
                '<li><a href="?page={}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                    self.page_num - 1))

        for i in range(page_start, page_end + 1):
            if i == self.page_num:  # 如果点击的分页正好是当前按钮，就添加选中效果
                page_list.append('<li class="active"><a href="?page={}">{}</a></li>'.format(i, i))
            else:
                page_list.append('<li><a href="?page={}">{}</a></li>'.format(i, i))

        # 添加向后翻页效果，在最后一页时，禁止向后翻页
        if self.page_num == self.page_total_num:
            page_list.append(
                '<li class="disabled"><a aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            page_list.append(
                '<li><a href="?page={}" aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                    self.page_num + 1))

        # 生成html页面,使用mark_safe后，前端就不需要使用{{ page|safe }}的方式，直接使用{{ page }}
        return mark_safe(''.join(page_list))
