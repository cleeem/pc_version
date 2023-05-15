#!/usr/bin/env python
# s3s (ↄ) 2022-2023 eli fessler (frozenpandaman), clovervidia
# Based on splatnet2statink (ↄ) 2017-2023 eli fessler (frozenpandaman), clovervidia
# https://github.com/frozenpandaman/s3s
# License: GPLv3

import argparse, base64, datetime, json, os, shutil, re, requests, sys, time, uuid
from concurrent.futures import ThreadPoolExecutor
from subprocess import call
import msgpack
from packaging import version
import iksm, utils
import customtkinter


A_VERSION = "0.4.0"

DEBUG = False

thread_pool = ThreadPoolExecutor(max_workers=4)


# SET HTTP HEADERS
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Linux; Android 11; Pixel 5) ' \
						'AppleWebKit/537.36 (KHTML, like Gecko) ' \
						'Chrome/94.0.4606.61 Mobile Safari/537.36'
APP_USER_AGENT = str(DEFAULT_USER_AGENT)

def addincsv(url_file,objet,newline =True, delimiter =  None):
    csv = open(url_file,'a',encoding='utf-8')
    if newline:
        csv.write((str(objet)+'\n'))
    else:
        csv.write(str(objet))
        csv.write(str(delimiter))
    csv.close()


def setup():


	global CONFIG_DATA, USER_LANG, USER_COUNTRY, GTOKEN, BULLETTOKEN, \
		   SESSION_TOKEN, F_GEN_URL, config_file, config_path, APP_USER_AGENT

	

	os.system("") # ANSI escape setup
	if sys.version_info[1] >= 7: # only works on python 3.7+
		sys.stdout.reconfigure(encoding='utf-8') # note: please stop using git bash

	# CONFIG.TXT CREATION
	if getattr(sys, 'frozen', False): # place config.txt in same directory as script (bundled or not)
		app_path = os.path.dirname(sys.executable)
	elif __file__:
		app_path = os.path.dirname(__file__)
	config_path = os.path.join(app_path, "config.txt")

	# print(config_path)

	try:
		config_file = open(config_path, "r")
		CONFIG_DATA = json.load(config_file)
		config_file.close()
	except (IOError, ValueError):
		print("Generating new config file.")
		CONFIG_DATA = { "acc_loc": "", "gtoken": "", "bullettoken": "", "session_token": "", "f_gen": "https://api.imink.app/f"}
		config_file = open(config_path, "w")
		config_file.seek(0)
		config_file.write(json.dumps(CONFIG_DATA, indent=4, sort_keys=False, separators=(',', ': ')))
		config_file.close()
		config_file = open(config_path, "r")
		CONFIG_DATA = json.load(config_file)
		config_file.close()

	# SET GLOBALS
	USER_LANG     = CONFIG_DATA["acc_loc"][:5]   # user input
	USER_COUNTRY  = CONFIG_DATA["acc_loc"][-2:]  # nintendo account info
	GTOKEN        = CONFIG_DATA["gtoken"]        # for accessing splatnet - base64 json web token
	BULLETTOKEN   = CONFIG_DATA["bullettoken"]   # for accessing splatnet - base64
	SESSION_TOKEN = CONFIG_DATA["session_token"] # for nintendo login
	F_GEN_URL     = CONFIG_DATA["f_gen"]         # endpoint for generating f (imink API by default)



def write_config(tokens):
	'''Writes config file and updates the global variables.'''

	config_file = open(config_path, "w")
	config_file.seek(0)
	config_file.write(json.dumps(tokens, indent=4, sort_keys=False, separators=(',', ': ')))
	config_file.close()

	config_file = open(config_path, "r")
	CONFIG_DATA = json.load(config_file)

	global USER_LANG
	USER_LANG = CONFIG_DATA["acc_loc"][:5]
	global USER_COUNTRY
	USER_COUNTRY = CONFIG_DATA["acc_loc"][-2:]
	global GTOKEN
	GTOKEN = CONFIG_DATA["gtoken"]
	global BULLETTOKEN
	BULLETTOKEN = CONFIG_DATA["bullettoken"]
	global SESSION_TOKEN
	SESSION_TOKEN = CONFIG_DATA["session_token"]

	config_file.close()


