from app import db, app
from app.model.BookGerne import BookGerne
from app.model.Book import Book
from app.model.Order import Order
from app.model.Order import OrderDetail, OnlineOrder, OfflineOrder
from app.model.User import User
from app.model.Account import Account
from app.model.Publisher import Publisher
from sqlalchemy import or_, func, case, desc
from datetime import datetime, timedelta, date
from sqlalchemy.sql import extract
from flask_login import current_user
from app.model.Config import Config
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import join


def count_book():
    books = db.session.query(Book).all()
    return len(books)


def count_book_gerne():
    books = db.session.query(BookGerne).all()
    return len(books)


def count_account():
    books = db.session.query(Account).all()
    return len(books)


def stats_revenue_online_by_month(year=None):
    """
    Thống kê doanh thu từ các đơn hàng online và sách theo tháng của năm.
    Bao gồm cả các tháng không có doanh thu.

    :param year: Năm cần thống kê doanh thu (mặc định là None, sẽ lấy năm hiện tại).
    :return: Danh sách tuple gồm (tháng, tổng doanh thu), sắp xếp từ tháng 1 đến 12.
    """
    if year is None:
        year = datetime.now().year

    # Truy vấn doanh thu từ các đơn hàng online (OrderDetail * OnlineOrder)
    online_revenue = db.session.query(
        extract('month', Order.created_at).label('month'),
        func.coalesce(func.sum(OrderDetail.quantity * OrderDetail.price), 0).label('total_online_revenue')
    ).join(
        OrderDetail, OrderDetail.order_id == Order.order_id  # JOIN giữa OrderDetail và Order
    ).join(
        OnlineOrder, OnlineOrder.order_id == Order.order_id  # JOIN với OnlineOrder (bắt buộc có sự kết nối với OnlineOrder)
    ).filter(
        Order.status == 'DA_HOAN_THANH'  # Chỉ tính các đơn hàng đã hoàn thành
    ).filter(
        extract('year', Order.created_at) == year  # Lọc theo năm
    ).group_by(
        extract('month', Order.created_at)  # Nhóm theo tháng
    ).all()

    # Truy vấn doanh thu từ các đơn hàng sách (OrderDetail * Book)
    book_revenue = db.session.query(
        extract('month', Order.created_at).label('month'),
        func.coalesce(func.sum(Book.price * OrderDetail.quantity), 0).label('total_book_revenue')
    ).join(
        OrderDetail, OrderDetail.order_id == Order.order_id, isouter=True  # LEFT JOIN với OrderDetail
    ).join(
        Book, Book.book_id == OrderDetail.book_id, isouter=True  # LEFT JOIN với Book
    ).join(
        OnlineOrder, OnlineOrder.order_id == OrderDetail.order_id  # JOIN với OnlineOrder để lấy doanh thu từ đơn hàng online
    ).filter(
        Order.status == 'DA_HOAN_THANH'  # Chỉ tính các đơn hàng đã hoàn thành
    ).filter(
        extract('year', Order.created_at) == year  # Lọc theo năm
    ).group_by(
        extract('month', Order.created_at)  # Nhóm theo tháng
    ).all()

    # Chuyển kết quả thành dictionary để dễ tra cứu
    online_revenue_by_month = {int(month): revenue for month, revenue in online_revenue}
    book_revenue_by_month = {int(month): revenue for month, revenue in book_revenue}

    # Tạo danh sách đầy đủ từ tháng 1 đến 12
    full_result = [
        (month,
         online_revenue_by_month.get(month, 0) + book_revenue_by_month.get(month, 0))  # Tổng doanh thu từ online và sách
        for month in range(1, 13)
    ]

    return full_result



