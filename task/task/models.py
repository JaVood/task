from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext as _


class Element(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name=_('Element'))

    image = models.ImageField(
        verbose_name=_('Image'),
        blank=False
        )

    description = models.CharField(
        max_length=512,
        blank=True,
        verbose_name=_('Description')
    )

    created = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Created at')
    )

    check_by_moderator = models.NullBooleanField(
        verbose_name=_('Check by moderator'),
    )

    group = models.ForeignKey(
        to='Group',
        related_name='elements',
        verbose_name=_('Group'),
        on_delete=models.PROTECT,
        blank=False
    )

    group_check = models.IntegerField(
        default=-1,
        verbose_name='group check'
    )

    class Meta:
        db_table = 'element'
        verbose_name = _('Element')
        verbose_name_plural = _('Elements')

    def save(self, *args, **kwargs):
        if not self.pk:
            t = Group.objects.get(id=self.group_id)
            t.number_of_elements += 1
            t.save()
            self.group_check = t.id
        elif self.group_id != self.group_check:
            t = Group.objects.get(id=self.group_id)
            t.number_of_elements += 1
            t.save()
            b = Group.objects.get(id=self.group_check)
            b.number_of_elements -= 1
            b.save()
            self.group_check = self.group_id

        super(Element, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        t = Group.objects.get(id=self.group_id)
        t.number_of_elements -= 1
        t.save()
        super(Element, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Group(MPTTModel):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name=_('Group'))

    image = models.ImageField(
        verbose_name=_('Image'),
        blank=False
        )

    description = models.CharField(
        max_length=512,
        blank=True,
        verbose_name=_('Description')
    )

    number_of_children = models.IntegerField(
        default=0,
        verbose_name=_('Number of children groups')
    )

    number_of_elements = models.IntegerField(
        default=0,
        verbose_name=_('Number of elements')
    )

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        verbose_name='parent group',
        on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['name']
        db_table = 'group'
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')

    parent_check = models.IntegerField(
        default=-1,
        verbose_name='parent check'
    )

    def save(self, *args, **kwargs):
        if self.parent_id is not None and self.parent_check == -1:
            t = Group.objects.get(id=self.parent_id)
            t.number_of_children += 1
            t.save()
            self.parent_check = self.parent_id
        elif self.parent_check != self.parent_id and self.parent_id is not None:
            t = Group.objects.get(id=self.parent_id)
            t.number_of_children += 1
            t.save()
            b = Group.objects.get(id=self.parent_check)
            b.number_of_children += 1
            b.save()
            self.parent_check = self.parent_id
        super(Group, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.parent_id is not None:
            t = Group.objects.get(id=self.parent_id)
            t.number_of_children -= 1
            t.save()
        super(Group, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name

