# ************************************************************
# Sequel Pro SQL dump
# Version 4499
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.1-m11)
# Database: isi_payslip_email
# Generation Time: 2015-10-10 08:42:41 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table auth_group
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table auth_group_permissions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table auth_permission
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`)
VALUES
	(1,'Can add log entry',1,'add_logentry'),
	(2,'Can change log entry',1,'change_logentry'),
	(3,'Can delete log entry',1,'delete_logentry'),
	(4,'Can add permission',2,'add_permission'),
	(5,'Can change permission',2,'change_permission'),
	(6,'Can delete permission',2,'delete_permission'),
	(7,'Can add group',3,'add_group'),
	(8,'Can change group',3,'change_group'),
	(9,'Can delete group',3,'delete_group'),
	(10,'Can add user',4,'add_user'),
	(11,'Can change user',4,'change_user'),
	(12,'Can delete user',4,'delete_user'),
	(13,'Can add content type',5,'add_contenttype'),
	(14,'Can change content type',5,'change_contenttype'),
	(15,'Can delete content type',5,'delete_contenttype'),
	(16,'Can add session',6,'add_session'),
	(17,'Can change session',6,'change_session'),
	(18,'Can delete session',6,'delete_session'),
	(19,'Can add employee',7,'add_employee'),
	(20,'Can change employee',7,'change_employee'),
	(21,'Can delete employee',7,'delete_employee'),
	(22,'Can add payslip',8,'add_payslip'),
	(23,'Can change payslip',8,'change_payslip'),
	(24,'Can delete payslip',8,'delete_payslip');

/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table auth_user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_user`;

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`)
VALUES
	(1,'pbkdf2_sha256$20000$5FlENbRsfzoU$C1Ewx6JOQrqKVD7+U0DvyZjP7gwSTcYtFPuhRN6BouQ=','2015-10-10 08:26:12.663513',1,'jonel','','','jonel@test.com',1,1,'2015-10-10 01:47:30.658785');

/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table auth_user_groups
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_user_groups`;

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table auth_user_user_permissions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_user_user_permissions`;

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissi_user_id_7f0938558328534a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table django_admin_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_697914295151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`)
VALUES
	(1,'2015-10-10 01:53:56.533795','1','Employee object',1,'',7,1),
	(2,'2015-10-10 02:01:04.860950','2','marcelo',1,'',7,1),
	(3,'2015-10-10 02:05:42.784764','1','Payslip object',1,'',8,1),
	(4,'2015-10-10 02:06:16.647600','1','Payslip object',3,'',8,1),
	(5,'2015-10-10 02:26:40.909193','2','Payslip object',1,'',8,1),
	(6,'2015-10-10 02:27:39.042830','2','Payslip object',3,'',8,1),
	(7,'2015-10-10 02:29:39.935860','3','Payslip object',1,'',8,1),
	(8,'2015-10-10 02:53:51.423627','2','marcelo',2,'Changed email.',7,1),
	(9,'2015-10-10 03:49:12.619173','2','John Lloyd Cruz',2,'Changed name.',7,1),
	(10,'2015-10-10 03:49:36.745292','1','Bea Alonzo',2,'Changed name.',7,1),
	(11,'2015-10-10 05:48:49.811617','3','Payslip object',3,'',8,1),
	(12,'2015-10-10 05:51:02.981754','5','Payslip object',3,'',8,1),
	(13,'2015-10-10 05:51:02.985431','4','Payslip object',3,'',8,1),
	(14,'2015-10-10 05:52:04.225803','7','Payslip object',3,'',8,1),
	(15,'2015-10-10 05:52:04.239568','6','Payslip object',3,'',8,1),
	(16,'2015-10-10 06:12:46.665425','9','Payslip object',3,'',8,1),
	(17,'2015-10-10 06:12:46.666834','8','Payslip object',3,'',8,1),
	(18,'2015-10-10 06:20:15.025820','2','John Lloyd Cruz',2,'Changed email.',7,1),
	(19,'2015-10-10 06:20:28.864952','1','Bea Alonzo',2,'Changed email.',7,1),
	(20,'2015-10-10 06:21:25.176404','11','John Lloyd Cruz',3,'',8,1),
	(21,'2015-10-10 06:21:25.193088','10','Bea Alonzo',3,'',8,1),
	(22,'2015-10-10 06:38:23.203729','13','John Lloyd Cruz',3,'',8,1),
	(23,'2015-10-10 06:38:23.205181','12','Bea Alonzo',3,'',8,1),
	(24,'2015-10-10 06:38:47.785384','15','John Lloyd Cruz',3,'',8,1),
	(25,'2015-10-10 06:38:47.786766','14','Bea Alonzo',3,'',8,1),
	(26,'2015-10-10 07:16:36.427215','17','John Lloyd Cruz',3,'',8,1),
	(27,'2015-10-10 07:16:36.431273','16','Bea Alonzo',3,'',8,1),
	(28,'2015-10-10 08:41:55.359262','19','John Lloyd Cruz',3,'',8,1),
	(29,'2015-10-10 08:41:55.363721','18','Bea Alonzo',3,'',8,1);

