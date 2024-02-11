# Author: Tushar Yadav
# CWID: 885174284
# Course: CPSC-535
# FirstCodeAssignment


# ====================== Initial Book Dump ==========================

# bookDump = [
#         {"title": "Lord Of The Rings 1", "author":"J.R.R. Tolkien3"},
#         {"title": "Lord Of The Rings 3", "author":"J.R.R. Tolkien1"},
#         {"title": "Lord Of The Rings 2", "author":"J.R.R. Tolkien2"},
#         {"title": "Harry Potter 1", "author":"J.K. Rowlings8"},
#         {"title": "Harry Potter 2", "author":"J.K. Rowlings5"},
#         {"title": "Harry Potter 3", "author":"J.K. Rowlings6"},
#         {"title": "Harry Potter 5", "author":"J.K. Rowlings1"},
#         {"title": "Harry Potter 4", "author":"J.K. Rowlings2"},
#         {"title": "Harry Potter 6", "author":"J.K. Rowlings3"},
#         {"title": "Harry Potter 7", "author":"J.K. Rowlings4"},
#     ]

bookDump = [
        {"title": "The Old Man and the Sea", "author":"Ernest Hemingway"},
        {"title": "Pride and Prejudice", "author":"Jane Austen"},
        {"title": "The Great Gatsby", "author":"F. Scott Fitzgerald"},
        {"title": "1984", "author":"George Orwell"},
        {"title": "To Kill a Mockingbird", "author":"Harper Lee"}
]

# ===================== Book Class ===================================

class Book:

    books = []

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.books.append({"title": self.title, "author": self.author})
    
    def __lt__(self, other):
        return self.author.lower() < other.author.lower()

    @classmethod
    def list_books(cls):

        print("Unsorted Dump of Books")
        for book in cls.books:
            print(f'"{book["title"]}" by {book["author"]}')
            
        # print("\n---------\n")
        # print("Sorted Books")

        # for book in sorted(cls.books, key=lambda x: x["author"].lower()):
        #     print(f'"{book["title"]}" by {book["author"]}')

    @classmethod
    def find_book(cls, title):
        for book in cls.books:
            if book['title'].lower() == title.lower():
                return book
        return None

    @classmethod
    def delete_book(cls, title):
        for book in cls.books:
            if book['title'].lower() == title.lower():
                cls.books = [book for book in cls.books if book['title'].lower() != title.lower()]
                return book['title'], book['author']
        return None, None

# =========================== Sort Books Method =====================
    
def sort_books(book_list):
    return sorted(book_list)

# =========================== Main Function =====================

if __name__ == "__main__":

    Library_Books = []

    # Creating book objects from Initial Book Dump
    for book in bookDump:           
        Library_Books.append(Book(book["title"], book["author"]))


    # Options Menu for user  
    while True:                        
        print("\nChoose action:")
        print("1: Add Book")
        print("2: List Books")
        print("3: Find Book")
        print("4: Delete Book")
        print("5: Sort Books")
        print("6: Exit")
        
        choice = input()

        # Add Book
        if choice == "1":
            title = input("\nEnter book title: ")
            author = input("Enter author: ")
            Library_Books.append(Book(title, author))

        # Print All Books (Unsorted)
        elif choice == "2":
            Book.list_books()

        # Find Book by Title
        elif choice == "3":
            title = input("\nEnter book title to find: ")
            book = Book.find_book(title)
            if book:
                print(f'"{book["title"]}" by {book["author"]}')
            else:
                print("\nBook not found.\n")

        # Delete a book by Title
        elif choice == "4":
            title = input("\nEnter book title to delete: ")
            deletedBook,author = Book.delete_book(title)
            if deletedBook:
                print(f'"{deletedBook}" by {author} is deleted from the database !')
            else:
                print("\nBook not found.\n")

        # Sort Books by Author using sort_books() function
        elif choice == "5":    
            print("Books before sorting:")
            for book in Library_Books:
                print(f'"{book.title}" by {book.author}')

            sorted_books = sort_books(Library_Books)

            print("\nBooks after sorting:")
            for book in sorted_books:
                print(f'"{book.title}" by {book.author}')

        # terminate 
        elif choice == "6":
            break
