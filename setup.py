# setup.py es un archivo necesario para publicar el proyecto
# y después usarlo con pip.
# Referencia: https://packaging.python.org/tutorials/distributing-packages/#setup-args

from setuptools import setup, find_packages

setup(
    name="tec.ic.ia.pc2.g03",
    packages=find_packages(),
    description="Inteligencia Artificial: Proyecto Corto II",
    long_description="Buscador de Zanahorias usando Algoritmos genéticos y búsqueda A*",
    version="1.0.0",
    author="Julian Salinas, Brandon Dinarte, Armando López",
    license="GNU General Public License v3.0",
    keywords=['tec', 'ic', 'ia', "g03", "buscador", "zanahorias"],
    url='https://github.com/JulianSalinas/Buscador_Zanahorias',
    download_url="https://github.com/bdinarte/SimuladorVotantes/archive/v1.0.0.tar.gz",
    install_requires=['pandas', 'numpy'],
    python_requires='>=3',
    include_package_data=True,
    package_data={"tec": ["*.txt", "*.csv", ".xlsx"]},
    classifiers=[],
)
