from django.db import models


class DateNameAwareModel(models.Model):
    # Automatically add timestamps when object is created
    added = models.DateTimeField(auto_now_add=True)
    # Automatically add timestamps when object is updated
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=60)

    class Meta:
        abstract = True


class Infrastructure(DateNameAwareModel):
    pass

    def __str__(self):
        return self.name


class AWSEC2(Infrastructure):
    region_name = models.CharField(max_length=100)
    region_endpoint = models.CharField(max_length=255)
    is_secure = models.BooleanField()
    ec2_port = models.IntegerField(blank=True, null=True,
                                   verbose_name="EC2 port")
    ec2_conn_path = models.CharField(max_length=255, default='/',
                                     verbose_name="EC2 conn path")

    class Meta:
        verbose_name = "AWS EC2"
        verbose_name_plural = "AWS EC2"


class AWSS3(Infrastructure):
    s3_host = models.CharField(max_length=255, blank=True, null=True)
    s3_port = models.IntegerField(blank=True, null=True)
    s3_conn_path = models.CharField(max_length=255, default='/', blank=True,
                                    null=True)

    class Meta:
        verbose_name = "AWS S3"
        verbose_name_plural = "AWS S3"


class OpenStack(Infrastructure):
    auth_url = models.CharField(max_length=255)
    region_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "OpenStack"
        verbose_name_plural = "OpenStack"


class Image(DateNameAwareModel):
    image_id = models.CharField(max_length=50, verbose_name="Image ID")
    description = models.CharField(max_length=255, blank=True, null=True)
    infrastructure = models.ForeignKey(Infrastructure, blank=True, null=True)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.image_id)


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Application category"
        verbose_name_plural = "Application categories"


class Application(DateNameAwareModel):
    version = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    info_url = models.URLField(blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    image_id = models.ManyToManyField(Image, blank=True)
    # Userdata max length is 16KB
    launch_data = models.TextField(max_length=1024 * 16, help_text="Instance "
                                   "user data to parameterize the launch.",
                                   blank=True, null=True)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.version)