def stats_revenue_offline_by_month(year=None):
    if year is None:
        year = datetime.now().year

    offline_revenue = db.session.query(
        extract('month', Order.created_at).label('month'),
        func.coalesce(func.sum(OrderDetail.quantity * OrderDetail.price), 0).label('total_offline_revenue')
    ).join(
        OrderDetail, OrderDetail.order_id == Order.order_id, isouter=True
    ).join(
        OfflineOrder, OfflineOrder.order_id == Order.order_id, isouter=True
    ).filter(
        Order.status == 'DA_HOAN_THANH'
    ).filter(
        extract('year', Order.created_at) == year
    ).group_by(
        extract('month', Order.created_at)
    ).all()

    book_revenue = db.session.query(
        extract('month', Order.created_at).label('month'),
        func.coalesce(func.sum(Book.price * OrderDetail.quantity), 0).label('total_book_revenue')
    ).join(
        OrderDetail, OrderDetail.order_id == Order.order_id, isouter=True
    ).join(
        Book, Book.book_id == OrderDetail.book_id, isouter=True
    ).join(
        OfflineOrder, OfflineOrder.order_id == OrderDetail.order_id, isouter=True
    ).filter(
        Order.status == 'DA_HOAN_THANH'
    ).filter(
        extract('year', Order.created_at) == year  # Lọc theo năm
    ).group_by(
        extract('month', Order.created_at)  # Nhóm theo tháng
    ).all()

    # Chuyển kết quả thành dictionary để dễ tra cứu
    offline_revenue_by_month = {int(month): revenue for month, revenue in offline_revenue}
    book_revenue_by_month = {int(month): revenue for month, revenue in book_revenue}

    # Tạo danh sách đầy đủ từ tháng 1 đến 12
    full_result = [
        (month,
         offline_revenue_by_month.get(month, 0) + book_revenue_by_month.get(month, 0))
        # Tổng doanh thu từ offline và sách
        for month in range(1, 13)
    ]

    return full_result


def stats_sales_count_by_month(year=None):
    if year is None:
        year = datetime.now().year

    # Truy vấn số lượng sản phẩm bán ra từ OrderDetail
    sales_count = db.session.query(
        extract('month', Order.created_at).label('month'),
        func.coalesce(func.sum(OrderDetail.quantity), 0).label('total_sales')
    ).join(
        OrderDetail, OrderDetail.order_id == Order.order_id, isouter=True
    ).filter(
        Order.status == 'DA_HOAN_THANH'  # Chỉ tính các đơn hàng đã hoàn thành
    ).filter(
        extract('year', Order.created_at) == year  # Lọc theo năm
    ).group_by(
        extract('month', Order.created_at)  # Nhóm theo tháng
    ).all()

    # Chuyển kết quả thành dictionary để dễ tra cứu
    sales_by_month = {int(month): sales for month, sales in sales_count}

    # Tạo danh sách đầy đủ từ tháng 1 đến 12
    full_result = [
        (month, sales_by_month.get(month, 0))  # Số lượng bán ra hoặc 0 nếu không có
        for month in range(1, 13)
    ]

    return full_result


def top_5_best_selling_books(year=None):
    if year is None:
        year = datetime.now().year

    # Truy vấn dữ liệu các sách bán chạy nhất
    book_stats = db.session.query(
        Book.title.label('book_title'),  # Tên sách
        func.sum(OrderDetail.quantity).label('total_sales'),  # Tổng số lượng bán
        func.sum(OrderDetail.quantity * Book.price).label('total_revenue')  # Tổng doanh thu
    ).select_from(OrderDetail).join(Book, Book.book_id == OrderDetail.book_id).join(Order, OrderDetail.order_id == Order.order_id).filter(
        Order.status == 'DA_HOAN_THANH'  # Chỉ tính các đơn hàng đã hoàn thành
    ).filter(
        extract('year', Order.created_at) == year  # Lọc theo năm
    ).group_by(
        Book.title
    ).order_by(
        func.sum(OrderDetail.quantity).desc()  # Sắp xếp theo số lượng bán giảm dần
    ).limit(5).all()  # Lấy 5 sách bán chạy nhất

    # Tổng doanh thu của tất cả các sách
    total_revenue = db.session.query(
        func.sum(OrderDetail.quantity * Book.price).label('total_revenue')
    ).select_from(OrderDetail).join(Book, Book.book_id == OrderDetail.book_id).join(Order, OrderDetail.order_id == Order.order_id).filter(
        Order.status == 'DA_HOAN_THANH'
    ).filter(
        extract('year', Order.created_at) == year
    ).scalar() or 0

    # Tính phần trăm doanh thu từng sách so với tổng doanh thu
    result = [
        {
            "book_title": book.book_title,
            "total_sales": int(book.total_sales) if book.total_sales else 0,
            "total_revenue": float(book.total_revenue) if book.total_revenue else 0.0,
            "revenue_percentage": round((book.total_revenue / total_revenue * 100) if total_revenue > 0 else 0, 2)
        }
        for book in book_stats
    ]

    return result