def headbutt(forcelang=None):
	'''Returns a (dynamic!) header used for GraphQL requests.'''

	if forcelang:
		lang    = forcelang
		country = forcelang[-2:]
	else:
		lang    = USER_LANG
		country = USER_COUNTRY

	graphql_head = {
		'Authorization':    f'Bearer {BULLETTOKEN}', # update every time it's called with current global var
		'Accept-Language':  lang,
		'User-Agent':       APP_USER_AGENT,
		'X-Web-View-Ver':   iksm.get_web_view_ver(),
		'Content-Type':     'application/json',
		'Accept':           '*/*',
		'Origin':           iksm.SPLATNET3_URL,
		'X-Requested-With': 'com.nintendo.znca',
		'Referer':          f'{iksm.SPLATNET3_URL}?lang={lang}&na_country={country}&na_lang={lang}',
		'Accept-Encoding':  'gzip, deflate'
	}
	return graphql_head


def prefetch_checks(printout=False):
	'''Queries the SplatNet 3 homepage to check if our gtoken & bulletToken are still valid and regenerates them if not.'''

	if printout:
		print("Validating your tokens...", end='\r')

	iksm.get_web_view_ver() # setup

	if SESSION_TOKEN == "" or GTOKEN == "" or BULLETTOKEN == "":
		gen_new_tokens("blank")

	sha = utils.translate_rid["HomeQuery"]
	test = requests.post(utils.GRAPHQL_URL, data=utils.gen_graphql_body(sha), headers=headbutt(), cookies=dict(_gtoken=GTOKEN))
	if test.status_code != 200:
		if printout:
			print("\n")
		gen_new_tokens("expiry")
	else:
		if printout:
			print("Validating your tokens... done.\n")


def gen_new_tokens(reason="expiry", force=False):
	'''Attempts to generate new tokens when the saved ones have expired.'''

	manual_entry = False
	if force != True: # unless we force our way through
		if reason == "blank":
			print("Blank token(s).          ")
		elif reason == "expiry":
			print("The stored tokens have expired.")
		else:
			print("Cannot access SplatNet 3 without having played online.")
			sys.exit(0)

	if SESSION_TOKEN == "":
		url_login, auth_code = iksm.get_login_url(app_user_agent=APP_USER_AGENT)
		print("Please log in to your Nintendo Account to obtain your session_token.")
		new_token = iksm.log_in(ver=A_VERSION,auth_code_verifier=auth_code, use_account_url=user_account)
		if new_token is None:
			print("There was a problem logging you in. Please try again later.")
		elif new_token == "skip":
			manual_entry = True
		else:
			print("\nWrote session_token to config.txt.")
		CONFIG_DATA["session_token"] = new_token
		write_config(CONFIG_DATA)
	elif SESSION_TOKEN == "skip":
		manual_entry = True

	if manual_entry: # no session_token ever gets stored
		print("\nYou have opted against automatic token generation and must manually input your tokens.\n")
		new_gtoken, new_bullettoken = iksm.enter_tokens()
		acc_lang = "en-US" # overwritten by user setting
		acc_country = "US"
		print("Using `US` for country by default. This can be changed in config.txt.")
	else:
		print("Attempting to generate new gtoken and bulletToken...")
		new_gtoken, acc_name, acc_lang, acc_country = iksm.get_gtoken(F_GEN_URL, SESSION_TOKEN, A_VERSION)
		new_bullettoken = iksm.get_bullet(new_gtoken, APP_USER_AGENT, acc_lang, acc_country)
	CONFIG_DATA["gtoken"] = new_gtoken # valid for 6 hours
	CONFIG_DATA["bullettoken"] = new_bullettoken # valid for 2 hours

	global USER_LANG
	if acc_lang != USER_LANG:
		acc_lang = USER_LANG
	CONFIG_DATA["acc_loc"] = f"{acc_lang}|{acc_country}"

	write_config(CONFIG_DATA)

	if new_bullettoken == "":
		print("Wrote gtoken to config.txt, but could not generate bulletToken.")
		print("Is SplatNet 3 undergoing maintenance?")
		sys.exit(1)
	if manual_entry:
		print("Wrote tokens to config.txt.\n") # and updates acc_country if necessary...
	else:
		print(f"Wrote tokens for {acc_name} to config.txt.\n")


