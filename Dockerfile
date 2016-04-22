FROM jelasticdocker/jelastic-centos7-base:latest

RUN rpm -Uvh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-6.noarch.rpm; \
	yum -y install openssh-server openssh-clients pwgen iptables patch dbus dbus-libs vim mc nano file acl \
	rsyslog sendmail strace bzip2 bzip2-libs bzip2-devel net-snml-libs && yum -y update && yum clean all; \
	sed -i 's/#UseDNS/UseDNS/g' /etc/ssh/sshd_config; \
	sed -i 's/UseDNS yes/UseDNS no/g' /etc/ssh/sshd_config; \
	sed -i -re '/^[\#]?ClientAliveInterval/cClientAliveInterval 30' /etc/ssh/sshd_config; \
	sed -i -re '/^[\#]?ClientAliveCountMax/cClientAliveCountMax 50' /etc/ssh/sshd_config; \
	/sbin/chkconfig --add iptables 2>&1 1>/dev/null; \
	/sbin/chkconfig sendmail off 2>/dev/null 1>/dev/null;

COPY src/usr/local/sbin/* /usr/local/sbin/
COPY src/etc/security/* /etc/security/
COPY src/etc/jelastic/* /etc/jelastic/
COPY src/etc/logrotate.d/* /etc/logrotate.d/
COPY src/etc/rc.d/init.d/* /etc/rc.d/init.d/

RUN chmod +x /etc/rc.d/init.d/*

CMD /bin/bash