def book_gerne_statistic(kw=None, selected_month=None):
    g = db.session.query(
        BookGerne.book_gerne_id,
        BookGerne.name,
        func.coalesce(func.sum(Book.price * OrderDetail.quantity), 0).label('total_revenue'),
        func.coalesce(func.sum(OrderDetail.quantity), 0).label('total_quantity'),
        func.round(
            func.coalesce(func.sum(Book.price * OrderDetail.quantity) / total_revenue_per_gerne() * 100, 0), 2
        ).label('revenue_percentage')
    ).join(
        Book, BookGerne.book_gerne_id == Book.book_gerne_id, isouter=True
    ).join(
        OrderDetail, Book.book_id == OrderDetail.book_id, isouter=True
    ).join(
        Order, OrderDetail.order_id == Order.order_id, isouter=True
    ).filter(
        or_(Order.status == 'DA_HOAN_THANH', Order.status.is_(None))  # Bao gồm những đơn đã hoàn tất hoặc không có đơn
    )

    if kw:
        g = g.filter(BookGerne.name.contains(kw))

    if selected_month:
        # Nếu selected_month là chuỗi (định dạng "YYYY-MM"), chuyển nó thành datetime
        if isinstance(selected_month, str):
            selected_month = datetime.strptime(selected_month, "%Y-%m").date()

        # Xác định ngày đầu tiên và ngày cuối cùng của tháng
        first_day_of_month = date(selected_month.year, selected_month.month, 1)
        # Lấy ngày đầu tháng tiếp theo, sau đó trừ đi một ngày để có ngày cuối tháng hiện tại
        if selected_month.month == 12:
            last_day_of_month = date(selected_month.year, 12, 31)  # Tháng 12, ngày cuối cùng là 31
        else:
            next_month = date(selected_month.year, selected_month.month + 1, 1)
            last_day_of_month = next_month - timedelta(days=1)

        # Thêm điều kiện lọc cho ngày trong tháng đã chọn
        g = g.filter(Order.created_at >= first_day_of_month)
        g = g.filter(Order.created_at <= last_day_of_month)

    g = g.group_by(BookGerne.book_gerne_id, BookGerne.name).order_by(BookGerne.book_gerne_id)

    return g.all()


def stats_revenue_by_month(year=None):
    if year is None:
        year = datetime.now().year

    result = db.session.query(
        extract('month', Order.created_at).label('month'),
        func.coalesce(func.sum(Book.price * OrderDetail.quantity), 0).label('total_revenue'),
        func.coalesce(func.sum(OrderDetail.quantity), 0).label('total_quantity'),
        func.round(
            func.coalesce(func.sum(Book.price * OrderDetail.quantity) / total_revenue_per_gerne() * 100, 0), 2
        ).label('revenue_percentage')

    ).join(
        OrderDetail, OrderDetail.order_id == Order.order_id, isouter=True
    ).join(
        Book, Book.book_id == OrderDetail.book_id, isouter=True
    ).filter(
        Order.status == 'DA_HOAN_THANH'
    ).filter(
        extract('year', Order.created_at) == year
    ).group_by(
        extract('month', Order.created_at)
    ).all()

    # Chuyển kết quả thành dictionary để dễ tra cứu
    revenue_by_month = {
        int(month): {
            'total_revenue': total_revenue,
            'total_quantity': total_quantity,
            'revenue_percentage': revenue_percentage
        }
        for month, total_revenue, total_quantity, revenue_percentage in result
    }

    # Tạo danh sách đầy đủ từ tháng 1 đến 12
    full_result = [
        (month, revenue_by_month.get(month, {'total_revenue': 0, 'total_quantity': 0, 'revenue_percentage': 0})['total_revenue'],
         revenue_by_month.get(month, {'total_revenue': 0, 'total_quantity': 0, 'revenue_percentage': 0})['total_quantity'],
         revenue_by_month.get(month, {'total_revenue': 0, 'total_quantity': 0, 'revenue_percentage': 0})['revenue_percentage'])
        for month in range(1, 13)
    ]

    return full_result