def fetch_json(which, bar, separate=False, exportall=False, specific=False, numbers_only=False, printout=False, skipprefetch=False):
	'''Returns results JSON from SplatNet 3, including a combined dictionary for battles + SR jobs if requested.'''

	# swim = SquidProgress()

	if DEBUG:
		print(f"* fetch_json() called with which={which}, separate={separate}, " \
			f"exportall={exportall}, specific={specific}, numbers_only={numbers_only}")

	if exportall and not separate:
		print("* fetch_json() must be called with separate=True if using exportall.")
		sys.exit(1)

	if not skipprefetch:
		prefetch_checks(printout)
		if DEBUG:
			print("* prefetch_checks() succeeded")
	else:
		if DEBUG:
			print("* skipping prefetch_checks()")
	# swim()

	ink_list, salmon_list = [], []
	parent_files = []

	queries = []
	# if which in ("both", "ink"):
	# 	if specific in (True, "regular"):
	# 		queries.append("RegularBattleHistoriesQuery")
	# 	if specific in (True, "anarchy"):
	# 		queries.append("BankaraBattleHistoriesQuery")
	# 	if specific in (True, "x"):
	# 		queries.append("XBattleHistoriesQuery")
	# 	# if specific in (True, "league"):
	# 		# queries.append("LeagueBattleHistoriesQuery") # LEAGUE TODO & check query name
	# 	if specific in (True, "private") and not utils.custom_key_exists("ignore_private", CONFIG_DATA):
	# 		queries.append("PrivateBattleHistoriesQuery")
	# 	if not specific: # False
	# 		if DEBUG:
	# 			print("* not specific, just looking at latest")
	queries.append("LatestBattleHistoriesQuery")
	# else:
	# 	queries.append(None)
	# if which in ("both", "salmon"):
	# 	queries.append("CoopHistoryQuery")
	# else:
	# 	queries.append(None)

	needs_sorted = False # https://ygdp.yale.edu/phenomena/needs-washed :D

	for sha in queries:
		if sha is not None:
			if DEBUG:
				print(f"* making query1 to {sha}")
			lang = 'en-US' if sha == "CoopHistoryQuery" else None
			sha = utils.translate_rid[sha]
			battle_ids, job_ids = [], []

			query1 = requests.post(utils.GRAPHQL_URL,
				data=utils.gen_graphql_body(sha),
				headers=headbutt(forcelang=lang),
				cookies=dict(_gtoken=GTOKEN))
			query1_resp = json.loads(query1.text)
			# swim()

			# ink battles - latest 50 of any type
			if "latestBattleHistories" in query1_resp["data"]:
				for k, battle_group in enumerate(query1_resp["data"]["latestBattleHistories"]["historyGroups"]["nodes"]):
					size = len(battle_group)
					for i, battle in enumerate(battle_group["historyDetails"]["nodes"]):
						if not bar is None:
							bar.set(i/size)
							bar.update()
						battle_ids.append(battle["id"]) # don't filter out private battles here - do that in post_result()

			# # ink battles - latest 50 turf war
			# elif "regularBattleHistories" in query1_resp["data"]:
			# 	needs_sorted = True
			# 	for battle_group in query1_resp["data"]["regularBattleHistories"]["historyGroups"]["nodes"]:
			# 		for battle in battle_group["historyDetails"]["nodes"]:
			# 			battle_ids.append(battle["id"])
			# # ink battles - latest 50 anarchy battles
			# elif "bankaraBattleHistories" in query1_resp["data"]:
			# 	needs_sorted = True
			# 	for battle_group in query1_resp["data"]["bankaraBattleHistories"]["historyGroups"]["nodes"]:
			# 		for battle in battle_group["historyDetails"]["nodes"]:
			# 			battle_ids.append(battle["id"])
			# # ink battles - latest 50 x battles
			# elif "xBattleHistories" in query1_resp["data"]:
			# 	needs_sorted = True
			# 	for battle_group in query1_resp["data"]["xBattleHistories"]["historyGroups"]["nodes"]:
			# 		for battle in battle_group["historyDetails"]["nodes"]:
			# 			battle_ids.append(battle["id"])
			# # ink battles - latest 50 private battles
			# elif "privateBattleHistories" in query1_resp["data"] \
			# and not utils.custom_key_exists("ignore_private", CONFIG_DATA):
			# 	needs_sorted = True
			# 	for battle_group in query1_resp["data"]["privateBattleHistories"]["historyGroups"]["nodes"]:
			# 		for battle in battle_group["historyDetails"]["nodes"]:
			# 			battle_ids.append(battle["id"])

			# # salmon run jobs - latest 50
			# elif "coopResult" in query1_resp["data"]:
			# 	for shift in query1_resp["data"]["coopResult"]["historyGroups"]["nodes"]:
			# 		for job in shift["historyDetails"]["nodes"]:
			# 			job_ids.append(job["id"])

			if numbers_only:
				ink_list.extend(battle_ids)
				# salmon_list.extend(job_ids)
			# else: # ALL DATA - TAKES A LONG TIME
			# 	ink_list.extend(thread_pool.map(fetch_detailed_result, [True]*len(battle_ids), battle_ids, [swim]*len(battle_ids)))

			# 	salmon_list.extend(thread_pool.map(fetch_detailed_result, [False]*len(job_ids), job_ids, [swim]*len(job_ids)))

			# 	if needs_sorted: # put regular, bankara, and private in order, since they were exported in sequential chunks
			# 		try:
			# 			ink_list = [x for x in ink_list if x['data']['vsHistoryDetail'] is not None] # just in case
			# 			ink_list = sorted(ink_list, key=lambda d: d['data']['vsHistoryDetail']['playedTime'])
			# 		except:
			# 			print("(!) Exporting without sorting results.json")
			# 		try:
			# 			salmon_list = [x for x in salmon_list if x['data']['coopHistoryDetail'] is not None]
			# 			salmon_list = sorted(salmon_list, key=lambda d: d['data']['coopHistoryDetail']['playedTime'])
			# 		except:
			# 			print("(!) Exporting without sorting coop_results.json")
			parent_files.append(query1_resp)
		else: # sha = None (we don't want to get the specified result type)
			pass

	if exportall:
		return parent_files, ink_list, salmon_list
	else:
		if separate:
			return ink_list, salmon_list
		else:
			combined = ink_list + salmon_list
			return combined


