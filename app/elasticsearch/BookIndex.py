from app import es, app
from app.model.Book import Book


class BookIndex:
    index_name = 'book-index'

    def __init__(self, book_data):
        # Initialize with data that you want to index
        self.book_data = book_data

    @classmethod
    def create_index(cls):
        """
        Creates the index in Elasticsearch if it does not already exist.
        """
        if not es.indices.exists(index=cls.index_name):
            mappings = {
                "mappings": {
                    "properties": {
                        "book_id": {"type": "integer"},
                        "author": {"type": "text"},
                        "title": {"type": "text"},
                        "quantity": {"type": "integer"},
                        "price": {"type": "float"},
                        "description": {"type": "text"},
                        "num_page": {"type": "integer"},
                        "weight": {"type": "float"},
                        "format": {"type": "keyword"},
                        "publisher": {"type": "keyword"},
                        "book_images": {"type": "keyword"},
                        "book_gerne": {"type": "object", "properties": {
                            'book_gerne_id': {'type': 'integer'},
                            'name': {'type': 'text'},
                            'attributes': {'type': 'nested', "properties": {
                                'attribute_id': {'type': 'integer'},
                                'attribute_name': {'type': 'text'},
                            }},
                        }},
                        "extended_books": {"type": "keyword"},
                    }
                }
            }

            # Create the index with the mappings
            es.indices.create(index=cls.index_name, body=mappings)
            print(f"Index '{cls.index_name}' created.")
        else:
            print(f"Index '{cls.index_name}' already exists.")


if __name__ == '__main__':
    # with app.app_context():
    #     book = Book.query.all()
    #     book_document = book.to_dto()
    #     res = es.index(index=BookIndex.index_name, body=book_document)

    BookIndex.create_index()
