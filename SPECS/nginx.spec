Name:		nginx
Version:	1.12.2
Release:	1%{?dist}
Summary:	nginx-1.12.2.tar.gz

Group:		Applications/Archiving
License:	GPLv2		
URL:		http://www.baidu.com
Source0:	%{name}-%{version}.tar.gz
Source1:	nginx
Source2:	nginx.conf
Source3:	fastcgi_params
Source4:	nginx.logrotate
Source5:	80.conf

BuildRoot:	%_topdir/BUILDROOT
BuildRequires:	gcc,gcc-c++
Requires:	openssl,openssl-devel,pcre,pcre-devel

%description
This is nginx-1.12.2.rpm!


%prep
%setup -q 			


%build
./configure \
--prefix=/usr/local/nginx \
--user=www \
--group=www \
--with-http_ssl_module \
--with-http_flv_module \
--with-http_stub_status_module \
--with-http_gzip_static_module \
--with-pcre
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}/etc/rc.d/init.d/nginx
%{__install} -p -D %{SOURCE2} %{buildroot}/usr/local/nginx/conf/nginx.conf
%{__install} -p -D %{SOURCE3} %{buildroot}/usr/local/nginx/conf/fastcgi_params
%{__install} -p -D %{SOURCE4} %{buildroot}/etc/logrotate.d/nginx
%{__install} -p -D %{SOURCE5} %{buildroot}/usr/local/nginx/conf/conf.d/80.conf

%pre
if [ $1 == 1 ];then
	awk '{print $1}' /etc/passwd | grep -q www || /usr/sbin/useradd www -s /sbin/nologin -M &>/dev/null 
	[ -d /www ]  || mkdir /www 
	chown www.www /www -R 
	echo "Hello World!" >>/www/index.html
fi

%post
if [ $1 == 1 ];then
	/sbin/chkconfig --add %{name}
	/sbin/chkconfig %{name} on
	echo '# Add  #下面主要是内核参数的优化，包括tcp的快速释放和重利用等。   
net.ipv4.tcp_max_syn_backlog = 65536
net.core.netdev_max_backlog =  32768
net.core.somaxconn = 32768
  
net.core.wmem_default = 8388608
net.core.rmem_default = 8388608
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
  
net.ipv4.tcp_timestamps = 0
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 2
  
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_tw_reuse = 1
  
net.ipv4.tcp_mem = 94500000 915000000927000000
net.ipv4.tcp_max_orphans = 3276800
  
#net.ipv4.tcp_fin_timeout = 30
#net.ipv4.tcp_keepalive_time = 120
net.ipv4.ip_local_port_range = 1024  65535' >> /etc/sysctl.conf
sysctl -p 2>&1 /dev/null
fi

%preun
if [ $1 == 0 ];then
	/etc/init.d/nginx stop &>/dev/null
fi

%clean
rm -fr %{buildroot}

%files
/etc/logrotate.d/nginx
%defattr(-,root,root,0755)
/usr/local/nginx/
%attr(0755,root,root) /etc/rc.d/init.d/nginx
%config(noreplace) /usr/local/nginx/conf/nginx.conf
%config(noreplace) /usr/local/nginx/conf/conf.d/80.conf
%config(noreplace) /usr/local/nginx/conf/fastcgi_params

%changelog
* Tue Jan 16 2018 dtteam 1.12.2-1
- Initial version