def fetch_and_upload_single_result(hash, noun, dict_key):
	'''Performs a GraphQL request for a single vsResultId/coopHistoryDetailId and call post_result().'''

	if noun in ("battles", "battle"):
		if dict_key == "VsHistoryDetailQuery":
			dict_key2 = "vsResultId"
			key3 = hash
		else:
			dict_key2 = "id"
			with open("pid.txt") as file:
				key3=file.read()

		lang = None
	

	result_post = requests.post(utils.GRAPHQL_URL,
			data=utils.gen_graphql_body(utils.translate_rid[dict_key], dict_key2, key3),
			headers=headbutt(forcelang=lang),
			cookies=dict(_gtoken=GTOKEN))
	try:
		result = json.loads(result_post.text)

		# print()
		# print("resultat : ")
		# print(result.keys())

		return result

	except json.decoder.JSONDecodeError: # retry once, hopefully avoid a few errors
		result_post = requests.post(utils.GRAPHQL_URL,
				data=utils.gen_graphql_body(utils.translate_rid[dict_key], dict_key2, hash),
				headers=headbutt(forcelang=lang),
				cookies=dict(_gtoken=GTOKEN))
		try:
			result = json.loads(result_post.text)

		except json.decoder.JSONDecodeError:
			if utils.custom_key_exists("errors_pass_silently", CONFIG_DATA):
				print("Error uploading one of your battles. Continuing...")
				pass
			else:
				print("Error uploading one of your battles. Please try running s3s again.")
				sys.exit(1)


