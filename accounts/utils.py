def is_shop_customer(user):
    return user.is_authenticated and not user.is_staff
