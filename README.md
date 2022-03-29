# Ansible Role - System Users & Groups

Ansible Role to deploy users and groups on linux servers.

[![Ansible Galaxy](https://img.shields.io/ansible/role/56757)](https://galaxy.ansible.com/ansibleguy/linux_users)
[![Ansible Galaxy Downloads](https://img.shields.io/badge/dynamic/json?color=blueviolet&label=Galaxy%20Downloads&query=%24.download_count&url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv1%2Froles%2F56757%2F%3Fformat%3Djson)](https://galaxy.ansible.com/ansibleguy/linux_users)

**Tested:**
* Debian 11

## Functionality

* **Users**
  * User-scope => limit the servers a user should be created on
  * Sudoers-privileges for specific commands
  * SSH Authorized-keys
  * Set Bash aliases


* **Groups**
  * nested groups (_member inheritance_)

## Info

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of this functionality can be opted in or out using the main defaults file and variables!


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


## Requirements

* Posix collection: ```ansible-galaxy install -r requirements.yml```


## Usage

### Config

Define the system_auth config as needed:
```yaml
system_auth:
  users:
    guy:
      comment: 'AnsibleGuy'
      password: !vault |
        $ANSIBLE_VAULT;1.1;AES256
        64373031333937633163366236663237623464336461613334343739323763373330393930666331
        3333663262346337636536383539303834373733326631310a393865653831663238383937626238
        35396531316338373030353530663465343838373635363633613035356338353366373231343264
        3437356663383466630a666161363163346533333139656566386466383733646134616166376638
        35313765356134396130333439663461353336313230366338646165376666313232
      ssh_pub:
        - 'ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBKkIlii1iJM240yPSPS5WhrdQwGFa7BTJZ59ia40wgVWjjg1JlTtr9K2W66fNb2zNO7tLkaNzPddMEsov2bJAno= guy@ansibleguy.net'
      privileges:
        - '/usr/bin/rsync'
        - '/bin/systemctl restart apache2.service'
      bash_aliases:
        ll: 'ls -l'
  
    other_guy:
      comment: 'Unusual user'
      shell: '/bin/fancyshell'
      always_update_password: true  # else it will only be set on creation
      password: !vault |
        $ANSIBLE_VAULT;1.1;AES256
        61303431646338396364383939626630336436316661623830643636376130636163356234333464
        3430643134366635356130373139636664363139313831630a376436396134646665306361366464
        66386166663739316162346638323537346630333761366161386364646532633434613964396264
        3063306334636331320a653837663432643164626665353638643032336534653239666534373562
        62323631363638633239383839666337356538366133326136363033373338643138
      ssh_pub:
        - 'ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBBxS1MoeqDyN6+ZKsnLJHIA0/5nVQ6+a1Bgwknx3U7lGlqFIki/HgUX089YUzhbEKcxzTlR3Ji+gLnxhBZhe700= other@ansibleguy.net'
      scope: 'dc_europe_west'  # only create user on servers that are a member of the inventory-group 'dc_europe_west'
      privileges:
        - '/bin/systemctl restart some_service.service'
      sudoers_prompt: true  # user needs to confirm his/her/its password if running the listed commands via 'sudo'
  
    root:
      dont_touch: true  # user account will not be modified
      bash_aliases:
        ll: 'ls -l'
        la: 'ls -la'
        tc: 'tar -cJvf'
        tx: 'tar -xJvf'
  
  groups:
    ag_guest:
      members: ['joe', 'who?']
    ag_tester:
      members: ['hans']
    ag_users:
      members: ['lisa']
      nested_groups: ['ag_tester']
    ag_superguys:
      members: ['seppal']
      parents: ['ag_users']
    ag_devops:
      members: ['luis']
    ag_admins:
      members: ['reymond']
      member_of: ['ag_superguys']
```

You might want to use 'ansible-vault' to encrypt your passwords:
```bash
ansible-vault encrypt_string
```

### Execution

Run the playbook:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml --ask-vault-pass
```

#### Nested Groups
You can link two groups with each other and let them inherit the other ones members.

If another group should inherit all members of the current one:
* member_of
* parents

If the current group should inherit all members of another one:
* nested_groups
* children


### Example


**Config**
```yaml
system_auth:
  users:
    guy:
      comment: 'AnsibleGuy'
      password: !vault |
        $ANSIBLE_VAULT;1.1;AES256
        64373031333937633163366236663237623464336461613334343739323763373330393930666331
        3333663262346337636536383539303834373733326631310a393865653831663238383937626238
        35396531316338373030353530663465343838373635363633613035356338353366373231343264
        3437356663383466630a666161363163346533333139656566386466383733646134616166376638
        35313765356134396130333439663461353336313230366338646165376666313232
      ssh_pub:
        - 'ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBKkIlii1iJM240yPSPS5WhrdQwGFa7BTJZ59ia40wgVWjjg1JlTtr9K2W66fNb2zNO7tLkaNzPddMEsov2bJAno= guy@ansibleguy.net'
      privileges:
        - '/usr/bin/rsync'
        - '/bin/systemctl restart apache2.service'
  
    other_guy:
      comment: 'Unusual user'
      scope: 'dc_europe_west'
      remove: true  # if the files related to the user should be removed once he/she/it gets deleted
      force_remove: true  # force delete the above
  
    another_guy:
      comment: 'Nice guy'
      password: !vault |
            $ANSIBLE_VAULT;1.1;AES256
            61303431646338396364383939626630336436316661623830643636376130636163356234333464
            3430643134366635356130373139636664363139313831630a376436396134646665306361366464
            66386166663739316162346638323537346630333761366161386364646532633434613964396264
            3063306334636331320a653837663432643164626665353638643032336534653239666534373562
            62323631363638633239383839666337356538366133326136363033373338643138
      ssh_pub:
        - 'ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBBcfYHDR8O4A9uIHnw3v25rDPtqDlRmFIyJc1fxZx90K6BUNXV+TTkFH836EftHVAaMdlMZSfNm9O+o0UbrvbaI= another@ansibleguy.net'
      force_password_change: true
  
  groups:
    ag_guest:
      members: []
    ag_tester:
      members: ['other_guy', 'another_guy']
      state: 'absent'
    ag_users:
      members: []
      nested_group: ['ag_tester']
    ag_superguys:
      members: []
      parents: ['ag_users']
    ag_devops:
      members: []
    ag_admins:
      members: ['guy']
      member_of: ['ag_superguys']

```

**Result:**
```bash
guy@ansible:~# cat /etc/group
> ...
> ag_guest:x:1000:
> ag_users:x:1002:guy,another_guy
> ag_superguys:x:1003:guy
> ag_devops:x:1004:
> ag_admins:x:1005:guy
> guy:x:1006:
> another_guy:x:1007:

guy@ansible:~# cat /etc/passwd
> ...
> guy:x:1000:1006:Ansible managed - AnsibleGuy:/home/guy:/bin/bash
> another_guy:x:1001:1007:Ansible managed - Nice guy:/home/another_guy:/bin/bash

guy@ansible:~# cat /etc/sudoers.d/user_priv_guy 
> # Ansible managed
> 
> Cmnd_Alias USER_PRIV_GUY = \
>   /usr/bin/rsync, \
>   /bin/systemctl restart apache2.service
> 
> guy ALL=(ALL) NOPASSWD: USER_PRIV_GUY

guy@ansible:~# cat /etc/sudoers.d/user_priv_another_guy 
> # Ansible managed
> 
> Cmnd_Alias USER_PRIV_ANOTHERGUY = \
>   /bin/systemctl restart myNiceStuff.service
> 
> another_guy ALL=(ALL) USER_PRIV_ANOTHERGUY
```