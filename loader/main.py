from loader import ImageLoader, read_employees
from storage import FacesDatabase


# load reference images into database from existing folder
if __name__ == '__main__':
    db = FacesDatabase()
    print(f"Rows before truncate: {db.count_rows()}")
    db.truncate_table()
    print(f"Rows after truncate: {db.count_rows()}")
    loader = ImageLoader(db)
    loader.load_employees(read_employees())
    print(f"Rows after loading: {db.count_rows()}")
