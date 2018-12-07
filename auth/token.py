from functools import partial

from auth.user import User
from auth.typing import Maybe, Success
from auth.functools import bind


def _create_token(user: User) -> Maybe[Success]:
    print(user)
    return Success({'token': 'TODO'}, 200)


create_token = partial(bind, _create_token)
