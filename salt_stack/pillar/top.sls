base:
  '*':
    - scalyr

  'endpoint*':
    - endpoint
    - ch

  'cachemanager*':
    - cachemanager
    - chrony

  'activities*':
    - activities
    - chrony

  'ep-jenkins*':
    - endpoint-jenkins
    - chrony

  'proofreader-web*':
    - proofreader-web
    - chrony

  # Jenkins server for Django proofreader tests.
  'pr-jenkins*':
    - proofreader-jenkins
    - chrony

  # Jenkins server for Python scripts such as those in boss-tools.
  'jenkins*':
    - jenkins
    - chrony