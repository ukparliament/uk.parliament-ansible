# ansible-kibana
[Ansible Galaxy](https://galaxy.ansible.com/ashokc/kibana/)

Ansible role for Kibana that works with Elasticsearch 5.x. Tested platforms at this time are:

* Ubuntu 16.04

** Developed and Tested with Ansible version 2.4.1.0 **

##### Dependency
None.

Kibana needs an elasticsearch instance to funtion. This role has been used and tested with the [elastic.elasticsearch](https://github.com/elastic/ansible-elasticsearch) role as the provisioner for elasticsearch, [ashokc.filebeat](https://github.com/ashokc/ansible-filebeat) for Filebeat, and [ashokc.logstash](https://github.com/ashokc/ansible-logstash) for Logstash as part of an ELK stack in the blog article [ELK Stack with Vagrant and Ansible](http://xplordat.com/2017/12/12/elk-stack-with-vagrant-and-ansible/)

## Usage

* Create your Ansible playbook with your own tasks
* Include the role ashokc.kibana and override the role defaults

e.g. Deploy 2 instances of Kibana, at ports 5601 & 5602 on 'kibana-nodes'

```
- hosts: kibana-nodes
  become: true
  roles:
    - { role: ashokc.kibana, instance_port: 5601 }
- hosts: kibana-nodes
  become: true
  roles:
    - { role: ashokc.kibana, instance_port: 5602 }
```

The following variables in defaults/main.yml can be overridden:

```
es_major_version: 5.x
elk_version: 5.6.1
es_apt_key: https://artifacts.elastic.co/GPG-KEY-elasticsearch
es_apt_url: deb https://artifacts.elastic.co/packages/{{ es_major_version }}/apt stable main

kibana_user: kibana
kibana_group: kibana
kibana_version: "{{ elk_version }}"
kibana_server_port: "{{instance_port}}"
kibana_server_host: 0.0.0.0
kibana_enabled_on_boot: yes
kibana_elasticsearch_url: http://localhost:9200
kibana_instance: "{{instance_port}}"

```

## Sample playbook with [elastic.elasticsearch](https://github.com/elastic/ansible-elasticsearch) role 

Here is a typical use of this role along with [elastic.elasticsearch](https://github.com/elastic/ansible-elasticsearch). The result of the play is to set up 2 elasticsearch clusters across 2 hosts & a kibana instance targeting each.

* 2 elasticsearch instances at 9201/9301 & 9202/9302 ports on each of the elasticsearch-nodes. The elasticsearch instances at 9201/9301 are part of the cluster 9201_9301 & the ones at 9202/9302 port are part of the 9202_9302 cluster thus giving 2 elasticsearch clusters from the same of set of hosts
* 2 kibana instances at 5601 & 5602 on a single node. Kibana at 5601 talks to 9201_9301 cluster & 5602 talks to 9202_9302 cluster.

#### Inventory:

```
elasticsearch-nodes:
  hosts:
    es-node-1:                    	# hostname
      ansible_host: 192.168.33.25   # ip address
      ansible_user: vagrant
      memory: 4096                  # ram to be assigned in MB
      ansible_ssh_private_key_file: .vagrant/machines/es-node-1/virtualbox/private_key
    es-node-2:                    
      ansible_host: 192.168.33.26
      ansible_user: vagrant
      memory: 4096              
      ansible_ssh_private_key_file: .vagrant/machines/es-node-2/virtualbox/private_key
kibana-node:
  hosts:
    kibana-node-1:
      ansible_host: 192.168.33.27
      ansible_user: vagrant
      memory: 512
      ansible_ssh_private_key_file: .vagrant/machines/kibana-node-1/virtualbox/private_key
```
#### Playbook:

```
- hosts: elasticsearch-nodes
  become: true
  vars:
    es_major_version: 5.x
    es_apt_key: https://artifacts.elastic.co/GPG-KEY-elasticsearch
    es_apt_url: deb https://artifacts.elastic.co/packages/{{ es_major_version }}/apt stable main
    public_iface: eth1	# When using the vagrant provider, the public IP is with 'eth1'
    es_version: 5.6.1
  roles:
    - { role: elastic.elasticsearch, cluster_http_port: 9201, cluster_transport_tcp_port: 9301,
es_instance_name: "{{cluster_http_port}}_{{cluster_transport_tcp_port}}",
discovery: "{% for host in groups['elasticsearch-nodes'] %} {{hostvars[host]['ansible_'+public_iface]['ipv4']['address'] }}:{{cluster_transport_tcp_port}}{%endfor %}",
es_api_port: "{{cluster_http_port}}",
          es_config: {
            cluster.name: "{{es_instance_name}}",
            node.data: true,
            node.master: true,
            http.port: "{{cluster_http_port}}",
            transport.tcp.port: "{{cluster_transport_tcp_port}}",
            discovery.zen.ping.unicast.hosts: "{{ discovery.split() }}",
            network.host: ["{{ hostvars[inventory_hostname]['ansible_' + public_iface]['ipv4']['address'] }}","_local_" ],
            bootstrap.memory_lock: false
        }
    }

- hosts: elasticsearch-nodes
  become: true
  vars:
    es_major_version: 5.x
    es_apt_key: https://artifacts.elastic.co/GPG-KEY-elasticsearch
    es_apt_url: deb https://artifacts.elastic.co/packages/{{ es_major_version }}/apt stable main
    public_iface: eth1
    es_version: 5.6.1
  roles:
    - { role: elastic.elasticsearch, cluster_http_port: 9202, cluster_transport_tcp_port: 9302,
es_instance_name: "{{cluster_http_port}}_{{cluster_transport_tcp_port}}",
discovery: "{% for host in groups['elasticsearch-nodes'] %} {{hostvars[host]['ansible_'+public_iface]['ipv4']['address'] }}:{{cluster_transport_tcp_port}}{%endfor %}",
es_api_port: "{{cluster_http_port}}",
          es_config: {
            cluster.name: "{{es_instance_name}}",
            node.data: true,
            node.master: true,
            http.port: "{{cluster_http_port}}",
            transport.tcp.port: "{{cluster_transport_tcp_port}}",
            discovery.zen.ping.unicast.hosts: "{{ discovery.split() }}",
            network.host: ["{{ hostvars[inventory_hostname]['ansible_' + public_iface]['ipv4']['address'] }}","_local_" ],
            bootstrap.memory_lock: false
        }
    }

- hosts: kibana-nodes
  become: true
  vars:
    es_major_version: 5.x
    es_apt_key: https://artifacts.elastic.co/GPG-KEY-elasticsearch
    es_apt_url: deb https://artifacts.elastic.co/packages/{{ es_major_version }}/apt stable main
    public_iface: eth1
    elk_version: 5.6.1
    kibana_user: kibanaUser
    kibana_group: kibanaGroup
  roles:
    - { role: ashokc.kibana, instance_port: 5601, kibana_elasticsearch_url: "http://{{hostvars[groups['elasticsearch-nodes'][0]]['ansible_'+public_iface]['ipv4']['address'] }}:9201" }

- hosts: kibana-nodes
  become: true
  vars:
    es_major_version: 5.x
    es_apt_key: https://artifacts.elastic.co/GPG-KEY-elasticsearch
    es_apt_url: deb https://artifacts.elastic.co/packages/{{ es_major_version }}/apt stable main
    public_iface: eth1
    elk_version: 5.6.1
    kibana_user: kibanaUser
    kibana_group: kibanaGroup
  roles:
    - { role: ashokc.kibana, instance_port: 5602, kibana_elasticsearch_url: "http://{{hostvars[groups['elasticsearch-nodes'][0]]['ansible_'+public_iface]['ipv4']['address'] }}:9202" }

```
