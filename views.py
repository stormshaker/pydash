# The MIT License (MIT)
#
# Copyright (c) 2014 Florian Neagu - michaelneagu@gmail.com - https://github.com/k3oni/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import platform
import os
import multiprocessing
from datetime import timedelta, datetime
import json

from . import tasks

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response #remove
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponse
from pydash.models import Aquarium
from django.utils import timezone
from django.core import serializers

#All refresh values are in miliseconds, 1 second = 1000 miliseconds
#Adjust accordingly as you wish
TIME_JS_REFRESH = 30000
TIME_JS_REFRESH_LONG = 120000
TIME_JS_REFRESH_NET = 2000

time_refresh = TIME_JS_REFRESH
time_refresh_long = TIME_JS_REFRESH_LONG
time_refresh_net = TIME_JS_REFRESH_NET
version = "1.5.0"

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = timezone.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str("{0:.0f}".format(second_diff)) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str("{0:.0f}".format(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str("{0:.0f}".format(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str("{0:.0f}".format(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return str("{0:.0f}".format(day_diff / 30)) + " months ago"
    return str("{0:.0f}".format(day_diff / 365)) + " years ago"

def chunks(get, n):
    return [get[i:i + n] for i in range(0, len(get), n)]


def get_uptime():
    """
    Get uptime
    """
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_time = str(timedelta(seconds=uptime_seconds))
            data = uptime_time.split('.', 1)[0]

    except Exception as err:
        data = str(err)

    return data


def get_ipaddress():
    """
    Get the IP Address
    """
    data = []
    try:
        eth = os.popen("ip addr | grep LOWER_UP | awk '{print $2}'")
        iface = eth.read().strip().replace(':', '').split('\n')
        eth.close()
        del iface[0]

        for i in iface:
            pipe = os.popen("ip addr show " + i + "| awk '{if ($2 == \"forever\"){!$2} else {print $2}}'")
            data1 = pipe.read().strip().split('\n')
            pipe.close()
            if len(data1) == 2:
                data1.append('unavailable')
            if len(data1) == 3:
                data1.append('unavailable')
            data1[0] = i
            data.append(data1)

        ips = {'interface': iface, 'itfip': data}

        data = ips

    except Exception as err:
        data = str(err)

    return data


def get_cpus():
    """
    Get the number of CPUs and model/type
    """
    try:
        pipe = os.popen("cat /proc/cpuinfo |" + "grep 'model name'")
        data = pipe.read().strip().split(':')[-1]
        pipe.close()

        if not data:
            pipe = os.popen("cat /proc/cpuinfo |" + "grep 'Processor'")
            data = pipe.read().strip().split(':')[-1]
            pipe.close()

        cpus = multiprocessing.cpu_count()

        data = {'cpus': cpus, 'type': data}

    except Exception as err:
        data = str(err)

    return data


def get_users():
    """
    Get the current logged in users
    """
    try:
        pipe = os.popen("who |" + "awk '{print $1, $2, $6}'")
        data = pipe.read().strip().split('\n')
        pipe.close()

        if data == [""]:
            data = None
        else:
            data = [i.split(None, 3) for i in data]

    except Exception as err:
        data = str(err)

    return data


def get_traffic(request):
    """
    Get the traffic for the specified interface
    """
    try:
        pipe = os.popen("cat /proc/net/dev |" + "grep " + request + "| awk '{print $1, $9}'")
        data = pipe.read().strip().split(':', 1)[-1]
        pipe.close()

        if not data[0].isdigit():
            pipe = os.popen("cat /proc/net/dev |" + "grep " + request + "| awk '{print $2, $10}'")
            data = pipe.read().strip().split(':', 1)[-1]
            pipe.close()

        data = data.split()

        traffic_in = int(data[0])
        traffic_out = int(data[1])

        all_traffic = {'traffic_in': traffic_in, 'traffic_out': traffic_out}

        data = all_traffic

    except Exception as err:
        data = str(err)

    return data


def get_platform():
    """
    Get the OS name, hostname and kernel
    """
    try:
        osname = " ".join(platform.linux_distribution())
        uname = platform.uname()

        if osname == '  ':
            osname = uname[0]

        data = {'osname': osname, 'hostname': uname[1], 'kernel': uname[2]}
        print (data['osname'])
    
    except Exception as err:
        data = str(err)

    return data


def get_disk():
    """
    Get disk usage
    """
    try:
        pipe = os.popen("df -Ph | " + "grep -v Filesystem | " + "awk '{print $1, $2, $3, $4, $5, $6}'")
        data = pipe.read().strip().split('\n')
        pipe.close()

        data = [i.split(None, 6) for i in data]

    except Exception as err:
        data = str(err)

    return data


def get_disk_rw():
    """
    Get the disk reads and writes
    """
    try:
        pipe = os.popen("cat /proc/partitions | grep -v 'major' | awk '{print $4}'")
        data = pipe.read().strip().split('\n')
        pipe.close()

        rws = []
        for i in data:
            if i.isalpha():
                pipe = os.popen("cat /proc/diskstats | grep -w '" + i + "'|awk '{print $4, $8}'")
                rw = pipe.read().strip().split()
                pipe.close()

                rws.append([i, rw[0], rw[1]])

        if not rws:
            pipe = os.popen("cat /proc/diskstats | grep -w '" + data[0] + "'|awk '{print $4, $8}'")
            rw = pipe.read().strip().split()
            pipe.close()

            rws.append([data[0], rw[0], rw[1]])

        data = rws

    except Exception as err:
        data = str(err)

    return data


def get_mem():
    """
    Get memory usage
    """
    try:
        pipe = os.popen(
            "free -tm | " + "grep 'Mem' | " + "awk '{print $2,$4,$6,$7}'")
        data = pipe.read().strip().split()
        pipe.close()

        allmem = int(data[0])
        freemem = int(data[1])
        buffers = int(data[2])
        cachedmem = int(data[3])

        # Memory in buffers + cached is actually available, so we count it
        # as free. See http://www.linuxatemyram.com/ for details
        freemem += buffers + cachedmem

        percent = (100 - ((freemem * 100) / allmem))
        usage = (allmem - freemem)

        mem_usage = {'usage': usage, 'buffers': buffers, 'cached': cachedmem, 'free': freemem, 'percent': percent}

        data = mem_usage

    except Exception as err:
        data = str(err)

    return data


def get_cpu_usage():
    """
    Get the CPU usage and running processes
    """
    try:
        pipe = os.popen("ps aux --sort -%cpu,-rss")
        data = pipe.read().strip().split('\n')
        pipe.close()

        usage = [i.split(None, 10) for i in data]
        del usage[0]

        total_usage = []

        for element in usage:
            usage_cpu = element[2]
            total_usage.append(usage_cpu)

        total_usage = sum(float(i) for i in total_usage)

        total_free = ((100 * int(get_cpus()['cpus'])) - float(total_usage))

        cpu_used = {'free': total_free, 'used': float(total_usage), 'all': usage}

        data = cpu_used

    except Exception as err:
        data = str(err)

    return data


def get_load():
    """
    Get load average
    """
    try:
        data = os.getloadavg()[0]
    except Exception as err:
        data = str(err)

    return data


def get_temp():
    """
    Get temp and humidty from DHT 11 sensor on Arduino using nanpy
    """
    try:
        a = Aquarium()
        data = str(a.roomtemp)
    except Exception as err:
        data = str(err)
       
    return data


def get_humidity():
    """
    Get humidty from DHT 11 sensor on Arduino using nanpy
    """
    try:
        a = Aquarium()
        data = str(a.roomhumidity)
    except Exception as err:
        data = str(err)
       
    return data


def get_netstat():
    """
    Get ports and applications
    """
    try:
        pipe = os.popen(
            "ss -tnp | grep ESTAB | awk '{print $4, $5}'| sed 's/::ffff://g' | awk -F: '{print $1, $2}' "
            "| awk 'NF > 0' | sort -n | uniq -c")
        data = pipe.read().strip().split('\n')
        pipe.close()

        data = [i.split(None, 4) for i in data]

    except Exception as err:
        data = str(err)

    return data

@login_required(login_url='login/')
def index(request):
    context = {'time_refresh': time_refresh,
               'time_refresh_long': time_refresh_long,
               'time_refresh_net': time_refresh_net,
               'version': version}
    return render(request, 'main.html', context)

@login_required(login_url='login/')
def getnetstat(request):
    """
    Return netstat output
    """
    try:
        net_stat = get_netstat()
    except Exception:
        net_stat = None

    data = json.dumps(net_stat)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url='login/')
def platform_info(request, name):
    """
    Return the hostname
    """
    getplatform = get_platform()
    hostname = getplatform['hostname']
    osname = getplatform['osname']
    kernel = getplatform['kernel']

    data = {}

    if name == 'hostname':
        try:
            data = hostname
        except Exception:
            data = None

    if name == 'osname':
        try:
            data = osname
        except Exception:
            data = None

    if name == 'kernel':
        try:
            data = kernel
        except Exception:
            data = None

    data = json.dumps(data)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url='login/')
def getcpus(request, name):
    """
    Return the CPU number and type/model
    """
    cpus = get_cpus()
    cputype = cpus['type']
    cpucount = cpus['cpus']
    data = {}

    if name == 'type':
        try:
            data = cputype
        except Exception:
            data = None

    if name == 'count':
        try:
            data = cpucount
        except Exception:
            data = None

    data = json.dumps(data)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url='login/')
def uptime(request):
    """
    Return uptime
    """
    try:
        up_time = get_uptime()
    except Exception:
        up_time = None

    data = json.dumps(up_time)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url='login/')
def temp(request):
    """
    Return Temprature
    """
    try:
        temp = get_temp()
    except Exception:
        temp = None

    data = json.dumps(temp)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

@login_required(login_url='login/')
def lastupdated(request):
    """
    Return last updated time
    """
    try:
        a = Aquarium()
        updatetime = pretty_date(a.lastupdated())
    except Exception as err:
        updatetime = str(err)

    data = json.dumps(updatetime)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

@login_required(login_url='login/')
def frontlightoff(request):
    """
    Return last updated time
    """
    try:
        a = Aquarium.objects.get(pk=1)
        a.set_front_light_off()
        data = "Light Off"
    except Exception as err:
        data = str(err)
       
    data = json.dumps(data)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

@login_required(login_url='login/')
def frontlighton(request):
    """
    Return last updated time
    """
    try:
        a = Aquarium.objects.get(pk=1)
        a.set_front_light_on()
        data = "Light On"
    except Exception as err:
        data = str(err)
       
    data = json.dumps(data)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

@login_required(login_url='login/')
def humidity(request):
    """
    Return Humidity
    """
    try:
        humidity = get_humidity()
    except Exception:
        humidity = None

    data = json.dumps(humidity)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

@login_required(login_url='login/')
def aquariumstate(request):
    """
    Returns the state of all aquariums
    """
    try:
        states = serializers.serialize('json', Aquarium.objects.all())
    except Exception as err:
        states = str(err)

    data = json.dumps(states)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url='login/')
def getdisk(request):
    """
    Return the disk usage
    """
    try:
        diskusage = get_disk()
    except Exception:
        diskusage = None

    data = json.dumps(diskusage)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url='login/')
