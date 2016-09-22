import config
import requests
import json


COLOR_KEYS = {
	"green": 1,
	"yellow": 2,
	"orange": 3,
	"red": 4,
	"purple": 5,
	"blue": 6,
	"sky": 7,
	"lime": 8,
	"pink": 9,
	"black": 10
}
BOARD_IDS_URL = "https://api.trello.com/1/members/{username}/boards"
GET_LISTS_URL = "https://api.trello.com/1/boards/{board_id}/lists"
GET_CARDS_URL = "https://api.trello.com/1/lists/{list_id}/cards"
PUT_CARDS_URL = "https://api.trello.com/1/cards/{card_id}/pos"
BASIC_PARAMS = {
        "key": config.TRELLO_APP_KEY,
        "token": config.TRELLO_APP_TOKEN
        }


def get_key_value(card):
	try:
		color = COLOR_KEYS[card["labels"][0]["color"]]
	except IndexError, e:
		color = 0
	return color


def get_lists_from_board(board_id):
	resp = requests.get(GET_LISTS_URL.format(board_id=board_id), params=BASIC_PARAMS)
	json_resp = json.loads(resp.text)

	lists = []
	for l in json_resp:
		lists.append(l["id"])

	return lists


def sort_list(list_id):
	resp = requests.get(GET_CARDS_URL.format(list_id=list_id), params=BASIC_PARAMS)
	json_resp = json.loads(resp.text)

	json_resp.sort(key=get_key_value, reverse=True)

	for card in json_resp:
		payload = BASIC_PARAMS
		payload["value"] = "bottom"
		requests.put(PUT_CARDS_URL.format(card_id=card["id"]), data=payload)

	return True


def sort_lists_in_board(board_id):
	lists = get_lists_from_board(board_id)

	for l in lists:
		sort_list(l)

	return True


def sort_multiple_boards(board_id_list):
	for board_id in board_id_list:
		sort_lists_in_board(board_id)

	return True


def print_board_ids():
	resp = requests.get(BOARD_IDS_URL.format(username=config.TRELLO_USERNAME), params=BASIC_PARAMS)
	json_resp = json.loads(resp.text)

	for board in json_resp:
		print board["name"], "id:   ", board["id"]

print_board_ids()

sort_multiple_boards(config.TO_SORT_BOARD_IDS)








