from wand.image import Image
with Image(filename="book.pdf") as img:
     img.save(filename="/tmp/book.jpg")
# Resizing this image
with Image(filename="/book.pdf[2]") as img:
     img.resize(200, 150)
     img.save(filename="/book_2.jpg")
