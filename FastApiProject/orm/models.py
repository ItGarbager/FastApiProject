"""
@Time    : 2021/11/29 11:48
@Author  : Musuer
@Contact : linxuzhao2018@163.com
@File    : models.py
@Software: PyCharm
"""
from tortoise import models, fields


class TimestampMixin:
    id = fields.BigIntField(pk=True)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)

    class Meta:
        abstract = True


class Users(models.Model, TimestampMixin):
    uid = fields.BigIntField(null=False)
    sec_uid = fields.CharField(max_length=512, null=True)
    nickname = fields.CharField(max_length=255, null=False, default='')
    gender = fields.IntField(null=False, default=2)
    head_img = fields.CharField(max_length=255, null=False, default='')

    def full_name(self) -> str:
        """
        Returns the best name
        """
        return self.nickname

    # class PydanticMeta:
    #     computed = ["full_name"]
    #     exclude = ["password_hash"]

    class Meta:
        table = 'users'
