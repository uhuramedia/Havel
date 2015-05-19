import os
from setuptools import setup, find_packages


VERSION = "0.3"

setup(
    name="HavelCMS",
    version = VERSION,
    author="Julian Bez, Nar Chhantyal",
    author_email="julian@freshmilk.tv",
    url="https://github.com/Freshmilk/",
    description="""FM resource model""",
    packages=find_packages(),
    namespace_packages = [],
    include_package_data = True,
    package_data={
        'HavelCMS': [
        'locale/*/LC_MESSAGES/*',
        'templates/resources/*',
        ]
    },
    zip_safe=False,
    license="BSD",
    install_requires=["django-mptt", "feincms", "django-ckeditor"]
)