def getips(request):
    """
    Return the IPs and interfaces
    """
    try:
        get_ips = get_ipaddress()
    except Exception:
        get_ips = None

    data = json.dumps(get_ips['itfip'])
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url='login/')
def getusers(request):
    """
    Return online users
    """
    try:
        online_users = get_users()
    except Exception:
        online_users = None

    data = json.dumps(online_users)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url='login/')
def getproc(request):
    """
    Return the running processes
    """
    try:
        processes = get_cpu_usage()
        processes = processes['all']
    except Exception:
        processes = None

    data = json.dumps(processes)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url='login/')
def cpuusage(request):
    """
    Return CPU Usage in %
    """
    try:
        cpu_usage = get_cpu_usage()

    except Exception:
        cpu_usage = 0

    cpu = [
        {
            "value": cpu_usage['free'],
            "color": "#0AD11B"
        },
        {
            "value": cpu_usage['used'],
            "color": "#F7464A"
        }
    ]

    data = json.dumps(cpu)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

@login_required(login_url='login/')
def memusage(request):
    """
    Return Memory Usage in % and numeric
    """
    datasets_free = []
    datasets_used = []
    datasets_buffers = []
    datasets_cached = []

    try:
        mem_usage = get_mem()
    except Exception:
        mem_usage = 0

    try:
        cookies = request.COOKIES['memory_usage']
    except Exception:
        cookies = None

    if not cookies:
        datasets_free.append(0)
        datasets_used.append(0)
        datasets_buffers.append(0)
        datasets_cached.append(0)
    else:
        datasets = json.loads(cookies)
        datasets_free = datasets[0]
        datasets_used = datasets[1]
        datasets_buffers = datasets[2]
        datasets_cached = datasets[3]

    if len(datasets_free) > 10:
        while datasets_free:
            del datasets_free[0]
            if len(datasets_free) == 10:
                break
    if len(datasets_used) > 10:
        while datasets_used:
            del datasets_used[0]
            if len(datasets_used) == 10:
                break
    if len(datasets_buffers) > 10:
        while datasets_buffers:
            del datasets_buffers[0]
            if len(datasets_buffers) == 10:
                break
    if len(datasets_cached) > 10:
        while datasets_cached:
            del datasets_cached[0]
            if len(datasets_cached) == 10:
                break
    if len(datasets_free) <= 9:
        free_mem = mem_usage['free']
        datasets_free.append(int(free_mem))
    if len(datasets_free) == 10:
        datasets_free.append(int(mem_usage['free']))
        del datasets_free[0]
    if len(datasets_used) <= 9:
        datasets_used.append(int(mem_usage['usage']))
    if len(datasets_used) == 10:
        datasets_used.append(int(mem_usage['usage']))
        del datasets_used[0]
    if len(datasets_buffers) <= 9:
        datasets_buffers.append(int(mem_usage['buffers']))
    if len(datasets_buffers) == 10:
        datasets_buffers.append(int(mem_usage['buffers']))
        del datasets_buffers[0]
    if len(datasets_cached) <= 9:
        datasets_cached.append(int(mem_usage['cached']))
    if len(datasets_cached) == 10:
        datasets_cached.append(int(mem_usage['cached']))
        del datasets_cached[0]

    # Some fix division by 0 Chart.js
    if len(datasets_free) == 10:
        if sum(datasets_free) == 0:
            datasets_free[9] += 0.1
        if sum(datasets_free) / 10 == datasets_free[0]:
            datasets_free[9] += 0.1

    memory = {
        'labels': [""] * 10,
        'datasets': [
            {
                "fillColor": "rgba(247,70,74,0.5)",
                "strokeColor": "rgba(247,70,74,1)",
                "pointColor": "rgba(247,70,74,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_used
            },
            {
                "fillColor": "rgba(43,214,66,0.5)",
                "strokeColor": "rgba(43,214,66,1)",
                "pointColor": "rgba(43,214,66,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_free
            },
            {
                "fillColor": "rgba(0,154,205,0.5)",
                "strokeColor": "rgba(0,154,205,1)",
                "pointColor": "rgba(0,154,205,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_buffers
            },
            {
                "fillColor": "rgba(255,185,15,0.5)",
                "strokeColor": "rgba(255,185,15,1)",
                "pointColor": "rgba(265,185,15,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_cached
            }
        ]
    }

    cookie_memory = [datasets_free, datasets_used, datasets_buffers, datasets_cached]
    data = json.dumps(memory)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['memory_usage'] = cookie_memory
    response.write(data)
    return response