def total_revenue_per_gerne(kw=None, selected_month=None):
    result = db.session.query(
        BookGerne.name.label('gerne_name'),
        func.coalesce(func.sum(Book.price * OrderDetail.quantity), 0).label('total_revenue')
    ).join(
        Book, BookGerne.book_gerne_id == Book.book_gerne_id, isouter=True
    ).join(
        OrderDetail, Book.book_id == OrderDetail.book_id, isouter=True
    ).join(
        Order, OrderDetail.order_id == Order.order_id, isouter=True
    ).filter(
        Order.status == 'DA_HOAN_THANH'
    )

    if kw:
        result = result.filter(BookGerne.name.contains(kw))

    if selected_month:
        if isinstance(selected_month, str):
            selected_month = datetime.strptime(selected_month, "%Y-%m").date()

        first_day_of_month = date(selected_month.year, selected_month.month, 1)

        if selected_month.month == 12:
            last_day_of_month = date(selected_month.year, 12, 31)
        else:
            next_month = date(selected_month.year, selected_month.month + 1, 1)
            last_day_of_month = next_month - timedelta(days=1)

        result = result.filter(Order.created_at >= first_day_of_month)
        result = result.filter(Order.created_at <= last_day_of_month)

    result = result.group_by(BookGerne.name)

    total_revenue = sum(
        item.total_revenue if item.total_revenue is not None else 0 for item in result
    )

    return total_revenue


# def get_books_by_gerne(gerne_id=None):
#     query = db.session.query(
#         Book.book_id,
#         Book.title,
#         BookGerne.name.label("gerne_name"),
#         Book.quantity.label("total_quantity"),
#         func.coalesce(func.sum(OrderDetail.quantity), 0).label("ordered_quantity"),
#         (Book.quantity - func.coalesce(func.sum(OrderDetail.quantity), 0)).label("remaining_quantity")
#     ).outerjoin(BookGerne, BookGerne.book_gerne_id == Book.book_gerne_id) \
#         .outerjoin(OrderDetail, OrderDetail.book_id == Book.book_id) \
#         .group_by(Book.book_id, Book.title, BookGerne.name, Book.quantity)
#
#     if gerne_id is not None:
#         query = query.filter(Book.book_gerne_id == gerne_id)
#
#     return query.all()


def book_statistic_frequency(gerne_id=None, selected_month=None):
    query = db.session.query(
        Book.book_id,
        Book.title,
        BookGerne.name.label("gerne_name"),
        func.coalesce(func.sum(OrderDetail.quantity), 0).label("ordered_quantity"),
        func.round(
            func.coalesce(func.sum(OrderDetail.quantity), 0) / total_quantity_all_books(
                selected_month=selected_month) * 100, 2
        ).label('revenue_percentage')
    ).outerjoin(
        BookGerne, BookGerne.book_gerne_id == Book.book_gerne_id
    ).outerjoin(
        OrderDetail, OrderDetail.book_id == Book.book_id
    ).outerjoin(
        Order, OrderDetail.order_id == Order.order_id
    )

    # Nếu có filtre thể loại sách
    if gerne_id is not None:
        query = query.filter(Book.book_gerne_id == gerne_id)

    # Nếu có tháng được chọn, lọc theo tháng
    if selected_month:
        # Nếu selected_month là chuỗi (định dạng "YYYY-MM"), chuyển nó thành datetime
        if isinstance(selected_month, str):
            selected_month = datetime.strptime(selected_month, "%Y-%m").date()

        # Xác định ngày đầu tiên và ngày cuối cùng của tháng
        first_day_of_month = date(selected_month.year, selected_month.month, 1)
        if selected_month.month == 12:
            last_day_of_month = date(selected_month.year, 12, 31)
        else:
            next_month = date(selected_month.year, selected_month.month + 1, 1)
            last_day_of_month = next_month - timedelta(days=1)

        # Thêm điều kiện lọc cho ngày trong tháng đã chọn
        query = query.filter(Order.created_at >= first_day_of_month)
        query = query.filter(Order.created_at <= last_day_of_month)

    query = query.group_by(Book.book_id, Book.title, BookGerne.name).order_by(Book.book_id)

    # Trả về kết quả
    return query.all()


