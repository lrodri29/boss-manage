base:
  '*':
    - scalyr

  'endpoint*':
    - endpoint
    - chrony.config

  'cachemanager*':
    - cachemanager
    - chrony.config

  'activities*':
    - activities
    - chrony.config

  'ep-jenkins*':
    - endpoint-jenkins
    - chrony.config

  'proofreader-web*':
    - proofreader-web
    - chrony.config

  # Jenkins server for Django proofreader tests.
  'pr-jenkins*':
    - proofreader-jenkins
    - chrony.config

  # Jenkins server for Python scripts such as those in boss-tools.
  'jenkins*':
    - jenkins
    - chrony.config