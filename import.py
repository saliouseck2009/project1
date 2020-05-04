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
