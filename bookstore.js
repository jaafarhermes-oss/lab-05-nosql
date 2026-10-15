// Step 2: Select the bookstore database
db = db.getSiblingDB("bookstore");

// Step 3: Load authors from authors.json
db.authors.drop();
let authors = JSON.parse(fs.readFileSync("authors.json", "utf8"));
db.authors.insertMany(authors);

// Step 4: Load books from books.json
db.books.drop();
let books = JSON.parse(fs.readFileSync("books.json", "utf8"));
db.books.insertMany(books);

// Step 5: List every author and every book
db.authors.find();
db.books.find();

// Step 6: Insert two new books
db.books.insertMany([
  {
    title: "The Hobbit",
    published_year: 1937,
    author_ids: ["author_004"]
  },
  {
    title: "Dune",
    published_year: 1965,
    author_ids: ["author_005"]
  }
]);

// Step 7: Insert the missing authors
db.authors.insertMany([
  {
    _id: "author_004",
    name: "J. R. R. Tolkien",
    nationality: "British",
    bio: {
      short: "Author of The Hobbit and The Lord of the Rings.",
      long: "J. R. R. Tolkien was a British writer known for fantasy novels, including The Hobbit."
    }
  },
  {
    _id: "author_005",
    name: "Frank Herbert",
    nationality: "American",
    bio: {
      short: "American author known for Dune.",
      long: "Frank Herbert was an American science fiction author best known for the Dune series."
    }
  }
]);

// Step 8: Filter books by loaded and newly added authors
db.books.find({
  author_ids: {
    $in: ["author_001", "author_002", "author_004", "author_005"]
  }
});