# -*- coding: utf-8 -*-


class School(object):
    """Data class for schools."""

    def __init__(
        self,
        code,
        name,
        city,
        state,
        from_m,
        from_y,
        to_m,
        to_y,
        grad_m,
        grad_y,
    ):
        """Intitalization method."""
        self.school_code = code
        self.school_name = name
        self.school_city = city
        self.school_state = state
        self.from_month = from_m
        self.from_year = from_y
        self.to_month = to_m
        self.to_year = to_y
        self.grad_month = grad_m
        self.grad_year = grad_y