/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table django_content_type
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;

INSERT INTO `django_content_type` (`id`, `app_label`, `model`)
VALUES
	(1,'admin','logentry'),
	(3,'auth','group'),
	(2,'auth','permission'),
	(4,'auth','user'),
	(5,'contenttypes','contenttype'),
	(7,'payslip','employee'),
	(8,'payslip','payslip'),
	(6,'sessions','session');

/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table django_migrations
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`)
VALUES
	(1,'payslip','0001_initial','2015-10-10 01:37:42.570657'),
	(2,'contenttypes','0001_initial','2015-10-10 01:37:54.301737'),
	(3,'auth','0001_initial','2015-10-10 01:37:58.261635'),
	(4,'admin','0001_initial','2015-10-10 01:37:58.986586'),
	(5,'contenttypes','0002_remove_content_type_name','2015-10-10 01:37:59.322461'),
	(6,'auth','0002_alter_permission_name_max_length','2015-10-10 01:37:59.482113'),
	(7,'auth','0003_alter_user_email_max_length','2015-10-10 01:37:59.626971'),
	(8,'auth','0004_alter_user_username_opts','2015-10-10 01:37:59.640419'),
	(9,'auth','0005_alter_user_last_login_null','2015-10-10 01:37:59.780960'),
	(10,'auth','0006_require_contenttypes_0002','2015-10-10 01:37:59.782736'),
	(11,'sessions','0001_initial','2015-10-10 01:38:00.291886'),
	(12,'payslip','0002_employee_cc_email','2015-10-10 01:46:42.303252');

/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table django_session
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`)
VALUES
	('1pdy40qifdz7135i6z5zop661jxqyngx','OGU5NjE1MGNlMjEwNjk5MTI3MTgwYmFmMjE5MWYyM2JhZTRlMTNjNjp7Il9hdXRoX3VzZXJfaGFzaCI6IjQ3MWM3MmUyNGVkOWZmNTE1NDYwMzg2Y2I3Yzg4MzE2OTRmYTk5YTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2015-10-24 02:08:44.446008'),
	('ap39mtctuxumb6vg0f3emzx9hd3ti6ae','OGU5NjE1MGNlMjEwNjk5MTI3MTgwYmFmMjE5MWYyM2JhZTRlMTNjNjp7Il9hdXRoX3VzZXJfaGFzaCI6IjQ3MWM3MmUyNGVkOWZmNTE1NDYwMzg2Y2I3Yzg4MzE2OTRmYTk5YTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2015-10-24 08:26:12.669927');

/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table payslip_employee
# ------------------------------------------------------------

DROP TABLE IF EXISTS `payslip_employee`;

CREATE TABLE `payslip_employee` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1064) NOT NULL,
  `email` varchar(254) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `send_email` tinyint(1) NOT NULL,
  `cc_email` varchar(254) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `payslip_employee` WRITE;
/*!40000 ALTER TABLE `payslip_employee` DISABLE KEYS */;

INSERT INTO `payslip_employee` (`id`, `name`, `email`, `active`, `send_email`, `cc_email`)
VALUES
	(1,'Bea Alonzo','cabsjonel@gmail.com',1,1,'innovuze@gmail.com'),
	(2,'John Lloyd Cruz','nespera.eeweb@gmail.com',1,1,'innovuze@gmail.com');

/*!40000 ALTER TABLE `payslip_employee` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table payslip_payslip
# ------------------------------------------------------------

DROP TABLE IF EXISTS `payslip_payslip`;

CREATE TABLE `payslip_payslip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(100) NOT NULL,
  `date_release` datetime(6) NOT NULL,
  `created` datetime(6) NOT NULL,
  `employee_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payslip_pays_employee_id_4cc30d492a6e0aac_fk_payslip_employee_id` (`employee_id`),
  CONSTRAINT `payslip_pays_employee_id_4cc30d492a6e0aac_fk_payslip_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `payslip_employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
