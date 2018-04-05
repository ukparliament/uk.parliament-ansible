- name: Download Packer binary
  get_url:
    url: https://releases.hashicorp.com/packer/1.2.2/packer_1.2.2_linux_amd64.zip
    dest: /usr/local/bin/packer
    mode: 0775
