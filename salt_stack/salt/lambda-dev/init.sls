# Setup the lambda development/build server.
# Note that this server uses Amazon Linux so its setup
# differs from our usual Ubuntu server configuration.

{% set user = 'ec2-user' %}
{% set venv_home = '/home/' + user + '/lambdaenv' %}
{% set spdb_home = venv_home + '/local/lib/python3.4/site-packages/spdb' %}
{% set bossutils_home = venv_home + '/local/lib/python3.4/site-packages/bossutils' %}
{% set lambda_home = venv_home + '/local/lib/python3.4/site-packages/lambda' %}
{% set lambdautils_home = venv_home + '/local/lib/python3.4/site-packages/lambdautils' %}

make-base:
    file.managed:
        - name: /home/ec2-user/makebaseenv
        - source: salt://lambda-dev/files/makebaseenv
        - mode: 755
        - user: {{ user }}
        - group: {{ user }}

make-domain:
    file.managed:
        - name: /home/ec2-user/makedomainenv
        - source: salt://lambda-dev/files/makedomainenv
        - mode: 755
        - user: {{ user }}
        - group: {{ user }}

make-upload:
    file.managed:
        - name: /home/ec2-user/deploy_lambdas.py
        - source: salt://boss-tools/files/boss-tools.git/lambdautils/deploy_lambdas.py
        - mode: 755
        - user: {{ user }}
        - group: {{ user }}

make-requirements:
    file.managed:
        - name: /home/ec2-user/requirements.txt
        - source: salt://boss-tools/files/boss-tools.git/lambda/requirements.txt
        - mode: 755
        - user: {{ user }}
        - group: {{ user }}

python35:
    pkg.installed:
        - pkgs:
            - python27-pip.noarch
            - python35.x86_64
            - python35-devel.x86_64 # needed to compile C extensions
            #- python35-pip.noarch
            #- python35-virtualenv.noarch
    cmd.run:
        - name: |
            curl https://bootstrap.pypa.io/get-pip.py > /tmp/get-pip.py
            sudo python3 /tmp/get-pip.py
            sudo python3 -m pip install virtualenv
            sudo python3 -m pip install boto3
            sudo yum groupinstall -y "Development Tools"

environment:
    file.directory:
        - name: /home/ec2-user/sitezips
        - user: {{ user }}
        - group: {{ user }}
        - dir_mod: 755

