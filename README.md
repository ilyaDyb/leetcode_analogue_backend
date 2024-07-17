Leetcode_analogue pet project
=======================
[Installation](#installation)

Leetcode_analogue - speaks for itself. It is a platform where users can solve algorithmic problems.
-----------------------------------
Project's stack
* Python
* Django/DRF
* Postgres
* Celery
* Redis
* RPC
* JWT
* Docker
* docker-compose
* Swagger
  
app's design
-------------------
![system design](https://github.com/ilyaDyb/leetcode_analogue_backend/blob/main/system__design.png)
`If you are a recruiter and you are interested in me along with my project, please call or write, I can show all the functionality and explain why I used something here or somewhere else. My contacts: `

1. Telegram: http://t.me/wicki7

# Installation
Clone the repository:
```sh
$ git clone https://github.com/ilyaDyb/leetcode_analogue_backend.git
$ cd leetcode_analogue_backend

$ python3 -m venv venv
$ source venv/bin/activate

$ pip install -r requirements.txt

$ docker-compose up
```
Then stop container, migrate and load fixtures:

```sh
$ python3 manage.py migrate
$ python3 manage.py loaddata fixtures/fixture.json 
```
Set Up the Frontend:
---
To visualize everything and not just pass parameters in Swagger to view JSON responses, you should set up the frontend part of the application. The frontend can be found in the same repository.

Clone or navigate to the frontend part of the repository:
```sh
$ git clone https://github.com/ilyaDyb/leetcode_analogue_frontend.git
```
`Open the index.html file in your browser to interact with the application. Ensure that the server is restarted after loading the fixtures to reflect the changes.`

# Optional
Uncomment this code in core/main/signals.py:
```
# @receiver(post_save, sender=Problem)
# def drop_cache_after_problem_creating(created, **kwargs):
#     if created:
#         cache_key = "all_problems"
#         cache.delete(cache_key)
```