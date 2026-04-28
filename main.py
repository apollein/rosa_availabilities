import requests
from datetime import datetime, timedelta, date
from signalbot import SignalBot, Config, Command, Context, triggered, enable_console_logging
import asyncio
from os import path, getcwd
import time
import random
import sys
import json

def choose_user_agent():
	user_agents = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.10 Safari/605.1.1", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.", "Mozilla/5.0 (iPhone; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/360.1.737798518 Mobile/15E148 Safari/604.", "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.3", "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.3"]
	user_agent = user_agents[random.randint(0, len(user_agents)-1)]
	return user_agent

async def main(phone_number, server, url, cwd):
	headers = {"User-Agent": choose_user_agent()}
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
					if path.exists('{}/firstdate'.format(cwd)):
						with open('{}/firstdate'.format(cwd), w) as f:
							current_date = datetime.strptime(f.read().strip(), '%d-%m-%Y')
							f.write(current_date)
					if path.exists('{}/currentdate'.format(cwd)):
						with open('{}/currentdate'.format(cwd), 'r') as f:
							current_date = datetime.strptime(f.read().strip(), '%d-%m-%Y')
						if current_date.date()!=d.date():
							with open('{}/currentdate'.format(cwd), 'w') as f:
								f.write(d.strftime('%d-%m-%Y'))
							with open('{}/firstdate'.format(cwd), r) as f:
								first_date = datetime.strptime(f.read.strip(), '%d-%m-%Y')
							if d.date()<first_date:
								if current_date.date()>d.date():
									await bot.send(phone_number, '✨ nouveau rdv le {} pour Leempoel ✨'.format(d.strftime('%d-%m-%Y')))
					else:
						with open('{}/currentdate'.format(cwd), 'w') as f:
							f.write(d.strftime('%d-%m-%Y'))
	except Exception as e:
		print(str(e), file=sys.stderr)
		await bot.send(phone_number, "{} {}".format(datetime.now().strftime("%d/%m/%y %H:%M:%S"), str(e)))
		with open('{}/errors'.format(cwd), 'a') as f:
			f.write("{} {}".format(datetime.now().strftime("%d/%m/%y %H:%M:%S"), str(e)))
		exit(1)

if __name__=="__main__":
	cwd = getcwd()
	with open('{}/config.json'.format(str(cwd)), 'r') as f:
		try:
			parameters = json.load(f)
		except Exception as e:
			print("No configuration file found. Exiting.")
			exit(1)
		time.sleep(random.randint(0, 1))
		if parameters['signal']:
			asyncio.run(main(parameters['signal-phone-number'], parameters['signal-server'], parameters['rosa-url'], cwd))
		else:
			print("Not supported.")
			exit(1)
