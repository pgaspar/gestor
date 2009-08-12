from sorl.thumbnail.main import DjangoThumbnail

def thumbnail(image_path, size=(80,80)):
	t = DjangoThumbnail(relative_source=image_path, requested_size=size)
	return u'<img src="%s" alt="%s" />' % (t.absolute_url, image_path)