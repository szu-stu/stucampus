from setuptools import setup, find_packages


install_requires = [l.strip() for l in open("requirements.txt", "r")]


metadata = {"name": "stucampus",
            "version": "0.1",
            "packages": find_packages(),
            "author": "szulabs",
            "author_email": "szulabs@gmail.com",
            "url": "http://stu.szu.edu.cn",
            "zip_safe": False,
            "platforms": ["linux"],
            "package_data": {"": ["*.html", "*.jpg", "*.png", "*.css", "*.js",
                                  "*.ico", "*.coffee", "*.less"]},
            "install_requires": install_requires,
            "description": "StuCampus is a website for students in SZU."}


if __name__ == "__main__":
    setup(**metadata)

