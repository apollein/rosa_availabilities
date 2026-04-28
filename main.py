import requests
from datetime import datetime, timedelta, date
from signalbot import SignalBot, Config, Command, Context, triggered, enable_console_logging
import asyncio
import argparse
from os import path, getcwd
import time
import random
import sys

async def main(phone_number, server, url):
	headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0"}
	cwd = getcwd()
	try:
		bot = SignalBot(Config(signal_service=server, phone_number=phone_number, connection_mode="http_only",))
	except Exception as e:
		print(str(e), file=sys.stderr)
		print("Try linking API to your device via http://{}/v1/qrcodelink?device_name=signal-api".format(server))
		with open('{}/errors'.format(cwd), 'a') as f:
			f.write("{} {}".format(datetime.now().strftime("%d/%m/%y %H:%M:%S"), str(e)))
		exit(1)
	try:
		r = requests.get(url, headers=headers)
		if r.status_code!=200:
			print("{} status_code is {}, not 200".format(datetime.now().strftime("%d/%m/%y %H:%M:%S"), str(r.status_code)), file=sys.stderr)
			await bot.send(phone_number, "{} status_code is {}, not 200".format(datetime.now().strftime("%d/%m/%y %H:%M:%S"), str(r.status_code)))
			exit(1)
		r = r.json()
		if 'availabilities' in r:
			if len(r['availabilities'])!=0:
				if 'date' in r['availabilities'][0]:
					d = datetime.fromisoformat(r['availabilities'][0]['date'])+timedelta(hours=2)
					if path.exists('{}/currentdate'.format(cwd)):
						with open('{}/currentdate'.format(cwd), 'r') as f:
							current_date = datetime.strptime(f.read().strip(), '%d-%m-%Y')
						if current_date.date()!=d.date():
							with open('{}/currentdate'.format(cwd), 'w') as f:
								f.write(d.strftime('%d-%m-%Y'))
							if d.date()<date(2027, 3, 25):
								if current_date.date()>d.date():
									await bot.send(phone_number, '✨ nouveau rdv le {} pour Leempoel ✨'.format(d.strftime('%d-%m-%Y')))
					else:
						with open('{}/currentdate'.format(cwd), 'w') as f:
							f.write(d.strftime('%d-%m-%Y'))
	except Exception as e:
		print(str(e), file=sys.stderr)
		await bot.send("{} {}".format(datetime.now().strftime("%d/%m/%y %H:%M:%S"), str(e)))
		with open('{}/errors'.format(cwd), 'a') as f:
			f.write("{} {}".format(datetime.now().strftime("%d/%m/%y %H:%M:%S"), str(e)))
		exit(1)

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("phone_number", help="Signal phone number", type=str, )
	parser.add_argument("server", help="Signal REST API server", type=str, )
	parser.add_argument("url", help="ROSA Url", type=str, )
	args = parser.parse_args()
	time.sleep(random.randint(0, 10))
	asyncio.run(main(args.phone_number, args.server, args.url))
