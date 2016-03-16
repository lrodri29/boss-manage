include:
    - sun-java
    - sun-java.env

daemon:
    pkg.installed: []

download:
    file.managed:
        - name: /tmp/keycloak.tar.gz
        - source:
            - salt://keycloak/files/keycloak-1.9.1.Final.tar.gz
            - http://downloads.jboss.org/keycloak/1.9.1.Final/keycloak-1.9.1.Final.tar.gz
    cmd.run:
        - name: |
            cd /srv/
            tar -x -z -f /tmp/keycloak.tar.gz -C /srv
            ln -s keycloak-1.9.1.Final keycloak
        - user: root
        - group: root

keycloak-init.d:
    file.managed:
        - name: /etc/init.d/keycloak
        - source: salt://keycloak/files/service.sh
        - user: root
        - group: root
        - mode: 555
        - require:
            - pkg: daemon
    cmd.run:
        - name: update-rc.d keycloak defaults 99
        - user: root

create-java-symlink:
    file.symlink:
        - name: /usr/bin/java
        - target: /usr/lib/java/bin/java
        - force: True
        - user: root
        - group: root