@login_required(login_url='login/')
def loadaverage(request):
    """
    Return Load Average numeric
    """
    datasets = []

    try:
        load_average = get_load()
    except Exception:
        load_average = 0

    try:
        cookies = request.COOKIES['load_average']
    except Exception:
        cookies = None

    if not cookies:
        datasets.append(0)
    else:
        datasets = json.loads(cookies)
    if len(datasets) > 10:
        while datasets:
            del datasets[0]
            if len(datasets) == 10:
                break
    if len(datasets) <= 9:
        datasets.append(float(load_average))
    if len(datasets) == 10:
        datasets.append(float(load_average))
        del datasets[0]

    # Some fix division by 0 Chart.js
    if len(datasets) == 10:
        if sum(datasets) == 0:
            datasets[9] += 0.1
        if sum(datasets) / 10 == datasets[0]:
            datasets[9] += 0.1

    load = {
        'labels': [""] * 10,
        'datasets': [
            {
                "fillColor": "rgba(151,187,205,0.5)",
                "strokeColor": "rgba(151,187,205,1)",
                "pointColor": "rgba(151,187,205,1)",
                "pointStrokeColor": "#fff",
                "data": datasets
            }
        ]
    }

    data = json.dumps(load)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['load_average'] = datasets
    response.write(data)
    return response


