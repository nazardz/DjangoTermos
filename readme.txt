устонвка виртуальной среды:
	apt-get install python3-venv
	mkdir meteostat
	cd meteostat
	python3 -m venv meteostat
	source meteostat/bin/activate

	
установка сервера и библиотек:
	(распоковать архив сюда)
	pip install requirements.txt


Запуск сервера:
	python3 manage.py runserver [127.0.0.1:8000 - по умолчанию, можно изменит]
ИЛИ просто
	python3 manage.py runserver 


