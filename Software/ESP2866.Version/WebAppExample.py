import gc
import uasyncio as asyncio

from dawndoor import data
from dawndoor.datetime import DateTime, tz_to_offset
from dawndoor.door import DoorStatus, open_door, close_door
from dawndoor.astro import calculate_sunrise_sunset
from dawndoor.web import WebApp, jsonify
from dawndoor.wifi import connect, get_ip, start_ap, stop_ap, is_connected

webapp = WebApp()


@webapp.route('/', method='GET')
def index(request, response):
    """
    The main page
    """
    gc.collect()
    yield from webapp.sendfile(response, '/templates/index.html')


@webapp.route('/location', method='GET')
def get_location(request, response):
    """
    Get the location and timezone
    """
    location_data = data.get_location()
    gc.collect()
    yield from jsonify(response, location_data)


@webapp.route('/location', method='POST')
def save_location(request, response):
    """
    Save the location and timezone
    """
    yield from request.read_form_data()
    updated_data = {
        'latitude': request.form['latitude'],
        'longitude': request.form['longitude'],
        'timezone': request.form['timezone']
    }
    data.save_location(**updated_data)
    gc.collect()
    yield from jsonify(response, request.form)


@webapp.route('/network', method='GET')
def get_network(request, response):
    """
    Return the WiFi config
    """
    network_config = data.get_network()
    network_config['ip_address'] = get_ip()
    gc.collect()
    yield from jsonify(response, network_config)


@webapp.route('/network', method='POST')
def save_network(request, response):
    """
    Save the network config
    """
    yield from request.read_form_data()
    updated_config = {}
    for key in ['essid', 'password', 'can_start_ap']:
        if key in request.form:
            updated_config[key] = request.form[key]
    data.save_network(**updated_config)
    gc.collect()
    # Now try to connect to the WiFi network
    connect()
    gc.collect()
    if 'can_start_ap' in updated_config:
        updated_config['can_start_ap'] = updated_config['can_start_ap'].lower() == 'true'
        if updated_config['can_start_ap'] is False:
            stop_ap()
        else:
            start_ap()
    updated_config['ip_address'] = get_ip()
    gc.collect()
    yield from jsonify(response, updated_config)


@webapp.route('/door', method='GET')
def get_door_config(request, response):
    """
    Return the door status
    """
    door_data = data.get_door_config() or {'duration': 0}
    gc.collect()
    yield from jsonify(response, door_data)


@webapp.route('/door', method='POST')
def save_door_config(request, response):
    """
    Save the door config or status
    """
    yield from request.read_form_data()
    updated_config = data.get_door_config()
    for key in ['duration']:
        if key in request.form:
            updated_config[key] = request.form[key]
    if updated_config:
        data.save_door_config(updated_config)
    gc.collect()
    yield from jsonify(response, updated_config)


@webapp.route('/door/status', method='GET')
def get_door_status(request, response):
    """
    Return the door status
    """
    door_data = {
        'status': data.get_door_status() or '(unknown)'
    }
    gc.collect()
    yield from jsonify(response, door_data)


@webapp.route('/door/status', method='POST')
def save_door_status(request, response):
    """
    Save the door status
    """
    yield from request.read_form_data()
    if 'status' in request.form:
        data.save_door_status(request.form['status'])
    gc.collect()
    yield from jsonify(response, {'status': request.form['status']})


@webapp.route('/door/open', method='POST')
def force_door_open(request, response):
    """
    Open the door
    """
    open_door()
    gc.collect()
    yield from jsonify(response, {'status': data.get_door_status()})


@webapp.route('/door/close', method='POST')
def force_door_close(request, response):
    """
    Close the door
    """
    close_door()
    gc.collect()
    yield from jsonify(response, {'status': data.get_door_status()})


async def set_time():
    """
    Set the time from NTP
    """
    while True:
        if is_connected():
            try:
                from ntptime import settime
                settime()
            except Exception:
                # Ignore errors
                pass
        gc.collect()
        await asyncio.sleep(3600)


async def calc_sunrise_sunset():
    """
    Periodically check if there's a sunrise/sunset file with the current date, and if not then generate it.
    """
    while True:
        now = DateTime.now()
        sun_data = data.get_sunrise_sunset(now)
        location = data.get_location()
        gc.collect()
        if location and not sun_data:
            sunrise, sunset = calculate_sunrise_sunset(now, location['latitude'], location['longitude'],
                                                       tz_to_offset(location['timezone']))
            data.save_sunrise_sunset(sunrise, sunset)
            gc.collect()
        await asyncio.sleep(3600)


async def door_check():
    """
    Check the time and either open or close the coop door
    """
    while True:
        now = DateTime.now()
        sun_data = data.get_sunrise_sunset(now)
        door_status = data.get_door_status()
        gc.collect()
        if sun_data:
            sunrise = DateTime(**sun_data['sunrise'])
            sunset = DateTime(**sun_data['sunset'])
            if door_status == DoorStatus.Closed and now > sunrise:
                open_door()
            elif door_status == DoorStatus.Closed and now > sunset:
                close_door()
            gc.collect()
        await asyncio.sleep(3600)


def main():
    """
    Set up the tasks and start the event loop
    """
    connect()
    loop = asyncio.get_event_loop()
    loop.create_task(set_time())
    loop.create_task(calc_sunrise_sunset())
    loop.create_task(door_check())
    loop.create_task(asyncio.start_server(webapp.handle, '0.0.0.0', 80))
    gc.collect()
    loop.run_forever()