def export_seed_json(skipprefetch=False):
	'''Export a JSON file for use with Lean's seed checker at https://leanny.github.io/splat3seedchecker/.'''

	try:
		import pymmh3 as mmh3
	except ModuleNotFoundError:
		print("This function requires a Python module you don't have installed. " \
			"Please run " + '`\033[91m' + "pip install -r requirements.txt" + '\033[0m`' + " and try again.")
		sys.exit(1)

	if not skipprefetch:
		prefetch_checks(printout=True)

	sha = utils.translate_rid["MyOutfitCommonDataEquipmentsQuery"]
	outfit_post = requests.post(utils.GRAPHQL_URL, data=utils.gen_graphql_body(sha),
		headers=headbutt(), cookies=dict(_gtoken=GTOKEN))

	sha = utils.translate_rid["LatestBattleHistoriesQuery"]
	history_post = requests.post(utils.GRAPHQL_URL, data=utils.gen_graphql_body(sha),
		headers=headbutt(), cookies=dict(_gtoken=GTOKEN))

	if outfit_post.status_code != 200 or history_post.status_code != 200:
		print("Could not reach SplatNet 3. Exiting.")
		sys.exit(1)
	try:
		outfit = json.loads(outfit_post.text)
		history = json.loads(history_post.text)
	except:
		print("Ill-formatted JSON file received. Exiting.")
		sys.exit(1)

	try:
		pid = history["data"]["latestBattleHistories"]["historyGroupsOnlyFirst"]["nodes"][0]["historyDetails"]["nodes"][0]["player"]["id"]
		# VsPlayer-u-<20 char long player id>:RECENT:<YYYYMMDD>T<HHMMSS>_<UUID>:u-<same player id as earlier>
		s = utils.b64d(pid)
		r = s.split(":")[-1]
	except KeyError: # no recent battles (mr. grizz is pleased)
		try:
			sha = utils.translate_rid["CoopHistoryQuery"]
			history_post = requests.post(utils.GRAPHQL_URL, data=utils.gen_graphql_body(sha),
				headers=headbutt(), cookies=dict(_gtoken=GTOKEN))

			if history_post.status_code != 200:
				print("Could not reach SplatNet 3. Exiting.")
				sys.exit(1)
			try:
				history = json.loads(history_post.text)
			except:
				print("Ill-formatted JSON file received. Exiting.")
				sys.exit(1)

			pid = history["data"]["coopResult"]["historyGroupsOnlyFirst"]["nodes"][0]["historyDetails"]["nodes"][0]["id"]
			# CoopHistoryDetail-u-<20 char long player id>:<YYYYMMDD>T<HHMMSS>_<UUID>
			s = utils.b64d(pid)
			r = s.split(":")[0].replace("CoopHistoryDetail-", "")
		except KeyError:
			r = ""

	h = mmh3.hash(r)&0xFFFFFFFF # make positive
	key = base64.b64encode(bytes([k^(h&0xFF) for k in bytes(r, "utf-8")]))
	t = int(time.time())

	with open(os.path.join(os.getcwd(), f"gear_{t}.json"), "x") as fout:
		json.dump({"key": key.decode("utf-8"), "h": h, "timestamp": t, "gear": outfit}, fout)

	print(f"gear_{t}.json has been exported.")


def parse_arguments():
	'''Setup for command-line options.'''

	parser = argparse.ArgumentParser()
	srgroup = parser.add_mutually_exclusive_group()
	parser.add_argument("-M", dest="N", required=False, nargs="?", action="store",
		help="monitoring mode; pull data every N secs (default: 300)", const=300)
	parser.add_argument("-r", required=False, action="store_true",
		help="retroactively post unuploaded battles/jobs")
	srgroup.add_argument("-nsr", required=False, action="store_true",
		help="do not check for Salmon Run jobs")
	srgroup.add_argument("-osr", required=False, action="store_true",
		help="only check for Salmon Run jobs")
	parser.add_argument("--blackout", required=False, action="store_true",
		help="remove player names from uploaded scoreboard data")
	parser.add_argument("-o", required=False, action="store_true",
		help="export all possible results to local files")
	parser.add_argument("-i", dest="path", nargs=2, required=False,
		help="upload local results: `-i (coop_)results/ overview.json`")
	parser.add_argument("-t", required=False, action="store_true",
		help="dry run for testing (won't post to stat.ink)")
	parser.add_argument("--getseed", required=False, action="store_true",
		help="export JSON for gear & Shell-Out Machine seed checker")
	parser.add_argument("--skipprefetch", required=False, action="store_true", help=argparse.SUPPRESS)
	return parser.parse_args()


def main(bar=None, game_index = 1, use_account="", dict_key=""):
	'''Main process, including I/O and setup.'''

	global user_account
	user_account = use_account

	setup()

	# regular run
	#############
	which = "ink"

	# n = get_num_results(which)
	n = game_index - 1
	# print("Pulling data from online...")

	# ! fetch from online
	try:
		results = fetch_json(which, bar=bar, numbers_only=True, skipprefetch=False)
	except json.decoder.JSONDecodeError:
		print("\nCould not fetch results JSON. Are your tokens invalid?")
		sys.exit(1)

	# results = results[n:] # limit to n uploads
	# results.reverse() # sort from oldest to newest
	noun = utils.set_noun(which)

	return_list = []

	# for hash in results:
		
	return_list.append(fetch_and_upload_single_result(results[n], noun, dict_key)) # not monitoring mode

	thread_pool.shutdown(wait=True)

	return return_list[0]


# if __name__ == "__main__":
# 	setup()
# 	data = main()

# 	from Game import Game

# 	test = Game(data)

# 	print(test)