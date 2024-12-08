from app import es
from app.elasticsearch.BookIndex import BookIndex


def create_document(document):
    try:
        res = es.index(index=BookIndex.index_name, body=document)
        if res['result'] == 'created':
            print(f"Document {document} updated successfully in index {BookIndex.index_name}.")
        else:
            print(f"Failed to update document {document} in index {BookIndex.index_name}.")
    except Exception as e:
        print(f"Error updating document: {e}")


def update_document(document_id, updated_fields):
    try:
        # Perform the update operation
        response = es.update(index=BookIndex.index_name, id=document_id, body={'doc': updated_fields})
        if response['result'] == 'updated':
            print(f"Document {document_id} updated successfully in index {BookIndex.index_name}.")
        else:
            print(f"Failed to update document {document_id} in index {BookIndex.index_name}.")
    except Exception as e:
        print(f"Error updating document: {e}")


def delete_document(document_id):
    try:
        # Perform the delete operation
        response = es.delete(index=BookIndex.index_name, id=document_id)
        if response['result'] == 'deleted':
            print(f"Document {document_id} deleted successfully from index {BookIndex.index_name}.")
        else:
            print(f"Failed to delete document {document_id} from index {BookIndex.index_name}.")
    except Exception as e:
        print(f"Error deleting document: {e}")
