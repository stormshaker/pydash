pyDash - v1.5.0
======

Update: 10 Nov 2016
@Gadgetreactor - this is an awesome project. Rewritten it so it is a drop in app to your Django project and updated to Django 1.10 
Add pydash to your Django project folder.

+ Open your existing settings.py
+ Add pydash to your installed apps
+ modify your project urls.py
+ Add the following line `url(r'^dashboard/', include('pydash.urls')),`
+ dashboard can be replaced accordingly
+ copy the static folder to your own static location
+ Load up your server!


-----------------------
Forked from 

A small web-based monitoring dashboard for your linux pc/server writen in Python and Django + Chart.js.

The dashboard is built using only Python libraries available in the main Python distribution, trying to create a small list of dependencies without the need of installing many packages or libraries.


Current dependencies:

  - >= Django 1.10
  - >= Python 2.x
  - >= Python 3.x

Django App
==========
For the Django App please check [here](https://github.com/k3oni/pydash-django-app)

Installation
============

###[Installing pyDash](https://github.com/k3oni/pydash/wiki)


Settings
========

###[pyDash settings](https://github.com/k3oni/pydash/wiki/Settings)


Remote data retrieval
=====================

###[pyDash remote data retrieval](https://github.com/k3oni/pydash/wiki/Remote-data-retreival)


OS Support
==========

pyDash was tested and runs under the following OSs:
  - Centos
  - Fedora
  - Ubuntu
  - Debian
  - Raspbian
  - Pidora
  - Arch Linux


Might work under others, but didn't get to test any other OSs just yet.



License
=======

**[MIT](https://github.com/k3oni/pydash/blob/master/LICENSE.md)**



Credits
=======
[Dashboard Template](http://www.egrappler.com/templatevamp-free-twitter-bootstrap-admin-template/), 
[Bootstrap](http://getbootstrap.com/), 
[Font Awesome](http://fontawesome.io/)
[pyDash](https://github.com/k3oni/pydash)
