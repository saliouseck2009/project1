# from application import engine,db
# import csv

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