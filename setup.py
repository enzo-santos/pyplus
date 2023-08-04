import os
import setuptools

def main():
    packages = setuptools.find_packages()

    with open('requirements.txt', encoding='utf-8') as f:
        install_requires = list(map(str.strip, f))

    setuptools.setup(
        name='pyplus',
        version='0.1.0',
        packages=packages,
        include_package_data=True,
        description='Utilidades',
        long_description='Utilidades de leituras e escritas de arquivos.',
        package_dir={package: package.replace('.', os.path.sep) for package in packages},
        install_requires=install_requires,
        extras_require={},
        classifiers=[],
        entry_points={},
    )

if __name__ == '__main__':
    main()
