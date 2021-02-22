import setuptools
from importlib import import_module

# Check ROOT related requirements and raise error if not found
for pkg in ['ROOT', 'cppyy', 'cppyy_backend']:
    try:
        import_module(pkg)
    except ModuleNotFoundError:
        raise ImportError('{} not found. You need a full working installation of ROOT to install this package.\n' \
                'For more info, see: https://root.cern/install/'.format(pkg))

def get_dependencies(env_yaml_file):
    import yaml
    with open(env_yaml_file, "r") as f:
        environment = yaml.safe_load(f)
    dependencies = []
    for dep in environment["dependencies"]:
        if dep != "root" and not dep.startswith("python"):
            dependencies.append(dep)
    return dependencies

setuptools.setup(
    name="ultimate_plotter",
    author="Massimiliano Galli",
    author_email="massimiliano.galli.95@gmail.com",
    description="HEP data processor and plotter with interfaces to multiple scikit-hep packages",
    packages=["ultimate_plotter"],
    install_requires=get_dependencies("ultimate_plotter_env.yml"),
    scripts = ["scripts/plot_ratio.py"]
)
