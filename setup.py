from distutils.core import setup
import platform

setup(name='recce7',
      version='1.0',
      description='Honeypot',
      author='Jesse Nelson',
      author_email='jnels124@msudenver.edu',
      data_files=[('/etc/recce7/configs/', ['config/plugins.cfg'])],
      scripts=['startHoneyPot.sh'],
      packages=['framework', 'plugins', 'database', 'common'])
