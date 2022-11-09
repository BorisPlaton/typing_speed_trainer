# Typing speed trainer

Its is a typing speed trainer that is realised as a web-app via [Django](https://www.djangoproject.com/) and vanilla JavaScript.

![Main page](https://i.postimg.cc/XqMwcMTh/Screenshot-from-2022-11-09-09-19-22.png "Main page")

![User page](https://i.postimg.cc/gJ3wpxTS/Screenshot-from-2022-11-09-09-19-12.png "User page")

## Setup

### Development

### .env.dist

All environment variables that are used in development are specified in the `.env.dist` file in the `env` folder. Also, this file is used in the `docker-compose.dev.yml` file and shell scripts. 

#### Virtual environment

At first, you must install all necessarily dependencies. For this you should create a virtual environment. For instance, you may use a `virtualenv`:
```
$ virtualenv --python 3.10 venv
```
Afterwards, activate it:
```
$ . venv/bin/activate
```
The `requirements` directory has two files:
* `dev.txt` - contains all dependencies that are used during a development process
* `prod.txt` - contains all dependencies that are used at the production

Install all packages that are specified in the `dev.txt` file. Run the following command to make it:
```
$ pip install -r requirements/dev.txt
```

#### Application server

The application uses `Redis` and `Postgres` databases. Also, JavaScript at the frontend uses API for generating random words. To simplify the setup process of all this services you already have a `docker-compose.dev.yml` file that has done it for you. You can start them with all necessarily environment variables via shell script `start_dev_environment.sh` that is placed in the `scripts` folder. Type the following command to make it:
```
$ . scripts/start_dev_environment.sh
Creating network "typing_speed_trainer_default" with the default driver
Creating typing_speed_trainer_dev_random_words_api_1 ... done
Creating typing_speed_trainer_dev_database_1         ... done
Creating typing_speed_trainer_dev_redis_1            ... done
```
Afterwards, make migrations and run an application server:
```
$ cd typing_speed_trainer
$ python manage.py migrate
$ python manage.py runserver
```
To stop all of them you may run a shell script `down_dev_environment.sh` that is in the `scripts` folder too.
```
$ . scripts/down_dev_environment.sh
Stopping typing_speed_trainer_dev_database_1         ... done
Stopping typing_speed_trainer_dev_redis_1            ... done
Stopping typing_speed_trainer_dev_random_words_api_1 ... done
Removing typing_speed_trainer_dev_database_1         ... done
Removing typing_speed_trainer_dev_redis_1            ... done
Removing typing_speed_trainer_dev_random_words_api_1 ... done
Removing network typing_speed_trainer_default
```

#### Tests

The application uses the [Pytest](https://docs.pytest.org/en/7.2.x/) package for testing. You can run all tests via the following command if you are in the `typing_speed_trainer` directory:
```
$ pytest
```

### Production

#### .env

Before start the application you have to create `.env` in the `env` folder. You already have a `.env.dist` file which contains the template of the `.env` file and several default values. You may use it in the development.

#### Start application

You have a `docker-compose.yml` file in the root directory with all necessarily configuration. If you have created the `.env` file, you will start the application if you print following command:
```
$ docker-compose up
```
The application works on `8000` port at the `127.0.0.1` ip address. Now you can go to browser and check it out.


