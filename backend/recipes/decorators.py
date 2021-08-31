def recipe_filter_bool_param(func):
    def wrapper(*args):
        self, qs, _, value = args
        user = self.request.user

        if value and user.is_authenticated:
            qs = func(*args)
        return qs
    return wrapper
