import os
import urllib.request


class ImageDownloader:
    def __init__(self):
        self.cnt = 1

    def download_img(self, directory):
        print()
        user = "_mohab_ashraf_0"
        if not os.path.isdir(user):
            # Create folder
            os.mkdir(user)
        file_name = os.path.join(os.getcwd(), user, f"image{self.cnt}.jpeg")
        self.cnt += 1
        link = "https://instagram.fcai20-2.fna.fbcdn.net/v/t51.2885-15/64595710_312497109636580_8524038124056576659_n.jpg?stp=dst-jpg_e35_p480x480&_nc_ht=instagram.fcai20-2.fna.fbcdn.net&_nc_cat=104&_nc_ohc=B4_zuD12bOwAX9qrbQi&edm=ABmJApABAAAA&ccb=7-5&ig_cache_key=MjA3MTU1MjQxNDU4NzkwNDUzNQ%3D%3D.2-ccb7-5&oh=00_AfA6PEel2ensi28zRbRTGeJJp93V7wd2PDntutYoVLVMMg&oe=644E71D8&_nc_sid=6136e7"
        print("Image downloaded successfully as:", file_name)
        print(file_name)
        urllib.request.urlretrieve(link, file_name)


ob = ImageDownloader()
ob.download_img(directory="fdd")
