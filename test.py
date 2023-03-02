from flask import Flask, render_template, request,jsonify, make_response
import sqlite3 as sql
import requests
import ipaddress
import json
 
app = Flask(__name__)
 
app.config['DEBUG'] = True
 
 
@app.route('/')
def index(): 
        req = requests.get('https://ipgeolocation.abstractapi.com/v1/?ip_address=37.239.15.16&api_key=8c826ba938b54b9c8bfb44ad9ec5dc8f')
        con = sql.connect("thistube.db")
        cur = con.cursor()
        cur.execute("""INSERT INTO devices (idUser,devicesData) VALUES (?,?)""",("0",str(req.content)))
        con.commit()
        con.close
        return "ll"

 
@app.route('/geolocation', methods=['GET'])
def get_geolocation():
        return render_template('devices-logs.html')


@app.route('/fetch-gelocation', methods=['POST'])
def post_geolocation():
    try:
        a = b'{"ip_address":"37.239.15.16","city":"Karbala","city_geoname_id":94824,"region":"Karbal\xc4\x81\xca\xbc","region_iso_code":"KA","region_geoname_id":94823,"postal_code":null,"country":"Iraq","country_code":"IQ","country_geoname_id":99237,"country_is_eu":false,"continent":"Asia","continent_code":"AS","continent_geoname_id":6255147,"longitude":44.0,"latitude":33.0,"security":{"is_vpn":false},"timezone":{"name":"Asia/Baghdad","abbreviation":"+03","gmt_offset":3,"current_time":"10:30:51","is_dst":false},"flag":{"emoji":"\xf0\x9f\x87\xae\xf0\x9f\x87\xb6","unicode":"U+1F1EE U+1F1F6","png":"https://static.abstractapi.com/country-flags/IQ_flag.png","svg":"https://static.abstractapi.com/country-flags/IQ_flag.svg"},"currency":{"currency_name":"Iraqi Dinar","currency_code":"IQD"},"connection":{"autonomous_system_number":203214,"autonomous_system_organization":"Hulum Almustakbal Company for Communication Engineering and Services Ltd","connection_type":"Corporate","isp_name":"EarthLink Telecommunications","organization_name":"EarthLink Ltd. Communications&Internet Services"}}'
        data = json.loads(a)

        #req = requests.get('https://ipgeolocation.abstractapi.com/v1/?ip_address=37.239.15.16&api_key=8c826ba938b54b9c8bfb44ad9ec5dc8f')
        return make_response(jsonify(data))
    except ValueError:
        return make_response(jsonify({'error': 'Invalid IP Address'}))
    except Exception as e:
        return make_response(jsonify({'error': str(e)}))

        
 
if __name__ == "__main__":
    app.run(debug=True)