@login_required(login_url='login/')
def gettraffic(request):
    """
    Return the traffic for the interface
    """
    datasets_in = []
    datasets_in_i = []
    datasets_out = []
    datasets_out_o = []
    label = "KBps"

    try:
        intf = get_ipaddress()
        intf = intf['interface'][0]

        traffic = get_traffic(intf)
    except Exception:
        traffic = 0

    try:
        cookies = request.COOKIES['traffic']
    except Exception:
        cookies = None

    if not cookies:
        datasets_in.append(0)
        datasets_in_i.append(0)
        datasets_out.append(0)
        datasets_out_o.append(0)
    else:
        datasets = json.loads(cookies)
        datasets_in = datasets[0]
        datasets_out = datasets[1]
        datasets_in_i = datasets[2]
        datasets_out_o = datasets[3]

    if len(datasets_in) > 10:
        while datasets_in:
            del datasets_in[0]
            if len(datasets_in) == 10:
                break
    if len(datasets_in_i) > 2:
        while datasets_in_i:
            del datasets_in_i[0]
            if len(datasets_in_i) == 2:
                break
    if len(datasets_out) > 10:
        while datasets_out:
            del datasets_out[0]
            if len(datasets_out) == 10:
                break
    if len(datasets_out_o) > 2:
        while datasets_out_o:
            del datasets_out_o[0]
            if len(datasets_out_o) == 2:
                break

    if len(datasets_in_i) <= 1:
        datasets_in_i.append(float(traffic['traffic_in']))
    if len(datasets_in_i) == 2:
        datasets_in_i.append(float(traffic['traffic_in']))
        del datasets_in_i[0]
    if len(datasets_out_o) <= 1:
        datasets_out_o.append(float(traffic['traffic_out']))
    if len(datasets_out_o) == 2:
        datasets_out_o.append(float(traffic['traffic_out']))
        del datasets_out_o[0]

    dataset_in = (float(((datasets_in_i[1] - datasets_in_i[0]) / 1024) / (time_refresh_net / 1000)))
    dataset_out = (float(((datasets_out_o[1] - datasets_out_o[0]) / 1024) / (time_refresh_net / 1000)))

    if dataset_in > 1024 or dataset_out > 1024:
        dataset_in = (float(dataset_in / 1024))
        dataset_out = (float(dataset_out / 1024))
        label = "MBps"

    if len(datasets_in) <= 9:
        datasets_in.append(dataset_in)
    if len(datasets_in) == 10:
        datasets_in.append(dataset_in)
        del datasets_in[0]
    if len(datasets_out) <= 9:
        datasets_out.append(dataset_out)
    if len(datasets_out) == 10:
        datasets_out.append(dataset_out)
        del datasets_out[0]

    # Some fix division by 0 Chart.js
    if len(datasets_in) == 10:
        if sum(datasets_in) == 0:
            datasets_in[9] += 0.1
        if sum(datasets_in) / 10 == datasets_in[0]:
            datasets_in[9] += 0.1

    traff = {
        'labels': [label] * 10,
        'datasets': [
            {
                "fillColor": "rgba(105,210,231,0.5)",
                "strokeColor": "rgba(105,210,231,1)",
                "pointColor": "rgba(105,210,231,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_in
            },
            {
                "fillColor": "rgba(227,48,81,0.5)",
                "strokeColor": "rgba(227,48,81,1)",
                "pointColor": "rgba(227,48,81,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_out
            }
        ]
    }

    cookie_traffic = [datasets_in, datasets_out, datasets_in_i, datasets_out_o]
    data = json.dumps(traff)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['traffic'] = cookie_traffic
    response.write(data)
    return response


