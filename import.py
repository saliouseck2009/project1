# from application import engine,db
# import csv
#import requests
# def main():
#     f = open("books.csv")
#     reader = csv.reader(f)
#     i =0
#     for isbn, title, author, year in reader:
#         db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
#                    {"isbn": isbn, "title": title, "author": author, "year" : year})
#         i+=1
#         print(i)
#     db.commit()

# if __name__ == "__main__":
#     main()
# import requests
# res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "EGg09TETdsx6k7NS8aheJw", "isbns": "9781632168146"})
# if res.status_code != 200:
#     #flash("ERROR: API request unsuccessful.")
#     #redirect(url_for(''))
#     print("error")
# else:
#     data= res.json()
#     print(data['books'][0]['id'])
#export DATABASE_URL='postgres://zyixysspleqiwj:b726f330c847e132a5034c34d28051dc5ddcf3917ec5753f1da8f78b96cac334@ec2-46-137-84-173.eu-west-1.compute.amazonaws.com:5432/d736pv9i3rkvcg'
source /home/seck/virtual_env/projet1/bin/activate
export DATABASE_URL='postgres://zyixysspleqiwj:b726f330c847e132a5034c34d28051dc5ddcf3917ec5753f1da8f78b96cac334@ec2-46-137-84-173.eu-west-1.compute.amazonaws.com:5432/d736pv9i3rkvcg'
export FLASK_ENV=development
export FLASK_APP=application.py