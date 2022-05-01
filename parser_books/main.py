from bs4 import BeautifulSoup

import csv 
import lxml
import os 
import json
import requests


def get_data(url, headers):
	req = requests.get(url=url, headers=headers)
	src = req.text 

	soup = BeautifulSoup(src, 'lxml')
	count_books = int(soup.find('div', class_='comm_head_com').text.split(':')[-1].strip())
	book_data_dict = {}

	try:
		os.remove('result_data\\csv_data.csv')
	except FileNotFoundError as ex:
		print('file not found')

	for page in range(0, count_books, 20):
		url = f'https://bookclub.ua/catalog/books/pop/?i={page}'
		
		req = requests.get(url=url, headers=headers)
		src = req.text 
		soup = BeautifulSoup(src, 'lxml')

		book_data = soup.find_all('section', class_='book-inlist')
		
		for item in book_data:
			id_book = item.find('div', class_='book-inlist-name').find('a').get('onclick').split()[3].strip("',")
			name_book =  item.find('div', class_='book-inlist-name').find('a').text 
			author_book = item.find('div', class_='authorName').text 
			arcticle_book = item.find('div', class_='mainGoodContent').text 
			url_book =  'https://bookclub.ua/' + item.find('div', class_='book-inlist-name').find('a').get('href') 
			price_book = item.find('div', class_='book-inlist-price').text[0:4] + ' ГРН'
			

			book_data_dict[id_book] = {
				'Назва': name_book.strip("\t"),
				'Автор': author_book,
				'Опис': arcticle_book,
				'Ссилка': url_book,
				'Ціна': price_book.strip("\n"),
			}



			with open('result_data\\csv_data.csv', mode='a', newline='', encoding='cp1251') as f:
				writer = csv.writer(f, delimiter=';')
				writer.writerow((
						id_book,
						name_book,
						author_book,
						arcticle_book,
						url_book,
						price_book,
					))	

		print(f'successfully {page} of {count_books}')
	print(f'successfully {count_books} of {count_books}')

	with open('result_data\\json_data.json', 'w', encoding='utf-8') as f:
		json.dump(book_data_dict, f, indent=4, ensure_ascii=False)


def main():
	url = 'https://bookclub.ua/catalog/books/pop/?i=0'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	}

	get_data(url, headers)


if __name__ == '__main__':
	main()