@login_required(login_url='login/')
def getdiskio(request):
    """
    Return the reads and writes for the drive
    """
    datasets_in = []
    datasets_in_i = []
    datasets_out = []
    datasets_out_o = []

    try:
        diskrw = get_disk_rw()
        diskrw = diskrw[0]
    except Exception:
        diskrw = 0

    try:
        cookies = request.COOKIES['diskrw']
    except Exception:
        cookies = None

    if not cookies:
        datasets_in.append(0)
        datasets_in_i.append(0)
        datasets_out.append(0)
        datasets_out_o.append(0)
    else:
        datasets = json.loads(cookies)
        datasets_in = datasets[0]
        datasets_out = datasets[1]
        datasets_in_i = datasets[2]
        datasets_out_o = datasets[3]

    if len(datasets_in) > 10:
        while datasets_in:
            del datasets_in[0]
            if len(datasets_in) == 10:
                break
    if len(datasets_in_i) > 2:
        while datasets_in_i:
            del datasets_in_i[0]
            if len(datasets_in_i) == 2:
                break
    if len(datasets_out) > 10:
        while datasets_out:
            del datasets_out[0]
            if len(datasets_out) == 10:
                break
    if len(datasets_out_o) > 2:
        while datasets_out_o:
            del datasets_out_o[0]
            if len(datasets_out_o) == 2:
                break

    if len(datasets_in_i) <= 1:
        datasets_in_i.append(int(diskrw[1]))
    if len(datasets_in_i) == 2:
        datasets_in_i.append(int(diskrw[1]))
        del datasets_in_i[0]
    if len(datasets_out_o) <= 1:
        datasets_out_o.append(int(diskrw[2]))
    if len(datasets_out_o) == 2:
        datasets_out_o.append(int(diskrw[2]))
        del datasets_out_o[0]

    dataset_in = (int((datasets_in_i[1] - datasets_in_i[0]) / (time_refresh_net / 1000)))
    dataset_out = (int((datasets_out_o[1] - datasets_out_o[0]) / (time_refresh_net / 1000)))

    if len(datasets_in) <= 9:
        datasets_in.append(dataset_in)
    if len(datasets_in) == 10:
        datasets_in.append(dataset_in)
        del datasets_in[0]
    if len(datasets_out) <= 9:
        datasets_out.append(dataset_out)
    if len(datasets_out) == 10:
        datasets_out.append(dataset_out)
        del datasets_out[0]

    # Some fix division by 0 Chart.js
    if len(datasets_in) == 10:
        if sum(datasets_in) == 0:
            datasets_in[9] += 0.1
        if sum(datasets_in) / 10 == datasets_in[0]:
            datasets_in[9] += 0.1

    disk_rw = {
        'labels': [""] * 10,
        'datasets': [
            {
                "fillColor": "rgba(245,134,15,0.5)",
                "strokeColor": "rgba(245,134,15,1)",
                "pointColor": "rgba(245,134,15,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_in
            },
            {
                "fillColor": "rgba(15,103,245,0.5)",
                "strokeColor": "rgba(15,103,245,1)",
                "pointColor": "rgba(15,103,245,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_out
            }
        ]
    }

    cookie_diskrw = [datasets_in, datasets_out, datasets_in_i, datasets_out_o]
    data = json.dumps(disk_rw)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['diskrw'] = cookie_diskrw
    response.write(data)
    return response
