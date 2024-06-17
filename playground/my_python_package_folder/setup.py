from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1.0',
    author='Your Name',
    author_email='your_email@example.com',
    description='A short description of your package',
    packages=find_packages(),
    install_requires=[
        # List any dependencies your package requires
        'numpy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)