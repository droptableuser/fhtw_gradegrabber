# Install
```
pip install -r requirements.txt
```
#Run
```
python3 grades.py
```

# modifications
## User and Password
If you want to spare yourself of putting in your username and password evertime you can modify the lines 64-65:
```
  user=input("username: ")
  password=getpass.getpass(prompt="password: ")
```

## Switching Semester
On line 10 one can switch the semester:
```
sem="SS2018"
```
