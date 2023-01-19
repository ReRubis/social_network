# General
Social network. 
Stores users, posts created by them, and reactions to those posts 
The plan: 
https://whimsical.com/post-7SJ7sje7QRz4TmBHDWtDQD


# Installation
Preferable method is to use devcontainer
1. install the `Remote-Containers` VS-code extenstion
2. open the project folder
3. rebuild and open the folder in container.

# Running
1. Make sure that the virtual environment is opened. 
2. If it's not, usually restarting terminal sets it in virtual env. 
If it doesn't run the command:

```sh
. ./.venv/bin/activate
```
3. Run the uvicorn
```sh
uvicorn app.main:app --reload
```

4. When it's running, it's possible to open the automated documentation. 

```
http://127.0.0.1:8000/docs
```
It also might be used for testing the app. 