def total_quantity_all_books(kw=None, selected_month=None):
    result = db.session.query(
        func.coalesce(func.sum(OrderDetail.quantity), 0).label('total_quantity')
    ).join(
        Order, OrderDetail.order_id == Order.order_id
    ).filter(
        Order.status == 'DA_HOAN_THANH'  # Lọc theo đơn hàng đã hoàn thành
    )

    if kw:
        # Nếu có từ khóa tìm kiếm, có thể lọc theo tên sách
        result = result.join(Book, OrderDetail.book_id == Book.book_id).filter(Book.title.contains(kw))

    if selected_month:
        if isinstance(selected_month, str):
            selected_month = datetime.strptime(selected_month, "%Y-%m").date()

        first_day_of_month = date(selected_month.year, selected_month.month, 1)

        if selected_month.month == 12:
            last_day_of_month = date(selected_month.year, 12, 31)
        else:
            next_month = date(selected_month.year, selected_month.month + 1, 1)
            last_day_of_month = next_month - timedelta(days=1)

        result = result.filter(Order.created_at >= first_day_of_month)
        result = result.filter(Order.created_at <= last_day_of_month)

    total_quantity = result.scalar()  # Lấy tổng số lượng sách bán ra

    return total_quantity



def account_management(user_role=None, first_name=None, last_name=None, page=None):
    """
     User.user_id,
        User.first_name,
        User.last_name,
        Account.username,
        User.email,
        User.user_role
    """
    query = User.query.join(Account, Account.user_id == User.user_id)

    page_size = app.config['STATISTIC_FRE_PAGE_SIZE']

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size


    if user_role is not None:
        query = query.filter(User.user_role == user_role)

    if first_name:
        query = query.filter(User.first_name.contains(first_name))

    if last_name:
        query = query.filter(User.last_name.contains(last_name))
    query = query.slice(start_idx, end_idx)

    return query.all()


def book_management(gerne_id=None, kw=None, price_start=None, price_end=None):
    query = db.session.query(
        Book.book_id,
        Book.title,
        BookGerne.name.label("gerne_name"),
        Book.author,
        Publisher.publisher_name.label("publisher_name"),
        Book.price,
        Book.barcode,
        Book.num_page,
        Book.weight,
        Book.format,
        Book.dimension,
    ).outerjoin(BookGerne, BookGerne.book_gerne_id == Book.book_gerne_id) \
        .outerjoin(Publisher, Publisher.publisher_id == Book.publisher_id) \
        .group_by(Book.book_id, Book.title, BookGerne.name)

    if gerne_id is not None:
        query = query.filter(Book.book_gerne_id == gerne_id)

    if kw:
        keyword = f"%{kw}%"  # Chuẩn bị mẫu tìm kiếm
        query = query.filter(
            or_(
                Book.title.ilike(keyword),  # Tìm trong tiêu đề
                BookGerne.name.ilike(keyword),  # Tìm trong tên thể loại
                Book.author.ilike(keyword),  # Tìm trong tác giả
                Publisher.publisher_name.ilike(keyword)  # Tìm trong nhà xuất bản
            )
        )

    if price_start is not None:
        query = query.filter(Book.price >= price_start)

    if price_end is not None:
        query = query.filter(Book.price <= price_end)

    query = query.order_by(desc(Book.created_at))

    return query.all()


def bookgerne_management(kw=None):
    query = db.session.query(
        BookGerne.book_gerne_id,
        BookGerne.name
    ).group_by(BookGerne.book_gerne_id, BookGerne.name)

    if kw:
        query = query.filter(BookGerne.name.contains(kw))

    return query.all()


def profile():
    if not current_user.is_authenticated:
        return None

    query = db.session.query(
        Account.user_id,
        Account.username,
        User.first_name,
        User.last_name,
        User.email,
        User.phone_number,
        User.avt_url,
        case(
            (User.sex == 1, True), else_=False
        ).label('is_male'),
        case(
            (User.sex == 0, True), else_=False
        ).label('is_female'),
        extract('day', User.date_of_birth).label('day'),
        extract('month', User.date_of_birth).label('month'),
        extract('year', User.date_of_birth).label('year')
    ).join(Account, Account.user_id == User.user_id
           ).filter(User.user_id == current_user.user_id)

    return query.first()


def config():
    return Config.query.first()







